#include <gtest/gtest.h>
#include <sstream>
#include <string>
#include <vector>

#include "../include/graph/graph.h"
#include "../include/custom_object.h"

// ==========================================
// 1. БАЗОВОЕ СОСТОЯНИЕ И УПРАВЛЕНИЕ ПАМЯТЬЮ
// ==========================================

TEST(GraphTest, EmptyAndClear) {
    Graph<int> g;
    EXPECT_TRUE(g.empty());
    EXPECT_EQ(g.vertex_count(), 0);
    EXPECT_EQ(g.edge_count(), 0);

    g.insert_vertex(1);
    g.insert_edge(1, 1); // Петля
    EXPECT_FALSE(g.empty());

    g.clear();
    EXPECT_TRUE(g.empty());
    EXPECT_EQ(g.vertex_count(), 0);
    EXPECT_EQ(g.edge_count(), 0);
}

TEST(GraphTest, RuleOfFive) {
    Graph<int> g1;
    g1.insert_vertex(1);
    g1.insert_vertex(2);
    g1.insert_edge(1, 2);

    // Конструктор копирования
    Graph<int> g2(g1);
    EXPECT_EQ(g2.vertex_count(), 2);
    EXPECT_TRUE(g2.has_edge(1, 2));

    // Оператор присваивания
    Graph<int> g3;
    g3 = g1;
    EXPECT_TRUE(g3 == g1);

    // Конструктор перемещения
    Graph<int> g4(std::move(g1));
    EXPECT_EQ(g4.vertex_count(), 2);
    EXPECT_TRUE(g1.empty()); // g1 должен стать пустым после перемещения (поведение std::list)

    // Оператор перемещения
    Graph<int> g5;
    g5 = std::move(g2);
    EXPECT_EQ(g5.vertex_count(), 2);
}

// ==========================================
// 2. РАБОТА С ВЕРШИНАМИ И ИСКЛЮЧЕНИЯ
// ==========================================

TEST(GraphTest, VertexInsertEraseAndExceptions) {
    Graph<int> g;
    g.insert_vertex(10);
    EXPECT_TRUE(g.has_vertex(10));
    EXPECT_FALSE(g.has_vertex(20));

    // Дубликат вершины
    EXPECT_THROW(g.insert_vertex(10), std::invalid_argument);

    // Удаление существующей
    g.erase_vertex(10);
    EXPECT_FALSE(g.has_vertex(10));

    // Удаление несуществующей
    EXPECT_THROW(g.erase_vertex(99), std::invalid_argument);
}

TEST(GraphTest, EraseVertexRemovesIncidentEdges) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);
    g.insert_vertex(3);
    
    g.insert_edge(1, 2);
    g.insert_edge(2, 3);
    g.insert_edge(3, 1);

    g.erase_vertex(2); // Должны удалиться рёбра 1->2 и 2->3
    
    EXPECT_EQ(g.vertex_count(), 2);
    EXPECT_EQ(g.edge_count(), 1);
    EXPECT_TRUE(g.has_edge(3, 1));
    EXPECT_FALSE(g.has_edge(1, 2));
}

// ==========================================
// 3. РАБОТА С РЁБРАМИ И СТЕПЕНИ
// ==========================================

TEST(GraphTest, EdgeInsertEraseAndExceptions) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);

    g.insert_edge(1, 2);
    EXPECT_TRUE(g.has_edge(1, 2));

    // Дубликат ребра
    EXPECT_THROW(g.insert_edge(1, 2), std::invalid_argument);

    // Ребро с несуществующими вершинами
    EXPECT_THROW(g.insert_edge(1, 99), std::invalid_argument);
    EXPECT_THROW(g.insert_edge(99, 2), std::invalid_argument);

    g.erase_edge(1, 2);
    EXPECT_FALSE(g.has_edge(1, 2));

    // Удаление несуществующего ребра
    EXPECT_THROW(g.erase_edge(1, 2), std::invalid_argument);
}

TEST(GraphTest, Degrees) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);
    g.insert_vertex(3);

    g.insert_edge(1, 2);
    g.insert_edge(2, 1);
    g.insert_edge(2, 3);

    // Степень вершины = входы + выходы
    EXPECT_EQ(g.vertex_degree(2), 3); // Входит: 1->2. Выходит: 2->1, 2->3
    EXPECT_EQ(g.vertex_degree(1), 2); // Входит: 2->1. Выходит: 1->2
    EXPECT_EQ(g.vertex_degree(3), 1); // Входит: 2->3. Выходит: 0

    // Исключение для несуществующей вершины
    EXPECT_THROW(g.vertex_degree(99), std::invalid_argument);

    // Степень ребра = сумма степеней его вершин
    EXPECT_EQ(g.edge_degree(1, 2), 5); // 2 + 3 = 5

    // Исключение для степени несуществующего ребра
    EXPECT_THROW(g.edge_degree(1, 3), std::invalid_argument);
}

// ==========================================
// 4. ИТЕРАТОРЫ ВЕРШИН (Vertex Iterator)
// ==========================================

TEST(GraphTest, VertexIterators) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);

    // Прямой обход
    std::vector<int> vals;
    for (auto it = g.v_begin(); it != g.v_end(); ++it) {
        vals.push_back(*it);
    }
    EXPECT_EQ(vals, std::vector<int>({1, 2}));

    // Обратный обход
    std::vector<int> r_vals;
    for (auto it = g.v_rbegin(); it != g.v_rend(); ++it) {
        r_vals.push_back(*it);
    }
    EXPECT_EQ(r_vals, std::vector<int>({2, 1}));

    // Константный обход
    const Graph<int>& cg = g;
    EXPECT_EQ(*cg.v_cbegin(), 1);

    // Удаление по итератору
    g.erase_vertex(g.v_begin());
    EXPECT_FALSE(g.has_vertex(1));
}

// ==========================================
// 5. ИТЕРАТОРЫ РЁБЕР (Edge Iterator)
// ==========================================

TEST(GraphTest, EdgeIteratorsAndComplexDecrement) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);
    g.insert_vertex(3);

    // 1 имеет исходящие, 2 - ПУСТАЯ, 3 имеет исходящие
    // Это проверяет сложную логику отката (--it) через пустые узлы
    g.insert_edge(1, 2);
    g.insert_edge(3, 1);

    std::vector<std::pair<int, int>> edges;
    for (auto it = g.e_begin(); it != g.e_end(); ++it) {
        edges.push_back(*it);
    }
    
    ASSERT_EQ(edges.size(), 2);
    EXPECT_EQ(edges[0], std::make_pair(1, 2));
    EXPECT_EQ(edges[1], std::make_pair(3, 1));

    // Проверка декремента (откат назад от end)
    auto it = g.e_end();
    --it;
    EXPECT_EQ(*it, std::make_pair(3, 1));
    --it;
    EXPECT_EQ(*it, std::make_pair(1, 2));
    EXPECT_TRUE(it == g.e_begin());

    // Удаление по итератору
    g.erase_edge(g.e_begin());
    EXPECT_FALSE(g.has_edge(1, 2));
}

TEST(GraphTest, EdgeIteratorEmptyGraph) {
    Graph<int> g;
    EXPECT_TRUE(g.e_begin() == g.e_end());
}

// ==========================================
// 6. ИТЕРАТОРЫ СМЕЖНЫХ (Adjacent) И ИНЦИДЕНТНЫХ (Incident)
// ==========================================

TEST(GraphTest, AdjacentAndIncidentIterators) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);
    g.insert_vertex(3);
    g.insert_edge(1, 2);
    g.insert_edge(1, 3);

    // Adjacent (целевые вершины)
    std::vector<int> adj;
    for (auto it = g.adj_begin(1); it != g.adj_end(1); ++it) {
        adj.push_back(*it);
    }
    EXPECT_EQ(adj, std::vector<int>({2, 3}));

    // Incident (пары ребер)
    std::vector<std::pair<int, int>> inc;
    for (auto it = g.inc_begin(1); it != g.inc_end(1); ++it) {
        inc.push_back(*it);
    }
    EXPECT_EQ(inc[0], std::make_pair(1, 2));
    EXPECT_EQ(inc[1], std::make_pair(1, 3));

    // Исключения при запросе итераторов для несуществующих узлов
    EXPECT_THROW(g.adj_begin(99), std::invalid_argument);
    EXPECT_THROW(g.inc_begin(99), std::invalid_argument);
}

// ==========================================
// 7. СРАВНЕНИЯ И ОПЕРАТОР ВЫВОДА
// ==========================================

TEST(GraphTest, ComparisonOperators) {
    Graph<int> g1, g2;
    g1.insert_vertex(1);
    g2.insert_vertex(1);
    
    EXPECT_TRUE(g1 == g2);
    EXPECT_FALSE(g1 != g2);
    EXPECT_TRUE(g1 <= g2);

    g2.insert_vertex(2);
    EXPECT_TRUE(g1 < g2);
    EXPECT_TRUE(g1 != g2);
    EXPECT_TRUE(g2 > g1);
}

TEST(GraphTest, StreamOutput) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);
    g.insert_edge(1, 2);

    std::ostringstream oss;
    oss << g;
    std::string output = oss.str();
    
    EXPECT_NE(output.find("[1] -> 2"), std::string::npos);
    EXPECT_NE(output.find("[2] -> (нет исходящих)"), std::string::npos);
}

// ==========================================
// 8. ТЕСТ С ПОЛЬЗОВАТЕЛЬСКИМ ТИПОМ
// ==========================================

TEST(GraphTest, CustomObjectFlightInfo) {
    Graph<FlightInfo> g;
    FlightInfo f1("MSQ", 0.0, 1);
    FlightInfo f2("SVO", 700.0, 2);
    
    g.insert_vertex(f1);
    g.insert_vertex(f2);
    g.insert_edge(f1, f2);

    EXPECT_EQ(g.vertex_count(), 2);
    EXPECT_TRUE(g.has_edge(f1, f2));

    // Проверка обхода инцидентных рёбер для сложных объектов
    auto inc_it = g.inc_begin(f1);
    EXPECT_EQ((*inc_it).second.get_number(), "SVO");
}

// ==========================================
// 9. ДОПОЛНИТЕЛЬНЫЕ ИТЕРАТОРЫ И ГРАНИЧНЫЕ СЛУЧАИ
// ==========================================

TEST(GraphTest, PostfixOperatorsAndReverseIterators) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);
    g.insert_vertex(3);
    g.insert_edge(1, 2);
    g.insert_edge(1, 3);
    g.insert_edge(2, 3);

    // 1. Постфиксные операторы вершинных итераторов
    auto vit = g.v_begin();
    auto vit_post = vit++;
    EXPECT_EQ(*vit_post, 1);
    EXPECT_EQ(*vit, 2);
    auto vit_dec = vit--;
    EXPECT_EQ(*vit_dec, 2);
    EXPECT_EQ(*vit, 1);

    // Константные вершинные итераторы (постфикс)
    auto cvit = g.v_cbegin();
    auto cvit_post = cvit++;
    EXPECT_EQ(*cvit_post, 1);
    EXPECT_EQ(*cvit, 2);
    auto cvit_dec = cvit--;
    EXPECT_EQ(*cvit_dec, 2);
    EXPECT_EQ(*cvit, 1);

    // 2. Постфиксные операторы рёберных итераторов
    auto eit = g.e_begin();
    auto eit_post = eit++;
    EXPECT_EQ(*eit_post, (std::pair<int, int>{1, 2}));
    EXPECT_EQ(*eit, (std::pair<int, int>{1, 3}));
    auto eit_dec = eit--;
    EXPECT_EQ(*eit_dec, (std::pair<int, int>{1, 3}));
    EXPECT_EQ(*eit, (std::pair<int, int>{1, 2}));

    // Константные рёберные итераторы
    auto ceit = g.e_cbegin();
    auto ceit_post = ceit++;
    EXPECT_EQ(*ceit_post, (std::pair<int, int>{1, 2}));
    EXPECT_EQ(*ceit, (std::pair<int, int>{1, 3}));
    auto ceit_dec = ceit--;
    EXPECT_EQ(*ceit_dec, (std::pair<int, int>{1, 3}));
    EXPECT_EQ(*ceit, (std::pair<int, int>{1, 2}));

    // 3. Постфиксные операторы инцидентных итераторов
    auto inc_it = g.inc_begin(1);
    auto inc_post = inc_it++;
    EXPECT_EQ(*inc_post, (std::pair<int, int>{1, 2}));
    EXPECT_EQ(*inc_it, (std::pair<int, int>{1, 3}));
    auto inc_dec = inc_it--;
    EXPECT_EQ(*inc_dec, (std::pair<int, int>{1, 3}));
    EXPECT_EQ(*inc_it, (std::pair<int, int>{1, 2}));

    // 4. Обратные итераторы
    // Вершины в обратном порядке
    std::vector<int> rev_v;
    for (auto it = g.v_rbegin(); it != g.v_rend(); ++it) rev_v.push_back(*it);
    EXPECT_EQ(rev_v, (std::vector<int>{3, 2, 1}));

    std::vector<int> crev_v;
    for (auto it = g.v_crbegin(); it != g.v_crend(); ++it) crev_v.push_back(*it);
    EXPECT_EQ(crev_v, (std::vector<int>{3, 2, 1}));

    // Рёбра в обратном порядке
    std::vector<std::pair<int, int>> rev_e;
    for (auto it = g.e_rbegin(); it != g.e_rend(); ++it) rev_e.push_back(*it);
    EXPECT_EQ(rev_e.size(), 3);
    EXPECT_EQ(rev_e.front(), (std::pair<int, int>{2, 3}));

    std::vector<std::pair<int, int>> crev_e;
    for (auto it = g.e_crbegin(); it != g.e_crend(); ++it) crev_e.push_back(*it);
    EXPECT_EQ(crev_e.size(), 3);

    // Смежные в обратном порядке
    std::vector<int> rev_adj;
    for (auto it = g.adj_rbegin(1); it != g.adj_rend(1); ++it) rev_adj.push_back(*it);
    EXPECT_EQ(rev_adj, (std::vector<int>{3, 2}));

    std::vector<int> crev_adj;
    for (auto it = g.adj_crbegin(1); it != g.adj_crend(1); ++it) crev_adj.push_back(*it);
    EXPECT_EQ(crev_adj, (std::vector<int>{3, 2}));

    // Инцидентные в обратном порядке
    std::vector<std::pair<int, int>> rev_inc;
    for (auto it = g.inc_rbegin(1); it != g.inc_rend(1); ++it) rev_inc.push_back(*it);
    EXPECT_EQ(rev_inc.size(), 2);
    EXPECT_EQ(rev_inc.front(), (std::pair<int, int>{1, 3}));

    std::vector<std::pair<int, int>> crev_inc;
    for (auto it = g.inc_crbegin(1); it != g.inc_crend(1); ++it) crev_inc.push_back(*it);
    EXPECT_EQ(crev_inc.size(), 2);
}

TEST(GraphTest, ForwardAdjacentIterator) {
    Graph<int> g;
    g.insert_vertex(10);
    g.insert_vertex(20);
    g.insert_vertex(30);
    g.insert_edge(10, 20);
    g.insert_edge(10, 30);

    std::vector<int> adj_nodes;
    for (auto it = g.f_adj_begin(10); it != g.f_adj_end(10); ++it) {
        adj_nodes.push_back(*it);
    }
    EXPECT_EQ(adj_nodes, (std::vector<int>{20, 30}));

    // Проверка постфиксного инкремента и равенства
    auto fit = g.f_adj_begin(10);
    auto fit_post = fit++;
    EXPECT_EQ(*fit_post, 20);
    EXPECT_EQ(*fit, 30);
    EXPECT_FALSE(fit == fit_post);
    EXPECT_TRUE(fit != fit_post);
}

TEST(GraphTest, ComparisonOperatorsGreaterAndEqual) {
    Graph<int> g1, g2;
    g1.insert_vertex(1);
    g2.insert_vertex(1);

    EXPECT_TRUE(g1 >= g2);
    EXPECT_FALSE(g1 > g2);

    g1.insert_vertex(2);
    EXPECT_TRUE(g1 > g2);
    EXPECT_TRUE(g1 >= g2);
    EXPECT_FALSE(g2 >= g1);
}

TEST(GraphTest, EraseInvalidIteratorExceptions) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);
    g.insert_edge(1, 2);

    // Удаление через end() вершины
    EXPECT_THROW(g.erase_vertex(g.v_end()), std::invalid_argument);
    EXPECT_THROW(g.erase_vertex(g.v_cend()), std::invalid_argument);

    // Удаление через end() ребра
    EXPECT_THROW(g.erase_edge(g.e_end()), std::invalid_argument);
    EXPECT_THROW(g.erase_edge(g.e_cend()), std::invalid_argument);

    // Валидное удаление по итератору
    g.erase_edge(g.e_begin());
    EXPECT_EQ(g.edge_count(), 0);

    g.erase_vertex(g.v_begin());
    EXPECT_EQ(g.vertex_count(), 1);
}

TEST(GraphTest, EdgeDegreeCalculation) {
    Graph<int> g;
    g.insert_vertex(1);
    g.insert_vertex(2);
    g.insert_vertex(3);
    g.insert_edge(1, 2);
    g.insert_edge(2, 3);

    // vertex_degree(1) = 1 (исходящее 1->2)
    // vertex_degree(2) = 2 (входящее 1->2, исходящее 2->3)
    // edge_degree(1, 2) = vertex_degree(1) + vertex_degree(2) = 1 + 2 = 3
    EXPECT_EQ(g.edge_degree(1, 2), 3);

    // Несуществующее ребро
    EXPECT_THROW(g.edge_degree(1, 3), std::invalid_argument);
}
/**
 * @file graph.h
 * @brief Обобщённый контейнер ориентированного графа на основе структуры Вирта.
 */

#pragma once

#include <algorithm>
#include <iostream>
#include <iterator>
#include <list>
#include <numeric>
#include <stdexcept>
#include <utility>

/**
 * @class Graph
 * @brief Обобщённый контейнер ориентированного графа (Структура Вирта).
 *
 * Реализует структуру Вирта: основной связный список записей вершин (`std::list<VertexRecord>`),
 * где каждая запись хранит значение вершины и собственный список смежных вершин (исходящих дуг).
 *
 * @tparam T Тип данных, хранящихся в вершинах графа.
 */
template <typename T>
class Graph {
private:
    /**
     * @struct VertexRecord
     * @brief Узел структуры Вирта: хранит значение вершины и список её исходящих дуг.
     */
    struct VertexRecord {
        T data{};                   ///< Данные вершины
        std::list<T> adjacencies{}; ///< Список смежных вершин (исходящих дуг)

        /**
         * @brief Проверка равенства записей вершин.
         * @param other Другая запись вершины.
         * @return true, если данные и списки смежностей идентичны.
         */
        bool operator==(const VertexRecord& other) const {
            return data == other.data && adjacencies == other.adjacencies;
        }

        /**
         * @brief Лексикографическое сравнение "меньше" по значению вершины.
         * @param other Другая запись вершины.
         * @return true, если текущая вершина меньше other.
         */
        bool operator<(const VertexRecord& other) const {
            return data < other.data;
        }
    };

    std::list<VertexRecord> records{}; ///< Основной список записей вершин графа

    /**
     * @brief Находит запись вершины по значению (мутабельная версия).
     * @param value Искомое значение вершины.
     * @return Итератор на запись вершины либо records.end().
     */
    typename std::list<VertexRecord>::iterator find_vertex(const T& value) {
        return std::find_if(records.begin(), records.end(), [&](const VertexRecord& record) {
            return record.data == value;
        });
    }

    /**
     * @brief Находит запись вершины по значению (константная версия).
     * @param value Искомое значение вершины.
     * @return Константный итератор на запись вершины либо records.end().
     */
    typename std::list<VertexRecord>::const_iterator find_vertex(const T& value) const {
        return std::find_if(records.begin(), records.end(), [&](const VertexRecord& record) {
            return record.data == value;
        });
    }

    /**
     * @brief Ищет вершину или выбрасывает исключение, если она не найдена.
     * @param value Искомое значение вершины.
     * @return Константный итератор на запись вершины.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    typename std::list<VertexRecord>::const_iterator find_vertex_strict(const T& value) const {
        auto vertex_it = find_vertex(value);
        if (vertex_it == records.end()) {
            throw std::invalid_argument("Вершина не найдена!");
        }
        return vertex_it;
    }

public:
    using value_type = T;                   ///< Тип значения вершины
    using reference = T&;                   ///< Ссылка на значение вершины
    using const_reference = const T&;       ///< Константная ссылка на значение вершины
    using pointer = T*;                     ///< Указатель на значение вершины
    using const_pointer = const T*;         ///< Константный указатель на значение вершины
    using size_type = std::size_t;          ///< Беззнаковый целочисленный тип размера
    using difference_type = std::ptrdiff_t; ///< Знаковый тип разности итераторов
    using edge_type = std::pair<T, T>;      ///< Тип ориентированного ребра (from, to)

    // ==========================================
    // ОБЪЯВЛЕНИЯ ITERATOR-ТИПОВ
    // ==========================================

    #include "vertex_iterator.h"
    #include "edge_iterator.h"
    #include "adjacent_iterator.h"
    #include "incident_iterator.h"

    // ==========================================
    // КОНСТРУКТОРЫ И УПРАВЛЕНИЕ ПАМЯТЬЮ
    // ==========================================

    /** @brief Конструктор по умолчанию (создаёт пустой граф). */
    Graph() = default;

    /**
     * @brief Конструктор копирования.
     * @param other Копируемый граф.
     */
    Graph(const Graph& other) = default;

    /**
     * @brief Конструктор перемещения.
     * @param other Перемещаемый граф.
     */
    Graph(Graph&& other) noexcept = default;

    /** @brief Деструктор графа. */
    ~Graph() = default;

    /**
     * @brief Оператор присваивания копированием.
     * @param other Копируемый граф.
     * @return Ссылка на текущий экземпляр графа.
     */
    Graph& operator=(const Graph& other) = default;

    /**
     * @brief Оператор присваивания перемещением.
     * @param other Перемещаемый граф.
     * @return Ссылка на текущий экземпляр графа.
     */
    Graph& operator=(Graph&& other) noexcept = default;

    /**
     * @brief Проверка графа на пустоту.
     * @return true, если в графе нет ни одной вершины.
     */
    bool empty() const noexcept { return records.empty(); }

    /** @brief Полная очистка графа (удаление всех вершин и рёбер). */
    void clear() noexcept { records.clear(); }

    /**
     * @brief Возвращает общее количество вершин в графе.
     * @return Число вершин.
     */
    size_type vertex_count() const noexcept { return records.size(); }

    /**
     * @brief Возвращает общее количество ориентированных рёбер в графе.
     * @return Число рёбер.
     */
    size_type edge_count() const noexcept {
        return std::accumulate(records.begin(), records.end(), size_type{0},
            [](size_type sum, const VertexRecord& record) {
                return sum + record.adjacencies.size();
            });
    }

    // ==========================================
    // ФУНКЦИИ ВОЗВРАТА ИТЕРАТОРОВ (BEGIN/END)
    // ==========================================

    /** @brief Итератор на начало списка вершин. */
    vertex_iterator v_begin() { return vertex_iterator(records.begin()); }
    /** @brief Итератор на конец списка вершин. */
    vertex_iterator v_end() { return vertex_iterator(records.end()); }
    /** @brief Константный итератор на начало списка вершин. */
    const_vertex_iterator v_begin() const { return v_cbegin(); }
    /** @brief Константный итератор на конец списка вершин. */
    const_vertex_iterator v_end() const { return v_cend(); }
    /** @brief Явный константный итератор на начало списка вершин. */
    const_vertex_iterator v_cbegin() const { return const_vertex_iterator(records.begin()); }
    /** @brief Явный константный итератор на конец списка вершин. */
    const_vertex_iterator v_cend() const { return const_vertex_iterator(records.end()); }
    /** @brief Обратный итератор на начало списка вершин. */
    reverse_vertex_iterator v_rbegin() { return reverse_vertex_iterator(v_end()); }
    /** @brief Обратный итератор на конец списка вершин. */
    reverse_vertex_iterator v_rend() { return reverse_vertex_iterator(v_begin()); }
    /** @brief Константный обратный итератор на начало списка вершин. */
    const_reverse_vertex_iterator v_rbegin() const { return v_crbegin(); }
    /** @brief Константный обратный итератор на конец списка вершин. */
    const_reverse_vertex_iterator v_rend() const { return v_crend(); }
    /** @brief Явный константный обратный итератор на начало списка вершин. */
    const_reverse_vertex_iterator v_crbegin() const { return const_reverse_vertex_iterator(v_cend()); }
    /** @brief Явный константный обратный итератор на конец списка вершин. */
    const_reverse_vertex_iterator v_crend() const { return const_reverse_vertex_iterator(v_cbegin()); }

    /** @brief Итератор на первое ребро графа. */
    edge_iterator e_begin() {
        if (records.empty()) return e_end();
        return edge_iterator(records.begin(), records.end(), records.begin()->adjacencies.begin());
    }
    /** @brief Итератор на конец последовательности всех рёбер. */
    edge_iterator e_end() {
        if (records.empty()) return edge_iterator(records.end(), records.end(), {});
        return edge_iterator(records.end(), records.end(), records.back().adjacencies.end());
    }
    /** @brief Константный итератор на первое ребро графа. */
    const_edge_iterator e_begin() const { return e_cbegin(); }
    /** @brief Константный итератор на конец последовательности всех рёбер. */
    const_edge_iterator e_end() const { return e_cend(); }
    /** @brief Явный константный итератор на первое ребро графа. */
    const_edge_iterator e_cbegin() const {
        if (records.empty()) return e_cend();
        return const_edge_iterator(records.begin(), records.end(), records.begin()->adjacencies.begin());
    }
    /** @brief Явный константный итератор на конец последовательности всех рёбер. */
    const_edge_iterator e_cend() const {
        if (records.empty()) return const_edge_iterator(records.end(), records.end(), {});
        return const_edge_iterator(records.end(), records.end(), records.back().adjacencies.end());
    }
    /** @brief Обратный итератор на последнее ребро графа. */
    reverse_edge_iterator e_rbegin() { return reverse_edge_iterator(e_end()); }
    /** @brief Обратный итератор на конец обратной последовательности всех рёбер. */
    reverse_edge_iterator e_rend() { return reverse_edge_iterator(e_begin()); }
    /** @brief Константный обратный итератор на последнее ребро графа. */
    const_reverse_edge_iterator e_rbegin() const { return e_crbegin(); }
    /** @brief Константный обратный итератор на конец обратной последовательности всех рёбер. */
    const_reverse_edge_iterator e_rend() const { return e_crend(); }
    /** @brief Явный константный обратный итератор на последнее ребро графа. */
    const_reverse_edge_iterator e_crbegin() const { return const_reverse_edge_iterator(e_cend()); }
    /** @brief Явный константный обратный итератор на конец обратной последовательности всех рёбер. */
    const_reverse_edge_iterator e_crend() const { return const_reverse_edge_iterator(e_cbegin()); }

    /**
     * @brief Итератор на начало списка смежных вершин для заданной вершины.
     * @param value Значение вершины.
     * @return Итератор на первую смежную вершину.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    adjacent_iterator adj_begin(const T& value) const {
        return find_vertex_strict(value)->adjacencies.begin();
    }
    /**
     * @brief Итератор на конец списка смежных вершин для заданной вершины.
     * @param value Значение вершины.
     * @return Итератор на конец списка смежностей.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    adjacent_iterator adj_end(const T& value) const {
        return find_vertex_strict(value)->adjacencies.end();
    }
    /** @brief Константный итератор на начало списка смежных вершин. */
    const_adjacent_iterator adj_cbegin(const T& value) const { return adj_begin(value); }
    /** @brief Константный итератор на конец списка смежных вершин. */
    const_adjacent_iterator adj_cend(const T& value) const { return adj_end(value); }
    /** @brief Обратный итератор на начало списка смежных вершин. */
    reverse_adjacent_iterator adj_rbegin(const T& value) const { return reverse_adjacent_iterator(adj_end(value)); }
    /** @brief Обратный итератор на конец списка смежных вершин. */
    reverse_adjacent_iterator adj_rend(const T& value) const { return reverse_adjacent_iterator(adj_begin(value)); }
    /** @brief Константный обратный итератор на начало списка смежных вершин. */
    const_reverse_adjacent_iterator adj_crbegin(const T& value) const { return const_reverse_adjacent_iterator(adj_cend(value)); }
    /** @brief Константный обратный итератор на конец списка смежных вершин. */
    const_reverse_adjacent_iterator adj_crend(const T& value) const { return const_reverse_adjacent_iterator(adj_cbegin(value)); }

    /**
     * @brief Однонаправленный итератор на первую смежную вершину (Вариант 2.1.12).
     * @param value Значение вершины.
     * @return forward_adjacent_iterator на начало смежных вершин.
     */
    forward_adjacent_iterator f_adj_begin(const T& value) const {
        return forward_adjacent_iterator(adj_begin(value));
    }
    /**
     * @brief Однонаправленный итератор на конец смежных вершин (Вариант 2.1.12).
     * @param value Значение вершины.
     * @return forward_adjacent_iterator на конец смежных вершин.
     */
    forward_adjacent_iterator f_adj_end(const T& value) const {
        return forward_adjacent_iterator(adj_end(value));
    }
    /** @brief Константный однонаправленный итератор на первую смежную вершину. */
    const_forward_adjacent_iterator f_adj_cbegin(const T& value) const { return f_adj_begin(value); }
    /** @brief Константный однонаправленный итератор на конец смежных вершин. */
    const_forward_adjacent_iterator f_adj_cend(const T& value) const { return f_adj_end(value); }

    /**
     * @brief Итератор на первое инцидентное (исходящее) ребро вершины.
     * @param value Значение вершины-источника.
     * @return incident_iterator на первое исходящее ребро.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    incident_iterator inc_begin(const T& value) const {
        auto vertex_it = find_vertex_strict(value);
        return incident_iterator(&(vertex_it->data), vertex_it->adjacencies.begin());
    }
    /**
     * @brief Итератор на конец инцидентных рёбер вершины.
     * @param value Значение вершины-источника.
     * @return incident_iterator на конец исходящих рёбер.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    incident_iterator inc_end(const T& value) const {
        auto vertex_it = find_vertex_strict(value);
        return incident_iterator(&(vertex_it->data), vertex_it->adjacencies.end());
    }
    /** @brief Константный итератор на первое инцидентное ребро. */
    const_incident_iterator inc_cbegin(const T& value) const { return inc_begin(value); }
    /** @brief Константный итератор на конец инцидентных рёбер. */
    const_incident_iterator inc_cend(const T& value) const { return inc_end(value); }
    /** @brief Обратный итератор на последнее инцидентное ребро. */
    reverse_incident_iterator inc_rbegin(const T& value) const { return reverse_incident_iterator(inc_end(value)); }
    /** @brief Обратный итератор на конец инцидентных рёбер. */
    reverse_incident_iterator inc_rend(const T& value) const { return reverse_incident_iterator(inc_begin(value)); }
    /** @brief Константный обратный итератор на последнее инцидентное ребро. */
    const_reverse_incident_iterator inc_crbegin(const T& value) const { return const_reverse_incident_iterator(inc_cend(value)); }
    /** @brief Константный обратный итератор на конец инцидентных рёбер. */
    const_reverse_incident_iterator inc_crend(const T& value) const { return const_reverse_incident_iterator(inc_cbegin(value)); }

    // ==========================================
    // МОДИФИКАЦИЯ ГРАФА И УДАЛЕНИЕ ЧЕРЕЗ ИТЕРАТОРЫ
    // ==========================================

    /**
     * @brief Вставка новой вершины в граф.
     * @param value Значение добавляемой вершины.
     * @throws std::invalid_argument если вершина с таким значением уже существует.
     */
    void insert_vertex(const T& value) {
        if (has_vertex(value)) {
            throw std::invalid_argument("Вершина уже существует!");
        }
        records.push_back({value, {}});
    }

    /**
     * @brief Удаление вершины по значению (удаляет саму вершину и все инцидентные ей дуги).
     * @param value Значение удаляемой вершины.
     * @throws std::invalid_argument если вершина не найдена в графе.
     */
    void erase_vertex(const T& value) {
        auto target_it = find_vertex(value);
        if (target_it == records.end()) {
            throw std::invalid_argument("Вершина не найдена!");
        }
        records.erase(target_it);
        // Удаляем все входящие дуги, ведущие в удалённую вершину.
        for (auto& record : records) {
            record.adjacencies.remove(value);
        }
    }

    /**
     * @brief Удаление вершины по итератору.
     * @param it Итератор на удаляемую вершину.
     * @throws std::invalid_argument если передан невалидный итератор (v_end()).
     */
    void erase_vertex(vertex_iterator it) {
        if (it == v_end()) throw std::invalid_argument("Невалидный итератор вершины!");
        erase_vertex(*it);
    }

    /**
     * @brief Удаление вершины по константному итератору.
     * @param it Константный итератор на удаляемую вершину.
     * @throws std::invalid_argument если передан невалидный итератор (v_cend()).
     */
    void erase_vertex(const_vertex_iterator it) {
        if (it == v_cend()) throw std::invalid_argument("Невалидный итератор вершины!");
        erase_vertex(*it);
    }

    /**
     * @brief Вставка ориентированного ребра между двумя существующими вершинами.
     * @param from Вершина-источник.
     * @param to Вершина-назначение.
     * @throws std::invalid_argument если одна из вершин не существует или ребро уже присутствует.
     */
    void insert_edge(const T& from, const T& to) {
        auto source_it = find_vertex(from);
        if (source_it == records.end() || !has_vertex(to)) {
            throw std::invalid_argument("Одной из вершин не существует!");
        }
        auto& adjacencies = source_it->adjacencies;
        if (std::find(adjacencies.begin(), adjacencies.end(), to) != adjacencies.end()) {
            throw std::invalid_argument("Ребро уже существует!");
        }
        adjacencies.push_back(to);
    }

    /**
     * @brief Удаление ориентированного ребра по значениям вершин.
     * @param from Вершина-источник.
     * @param to Вершина-назначение.
     * @throws std::invalid_argument если вершина-источник или ребро не найдены.
     */
    void erase_edge(const T& from, const T& to) {
        auto source_it = find_vertex(from);
        if (source_it == records.end()) {
            throw std::invalid_argument("Исходная вершина не найдена!");
        }
        auto edge_it = std::find(source_it->adjacencies.begin(), source_it->adjacencies.end(), to);
        if (edge_it == source_it->adjacencies.end()) {
            throw std::invalid_argument("Ребро не найдено!");
        }
        source_it->adjacencies.erase(edge_it);
    }

    /**
     * @brief Удаление ориентированного ребра по рёберному итератору.
     * @param it Итератор на удаляемое ребро.
     * @throws std::invalid_argument если передан невалидный итератор (e_end()).
     */
    void erase_edge(edge_iterator it) {
        if (it == e_end()) throw std::invalid_argument("Невалидный итератор ребра!");
        it.vertex_it->adjacencies.erase(it.edge_it);
    }

    /**
     * @brief Удаление ориентированного ребра по константному рёберному итератору.
     * @param it Константный итератор на удаляемое ребро.
     * @throws std::invalid_argument если передан невалидный итератор (e_cend()).
     */
    void erase_edge(const_edge_iterator it) {
        if (it == e_cend()) throw std::invalid_argument("Невалидный итератор ребра!");
        erase_edge(it.vertex_it->data, *it.edge_it);
    }

    // ==========================================
    // ИНФОРМАЦИЯ О ГРАФЕ И ПОИСК
    // ==========================================

    /**
     * @brief Проверяет наличие вершины в графе.
     * @param value Искомое значение вершины.
     * @return true, если вершина присутствует в графе.
     */
    bool has_vertex(const T& value) const { return find_vertex(value) != records.end(); }

    /**
     * @brief Проверяет наличие ориентированного ребра между вершинами.
     * @param from Вершина-источник.
     * @param to Вершина-назначение.
     * @return true, если ориентированное ребро from -> to существует.
     */
    bool has_edge(const T& from, const T& to) const {
        auto source_it = find_vertex(from);
        if (source_it == records.end()) return false;
        const auto& adjacencies = source_it->adjacencies;
        return std::find(adjacencies.begin(), adjacencies.end(), to) != adjacencies.end();
    }

    /**
     * @brief Вычисляет общую степень вершины (входящие + исходящие рёбра).
     * @param value Значение вершины.
     * @return Общая степень вершины.
     * @throws std::invalid_argument если вершина не найдена.
     */
    size_type vertex_degree(const T& value) const {
        auto target_it = find_vertex_strict(value);
        // Начинаем с полустепени исхода, затем добавляем число входящих дуг.
        size_type total_degree = target_it->adjacencies.size();
        for (const auto& record : records) {
            if (std::find(record.adjacencies.begin(), record.adjacencies.end(), value) != record.adjacencies.end()) {
                ++total_degree;
            }
        }
        return total_degree;
    }

    /**
     * @brief Вычисляет степень ребра (сумму степеней инцидентных ему вершин).
     * @param from Вершина-источник.
     * @param to Вершина-назначение.
     * @return Степень ребра.
     * @throws std::invalid_argument если ребро не найдено.
     */
    size_type edge_degree(const T& from, const T& to) const {
        if (!has_edge(from, to)) throw std::invalid_argument("Ребро не найдено!");
        return vertex_degree(from) + vertex_degree(to);
    }

    // ==========================================
    // ОПЕРАТОРЫ СРАВНЕНИЯ И ВЫВОДА
    // ==========================================

    /** @brief Проверка двух графов на строгое поэлементное равенство. */
    bool operator==(const Graph& other) const { return records == other.records; }
    /** @brief Проверка двух графов на неравенство. */
    bool operator!=(const Graph& other) const { return !(*this == other); }
    /** @brief Лексикографическое сравнение "меньше". */
    bool operator<(const Graph& other) const { return records < other.records; }
    /** @brief Лексикографическое сравнение "больше". */
    bool operator>(const Graph& other) const { return other.records < records; }
    /** @brief Лексикографическое сравнение "меньше либо равно". */
    bool operator<=(const Graph& other) const { return !(other.records < records); }
    /** @brief Лексикографическое сравнение "больше либо равно". */
    bool operator>=(const Graph& other) const { return !(records < other.records); }

    /**
     * @brief Потоковый вывод графа в поток os.
     * Построен на основе итераторов графа и обобщённого алгоритма std::for_each.
     * @param os Выходной поток.
     * @param graph Выводимый граф.
     * @return Ссылка на выходной поток.
     */
    friend std::ostream& operator<<(std::ostream& os, const Graph<T>& graph) {
        os << "Граф (Структура Вирта):\n";
        std::for_each(graph.v_cbegin(), graph.v_cend(), [&](const T& vertex) {
            os << "[" << vertex << "] -> ";
            if (graph.adj_cbegin(vertex) == graph.adj_cend(vertex)) {
                os << "(нет исходящих)";
            } else {
                std::for_each(graph.adj_cbegin(vertex), graph.adj_cend(vertex), [&](const T& adjacent_vertex) {
                    os << adjacent_vertex << " ";
                });
            }
            os << "\n";
        });
        return os;
    }
};

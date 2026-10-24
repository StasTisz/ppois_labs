/**
 * @file graph.h
 * @brief Обобщённый контейнер ориентированного графа на основе структуры Вирта.
 */

#pragma once

#include <list>
#include <utility>
#include <stdexcept>
#include <algorithm>
#include <iostream>
#include <iterator>

/**
 * @class Graph
 * @brief Обобщённый контейнер ориентированного графа (Структура Вирта).
 * 
 * Представляет граф в виде списка вершин (std::list<VertexRecord>),
 * где каждая запись вершины хранит данные и собственный список исходящих дуг.
 * 
 * @tparam T Тип данных, хранящихся в вершинах графа.
 */
template <typename T>
class Graph {
private:
    /**
     * @struct VertexRecord
     * @brief Внутренний узел структуры Вирта, хранящий вершину и список смежных вершин.
     */
    struct VertexRecord {
        T data;                     ///< Данные вершины
        std::list<T> adjacencies;   ///< Список смежных вершин (исходящих дуг)

        /**
         * @brief Проверка равенства записей вершин.
         * @param other Другая запись вершины.
         * @return true, если данные и списки смежностей идентичны.
         */
        bool operator==(const VertexRecord& other) const {
            return data == other.data && adjacencies == other.adjacencies;
        }

        /**
         * @brief Оператор сравнения "меньше" для лексикографического упорядочивания.
         * @param other Другая запись вершины.
         * @return true, если текущая вершина меньше other.
         */
        bool operator<(const VertexRecord& other) const {
            return data < other.data;
        }
    };

    std::list<VertexRecord> records; ///< Список записей вершин графа

    /**
     * @brief Внутренний поиск итератора вершины по значению.
     * @param val Искомое значение вершины.
     * @return Итератор на запись вершины в списке records либо records.end().
     */
    typename std::list<VertexRecord>::iterator find_vertex(const T& val) {
        for (auto it = records.begin(); it != records.end(); ++it) {
            if (it->data == val) return it;
        }
        return records.end();
    }

    /**
     * @brief Внутренний поиск константного итератора вершины по значению.
     * @param val Искомое значение вершины.
     * @return Константный итератор на запись вершины либо records.end().
     */
    typename std::list<VertexRecord>::const_iterator find_vertex(const T& val) const {
        for (auto it = records.begin(); it != records.end(); ++it) {
            if (it->data == val) return it;
        }
        return records.end();
    }

public:
    using value_type = T;                       ///< Тип значения вершины
    using reference = T&;                       ///< Ссылка на значение вершины
    using const_reference = const T&;           ///< Константная ссылка на значение вершины
    using pointer = T*;                         ///< Указатель на значение вершины
    using const_pointer = const T*;             ///< Константный указатель на значение вершины
    using size_type = std::size_t;              ///< Беззнаковый целочисленный тип размера
    using difference_type = std::ptrdiff_t;     ///< Знаковый тип разности итераторов
    using edge_type = std::pair<T, T>;          ///< Тип ребра (пара вершин: from, to)

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

    /**
     * @brief Полная очистка графа (удаление всех вершин и рёбер).
     */
    void clear() noexcept { records.clear(); }

    /**
     * @brief Возвращает общее количество вершин в графе.
     * @return Число вершин.
     */
    size_type vertex_count() const noexcept { return records.size(); }

    /**
     * @brief Возвращает общее количество рёбер в графе.
     * @return Число ориентированных рёбер.
     */
    size_type edge_count() const noexcept {
        size_type count = 0;
        for (const auto& rec : records) {
            count += rec.adjacencies.size();
        }
        return count;
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
     * @param val Значение вершины.
     * @return Итератор на первую смежную вершину.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    adjacent_iterator adj_begin(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена");
        return it->adjacencies.begin();
    }
    /** 
     * @brief Итератор на конец списка смежных вершин для заданной вершины.
     * @param val Значение вершины.
     * @return Итератор на конец списка смежностей.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    adjacent_iterator adj_end(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена");
        return it->adjacencies.end();
    }
    /** @brief Константный итератор на начало списка смежных вершин. */
    const_adjacent_iterator adj_cbegin(const T& val) const { return adj_begin(val); }
    /** @brief Константный итератор на конец списка смежных вершин. */
    const_adjacent_iterator adj_cend(const T& val) const { return adj_end(val); }
    /** @brief Обратный итератор на начало списка смежных вершин. */
    reverse_adjacent_iterator adj_rbegin(const T& val) const { return reverse_adjacent_iterator(adj_end(val)); }
    /** @brief Обратный итератор на конец списка смежных вершин. */
    reverse_adjacent_iterator adj_rend(const T& val) const { return reverse_adjacent_iterator(adj_begin(val)); }
    /** @brief Константный обратный итератор на начало списка смежных вершин. */
    const_reverse_adjacent_iterator adj_crbegin(const T& val) const { return const_reverse_adjacent_iterator(adj_cend(val)); }
    /** @brief Константный обратный итератор на конец списка смежных вершин. */
    const_reverse_adjacent_iterator adj_crend(const T& val) const { return const_reverse_adjacent_iterator(adj_cbegin(val)); }

    /** 
     * @brief Однонаправленный итератор на первую смежную вершину (Вариант 2.1.12).
     * @param val Значение вершины.
     * @return forward_adjacent_iterator на начало смежных вершин.
     */
    forward_adjacent_iterator f_adj_begin(const T& val) const {
        return forward_adjacent_iterator(adj_begin(val));
    }
    /** 
     * @brief Однонаправленный итератор на конец смежных вершин (Вариант 2.1.12).
     * @param val Значение вершины.
     * @return forward_adjacent_iterator на конец смежных вершин.
     */
    forward_adjacent_iterator f_adj_end(const T& val) const {
        return forward_adjacent_iterator(adj_end(val));
    }

    /** 
     * @brief Итератор на первое инцидентное (исходящее) ребро вершины.
     * @param val Значение вершины-источника.
     * @return incident_iterator на первое исходящее ребро.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    incident_iterator inc_begin(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена");
        return incident_iterator(&(it->data), it->adjacencies.begin());
    }
    /** 
     * @brief Итератор на конец инцидентных рёбер вершины.
     * @param val Значение вершины-источника.
     * @return incident_iterator на конец исходящих рёбер.
     * @throws std::invalid_argument если вершина отсутствует в графе.
     */
    incident_iterator inc_end(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена");
        return incident_iterator(&(it->data), it->adjacencies.end());
    }
    /** @brief Константный итератор на первое инцидентное ребро. */
    const_incident_iterator inc_cbegin(const T& val) const { return inc_begin(val); }
    /** @brief Константный итератор на конец инцидентных рёбер. */
    const_incident_iterator inc_cend(const T& val) const { return inc_end(val); }
    /** @brief Обратный итератор на последнее инцидентное ребро. */
    reverse_incident_iterator inc_rbegin(const T& val) const { return reverse_incident_iterator(inc_end(val)); }
    /** @brief Обратный итератор на конец инцидентных рёбер. */
    reverse_incident_iterator inc_rend(const T& val) const { return reverse_incident_iterator(inc_begin(val)); }
    /** @brief Константный обратный итератор на последнее инцидентное ребро. */
    const_reverse_incident_iterator inc_crbegin(const T& val) const { return const_reverse_incident_iterator(inc_cend(val)); }
    /** @brief Константный обратный итератор на конец инцидентных рёбер. */
    const_reverse_incident_iterator inc_crend(const T& val) const { return const_reverse_incident_iterator(inc_cbegin(val)); }

    // ==========================================
    // МОДИФИКАЦИЯ ГРАФА И УДАЛЕНИЕ ЧЕРЕЗ ИТЕРАТОРЫ
    // ==========================================

    /**
     * @brief Вставка новой вершины в граф.
     * @param val Значение добавляемой вершины.
     * @throws std::invalid_argument если вершина с таким значением уже существует.
     */
    void insert_vertex(const T& val) {
        if (has_vertex(val)) throw std::invalid_argument("Вершина уже существует!");
        records.push_back({val, {}});
    }

    /**
     * @brief Удаление вершины по значению (удаляет саму вершину и все инцидентные ей рёбра).
     * @param val Значение удаляемой вершины.
     * @throws std::invalid_argument если вершина не найдена в графе.
     */
    void erase_vertex(const T& val) {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена!");
        records.erase(it);
        for (auto& rec : records) rec.adjacencies.remove(val);
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
        auto it_from = find_vertex(from);
        if (it_from == records.end() || !has_vertex(to)) {
            throw std::invalid_argument("Одной из вершин не существует!");
        }
        auto& adj = it_from->adjacencies;
        if (std::find(adj.begin(), adj.end(), to) != adj.end()) {
            throw std::invalid_argument("Ребро уже существует!");
        }
        adj.push_back(to);
    }

    /**
     * @brief Удаление ориентированного ребра по значениям вершин.
     * @param from Вершина-источник.
     * @param to Вершина-назначение.
     * @throws std::invalid_argument если вершина-источник или ребро не найдены.
     */
    void erase_edge(const T& from, const T& to) {
        auto it_from = find_vertex(from);
        if (it_from == records.end()) throw std::invalid_argument("Исходная вершина не найдена!");

        auto edge_it = std::find(it_from->adjacencies.begin(), it_from->adjacencies.end(), to);
        if (edge_it == it_from->adjacencies.end()) throw std::invalid_argument("Ребро не найдено!");

        it_from->adjacencies.erase(edge_it);
    }

    /**
     * @brief Удаление ориентированного ребра по рёберному итератору.
     * @param it Итератор на удаляемое ребро.
     * @throws std::invalid_argument если передан невалидный итератор (e_end()).
     */
    void erase_edge(edge_iterator it) {
        if (it == e_end()) throw std::invalid_argument("Невалидный итератор ребра!");
        it.v_it->adjacencies.erase(it.e_it);
    }

    /**
     * @brief Удаление ориентированного ребра по константному рёберному итератору.
     * @param it Константный итератор на удаляемое ребро.
     * @throws std::invalid_argument если передан невалидный итератор (e_cend()).
     */
    void erase_edge(const_edge_iterator it) {
        if (it == e_cend()) throw std::invalid_argument("Невалидный итератор ребра!");
        erase_edge(it.v_it->data, *it.e_it);
    }

    // ==========================================
    // ИНФОРМАЦИЯ О ГРАФЕ И ПОИСК
    // ==========================================

    /**
     * @brief Проверяет наличие вершины в графе.
     * @param val Искомое значение вершины.
     * @return true, если вершина присутствует в графе.
     */
    bool has_vertex(const T& val) const { return find_vertex(val) != records.end(); }

    /**
     * @brief Проверяет наличие ориентированного ребра между вершинами.
     * @param from Вершина-источник.
     * @param to Вершина-назначение.
     * @return true, если ориентированное ребро from -> to существует.
     */
    bool has_edge(const T& from, const T& to) const {
        auto it = find_vertex(from);
        if (it == records.end()) return false;
        return std::find(it->adjacencies.begin(), it->adjacencies.end(), to) != it->adjacencies.end();
    }

    /**
     * @brief Вычисляет общую степень вершины (сумму входящих и исходящих рёбер).
     * @param val Значение вершины.
     * @return Общая степень вершины.
     * @throws std::invalid_argument если вершина не найдена.
     */
    size_type vertex_degree(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена!");

        size_type degree = it->adjacencies.size();
        for (const auto& rec : records) {
            if (std::find(rec.adjacencies.begin(), rec.adjacencies.end(), val) != rec.adjacencies.end()) {
                degree++;
            }
        }
        return degree;
    }

    /**
     * @brief Вычисляет степень ребра (сумму степеней инцидентных вершин).
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
                std::for_each(graph.adj_cbegin(vertex), graph.adj_cend(vertex), [&](const T& adj) {
                    os << adj << " ";
                });
            }
            os << "\n";
        });
        return os;
    }
};
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

template <typename T>
class Graph {
private:
    struct VertexRecord {
        T data;
        std::list<T> adjacencies;

        bool operator==(const VertexRecord& other) const {
            return data == other.data && adjacencies == other.adjacencies;
        }
        bool operator<(const VertexRecord& other) const {
            return data < other.data;
        }
    };

    std::list<VertexRecord> records;

    typename std::list<VertexRecord>::iterator find_vertex(const T& val) {
        for (auto it = records.begin(); it != records.end(); ++it) {
            if (it->data == val) return it;
        }
        return records.end();
    }

    typename std::list<VertexRecord>::const_iterator find_vertex(const T& val) const {
        for (auto it = records.begin(); it != records.end(); ++it) {
            if (it->data == val) return it;
        }
        return records.end();
    }

public:
    using value_type = T;
    using reference = T&;
    using const_reference = const T&;
    using pointer = T*;
    using const_pointer = const T*;
    using size_type = std::size_t;
    using difference_type = std::ptrdiff_t;
    using edge_type = std::pair<T, T>;

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

    /** @brief Конструктор по умолчанию */
    Graph() = default;

    /** @brief Конструктор копирования */
    Graph(const Graph& other) = default;

    /** @brief Конструктор перемещения (РЕФАКТОРИНГ: Добавлено для ресурсоемких контейнеров) */
    Graph(Graph&& other) noexcept = default;

    /** @brief Деструктор */
    ~Graph() = default;

    /** @brief Оператор присваивания копированием */
    Graph& operator=(const Graph& other) = default;

    /** @brief Оператор присваивания перемещением (РЕФАКТОРИНГ: Добавлено) */
    Graph& operator=(Graph&& other) noexcept = default;

    bool empty() const noexcept { return records.empty(); }

    void clear() noexcept { records.clear(); }

    size_type vertex_count() const noexcept { return records.size(); }

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

    vertex_iterator v_begin() { return vertex_iterator(records.begin()); }
    vertex_iterator v_end() { return vertex_iterator(records.end()); }
    const_vertex_iterator v_begin() const { return v_cbegin(); }
    const_vertex_iterator v_end() const { return v_cend(); }
    const_vertex_iterator v_cbegin() const { return const_vertex_iterator(records.begin()); }
    const_vertex_iterator v_cend() const { return const_vertex_iterator(records.end()); }
    reverse_vertex_iterator v_rbegin() { return reverse_vertex_iterator(v_end()); }
    reverse_vertex_iterator v_rend() { return reverse_vertex_iterator(v_begin()); }
    const_reverse_vertex_iterator v_rbegin() const { return v_crbegin(); }
    const_reverse_vertex_iterator v_rend() const { return v_crend(); }
    const_reverse_vertex_iterator v_crbegin() const { return const_reverse_vertex_iterator(v_cend()); }
    const_reverse_vertex_iterator v_crend() const { return const_reverse_vertex_iterator(v_cbegin()); }

    edge_iterator e_begin() {
        if (records.empty()) return e_end();
        return edge_iterator(records.begin(), records.end(), records.begin()->adjacencies.begin());
    }
    edge_iterator e_end() {
        if (records.empty()) return edge_iterator(records.end(), records.end(), {});
        return edge_iterator(records.end(), records.end(), records.back().adjacencies.end());
    }
    const_edge_iterator e_begin() const { return e_cbegin(); }
    const_edge_iterator e_end() const { return e_cend(); }
    const_edge_iterator e_cbegin() const {
        if (records.empty()) return e_cend();
        return const_edge_iterator(records.begin(), records.end(), records.begin()->adjacencies.begin());
    }
    const_edge_iterator e_cend() const {
        if (records.empty()) return const_edge_iterator(records.end(), records.end(), {});
        return const_edge_iterator(records.end(), records.end(), records.back().adjacencies.end());
    }
    reverse_edge_iterator e_rbegin() { return reverse_edge_iterator(e_end()); }
    reverse_edge_iterator e_rend() { return reverse_edge_iterator(e_begin()); }
    const_reverse_edge_iterator e_rbegin() const { return e_crbegin(); }
    const_reverse_edge_iterator e_rend() const { return e_crend(); }
    const_reverse_edge_iterator e_crbegin() const { return const_reverse_edge_iterator(e_cend()); }
    const_reverse_edge_iterator e_crend() const { return const_reverse_edge_iterator(e_cbegin()); }

    adjacent_iterator adj_begin(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена");
        return it->adjacencies.begin();
    }
    adjacent_iterator adj_end(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена");
        return it->adjacencies.end();
    }
    const_adjacent_iterator adj_cbegin(const T& val) const { return adj_begin(val); }
    const_adjacent_iterator adj_cend(const T& val) const { return adj_end(val); }
    reverse_adjacent_iterator adj_rbegin(const T& val) const { return reverse_adjacent_iterator(adj_end(val)); }
    reverse_adjacent_iterator adj_rend(const T& val) const { return reverse_adjacent_iterator(adj_begin(val)); }
    const_reverse_adjacent_iterator adj_crbegin(const T& val) const { return const_reverse_adjacent_iterator(adj_cend(val)); }
    const_reverse_adjacent_iterator adj_crend(const T& val) const { return const_reverse_adjacent_iterator(adj_cbegin(val)); }

    forward_adjacent_iterator f_adj_begin(const T& val) const {
        return forward_adjacent_iterator(adj_begin(val));
    }
    forward_adjacent_iterator f_adj_end(const T& val) const {
        return forward_adjacent_iterator(adj_end(val));
    }

    incident_iterator inc_begin(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена");
        return incident_iterator(&(it->data), it->adjacencies.begin());
    }
    incident_iterator inc_end(const T& val) const {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена");
        return incident_iterator(&(it->data), it->adjacencies.end());
    }
    const_incident_iterator inc_cbegin(const T& val) const { return inc_begin(val); }
    const_incident_iterator inc_cend(const T& val) const { return inc_end(val); }
    reverse_incident_iterator inc_rbegin(const T& val) const { return reverse_incident_iterator(inc_end(val)); }
    reverse_incident_iterator inc_rend(const T& val) const { return reverse_incident_iterator(inc_begin(val)); }
    const_reverse_incident_iterator inc_crbegin(const T& val) const { return const_reverse_incident_iterator(inc_cend(val)); }
    const_reverse_incident_iterator inc_crend(const T& val) const { return const_reverse_incident_iterator(inc_cbegin(val)); }

    // ==========================================
    // МОДИФИКАЦИЯ ГРАФА И УДАЛЕНИЕ ЧЕРЕЗ ИТЕРАТОРЫ
    // ==========================================

    void insert_vertex(const T& val) {
        if (has_vertex(val)) throw std::invalid_argument("Вершина уже существует!");
        records.push_back({val, {}});
    }

    void erase_vertex(const T& val) {
        auto it = find_vertex(val);
        if (it == records.end()) throw std::invalid_argument("Вершина не найдена!");
        records.erase(it);
        for (auto& rec : records) rec.adjacencies.remove(val);
    }

    void erase_vertex(vertex_iterator it) {
        if (it == v_end()) throw std::invalid_argument("Невалидный итератор вершины!");
        erase_vertex(*it);
    }

    void erase_vertex(const_vertex_iterator it) {
        if (it == v_cend()) throw std::invalid_argument("Невалидный итератор вершины!");
        erase_vertex(*it);
    }

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

    void erase_edge(const T& from, const T& to) {
        auto it_from = find_vertex(from);
        if (it_from == records.end()) throw std::invalid_argument("Исходная вершина не найдена!");

        auto edge_it = std::find(it_from->adjacencies.begin(), it_from->adjacencies.end(), to);
        if (edge_it == it_from->adjacencies.end()) throw std::invalid_argument("Ребро не найдено!");

        it_from->adjacencies.erase(edge_it);
    }

    void erase_edge(edge_iterator it) {
        if (it == e_end()) throw std::invalid_argument("Невалидный итератор ребра!");
        it.v_it->adjacencies.erase(it.e_it);
    }

    void erase_edge(const_edge_iterator it) {
        if (it == e_cend()) throw std::invalid_argument("Невалидный итератор ребра!");
        erase_edge(it.v_it->data, *it.e_it);
    }

    // ==========================================
    // ИНФОРМАЦИЯ О ГРАФЕ И ПОИСК
    // ==========================================

    bool has_vertex(const T& val) const { return find_vertex(val) != records.end(); }

    bool has_edge(const T& from, const T& to) const {
        auto it = find_vertex(from);
        if (it == records.end()) return false;
        return std::find(it->adjacencies.begin(), it->adjacencies.end(), to) != it->adjacencies.end();
    }

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

    size_type edge_degree(const T& from, const T& to) const {
        if (!has_edge(from, to)) throw std::invalid_argument("Ребро не найдено!");
        return vertex_degree(from) + vertex_degree(to);
    }

    // ==========================================
    // ОПЕРАТОРЫ СРАВНЕНИЯ И ВЫВОДА
    // ==========================================

    bool operator==(const Graph& other) const { return records == other.records; }
    bool operator!=(const Graph& other) const { return !(*this == other); }
    bool operator<(const Graph& other) const { return records < other.records; }
    bool operator>(const Graph& other) const { return other.records < records; }
    bool operator<=(const Graph& other) const { return !(other.records < records); }
    bool operator>=(const Graph& other) const { return !(records < other.records); }

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
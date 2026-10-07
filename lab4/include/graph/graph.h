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
    using size_type = std::size_t;
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
    const_vertex_iterator v_cbegin() const { return const_vertex_iterator(records.begin()); }
    const_vertex_iterator v_cend() const { return const_vertex_iterator(records.end()); }
    reverse_vertex_iterator v_rbegin() { return reverse_vertex_iterator(v_end()); }
    reverse_vertex_iterator v_rend() { return reverse_vertex_iterator(v_begin()); }

    edge_iterator e_begin() {
        if (records.empty()) return e_end();
        return edge_iterator(records.begin(), records.end(), records.begin()->adjacencies.begin());
    }
    edge_iterator e_end() {
        if (records.empty()) return edge_iterator(records.end(), records.end(), {});
        return edge_iterator(records.end(), records.end(), records.back().adjacencies.end());
    }
    const_edge_iterator e_cbegin() const {
        if (records.empty()) return e_cend();
        return const_edge_iterator(records.begin(), records.end(), records.begin()->adjacencies.begin());
    }
    const_edge_iterator e_cend() const {
        if (records.empty()) return const_edge_iterator(records.end(), records.end(), {});
        return const_edge_iterator(records.end(), records.end(), records.back().adjacencies.end());
    }

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
        it.v_it->adjacencies.erase(it.e_it);
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
        for (const auto& rec : graph.records) {
            os << "[" << rec.data << "] -> ";
            if (rec.adjacencies.empty()) {
                os << "(нет исходящих)";
            } else {
                for (const auto& adj : rec.adjacencies) {
                    os << adj << " ";
                }
            }
            os << "\n";
        }
        return os;
    }
};
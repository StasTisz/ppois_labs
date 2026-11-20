/**
 * @file edge_iterator.h
 * @brief Итераторы рёбер для графа.
 * @note Файл предназначен для включения (include) внутрь шаблона Graph<T>.
 */

#pragma once

// ==========================================
// ИТЕРАТОРЫ РЁБЕР
// ==========================================

class const_edge_iterator; // Предварительное объявление

/**
 * @class edge_iterator
 * @brief Двунаправленный итератор по всем рёбрам графа.
 */
class edge_iterator {
private:
    typename std::list<VertexRecord>::iterator vertex_it{};  ///< Текущая вершина-источник
    typename std::list<VertexRecord>::iterator vertex_end{}; ///< Конец списка вершин
    typename std::list<T>::iterator edge_it{};               ///< Текущая смежная вершина (цель ребра)
    friend class Graph;
    friend class const_edge_iterator;

    /**
     * @brief Перемещает итератор на первую непустую смежность, если текущая исчерпана.
     */
    void advance_to_valid() {
        while (vertex_it != vertex_end && edge_it == vertex_it->adjacencies.end()) {
            ++vertex_it;
            if (vertex_it != vertex_end) {
                edge_it = vertex_it->adjacencies.begin();
            }
        }
    }

public:
    using iterator_category = std::bidirectional_iterator_tag; ///< Категория двунаправленного итератора
    using value_type = edge_type;                              ///< Тип значения (пара вершин: from, to)
    using difference_type = std::ptrdiff_t;                    ///< Тип разности итераторов
    using pointer = edge_type*;                                ///< Указатель на ребро
    using reference = edge_type;                               ///< Ребро возвращается по значению

    /** @brief Конструктор по умолчанию. */
    edge_iterator() = default;

    /**
     * @brief Параметризованный конструктор итератора рёбер.
     * @param current_vertex Итератор текущей вершины.
     * @param end_vertex Конец списка вершин.
     * @param current_edge Итератор смежной вершины в текущем списке adjacencies.
     */
    edge_iterator(typename std::list<VertexRecord>::iterator current_vertex,
                  typename std::list<VertexRecord>::iterator end_vertex,
                  typename std::list<T>::iterator current_edge)
        : vertex_it(current_vertex), vertex_end(end_vertex), edge_it(current_edge) {
        advance_to_valid();
    }

    /** @brief Разыменование: возвращает ребро как std::pair<T, T>{from, to}. */
    reference operator*() const { return {vertex_it->data, *edge_it}; }

    /** @brief Префиксный инкремент к следующему ребру. */
    edge_iterator& operator++() { ++edge_it; advance_to_valid(); return *this; }

    /** @brief Постфиксный инкремент к следующему ребру. */
    edge_iterator operator++(int) {
        edge_iterator previous = *this;
        ++(*this);
        return previous;
    }

    /** @brief Префиксный декремент к предыдущему ребру (пропускает вершины без исходящих дуг). */
    edge_iterator& operator--() {
        if (vertex_it == vertex_end || edge_it == vertex_it->adjacencies.begin()) {
            do { --vertex_it; } while (vertex_it->adjacencies.empty());
            edge_it = vertex_it->adjacencies.end();
        }
        --edge_it;
        return *this;
    }

    /** @brief Постфиксный декремент к предыдущему ребру. */
    edge_iterator operator--(int) {
        edge_iterator previous = *this;
        --(*this);
        return previous;
    }

    /** @brief Проверка равенства двух рёберных итераторов. */
    bool operator==(const edge_iterator& other) const {
        if (vertex_it == vertex_end && other.vertex_it == other.vertex_end) return true;
        return vertex_it == other.vertex_it && edge_it == other.edge_it;
    }

    /** @brief Проверка неравенства двух рёберных итераторов. */
    bool operator!=(const edge_iterator& other) const { return !(*this == other); }
};

/**
 * @class const_edge_iterator
 * @brief Константный итератор по рёбрам (предотвращает модификацию графа).
 */
class const_edge_iterator {
private:
    typename std::list<VertexRecord>::const_iterator vertex_it{};  ///< Константный итератор вершины-источника
    typename std::list<VertexRecord>::const_iterator vertex_end{}; ///< Конец списка вершин
    typename std::list<T>::const_iterator edge_it{};               ///< Константный итератор целевой вершины
    friend class Graph;

    /**
     * @brief Перемещает итератор на первую непустую смежность, если текущая исчерпана.
     */
    void advance_to_valid() {
        while (vertex_it != vertex_end && edge_it == vertex_it->adjacencies.end()) {
            ++vertex_it;
            if (vertex_it != vertex_end) {
                edge_it = vertex_it->adjacencies.begin();
            }
        }
    }

public:
    using iterator_category = std::bidirectional_iterator_tag; ///< Категория двунаправленного итератора
    using value_type = edge_type;                              ///< Тип значения (пара вершин: from, to)
    using difference_type = std::ptrdiff_t;                    ///< Тип разности итераторов
    using pointer = edge_type*;                                ///< Указатель на ребро
    using reference = edge_type;                               ///< Ребро возвращается по значению

    /** @brief Конструктор по умолчанию. */
    const_edge_iterator() = default;

    /**
     * @brief Параметризованный конструктор константного итератора рёбер.
     * @param current_vertex Константный итератор текущей вершины.
     * @param end_vertex Константный итератор конца списка вершин.
     * @param current_edge Константный итератор смежной вершины.
     */
    const_edge_iterator(typename std::list<VertexRecord>::const_iterator current_vertex,
                        typename std::list<VertexRecord>::const_iterator end_vertex,
                        typename std::list<T>::const_iterator current_edge)
        : vertex_it(current_vertex), vertex_end(end_vertex), edge_it(current_edge) {
        advance_to_valid();
    }

    /**
     * @brief Конструктор неявного преобразования из неконстантного итератора.
     * @param non_const Неконстантный итератор ребра.
     */
    const_edge_iterator(const edge_iterator& non_const)
        : vertex_it(non_const.vertex_it), vertex_end(non_const.vertex_end), edge_it(non_const.edge_it) {
        advance_to_valid();
    }

    /** @brief Разыменование: возвращает ребро как std::pair<T, T>{from, to}. */
    reference operator*() const { return {vertex_it->data, *edge_it}; }

    /** @brief Префиксный инкремент к следующему ребру. */
    const_edge_iterator& operator++() { ++edge_it; advance_to_valid(); return *this; }

    /** @brief Постфиксный инкремент к следующему ребру. */
    const_edge_iterator operator++(int) {
        const_edge_iterator previous = *this;
        ++(*this);
        return previous;
    }

    /** @brief Префиксный декремент к предыдущему ребру (пропускает вершины без исходящих дуг). */
    const_edge_iterator& operator--() {
        if (vertex_it == vertex_end || edge_it == vertex_it->adjacencies.begin()) {
            do { --vertex_it; } while (vertex_it->adjacencies.empty());
            edge_it = vertex_it->adjacencies.end();
        }
        --edge_it;
        return *this;
    }

    /** @brief Постфиксный декремент к предыдущему ребру. */
    const_edge_iterator operator--(int) {
        const_edge_iterator previous = *this;
        --(*this);
        return previous;
    }

    /** @brief Проверка равенства двух константных рёберных итераторов. */
    bool operator==(const const_edge_iterator& other) const {
        if (vertex_it == vertex_end && other.vertex_it == other.vertex_end) return true;
        return vertex_it == other.vertex_it && edge_it == other.edge_it;
    }

    /** @brief Проверка неравенства двух константных рёберных итераторов. */
    bool operator!=(const const_edge_iterator& other) const { return !(*this == other); }
};

using reverse_edge_iterator = std::reverse_iterator<edge_iterator>;             ///< Обратный итератор рёбер
using const_reverse_edge_iterator = std::reverse_iterator<const_edge_iterator>; ///< Константный обратный итератор рёбер

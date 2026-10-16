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
    typename std::list<VertexRecord>::iterator v_it;   ///< Текущая вершина-источник
    typename std::list<VertexRecord>::iterator v_end;  ///< Конец списка вершин
    typename std::list<T>::iterator e_it;              ///< Текущая смежная вершина (цель ребра)
    friend class Graph;
    friend class const_edge_iterator;

    /**
     * @brief Перемещает итератор на следующую непустую смежность, если текущая исчерпана.
     */
    void advance_to_valid() {
        while (v_it != v_end && e_it == v_it->adjacencies.end()) {
            ++v_it;
            if (v_it != v_end) e_it = v_it->adjacencies.begin();
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
     * @param v Итератор текущей вершины.
     * @param vend Конец списка вершин.
     * @param e Итератор смежной вершины в текущем списке adjacencies.
     */
    edge_iterator(typename std::list<VertexRecord>::iterator v,
                  typename std::list<VertexRecord>::iterator vend,
                  typename std::list<T>::iterator e) : v_it(v), v_end(vend), e_it(e) {
        advance_to_valid();
    }

    /** @brief Разыменование: возвращает ребро как std::pair<T, T>{from, to}. */
    reference operator*() const { return {v_it->data, *e_it}; }

    /** @brief Префиксный инкремент к следующему ребру. */
    edge_iterator& operator++() { ++e_it; advance_to_valid(); return *this; }

    /** @brief Постфиксный инкремент к следующему ребру. */
    edge_iterator operator++(int) {
        edge_iterator tmp = *this;
        ++(*this);
        return tmp;
    }

    /** @brief Префиксный декремент к предыдущему ребру. */
    edge_iterator& operator--() {
        if (v_it == v_end || e_it == v_it->adjacencies.begin()) {
            do { --v_it; } while (v_it->adjacencies.empty());
            e_it = v_it->adjacencies.end();
        }
        --e_it;
        return *this;
    }

    /** @brief Постфиксный декремент к предыдущему ребру. */
    edge_iterator operator--(int) {
        edge_iterator tmp = *this;
        --(*this);
        return tmp;
    }

    /** @brief Проверка равенства двух рёберных итераторов. */
    bool operator==(const edge_iterator& other) const {
        if (v_it == v_end && other.v_it == other.v_end) return true;
        return v_it == other.v_it && e_it == other.e_it;
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
    typename std::list<VertexRecord>::const_iterator v_it;  ///< Константный итератор вершины-источника
    typename std::list<VertexRecord>::const_iterator v_end; ///< Конец списка вершин
    typename std::list<T>::const_iterator e_it;             ///< Константный итератор целевой вершины
    friend class Graph;

    /**
     * @brief Перемещает итератор на следующую непустую смежность, если текущая исчерпана.
     */
    void advance_to_valid() {
        while (v_it != v_end && e_it == v_it->adjacencies.end()) {
            ++v_it;
            if (v_it != v_end) e_it = v_it->adjacencies.begin();
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
     * @param v Константный итератор текущей вершины.
     * @param vend Константный итератор конца списка вершин.
     * @param e Константный итератор смежной вершины.
     */
    const_edge_iterator(typename std::list<VertexRecord>::const_iterator v,
                        typename std::list<VertexRecord>::const_iterator vend,
                        typename std::list<T>::const_iterator e) : v_it(v), v_end(vend), e_it(e) {
        advance_to_valid();
    }

    /**
     * @brief Конструктор неявного преобразования из неконстантного итератора.
     * @param non_const Неконстантный итератор ребра.
     */
    const_edge_iterator(const edge_iterator& non_const)
        : v_it(non_const.v_it), v_end(non_const.v_end), e_it(non_const.e_it) {
        advance_to_valid();
    }

    /** @brief Разыменование: возвращает ребро как std::pair<T, T>{from, to}. */
    reference operator*() const { return {v_it->data, *e_it}; }

    /** @brief Префиксный инкремент к следующему ребру. */
    const_edge_iterator& operator++() { ++e_it; advance_to_valid(); return *this; }

    /** @brief Постфиксный инкремент к следующему ребру. */
    const_edge_iterator operator++(int) {
        const_edge_iterator tmp = *this;
        ++(*this);
        return tmp;
    }

    /** @brief Префиксный декремент к предыдущему ребру. */
    const_edge_iterator& operator--() {
        if (v_it == v_end || e_it == v_it->adjacencies.begin()) {
            do { --v_it; } while (v_it->adjacencies.empty());
            e_it = v_it->adjacencies.end();
        }
        --e_it;
        return *this;
    }

    /** @brief Постфиксный декремент к предыдущему ребру. */
    const_edge_iterator operator--(int) {
        const_edge_iterator tmp = *this;
        --(*this);
        return tmp;
    }

    /** @brief Проверка равенства двух константных рёберных итераторов. */
    bool operator==(const const_edge_iterator& other) const {
        if (v_it == v_end && other.v_it == other.v_end) return true;
        return v_it == other.v_it && e_it == other.e_it;
    }

    /** @brief Проверка неравенства двух константных рёберных итераторов. */
    bool operator!=(const const_edge_iterator& other) const { return !(*this == other); }
};

using reverse_edge_iterator = std::reverse_iterator<edge_iterator>;             ///< Обратный итератор рёбер
using const_reverse_edge_iterator = std::reverse_iterator<const_edge_iterator>; ///< Константный обратный итератор рёбер
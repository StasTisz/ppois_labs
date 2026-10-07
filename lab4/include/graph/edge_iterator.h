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
    typename std::list<VertexRecord>::iterator v_it;
    typename std::list<VertexRecord>::iterator v_end;
    typename std::list<T>::iterator e_it;
    friend class Graph;
    friend class const_edge_iterator; // РЕФАКТОРИНГ: Разрешаем доступ для конвертации

    void advance_to_valid() {
        while (v_it != v_end && e_it == v_it->adjacencies.end()) {
            ++v_it;
            if (v_it != v_end) e_it = v_it->adjacencies.begin();
        }
    }
public:
    using iterator_category = std::bidirectional_iterator_tag;
    using value_type = edge_type;
    using difference_type = std::ptrdiff_t;
    using pointer = edge_type*;
    using reference = edge_type;

    edge_iterator() = default;
    edge_iterator(typename std::list<VertexRecord>::iterator v,
                  typename std::list<VertexRecord>::iterator vend,
                  typename std::list<T>::iterator e) : v_it(v), v_end(vend), e_it(e) {
        advance_to_valid();
    }

    reference operator*() const { return {v_it->data, *e_it}; }

    edge_iterator& operator++() { ++e_it; advance_to_valid(); return *this; }
    edge_iterator& operator--() {
        if (v_it == v_end || e_it == v_it->adjacencies.begin()) {
            do { --v_it; } while (v_it->adjacencies.empty());
            e_it = v_it->adjacencies.end();
        }
        --e_it;
        return *this;
    }
    bool operator==(const edge_iterator& other) const { return v_it == other.v_it && e_it == other.e_it; }
    bool operator!=(const edge_iterator& other) const { return !(*this == other); }
};

/**
 * @class const_edge_iterator
 * @brief Честный константный итератор по рёбрам (предотвращает модификацию графа).
 */
class const_edge_iterator {
private:
    typename std::list<VertexRecord>::const_iterator v_it;
    typename std::list<VertexRecord>::const_iterator v_end;
    typename std::list<T>::const_iterator e_it;

    void advance_to_valid() {
        while (v_it != v_end && e_it == v_it->adjacencies.end()) {
            ++v_it;
            if (v_it != v_end) e_it = v_it->adjacencies.begin();
        }
    }
public:
    using iterator_category = std::bidirectional_iterator_tag;
    using value_type = edge_type;
    using difference_type = std::ptrdiff_t;
    using pointer = edge_type*;
    using reference = edge_type;

    const_edge_iterator() = default;
    const_edge_iterator(typename std::list<VertexRecord>::const_iterator v,
                        typename std::list<VertexRecord>::const_iterator vend,
                        typename std::list<T>::const_iterator e) : v_it(v), v_end(vend), e_it(e) {
        advance_to_valid();
    }

    const_edge_iterator(const edge_iterator& non_const)
        : v_it(non_const.v_it), v_end(non_const.v_end), e_it(non_const.e_it) { // Теперь это компилируется
        advance_to_valid();
    }

    reference operator*() const { return {v_it->data, *e_it}; }
    const_edge_iterator& operator++() { ++e_it; advance_to_valid(); return *this; }
    const_edge_iterator& operator--() {
        if (v_it == v_end || e_it == v_it->adjacencies.begin()) {
            do { --v_it; } while (v_it->adjacencies.empty());
            e_it = v_it->adjacencies.end();
        }
        --e_it;
        return *this;
    }
    bool operator==(const const_edge_iterator& other) const { return v_it == other.v_it && e_it == other.e_it; }
    bool operator!=(const const_edge_iterator& other) const { return !(*this == other); }
};

using reverse_edge_iterator = std::reverse_iterator<edge_iterator>;
using const_reverse_edge_iterator = std::reverse_iterator<const_edge_iterator>;
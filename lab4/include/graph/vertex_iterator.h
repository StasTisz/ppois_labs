/**
 * @file vertex_iterator.h
 * @brief Итераторы вершин для графа.
 * @note Файл предназначен для включения (include) внутрь шаблона Graph<T>.
 */

#pragma once

// ==========================================
// ИТЕРАТОРЫ ВЕРШИН
// ==========================================

class const_vertex_iterator; // Предварительное объявление

/**
 * @class vertex_iterator
 * @brief Двунаправленный итератор по вершинам графа.
 */
class vertex_iterator {
private:
    typename std::list<VertexRecord>::iterator it;
    friend class Graph;
    friend class const_vertex_iterator; // РЕФАКТОРИНГ: Разрешаем доступ для конвертации
public:
    using iterator_category = std::bidirectional_iterator_tag;
    using value_type = T;
    using difference_type = std::ptrdiff_t;
    using pointer = T*;
    using reference = T&;

    vertex_iterator() = default;
    explicit vertex_iterator(typename std::list<VertexRecord>::iterator iter) : it(iter) {}

    reference operator*() const { return it->data; }
    pointer operator->() const { return &(it->data); }

    vertex_iterator& operator++() { ++it; return *this; }
    vertex_iterator operator++(int) { vertex_iterator tmp = *this; ++it; return tmp; }
    vertex_iterator& operator--() { --it; return *this; }
    vertex_iterator operator--(int) { vertex_iterator tmp = *this; --it; return tmp; }

    bool operator==(const vertex_iterator& other) const { return it == other.it; }
    bool operator!=(const vertex_iterator& other) const { return it != other.it; }
};

/**
 * @class const_vertex_iterator
 * @brief Константный двунаправленный итератор по вершинам графа.
 */
class const_vertex_iterator {
private:
    typename std::list<VertexRecord>::const_iterator it;
    friend class Graph;
public:
    using iterator_category = std::bidirectional_iterator_tag;
    using value_type = const T;
    using difference_type = std::ptrdiff_t;
    using pointer = const T*;
    using reference = const T&;

    const_vertex_iterator() = default;
    explicit const_vertex_iterator(typename std::list<VertexRecord>::const_iterator iter) : it(iter) {}
    const_vertex_iterator(const vertex_iterator& non_const) : it(non_const.it) {} // Теперь это компилируется

    reference operator*() const { return it->data; }
    pointer operator->() const { return &(it->data); }

    const_vertex_iterator& operator++() { ++it; return *this; }
    const_vertex_iterator operator++(int) { const_vertex_iterator tmp = *this; ++it; return tmp; }
    const_vertex_iterator& operator--() { --it; return *this; }
    const_vertex_iterator operator--(int) { const_vertex_iterator tmp = *this; --it; return tmp; }

    bool operator==(const const_vertex_iterator& other) const { return it == other.it; }
    bool operator!=(const const_vertex_iterator& other) const { return it != other.it; }
};

using reverse_vertex_iterator = std::reverse_iterator<vertex_iterator>;
using const_reverse_vertex_iterator = std::reverse_iterator<const_vertex_iterator>;
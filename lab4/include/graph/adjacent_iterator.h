/**
* @file adjacent_iterator.h
 * @brief Итераторы смежных вершин для графа.
 * @note Файл предназначен для включения (include) внутрь шаблона Graph<T>.
 */

#pragma once

// ==========================================
// ИТЕРАТОРЫ СМЕЖНЫХ ВЕРШИН
// ==========================================

// Итераторы смежных вершин обязаны быть константными, чтобы пользователь
// не сломал структуру Вирта, перезаписав ключ назначения в обход методов графа.
using adjacent_iterator = typename std::list<T>::const_iterator;
using const_adjacent_iterator = typename std::list<T>::const_iterator;
using reverse_adjacent_iterator = std::reverse_iterator<adjacent_iterator>;
using const_reverse_adjacent_iterator = std::reverse_iterator<const_adjacent_iterator>;

/**
 * @class forward_adjacent_iterator
 * @brief Однонаправленный итератор по смежным вершинам (Вариант 2.1.12).
 * Поддерживает только движение вперед (без operator--).
 */
class forward_adjacent_iterator {
private:
    typename std::list<T>::const_iterator it;
    friend class Graph;
public:
    using iterator_category = std::forward_iterator_tag;
    using value_type = const T;
    using difference_type = std::ptrdiff_t;
    using pointer = const T*;
    using reference = const T&;

    forward_adjacent_iterator() = default;
    explicit forward_adjacent_iterator(typename std::list<T>::const_iterator iter) : it(iter) {}

    reference operator*() const { return *it; }
    pointer operator->() const { return &(*it); }

    forward_adjacent_iterator& operator++() { ++it; return *this; }
    forward_adjacent_iterator operator++(int) {
        forward_adjacent_iterator tmp = *this;
        ++it;
        return tmp;
    }

    bool operator==(const forward_adjacent_iterator& other) const { return it == other.it; }
    bool operator!=(const forward_adjacent_iterator& other) const { return it != other.it; }
};

using const_forward_adjacent_iterator = forward_adjacent_iterator;
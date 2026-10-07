/**
* @file incident_iterator.h
 * @brief Итераторы инцидентных рёбер для графа.
 * @note Файл предназначен для включения (include) внутрь шаблона Graph<T>.
 */

#pragma once

// ==========================================
// ИТЕРАТОРЫ ИНЦИДЕНТНЫХ РЁБЕР
// ==========================================

/**
 * @class incident_iterator
 * @brief Итератор по инцидентным (исходящим) рёбрам конкретной вершины.
 */
class incident_iterator {
private:
    const T* source_ptr; // Храним указатель для избежания тяжелого копирования
    typename std::list<T>::const_iterator adj_it;
public:
    using iterator_category = std::bidirectional_iterator_tag;
    using value_type = edge_type;
    using difference_type = std::ptrdiff_t;
    using pointer = edge_type*;
    using reference = edge_type;

    incident_iterator() = default;
    incident_iterator(const T* src, typename std::list<T>::const_iterator it)
        : source_ptr(src), adj_it(it) {}

    reference operator*() const { return {*source_ptr, *adj_it}; }
    incident_iterator& operator++() { ++adj_it; return *this; }
    incident_iterator& operator--() { --adj_it; return *this; }
    bool operator==(const incident_iterator& other) const { return adj_it == other.adj_it; }
    bool operator!=(const incident_iterator& other) const { return adj_it != other.adj_it; }
};

using const_incident_iterator = incident_iterator;
using reverse_incident_iterator = std::reverse_iterator<incident_iterator>;
using const_reverse_incident_iterator = std::reverse_iterator<const_incident_iterator>;
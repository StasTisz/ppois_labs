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
    const T* source_ptr{nullptr};               ///< Указатель на исходную вершину
    typename std::list<T>::const_iterator adj_it{}; ///< Итератор списка смежных вершин

public:
    using iterator_category = std::bidirectional_iterator_tag; ///< Категория двунаправленного итератора
    using value_type = edge_type;                              ///< Тип значения (пара вершин: from, to)
    using difference_type = std::ptrdiff_t;                    ///< Тип разности итераторов
    using pointer = edge_type*;                                ///< Указатель на ребро
    using reference = edge_type;                               ///< Ребро возвращается по значению

    /** @brief Конструктор по умолчанию. */
    incident_iterator() = default;

    /**
     * @brief Параметризованный конструктор.
     * @param source Указатель на исходную вершину.
     * @param iter Итератор списка смежных вершин.
     */
    incident_iterator(const T* source, typename std::list<T>::const_iterator iter)
        : source_ptr(source), adj_it(iter) {}

    /** @brief Оператор разыменования (возвращает пару вершин {source, target}). */
    reference operator*() const { return {*source_ptr, *adj_it}; }

    /** @brief Префиксный инкремент. */
    incident_iterator& operator++() { ++adj_it; return *this; }

    /** @brief Постфиксный инкремент. */
    incident_iterator operator++(int) {
        incident_iterator previous = *this;
        ++adj_it;
        return previous;
    }

    /** @brief Префиксный декремент. */
    incident_iterator& operator--() { --adj_it; return *this; }

    /** @brief Постфиксный декремент. */
    incident_iterator operator--(int) {
        incident_iterator previous = *this;
        --adj_it;
        return previous;
    }

    /** @brief Оператор проверки равенства. */
    bool operator==(const incident_iterator& other) const {
        return source_ptr == other.source_ptr && adj_it == other.adj_it;
    }

    /** @brief Оператор проверки неравенства. */
    bool operator!=(const incident_iterator& other) const { return !(*this == other); }
};

/** @brief Константный итератор по инцидентным рёбрам. */
using const_incident_iterator = incident_iterator;
/** @brief Обратный итератор по инцидентным рёбрам. */
using reverse_incident_iterator = std::reverse_iterator<incident_iterator>;
/** @brief Константный обратный итератор по инцидентным рёбрам. */
using const_reverse_incident_iterator = std::reverse_iterator<const_incident_iterator>;

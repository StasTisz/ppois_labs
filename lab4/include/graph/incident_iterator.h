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
    const T* source_ptr; /**< Указатель на исходную вершину */
    typename std::list<T>::const_iterator adj_it; /**< Итератор списка смежных вершин */
public:
    using iterator_category = std::bidirectional_iterator_tag;
    using value_type = edge_type;
    using difference_type = std::ptrdiff_t;
    using pointer = edge_type*;
    using reference = edge_type;

    /** @brief Конструктор по умолчанию. */
    incident_iterator() = default;

    /**
     * @brief Параметризованный конструктор.
     * @param src Указатель на исходную вершину.
     * @param it Итератор списка смежных вершин.
     */
    incident_iterator(const T* src, typename std::list<T>::const_iterator it)
        : source_ptr(src), adj_it(it) {}

    /**
     * @brief Оператор разыменования.
     * @return Ребро графа (пара вершин).
     */
    reference operator*() const { return {*source_ptr, *adj_it}; }

    /**
     * @brief Префиксный инкремент.
     * @return Ссылка на себя.
     */
    incident_iterator& operator++() { ++adj_it; return *this; }

    /**
     * @brief Постфиксный инкремент.
     * @return Копия до инкремента.
     */
    incident_iterator operator++(int) {
        incident_iterator tmp = *this;
        ++adj_it;
        return tmp;
    }

    /**
     * @brief Префиксный декремент.
     * @return Ссылка на себя.
     */
    incident_iterator& operator--() { --adj_it; return *this; }

    /**
     * @brief Постфиксный декремент.
     * @return Копия до декремента.
     */
    incident_iterator operator--(int) {
        incident_iterator tmp = *this;
        --adj_it;
        return tmp;
    }

    /**
     * @brief Оператор проверки равенства.
     * @param other Другой итератор для сравнения.
     * @return true, если итераторы равны, иначе false.
     */
    bool operator==(const incident_iterator& other) const {
        return source_ptr == other.source_ptr && adj_it == other.adj_it;
    }

    /**
     * @brief Оператор проверки неравенства.
     * @param other Другой итератор для сравнения.
     * @return true, если итераторы не равны, иначе false.
     */
    bool operator!=(const incident_iterator& other) const { return !(*this == other); }
};

/** @brief Константный итератор по инцидентным рёбрам. */
using const_incident_iterator = incident_iterator;
/** @brief Обратный итератор по инцидентным рёбрам. */
using reverse_incident_iterator = std::reverse_iterator<incident_iterator>;
/** @brief Константный обратный итератор по инцидентным рёбрам. */
using const_reverse_incident_iterator = std::reverse_iterator<const_incident_iterator>;
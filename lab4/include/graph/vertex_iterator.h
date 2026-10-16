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
    typename std::list<VertexRecord>::iterator it; ///< Внутренний итератор списка записей вершин
    friend class Graph;
    friend class const_vertex_iterator;
public:
    using iterator_category = std::bidirectional_iterator_tag; ///< Категория двунаправленного итератора
    using value_type = T;                                      ///< Тип значения вершины
    using difference_type = std::ptrdiff_t;                    ///< Тип разности итераторов
    using pointer = T*;                                        ///< Указатель на значение вершины
    using reference = T&;                                      ///< Ссылка на значение вершины

    /** @brief Конструктор по умолчанию. */
    vertex_iterator() = default;

    /** 
     * @brief Параметризованный конструктор из итератора списка.
     * @param iter Итератор списка записей вершин.
     */
    explicit vertex_iterator(typename std::list<VertexRecord>::iterator iter) : it(iter) {}

    /** @brief Разыменование: доступ к значению вершины. */
    reference operator*() const { return it->data; }

    /** @brief Доступ к членам значения вершины по стрелке. */
    pointer operator->() const { return &(it->data); }

    /** @brief Префиксный инкремент. */
    vertex_iterator& operator++() { ++it; return *this; }

    /** @brief Постфиксный инкремент. */
    vertex_iterator operator++(int) { vertex_iterator tmp = *this; ++it; return tmp; }

    /** @brief Префиксный декремент. */
    vertex_iterator& operator--() { --it; return *this; }

    /** @brief Постфиксный декремент. */
    vertex_iterator operator--(int) { vertex_iterator tmp = *this; --it; return tmp; }

    /** @brief Проверка двух итераторов на равенство. */
    bool operator==(const vertex_iterator& other) const { return it == other.it; }

    /** @brief Проверка двух итераторов на неравенство. */
    bool operator!=(const vertex_iterator& other) const { return it != other.it; }
};

/**
 * @class const_vertex_iterator
 * @brief Константный двунаправленный итератор по вершинам графа.
 */
class const_vertex_iterator {
private:
    typename std::list<VertexRecord>::const_iterator it; ///< Внутренний константный итератор списка
    friend class Graph;
public:
    using iterator_category = std::bidirectional_iterator_tag; ///< Категория двунаправленного итератора
    using value_type = const T;                                ///< Константный тип значения вершины
    using difference_type = std::ptrdiff_t;                    ///< Тип разности итераторов
    using pointer = const T*;                                  ///< Константный указатель на вершину
    using reference = const T&;                                ///< Константная ссылка на вершину

    /** @brief Конструктор по умолчанию. */
    const_vertex_iterator() = default;

    /** 
     * @brief Конструктор из константного итератора списка.
     * @param iter Константный итератор списка записей вершин.
     */
    explicit const_vertex_iterator(typename std::list<VertexRecord>::const_iterator iter) : it(iter) {}

    /** 
     * @brief Конструктор неявного преобразования из неконстантного итератора.
     * @param non_const Неконстантный итератор вершины.
     */
    const_vertex_iterator(const vertex_iterator& non_const) : it(non_const.it) {}

    /** @brief Разыменование: доступ к константному значению вершины. */
    reference operator*() const { return it->data; }

    /** @brief Доступ к членам константного значения вершины по стрелке. */
    pointer operator->() const { return &(it->data); }

    /** @brief Префиксный инкремент. */
    const_vertex_iterator& operator++() { ++it; return *this; }

    /** @brief Постфиксный инкремент. */
    const_vertex_iterator operator++(int) { const_vertex_iterator tmp = *this; ++it; return tmp; }

    /** @brief Префиксный декремент. */
    const_vertex_iterator& operator--() { --it; return *this; }

    /** @brief Постфиксный декремент. */
    const_vertex_iterator operator--(int) { const_vertex_iterator tmp = *this; --it; return tmp; }

    /** @brief Проверка константных итераторов на равенство. */
    bool operator==(const const_vertex_iterator& other) const { return it == other.it; }

    /** @brief Проверка константных итераторов на неравенство. */
    bool operator!=(const const_vertex_iterator& other) const { return it != other.it; }
};

using reverse_vertex_iterator = std::reverse_iterator<vertex_iterator>;             ///< Обратный итератор вершин
using const_reverse_vertex_iterator = std::reverse_iterator<const_vertex_iterator>; ///< Константный обратный итератор вершин
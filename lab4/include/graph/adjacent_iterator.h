/**
 * @file adjacent_iterator.h
 * @brief Итераторы смежных вершин для графа.
 * @note Файл предназначен для включения (include) внутрь шаблона Graph<T>.
 */

#pragma once

// ==========================================
// ИТЕРАТОРЫ СМЕЖНЫХ ВЕРШИН
// ==========================================

/** @brief Итератор по смежным вершинам (константный двунаправленный). */
using adjacent_iterator = typename std::list<T>::const_iterator;
/** @brief Константный итератор по смежным вершинам. */
using const_adjacent_iterator = typename std::list<T>::const_iterator;
/** @brief Обратный итератор по смежным вершинам. */
using reverse_adjacent_iterator = std::reverse_iterator<adjacent_iterator>;
/** @brief Константный обратный итератор по смежным вершинам. */
using const_reverse_adjacent_iterator = std::reverse_iterator<const_adjacent_iterator>;

/**
 * @class forward_adjacent_iterator
 * @brief Однонаправленный итератор по смежным вершинам (Вариант 2.1.12).
 * Поддерживает только движение вперед (без operator--).
 */
class forward_adjacent_iterator {
private:
    typename std::list<T>::const_iterator it{}; ///< Внутренний итератор списка смежности
    friend class Graph;

public:
    using iterator_category = std::forward_iterator_tag; ///< Категория однонаправленного итератора
    using value_type = const T;                          ///< Константный тип значения вершины
    using difference_type = std::ptrdiff_t;              ///< Тип разности итераторов
    using pointer = const T*;                            ///< Константный указатель на вершину
    using reference = const T&;                          ///< Константная ссылка на вершину

    /** @brief Конструктор по умолчанию. */
    forward_adjacent_iterator() = default;

    /**
     * @brief Конструктор из итератора списка.
     * @param iter Исходный итератор списка.
     */
    explicit forward_adjacent_iterator(typename std::list<T>::const_iterator iter) : it(iter) {}

    /** @brief Оператор разыменования (константная ссылка на значение вершины). */
    reference operator*() const { return *it; }

    /** @brief Оператор доступа по указателю. */
    pointer operator->() const { return &(*it); }

    /** @brief Префиксный инкремент. */
    forward_adjacent_iterator& operator++() { ++it; return *this; }

    /** @brief Постфиксный инкремент. */
    forward_adjacent_iterator operator++(int) {
        forward_adjacent_iterator previous = *this;
        ++it;
        return previous;
    }

    /** @brief Оператор проверки равенства. */
    bool operator==(const forward_adjacent_iterator& other) const { return it == other.it; }

    /** @brief Оператор проверки неравенства. */
    bool operator!=(const forward_adjacent_iterator& other) const { return it != other.it; }
};

/** @brief Псевдоним для константного однонаправленного итератора смежных вершин. */
using const_forward_adjacent_iterator = forward_adjacent_iterator;

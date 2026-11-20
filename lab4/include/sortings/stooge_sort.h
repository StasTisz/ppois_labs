/**
 * @file stooge_sort.h
 * @brief Обобщённая реализация сортировки Студжа (Stooge sort).
 */

#pragma once

#include <algorithm>
#include <cstddef>
#include <functional>
#include <iterator>
#include <type_traits>

namespace detail {
    /**
     * @brief Рекурсивная реализация сортировки Студжа.
     * Сложность: O(N^2.709) в худшем, среднем и лучшем случаях.
     * Память: O(log N) из-за глубины стека рекурсии.
     *
     * @tparam RandomIt Тип итератора произвольного доступа.
     * @tparam Compare Тип компаратора.
     * @param first Итератор на начало диапазона.
     * @param last Итератор на конец диапазона (эксклюзивный, указывает за последний элемент).
     * @param comp Функция-компаратор.
     */
    template <typename RandomIt, typename Compare>
    void stooge_sort_impl(RandomIt first, RandomIt last, Compare comp) {
        const auto range_length = std::distance(first, last);
        if (range_length < 2) {
            return; // Базовый случай: 0 или 1 элемент уже отсортированы.
        }

        // Упорядочиваем крайние элементы текущего поддиапазона.
        if (comp(*(last - 1), *first)) {
            std::iter_swap(first, last - 1);
        }

        // Для трёх и более элементов рекурсивно сортируем перекрывающиеся 2/3 диапазона.
        if (range_length > 2) {
            const auto one_third = range_length / 3;
            stooge_sort_impl(first, last - one_third, comp);
            stooge_sort_impl(first + one_third, last, comp);
            stooge_sort_impl(first, last - one_third, comp);
        }
    }
} // namespace detail

/**
 * @brief Сортировка Студжа (Stooge sort) для диапазона итераторов.
 *
 * @tparam RandomIt Тип итератора произвольного доступа.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param first Итератор на начало диапазона.
 * @param last Итератор на конец диапазона (эксклюзивный).
 * @param comp Функция-компаратор.
 */
template <typename RandomIt, typename Compare = std::less<>>
void stooge_sort(RandomIt first, RandomIt last, Compare comp = Compare()) {
    detail::stooge_sort_impl(first, last, comp);
}

/**
 * @brief Обёртка Stooge sort для стандартных контейнеров (std::vector, std::array и т. д.).
 *
 * @tparam Container Тип контейнера.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param container Контейнер для сортировки.
 * @param comp Функция-компаратор.
 */
template <typename Container, typename Compare = std::less<>>
    requires (!std::is_pointer_v<std::decay_t<Container>> && !std::is_integral_v<Compare>)
void stooge_sort(Container& container, Compare comp = Compare()) {
    stooge_sort(std::begin(container), std::end(container), comp);
}

/**
 * @brief Перегрузка Stooge sort для классических C-массивов фиксированного размера.
 *
 * @tparam T Тип элементов массива.
 * @tparam N Размер массива.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param array Массив для сортировки.
 * @param comp Функция-компаратор.
 */
template <typename T, std::size_t N, typename Compare = std::less<>>
    requires (!std::is_integral_v<Compare>)
void stooge_sort(T (&array)[N], Compare comp = Compare()) {
    stooge_sort(array, array + N, comp);
}

/**
 * @brief Перегрузка Stooge sort для классических C-массивов (указатель и размер).
 *
 * @tparam T Тип элементов массива.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param array Указатель на начало массива.
 * @param size Количество элементов в массиве.
 * @param comp Функция-компаратор.
 */
template <typename T, typename Compare = std::less<>>
void stooge_sort(T* array, std::size_t size, Compare comp = Compare()) {
    if (array == nullptr || size <= 1) return;
    stooge_sort(array, array + size, comp);
}

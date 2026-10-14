#pragma once

#include <iterator>
#include <functional>
#include <algorithm>
#include <type_traits>

namespace detail {
    /**
     * @brief Рекурсивная реализация сортировки Студжа.
     * Сложность: O(N^2.709) в худшем, среднем и лучшем случаях.
     * Память: O(log N) из-за глубины стека рекурсии.
     * Алгоритм крайне неэффективен и используется в основном в учебных целях.
     * 
     * @tparam RandomIt Тип итератора произвольного доступа.
     * @tparam Compare Тип компаратора.
     * @param first Итератор на начало диапазона.
     * @param last Итератор на конец диапазона (эксклюзивный, указывает за последний элемент).
     * @param comp Функция-компаратор.
     */
    template <typename RandomIt, typename Compare>
    void stooge_sort_impl(RandomIt first, RandomIt last, Compare comp) {
        // Вычисляем размер текущего подмассива
        auto n = std::distance(first, last);
        
        // Базовый случай: массив из 0 или 1 элемента уже отсортирован
        if (n < 2) {
            return;
        }

        // Шаг 1: Если последний элемент "меньше" первого, меняем их местами.
        // last указывает ЗА конец, поэтому последний элемент это (last - 1).
        if (comp(*(last - 1), *first)) {
            std::iter_swap(first, last - 1);
        }

        // Шаг 2: Если в массиве 3 и более элементов, рекурсивно сортируем его трети.
        if (n > 2) {
            auto third = n / 3;

            // 1. Сортируем начальные 2/3 массива
            stooge_sort_impl(first, last - third, comp);
            
            // 2. Сортируем конечные 2/3 массива
            stooge_sort_impl(first + third, last, comp);
            
            // 3. Снова сортируем начальные 2/3 массива, чтобы гарантировать порядок
            stooge_sort_impl(first, last - third, comp);
        }
    }
}

/**
     * @brief Публичная версия для сортировки Студжа.
*/
template <typename RandomIt, typename Compare = std::less<>>
void stooge_sort(RandomIt first, RandomIt last, Compare comp = Compare()) {
    detail::stooge_sort_impl(first, last, comp);
}

/**
 * @brief Удобная обертка Stooge sort для целых контейнеров (std::vector, std::array, и т.д.).
 * 
 * @tparam Container Тип контейнера.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param c Контейнер для сортировки.
 * @param comp Функция-компаратор.
 */
template <typename Container, typename Compare = std::less<>>
    requires (!std::is_pointer_v<std::decay_t<Container>> && !std::is_integral_v<Compare>)
void stooge_sort(Container& c, Compare comp = Compare()) {
    stooge_sort(std::begin(c), std::end(c), comp);
}

/**
 * @brief Перегрузка Stooge sort для классических C-массивов фиксированного размера.
 */
template <typename T, std::size_t N, typename Compare = std::less<>>
    requires (!std::is_integral_v<Compare>)
void stooge_sort(T (&arr)[N], Compare comp = Compare()) {
    stooge_sort(arr, arr + N, comp);
}

/**
 * @brief Перегрузка Stooge sort для классических C-массивов (указатель и размер).
 */
template <typename T, typename Compare = std::less<>>
void stooge_sort(T* arr, std::size_t n, Compare comp = Compare()) {
    if (arr == nullptr || n <= 1) return;
    stooge_sort(arr, arr + n, comp);
}
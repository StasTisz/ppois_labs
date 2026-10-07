#pragma once

#include <iterator>
#include <functional>
#include <algorithm>

namespace detail {
    /**
     * @brief Вспомогательная функция просеивания элемента вниз (восстановление свойств кучи).
     * 
     * @tparam RandomIt Тип итератора произвольного доступа.
     * @tparam Compare Тип компаратора.
     * @param first Итератор на начало сортируемого диапазона.
     * @param root_index Индекс текущего корня, который нужно просеять.
     * @param bottom_index Граница кучи (элементы с индексом >= bottom_index уже отсортированы).
     * @param comp Функция-компаратор.
     */
    template <typename RandomIt, typename Compare>
    void sift_down(RandomIt first, size_t root_index, size_t bottom_index, Compare comp) {
        size_t max_child;
        bool done = false;

        while ((root_index * 2 + 1 < bottom_index) && !done) {
            max_child = root_index * 2 + 1; // Левый потомок
            
            // Если есть правый потомок и он "больше" левого (согласно компаратору)
            if (max_child + 1 < bottom_index && comp(first[max_child], first[max_child + 1])) {
                max_child += 1;
            }

            // Если корень "меньше" максимального потомка, меняем их местами
            if (comp(first[root_index], first[max_child])) {
                std::iter_swap(first + root_index, first + max_child);
                root_index = max_child;
            } else {
                done = true; // Свойство кучи восстановлено
            }
        }
    }
}

/**
 * @brief Пирамидальная сортировка (Heapsort) для диапазона итераторов.
 * Сложность: O(N log N) в худшем, среднем и лучшем случаях.
 * Память: O(1) (сортировка на месте).
 * 
 * @tparam RandomIt Тип итератора произвольного доступа.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 */
template <typename RandomIt, typename Compare = std::less<>>
void heapsort(RandomIt first, RandomIt last, Compare comp = Compare()) {
    // Используем auto, чтобы тип точно совпадал с difference_type итератора
    auto n = std::distance(first, last);
    if (n <= 1) return;

    // Шаг 1: Построение Max-Heap (пирамиды) из неотсортированного массива.
    // Начинаем с последнего узла, имеющего потомков.
    // Используем size_t (i > 0) и передаем (i - 1), чтобы избежать underflow беззнакового нуля.
    for (size_t i = n / 2; i > 0; --i) {
        detail::sift_down(first, i - 1, n, comp);
    }

    // Шаг 2: Извлечение максимума и перестройка кучи.
    for (size_t i = n - 1; i > 0; --i) {
        // Перемещаем текущий корень (максимум) в конец
        std::iter_swap(first, first + i);
        // Восстанавливаем свойство кучи для оставшейся неотсортированной части
        detail::sift_down(first, 0, i, comp);
    }
}

/**
 * @brief Удобная обертка Heapsort для целых контейнеров (std::vector, std::array, и т.д.).
 */
template <typename Container, typename Compare = std::less<>>
void heapsort(Container& c, Compare comp = Compare()) {
    heapsort(std::begin(c), std::end(c), comp);
}
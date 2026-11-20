/**
 * @file heapsort.h
 * @brief Обобщённая реализация пирамидальной сортировки (Heapsort).
 */

#pragma once

#include <algorithm>
#include <cstddef>
#include <functional>
#include <iterator>
#include <type_traits>

namespace detail {
    /**
     * @brief Вспомогательная функция просеивания элемента вниз (восстановление свойств кучи).
     *
     * @tparam RandomIt Тип итератора произвольного доступа.
     * @tparam Compare Тип компаратора.
     * @param first Итератор на начало сортируемого диапазона.
     * @param root_index Индекс текущего корня поддерева для просеивания.
     * @param heap_size Текущая граница кучи (элементы >= heap_size уже отсортированы).
     * @param comp Функция-компаратор.
     */
    template <typename RandomIt, typename Compare>
    void sift_down(RandomIt first, std::size_t root_index, std::size_t heap_size, Compare comp) {
        // Бинарная куча: левый потомок = 2 * root_index + 1, правый = 2 * root_index + 2.
        while (root_index * 2 + 1 < heap_size) {
            std::size_t target_child = root_index * 2 + 1;
            std::size_t right_child = target_child + 1;

            // Если существует правый потомок и он приоритетнее левого, выбираем его.
            if (right_child < heap_size && comp(first[target_child], first[right_child])) {
                target_child = right_child;
            }
            if (!comp(first[root_index], first[target_child])) {
                break; // Свойство пирамиды восстановлено.
            }
            std::iter_swap(first + root_index, first + target_child);
            root_index = target_child;
        }
    }
} // namespace detail

/**
 * @brief Пирамидальная сортировка (Heapsort) для диапазона итераторов.
 * Сложность: O(N log N) в худшем, среднем и лучшем случаях.
 * Память: O(1) (сортировка на месте).
 *
 * @tparam RandomIt Тип итератора произвольного доступа.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param first Итератор на начало сортируемого диапазона.
 * @param last Итератор на конец диапазона (эксклюзивный).
 * @param comp Функция-компаратор.
 */
template <typename RandomIt, typename Compare = std::less<>>
void heapsort(RandomIt first, RandomIt last, Compare comp = Compare()) {
    const auto distance = std::distance(first, last);
    if (distance <= 1) return;
    const auto element_count = static_cast<std::size_t>(distance);

    // Шаг 1: Построение кучи, начиная с последнего нелистового узла.
    for (std::size_t index = element_count / 2; index > 0; --index) {
        detail::sift_down(first, index - 1, element_count, comp);
    }

    // Шаг 2: Переносим вершину кучи в конец и восстанавливаем инвариант на остатке.
    for (std::size_t index = element_count - 1; index > 0; --index) {
        std::iter_swap(first, first + index);
        detail::sift_down(first, 0, index, comp);
    }
}

/**
 * @brief Обёртка Heapsort для стандартных контейнеров (std::vector, std::array и т. д.).
 *
 * @tparam Container Тип контейнера.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param container Контейнер для сортировки.
 * @param comp Функция-компаратор.
 */
template <typename Container, typename Compare = std::less<>>
    requires (!std::is_pointer_v<std::decay_t<Container>> && !std::is_integral_v<Compare>)
void heapsort(Container& container, Compare comp = Compare()) {
    heapsort(std::begin(container), std::end(container), comp);
}

/**
 * @brief Перегрузка Heapsort для классических C-массивов фиксированного размера.
 *
 * @tparam T Тип элементов массива.
 * @tparam N Размер массива.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param array Массив для сортировки.
 * @param comp Функция-компаратор.
 */
template <typename T, std::size_t N, typename Compare = std::less<>>
    requires (!std::is_integral_v<Compare>)
void heapsort(T (&array)[N], Compare comp = Compare()) {
    heapsort(array, array + N, comp);
}

/**
 * @brief Перегрузка Heapsort для классических C-массивов (указатель и размер).
 *
 * @tparam T Тип элементов массива.
 * @tparam Compare Тип компаратора (по умолчанию std::less<>).
 * @param array Указатель на начало массива.
 * @param size Количество элементов в массиве.
 * @param comp Функция-компаратор.
 */
template <typename T, typename Compare = std::less<>>
void heapsort(T* array, std::size_t size, Compare comp = Compare()) {
    if (array == nullptr || size <= 1) return;
    heapsort(array, array + size, comp);
}

#include <gtest/gtest.h>
#include <vector>
#include <array>
#include <functional>

#include "../include/sortings/heapsort.h"
#include "../include/sortings/stooge_sort.h"
#include "../include/custom_object.h"

// ==========================================
// ТЕСТЫ HEAPSORT
// ==========================================

TEST(HeapsortTest, EmptyAndSingleElement) {
    std::vector<int> empty_vec;
    heapsort(empty_vec);
    EXPECT_TRUE(empty_vec.empty());

    std::vector<int> single = {42};
    heapsort(single);
    EXPECT_EQ(single.size(), 1);
    EXPECT_EQ(single[0], 42);
}

TEST(HeapsortTest, AlreadySorted) {
    // Покрывает ветку `done = true` в sift_down, когда элементы уже стоят правильно
    std::vector<int> data = {1, 2, 3, 4, 5};
    std::vector<int> expected = {1, 2, 3, 4, 5};
    heapsort(data);
    EXPECT_EQ(data, expected);
}

TEST(HeapsortTest, ReverseSorted) {
    // Покрывает ветку смены `max_child` (переход на правого потомка) и `iter_swap`
    std::vector<int> data = {5, 4, 3, 2, 1};
    std::vector<int> expected = {1, 2, 3, 4, 5};
    heapsort(data);
    EXPECT_EQ(data, expected);
}

TEST(HeapsortTest, AllIdentical) {
    std::vector<int> data = {7, 7, 7, 7, 7};
    std::vector<int> expected = {7, 7, 7, 7, 7};
    heapsort(data);
    EXPECT_EQ(data, expected);
}

TEST(HeapsortTest, CustomComparatorGreater) {
    std::vector<int> data = {3, 1, 4, 1, 5, 9};
    std::vector<int> expected = {9, 5, 4, 3, 1, 1};
    heapsort(data, std::greater<int>());
    EXPECT_EQ(data, expected);
}

TEST(HeapsortTest, ContainerWrapperVsIterator) {
    std::array<int, 4> data1 = {4, 3, 2, 1};
    std::array<int, 4> data2 = {4, 3, 2, 1};

    // Проверка обертки для контейнера
    heapsort(data1);
    // Проверка явной передачи итераторов
    heapsort(data2.begin(), data2.end());

    EXPECT_EQ(data1, data2);
}

TEST(HeapsortTest, CustomObjectFlightInfo) {
    std::vector<FlightInfo> flights = {
        {"B2-710", 1250.5, 2},
        {"SU-100", 720.0, 1},
        {"LH-144", 720.0, 3}
    };

    heapsort(flights);

    // SU-100 и LH-144 имеют одинаковую дистанцию (720.0), но у SU-100 приоритет 1, у LH-144 приоритет 3
    EXPECT_EQ(flights[0].get_number(), "SU-100");
    EXPECT_EQ(flights[1].get_number(), "LH-144");
    EXPECT_EQ(flights[2].get_number(), "B2-710");
}

// ==========================================
// ТЕСТЫ STOOGE SORT
// ==========================================

TEST(StoogeSortTest, EmptyAndSingleElement) {
    // Покрывает базовый случай `n < 2`
    std::vector<int> empty_vec;
    stooge_sort(empty_vec);
    EXPECT_TRUE(empty_vec.empty());

    std::vector<int> single = {99};
    stooge_sort(single);
    EXPECT_EQ(single.size(), 1);
    EXPECT_EQ(single[0], 99);
}

TEST(StoogeSortTest, TwoElementsWithSwap) {
    // Покрывает случай `n == 2` и выполнение `std::iter_swap`
    std::vector<int> data = {10, 5};
    std::vector<int> expected = {5, 10};
    stooge_sort(data);
    EXPECT_EQ(data, expected);
}

TEST(StoogeSortTest, TwoElementsNoSwap) {
    // Покрывает случай `n == 2` без выполнения `std::iter_swap`
    std::vector<int> data = {5, 10};
    std::vector<int> expected = {5, 10};
    stooge_sort(data);
    EXPECT_EQ(data, expected);
}

TEST(StoogeSortTest, MultipleElementsRecursion) {
    // Покрывает ветку `n > 2` (рекурсивные вызовы для третей массива)
    std::vector<int> data = {30, 2, 45, 10, 6, 8, 1, 99, 0};
    std::vector<int> expected = {0, 1, 2, 6, 8, 10, 30, 45, 99};
    stooge_sort(data);
    EXPECT_EQ(data, expected);
}

TEST(StoogeSortTest, CustomComparatorGreater) {
    std::vector<int> data = {5, 8, 1, 3, 7};
    std::vector<int> expected = {8, 7, 5, 3, 1};
    stooge_sort(data, std::greater<int>());
    EXPECT_EQ(data, expected);
}

TEST(StoogeSortTest, ContainerWrapperVsIterator) {
    std::vector<int> data1 = {9, 2, 7, 4};
    std::vector<int> data2 = {9, 2, 7, 4};

    stooge_sort(data1);
    stooge_sort(data2.begin(), data2.end());

    EXPECT_EQ(data1, data2);
}

TEST(StoogeSortTest, CustomObjectFlightInfoWithLambda) {
    std::vector<FlightInfo> flights = {
        {"F1", 500.0, 1},
        {"F2", 1500.0, 5},
        {"F3", 1000.0, 3}
    };

    // Сортировка по убыванию приоритета с помощью лямбды
    stooge_sort(flights, [](const FlightInfo& a, const FlightInfo& b) {
        return a.get_priority() > b.get_priority();
    });

    EXPECT_EQ(flights[0].get_number(), "F2");
    EXPECT_EQ(flights[1].get_number(), "F3");
    EXPECT_EQ(flights[2].get_number(), "F1");
}

#include <sstream>

// ==========================================
// ТЕСТЫ ПОЛЬЗОВАТЕЛЬСКОГО ТИПА (FlightInfo)
// ==========================================

TEST(FlightInfoTest, ConstructorsAndGetters) {
    FlightInfo default_flight;
    EXPECT_EQ(default_flight.get_number(), "UNKNOWN");
    EXPECT_DOUBLE_EQ(default_flight.get_distance(), 0.0);
    EXPECT_EQ(default_flight.get_priority(), 0);

    FlightInfo custom_flight("SU-100", 720.5, 3);
    EXPECT_EQ(custom_flight.get_number(), "SU-100");
    EXPECT_DOUBLE_EQ(custom_flight.get_distance(), 720.5);
    EXPECT_EQ(custom_flight.get_priority(), 3);
}

TEST(FlightInfoTest, Setters) {
    FlightInfo flight;
    flight.set_number("B2-999");
    flight.set_distance(1500.0);
    flight.set_priority(5);

    EXPECT_EQ(flight.get_number(), "B2-999");
    EXPECT_DOUBLE_EQ(flight.get_distance(), 1500.0);
    EXPECT_EQ(flight.get_priority(), 5);
}

TEST(FlightInfoTest, ComparisonOperators) {
    FlightInfo a("A", 100.0, 1);
    FlightInfo b("B", 100.0, 2); // выше приоритет
    FlightInfo c("C", 200.0, 1); // больше дистанция
    FlightInfo a_copy("A", 100.0, 1);

    // Проверка всех операторов (==, !=, <, <=, >, >=)
    EXPECT_TRUE(a == a_copy);
    EXPECT_FALSE(a != a_copy);
    EXPECT_TRUE(a < b);
    EXPECT_TRUE(a <= b);
    EXPECT_TRUE(c > b);
    EXPECT_TRUE(c >= b);
    EXPECT_FALSE(b < a);
}

TEST(FlightInfoTest, StreamInputOutput) {
    FlightInfo flight("LH-123", 850.0, 2);

    // Проверка потокового вывода operator<<
    std::ostringstream out;
    out << flight;
    EXPECT_FALSE(out.str().empty());

    // Проверка потокового ввода operator>>
    std::istringstream in("TK-999 1300.5 4");
    FlightInfo read_flight;
    in >> read_flight;

    EXPECT_EQ(read_flight.get_number(), "TK-999");
    EXPECT_DOUBLE_EQ(read_flight.get_distance(), 1300.5);
    EXPECT_EQ(read_flight.get_priority(), 4);
}
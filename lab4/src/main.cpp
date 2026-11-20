/**
 * @file main.cpp
 * @brief Главный модуль консольного интерфейса (CLI) для демонстрации сортировок и графов.
 */

#include <cstddef>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

#include "custom_object.h"
#include "graph/graph.h"
#include "sortings/heapsort.h"
#include "sortings/stooge_sort.h"

namespace cli {

constexpr double MIN_DISTANCE = 0.1;
constexpr int MIN_PRIORITY = 1;
constexpr int MAX_PRIORITY = 10;
constexpr int INDEX_COLUMN_WIDTH = 3;
constexpr int MAX_SORT_MENU_OPTION = 9;
constexpr int MAX_GRAPH_MENU_OPTION = 10;
constexpr int MAX_MAIN_MENU_OPTION = 2;

/** @brief Очистка потока ввода cin от ошибок и остаточных символов. */
void clearInputStream() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

/**
 * @brief Безопасное чтение целого числа из потока ввода в заданном диапазоне.
 * @param prompt Текст подсказки пользователю.
 * @param min_val Минимальное допустимое значение.
 * @param max_val Максимальное допустимое значение.
 * @return Считанное целое число.
 */
int readInt(const std::string& prompt, int min_val, int max_val) {
    int value = 0;
    while (true) {
        std::cout << prompt;
        if (std::cin >> value && value >= min_val && value <= max_val) {
            clearInputStream();
            return value;
        }
        std::cout << "Ошибка ввода! Введите число от " << min_val << " до " << max_val << ".\n";
        clearInputStream();
    }
}

/**
 * @brief Безопасное чтение вещественного числа из потока ввода.
 * @param prompt Текст подсказки пользователю.
 * @param min_val Минимальное допустимое значение.
 * @return Считанное вещественное число.
 */
double readDouble(const std::string& prompt, double min_val) {
    double value = 0.0;
    while (true) {
        std::cout << prompt;
        if (std::cin >> value && value >= min_val) {
            clearInputStream();
            return value;
        }
        std::cout << "Ошибка ввода! Число должно быть не меньше " << min_val << ".\n";
        clearInputStream();
    }
}

/**
 * @brief Чтение непустой строки из потока ввода.
 * @param prompt Текст подсказки пользователю.
 * @return Считанная строка.
 */
std::string readString(const std::string& prompt) {
    std::string line;
    while (true) {
        std::cout << prompt;
        if (std::getline(std::cin, line) && !line.empty()) {
            return line;
        }
        std::cout << "Ошибка! Поле не может быть пустым.\n";
    }
}

/**
 * @brief Заполнение вектора рейсов начальными тестовыми данными.
 * @param flights Целевой список рейсов.
 */
void seedDefaultData(std::vector<FlightInfo>& flights) {
    flights.clear();
    flights.emplace_back("B2-710", 1250.5, 2);
    flights.emplace_back("SU-100", 720.0, 1);
    flights.emplace_back("LH-144", 1830.0, 3);
    flights.emplace_back("TK-401", 1420.0, 1);
    flights.emplace_back("LO-678", 510.2, 2);
    flights.emplace_back("BA-890", 2100.0, 4);
}

/**
 * @brief Отображение форматированного списка авиарейсов.
 * @param flights Список рейсов для отображения.
 */
void displayList(const std::vector<FlightInfo>& flights) {
    std::cout << "\n---------------- ТЕКУЩИЙ СПИСОК РЕЙСОВ ----------------\n";
    if (flights.empty()) {
        std::cout << "[Список пуст]\n";
    } else {
        for (std::size_t index = 0; index < flights.size(); ++index) {
            std::cout << std::setw(INDEX_COLUMN_WIDTH) << index << ". " << flights[index] << "\n";
        }
    }
    std::cout << "-------------------------------------------------------\n";
}

/**
 * @brief Интерактивное добавление рейса по полям.
 * @param flights Целевой список рейсов.
 */
void addFlightInteractive(std::vector<FlightInfo>& flights) {
    std::cout << "\n--- Добавление нового авиарейса ---\n";
    std::string number = readString("Введите номер рейса (например, AF-112): ");
    double distance = readDouble("Введите дистанцию полёта (км, > 0): ", MIN_DISTANCE);
    int priority = readInt("Введите уровень приоритета (от 1 до 10): ", MIN_PRIORITY, MAX_PRIORITY);
    flights.emplace_back(std::move(number), distance, priority);
    std::cout << "Рейс успешно добавлен!\n";
}

/**
 * @brief Добавление рейса через потоковый ввод (operator>>).
 * @param flights Целевой список рейсов.
 */
void addFlightViaStream(std::vector<FlightInfo>& flights) {
    std::cout << "\n--- Добавление рейса через поток ввода (operator>>) ---\n";
    std::cout << "Введите данные через пробел: [Номер] [Дистанция] [Приоритет]\n> ";
    FlightInfo new_flight;
    if (std::cin >> new_flight) {
        flights.push_back(new_flight);
        std::cout << "Объект успешно считан и добавлен!\n";
    } else {
        std::cout << "Ошибка формата ввода! Данные не добавлены.\n";
    }
    clearInputStream();
}

/**
 * @brief Удаление рейса по индексу из списка.
 * @param flights Целевой список рейсов.
 */
void removeFlight(std::vector<FlightInfo>& flights) {
    if (flights.empty()) {
        std::cout << "Список пуст!\n";
        return;
    }
    displayList(flights);
    int index = readInt("Введите индекс рейса для удаления: ", 0, static_cast<int>(flights.size() - 1));
    flights.erase(flights.begin() + index);
    std::cout << "Рейс успешно удалён.\n";
}

/** @brief Демонстрация сортировки фиксированного C-массива. */
void demoRawArraySort() {
    FlightInfo raw_flights[] = {
        FlightInfo("KL-101", 1300.0, 2),
        FlightInfo("AF-202", 850.0, 1),
        FlightInfo("BA-303", 2100.0, 3)
    };
    constexpr std::size_t array_size = sizeof(raw_flights) / sizeof(raw_flights[0]);
    std::cout << "\n--- Сортировка C-массива FlightInfo (" << array_size << " элементов) ---\nДо:\n";
    for (std::size_t index = 0; index < array_size; ++index) std::cout << "  " << raw_flights[index] << "\n";
    heapsort(raw_flights, array_size);
    std::cout << "После Heapsort (arr, size):\n";
    for (std::size_t index = 0; index < array_size; ++index) std::cout << "  " << raw_flights[index] << "\n";
}

/**
 * @brief Демонстрация пирамидальной сортировки (Heapsort).
 * @param flights Список рейсов для сортировки.
 */
void sortHeapsortDemo(std::vector<FlightInfo>& flights) {
    heapsort(flights);
    std::cout << "Отсортировано (Heapsort)!\n";
    displayList(flights);
}

/**
 * @brief Демонстрация сортировки Студжа (Stooge sort).
 * @param flights Список рейсов для сортировки.
 */
void sortStoogeDemo(std::vector<FlightInfo>& flights) {
    stooge_sort(flights);
    std::cout << "Отсортировано (Stooge sort)!\n";
    displayList(flights);
}

/**
 * @brief Демонстрация сортировки с пользовательским компаратором (лямбда).
 * @param flights Список рейсов для сортировки.
 */
void sortLambdaDemo(std::vector<FlightInfo>& flights) {
    heapsort(flights, [](const FlightInfo& first_flight, const FlightInfo& second_flight) {
        return first_flight.get_distance() > second_flight.get_distance();
    });
    std::cout << "Отсортировано по убыванию дистанции!\n";
    displayList(flights);
}

/** @brief Вывод меню операций сортировки. */
void printSortingMenu() {
    std::cout << "\n=== ЗАДАНИЕ 1: СОРТИРОВКИ ===\n"
              << "1. Показать список рейсов\n"
              << "2. Добавить рейс (пошагово)\n"
              << "3. Добавить рейс (строкой operator>>)\n"
              << "4. Удалить рейс по индексу\n"
              << "5. Сбросить данные (Seed)\n"
              << "6. Heapsort (по умолчанию)\n"
              << "7. Stooge sort (по умолчанию)\n"
              << "8. Heapsort (лямбда: дистанция убыв.)\n"
              << "9. Heapsort для сырого C-массива (FlightInfo[])\n"
              << "0. Вернуться в главное меню\n";
}

/**
 * @brief Обработка выбора пользователя в меню сортировок.
 * @param choice Выбранный пункт меню.
 * @param flights Список рейсов.
 */
void handleSortingChoice(int choice, std::vector<FlightInfo>& flights) {
    switch (choice) {
        case 1: displayList(flights); break;
        case 2: addFlightInteractive(flights); break;
        case 3: addFlightViaStream(flights); break;
        case 4: removeFlight(flights); break;
        case 5: seedDefaultData(flights); std::cout << "Сброшено.\n"; break;
        case 6: sortHeapsortDemo(flights); break;
        case 7: sortStoogeDemo(flights); break;
        case 8: sortLambdaDemo(flights); break;
        case 9: demoRawArraySort(); break;
        default: break;
    }
}

/** @brief Меню управления разделом сортировок. */
void sortingMenu() {
    std::vector<FlightInfo> flights;
    seedDefaultData(flights);
    int choice = -1;
    while (choice != 0) {
        printSortingMenu();
        choice = readInt("Выберите действие: ", 0, MAX_SORT_MENU_OPTION);
        handleSortingChoice(choice, flights);
    }
}

/**
 * @brief Заполнение графа тестовыми маршрутами перелётов.
 * @param graph Целевой граф.
 */
void seedGraphData(Graph<std::string>& graph) {
    graph.clear();
    graph.insert_vertex("MSQ");
    graph.insert_vertex("SVO");
    graph.insert_vertex("IST");
    graph.insert_vertex("DXB");
    graph.insert_edge("MSQ", "SVO");
    graph.insert_edge("MSQ", "IST");
    graph.insert_edge("MSQ", "DXB");
    graph.insert_edge("IST", "DXB");
    std::cout << "Граф заполнен тестовой картой авиамаршрутов.\n";
}

/**
 * @brief Добавление новой вершины (аэропорта) в граф.
 * @param graph Целевой граф.
 */
void addVertex(Graph<std::string>& graph) {
    std::string vertex_code = readString("Введите код аэропорта (например, MSQ): ");
    try {
        graph.insert_vertex(vertex_code);
        std::cout << "Аэропорт " << vertex_code << " успешно добавлен.\n";
    } catch (const std::exception& error) {
        std::cout << "Ошибка: " << error.what() << "\n";
    }
}

/**
 * @brief Удаление вершины (аэропорта) из графа.
 * @param graph Целевой граф.
 */
void removeVertex(Graph<std::string>& graph) {
    std::string vertex_code = readString("Введите код аэропорта для удаления: ");
    try {
        graph.erase_vertex(vertex_code);
        std::cout << "Аэропорт " << vertex_code << " и все его маршруты удалены.\n";
    } catch (const std::exception& error) {
        std::cout << "Ошибка: " << error.what() << "\n";
    }
}

/**
 * @brief Добавление ориентированного ребра (маршрута) в граф.
 * @param graph Целевой граф.
 */
void addEdge(Graph<std::string>& graph) {
    std::string origin = readString("Откуда летим (аэропорт): ");
    std::string destination = readString("Куда летим (аэропорт): ");
    try {
        graph.insert_edge(origin, destination);
        std::cout << "Маршрут " << origin << " -> " << destination << " успешно открыт!\n";
    } catch (const std::exception& error) {
        std::cout << "Ошибка: " << error.what() << "\n";
    }
}

/**
 * @brief Удаление ориентированного ребра (маршрута) из графа.
 * @param graph Целевой граф.
 */
void removeEdge(Graph<std::string>& graph) {
    std::string origin = readString("Откуда летим (аэропорт): ");
    std::string destination = readString("Куда летим (аэропорт): ");
    try {
        graph.erase_edge(origin, destination);
        std::cout << "Маршрут " << origin << " -> " << destination << " закрыт.\n";
    } catch (const std::exception& error) {
        std::cout << "Ошибка: " << error.what() << "\n";
    }
}

/**
 * @brief Вывод степени вершины графа.
 * @param graph Исходный граф.
 */
void printVertexInfo(const Graph<std::string>& graph) {
    std::string vertex_code = readString("Введите код аэропорта: ");
    if (!graph.has_vertex(vertex_code)) {
        std::cout << "Аэропорт " << vertex_code << " не найден в графе.\n";
        return;
    }
    std::cout << "Аэропорт найден. Общая степень узла: "
              << graph.vertex_degree(vertex_code) << "\n";
}

/**
 * @brief Вывод степени ребра графа.
 * @param graph Исходный граф.
 */
void printEdgeDegree(const Graph<std::string>& graph) {
    std::string origin = readString("Исходный аэропорт: ");
    std::string destination = readString("Целевой аэропорт: ");
    try {
        std::cout << "Степень ребра (" << origin << " -> " << destination << "): "
                  << graph.edge_degree(origin, destination) << "\n";
    } catch (const std::exception& error) {
        std::cout << "Ошибка: " << error.what() << "\n";
    }
}

/**
 * @brief Демонстрация работы обратных и однонаправленных итераторов.
 * @param graph Исходный граф.
 */
void demoGraphIterators(const Graph<std::string>& graph) {
    std::cout << "\n--- Демонстрация обратных и однонаправленных итераторов ---\n";
    std::cout << "Вершины в обратном порядке (v_crbegin -> v_crend):\n  ";
    for (auto rev_it = graph.v_crbegin(); rev_it != graph.v_crend(); ++rev_it) {
        std::cout << *rev_it << " ";
    }
    std::cout << "\nСмежные вершины для первой вершины через f_adj (forward_iterator):\n  ";
    if (!graph.empty()) {
        const std::string& first_vertex = *graph.v_cbegin();
        std::cout << "[" << first_vertex << "]: ";
        for (auto fwd_it = graph.f_adj_begin(first_vertex); fwd_it != graph.f_adj_end(first_vertex); ++fwd_it) {
            std::cout << *fwd_it << " ";
        }
    }
    std::cout << "\n";
}

/** @brief Вывод меню операций с графом. */
void printGraphMenu() {
    std::cout << "\n=== ЗАДАНИЕ 2: ГРАФЫ (Карта перелётов) ===\n"
              << "1. Вывести структуру графа\n"
              << "2. Добавить аэропорт (вершину)\n"
              << "3. Удалить аэропорт (вершину)\n"
              << "4. Открыть маршрут (добавить ребро)\n"
              << "5. Закрыть маршрут (удалить ребро)\n"
              << "6. Степень вершины (vertex_degree)\n"
              << "7. Степень ребра (edge_degree)\n"
              << "8. Демонстрация итераторов (reverse, forward)\n"
              << "9. Очистить карту перелётов\n"
              << "10. Вернуть базовые маршруты (Seed)\n"
              << "0. Вернуться в главное меню\n";
}

/**
 * @brief Обработка выбора пользователя в меню графов.
 * @param choice Выбранный пункт меню.
 * @param graph Целевой граф.
 */
void handleGraphChoice(int choice, Graph<std::string>& graph) {
    switch (choice) {
        case 1:
            std::cout << graph << "Вершин: " << graph.vertex_count()
                      << ", Рёбер: " << graph.edge_count() << "\n";
            break;
        case 2: addVertex(graph); break;
        case 3: removeVertex(graph); break;
        case 4: addEdge(graph); break;
        case 5: removeEdge(graph); break;
        case 6: printVertexInfo(graph); break;
        case 7: printEdgeDegree(graph); break;
        case 8: demoGraphIterators(graph); break;
        case 9: graph.clear(); std::cout << "Карта очищена.\n"; break;
        case 10: seedGraphData(graph); break;
        default: break;
    }
}

/** @brief Меню управления разделом графов. */
void graphMenu() {
    Graph<std::string> graph;
    seedGraphData(graph);
    int choice = -1;
    while (choice != 0) {
        printGraphMenu();
        choice = readInt("Выберите действие: ", 0, MAX_GRAPH_MENU_OPTION);
        handleGraphChoice(choice, graph);
    }
}

} // namespace cli

/** @brief Точка входа в программу. */
int main() {
    int choice = -1;
    while (choice != 0) {
        std::cout << "\n============================================\n"
                  << "      ЛАБОРАТОРНАЯ РАБОТА №4: ГЛАВНОЕ МЕНЮ  \n"
                  << "============================================\n"
                  << "1. Задание 1: Обобщённые алгоритмы сортировки\n"
                  << "2. Задание 2: Обобщённый контейнер Граф\n"
                  << "0. Выход из программы\n";
        choice = cli::readInt("Выберите раздел: ", 0, cli::MAX_MAIN_MENU_OPTION);
        if (choice == 1) cli::sortingMenu();
        else if (choice == 2) cli::graphMenu();
        else if (choice == 0) std::cout << "До свидания!\n";
    }
    return 0;
}

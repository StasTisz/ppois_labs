/**
 * @file main.cpp
 * @brief Главный модуль консольного интерфейса (CLI) для демонстрации сортировок и графов.
 */

#include <iostream>
#include <vector>
#include <string>
#include <limits>
#include <iomanip>
#include <stdexcept>

#include "custom_object.h"
#include "sortings/heapsort.h"
#include "sortings/stooge_sort.h"
#include "graph/graph.h"

namespace cli {

constexpr double MIN_DISTANCE = 0.1;
constexpr int MIN_PRIORITY = 1;
constexpr int MAX_PRIORITY = 10;

void clearInputStream() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

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

void seedDefaultData(std::vector<FlightInfo>& list) {
    list.clear();
    list.emplace_back("B2-710", 1250.5, 2);
    list.emplace_back("SU-100", 720.0, 1);
    list.emplace_back("LH-144", 1830.0, 3);
    list.emplace_back("TK-401", 1420.0, 1);
    list.emplace_back("LO-678", 510.2, 2);
    list.emplace_back("BA-890", 2100.0, 4);
}

void displayList(const std::vector<FlightInfo>& list) {
    std::cout << "\n---------------- ТЕКУЩИЙ СПИСОК РЕЙСОВ ----------------\n";
    if (list.empty()) {
        std::cout << "[Список пуст]\n";
    } else {
        for (std::size_t i = 0; i < list.size(); ++i) {
            std::cout << std::setw(3) << i << ". " << list[i] << "\n";
        }
    }
    std::cout << "-------------------------------------------------------\n";
}

void addFlightInteractive(std::vector<FlightInfo>& list) {
    std::cout << "\n--- Добавление нового авиарейса ---\n";
    std::string number = readString("Введите номер рейса (например, AF-112): ");
    double distance = readDouble("Введите дистанцию полёта (км, > 0): ", MIN_DISTANCE);
    int priority = readInt("Введите уровень приоритета (от 1 до 10): ", MIN_PRIORITY, MAX_PRIORITY);
    list.emplace_back(std::move(number), distance, priority);
    std::cout << "Рейс успешно добавлен!\n";
}

void addFlightViaStream(std::vector<FlightInfo>& list) {
    std::cout << "\n--- Добавление рейса через поток ввода (operator>>) ---\n";
    std::cout << "Введите данные через пробел: [Номер] [Дистанция] [Приоритет]\n> ";
    FlightInfo new_flight;
    if (std::cin >> new_flight) {
        list.push_back(new_flight);
        std::cout << "Объект успешно считан и добавлен!\n";
    } else {
        std::cout << "Ошибка формата ввода! Данные не добавлены.\n";
    }
    clearInputStream();
}

void removeFlight(std::vector<FlightInfo>& list) {
    if (list.empty()) {
        std::cout << "Список пуст!\n";
        return;
    }
    displayList(list);
    int index = readInt("Введите индекс рейса для удаления: ", 0, static_cast<int>(list.size() - 1));
    list.erase(list.begin() + index);
    std::cout << "Рейс успешно удалён.\n";
}

void demoRawArraySort() {
    FlightInfo raw_flights[] = {
        FlightInfo("KL-101", 1300.0, 2),
        FlightInfo("AF-202", 850.0, 1),
        FlightInfo("BA-303", 2100.0, 3)
    };
    constexpr std::size_t n = sizeof(raw_flights) / sizeof(raw_flights[0]);
    std::cout << "\n--- Сортировка C-массива FlightInfo (" << n << " элементов) ---\n";
    std::cout << "До сортировки:\n";
    for (std::size_t i = 0; i < n; ++i) std::cout << "  " << raw_flights[i] << "\n";
    heapsort(raw_flights, n);
    std::cout << "После Heapsort (arr, n):\n";
    for (std::size_t i = 0; i < n; ++i) std::cout << "  " << raw_flights[i] << "\n";
}

void sortHeapsortDemo(std::vector<FlightInfo>& flights) {
    heapsort(flights);
    std::cout << "Отсортировано (Heapsort)!\n";
    displayList(flights);
}

void sortStoogeDemo(std::vector<FlightInfo>& flights) {
    stooge_sort(flights);
    std::cout << "Отсортировано (Stooge sort)!\n";
    displayList(flights);
}

void sortLambdaDemo(std::vector<FlightInfo>& flights) {
    heapsort(flights, [](const FlightInfo& a, const FlightInfo& b) {
        return a.get_distance() > b.get_distance();
    });
    std::cout << "Отсортировано по убыванию дистанции!\n";
    displayList(flights);
}

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

void sortingMenu() {
    std::vector<FlightInfo> flights;
    seedDefaultData(flights);
    int choice = -1;
    while (choice != 0) {
        printSortingMenu();
        choice = readInt("Выберите действие: ", 0, 9);
        handleSortingChoice(choice, flights);
    }
}

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

void addVertex(Graph<std::string>& graph) {
    std::string vertex_code = readString("Введите код аэропорта (например, MSQ): ");
    try {
        graph.insert_vertex(vertex_code);
        std::cout << "Аэропорт " << vertex_code << " успешно добавлен.\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void removeVertex(Graph<std::string>& graph) {
    std::string vertex_code = readString("Введите код аэропорта для удаления: ");
    try {
        graph.erase_vertex(vertex_code);
        std::cout << "Аэропорт " << vertex_code << " и все его маршруты удалены.\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void addEdge(Graph<std::string>& graph) {
    std::string from = readString("Откуда летим (аэропорт): ");
    std::string to = readString("Куда летим (аэропорт): ");
    try {
        graph.insert_edge(from, to);
        std::cout << "Маршрут " << from << " -> " << to << " успешно открыт!\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void removeEdge(Graph<std::string>& graph) {
    std::string from = readString("Откуда летим (аэропорт): ");
    std::string to = readString("Куда летим (аэропорт): ");
    try {
        graph.erase_edge(from, to);
        std::cout << "Маршрут " << from << " -> " << to << " закрыт.\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void printVertexInfo(Graph<std::string>& graph) {
    std::string vertex_code = readString("Введите код аэропорта: ");
    if (!graph.has_vertex(vertex_code)) {
        std::cout << "Аэропорт " << vertex_code << " не найден в графе.\n";
        return;
    }
    std::cout << "Аэропорт найден. Общая степень узла: "
              << graph.vertex_degree(vertex_code) << "\n";
}

void printEdgeDegree(const Graph<std::string>& graph) {
    std::string from = readString("Исходный аэропорт: ");
    std::string to = readString("Целевой аэропорт: ");
    try {
        std::cout << "Степень ребра (" << from << " -> " << to << "): "
                  << graph.edge_degree(from, to) << "\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void demoGraphIterators(const Graph<std::string>& graph) {
    std::cout << "\n--- Демонстрация обратных и однонаправленных итераторов ---\n";
    std::cout << "Вершины в обратном порядке (v_crbegin -> v_crend):\n  ";
    for (auto it = graph.v_crbegin(); it != graph.v_crend(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\nСмежные вершины для первой вершины через f_adj (forward_iterator):\n  ";
    if (graph.vertex_count() > 0) {
        const std::string& first_v = *graph.v_cbegin();
        std::cout << "[" << first_v << "]: ";
        for (auto it = graph.f_adj_begin(first_v); it != graph.f_adj_end(first_v); ++it) {
            std::cout << *it << " ";
        }
    }
    std::cout << "\n";
}

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

void handleGraphChoice(int choice, Graph<std::string>& graph) {
    switch (choice) {
        case 1:
            std::cout << graph;
            std::cout << "Вершин: " << graph.vertex_count() << ", Рёбер: " << graph.edge_count() << "\n";
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

void graphMenu() {
    Graph<std::string> graph;
    seedGraphData(graph);
    int choice = -1;
    while (choice != 0) {
        printGraphMenu();
        choice = readInt("Выберите действие: ", 0, 10);
        handleGraphChoice(choice, graph);
    }
}

} // namespace cli

int main() {
    int choice = -1;
    while (choice != 0) {
        std::cout << "\n============================================\n"
                  << "      ЛАБОРАТОРНАЯ РАБОТА №4: ГЛАВНОЕ МЕНЮ  \n"
                  << "============================================\n"
                  << "1. Задание 1: Обобщённые алгоритмы сортировки\n"
                  << "2. Задание 2: Обобщённый контейнер Граф\n"
                  << "0. Выход из программы\n";
        choice = cli::readInt("Выберите раздел: ", 0, 2);
        if (choice == 1) cli::sortingMenu();
        else if (choice == 2) cli::graphMenu();
        else if (choice == 0) std::cout << "До свидания!\n";
    }
    return 0;
}
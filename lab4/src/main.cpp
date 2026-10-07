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
#include "graph/graph.h" // Подключаем наш граф

namespace cli {

// ==========================================
// БАЗОВЫЕ ФУНКЦИИ ВВОДА
// ==========================================

/**
 * @brief Очищает поток ввода std::cin от некорректных символов и сбрасывает флаги ошибок.
 */
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

// ==========================================
// ФУНКЦИИ ДЛЯ ЗАДАНИЯ 1: СОРТИРОВКИ
// ==========================================

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
    double distance = readDouble("Введите дистанцию полёта (км, > 0): ", 0.1);
    int priority = readInt("Введите уровень приоритета (целое число от 1 до 10): ", 1, 10);
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

void sortingMenu() {
    std::vector<FlightInfo> flights;
    seedDefaultData(flights);
    int choice = -1;
    while (choice != 0) {
        std::cout << "\n=== ЗАДАНИЕ 1: СОРТИРОВКИ ===\n"
                  << "1. Показать текущий список рейсов\n"
                  << "2. Добавить новый рейс (пошагово)\n"
                  << "3. Добавить рейс строкой (через operator>>)\n"
                  << "4. Удалить рейс по индексу\n"
                  << "5. Сбросить данные к начальным\n"
                  << "6. Сортировка Heapsort (по умолчанию)\n"
                  << "7. Сортировка Stooge sort (по умолчанию)\n"
                  << "8. Сортировка Heapsort (лямбда: дистанция по убыванию)\n"
                  << "0. Вернуться в главное меню\n";

        choice = readInt("Выберите действие: ", 0, 8);

        switch (choice) {
            case 1: displayList(flights); break;
            case 2: addFlightInteractive(flights); break;
            case 3: addFlightViaStream(flights); break;
            case 4: removeFlight(flights); break;
            case 5: seedDefaultData(flights); std::cout << "Сброшено.\n"; break;
            case 6:
                heapsort(flights);
                std::cout << "Отсортировано (Heapsort)!\n";
                displayList(flights);
                break;
            case 7:
                stooge_sort(flights);
                std::cout << "Отсортировано (Stooge sort)!\n";
                displayList(flights);
                break;
            case 8:
                heapsort(flights, [](const FlightInfo& a, const FlightInfo& b) {
                    return a.get_distance() > b.get_distance();
                });
                std::cout << "Отсортировано по убыванию дистанции!\n";
                displayList(flights);
                break;
        }
    }
}

// ==========================================
// ФУНКЦИИ ДЛЯ ЗАДАНИЯ 2: ГРАФЫ
// ==========================================

void seedGraphData(Graph<std::string>& g) {
    g.clear();
    g.insert_vertex("MSQ"); // Минск
    g.insert_vertex("SVO"); // Москва
    g.insert_vertex("IST"); // Стамбул
    g.insert_vertex("DXB"); // Дубай

    g.insert_edge("MSQ", "SVO");
    g.insert_edge("MSQ", "IST");
    g.insert_edge("MSQ", "DXB");
    g.insert_edge("IST", "DXB");
    std::cout << "Граф заполнен тестовой картой авиамаршрутов.\n";
}

void addVertex(Graph<std::string>& g) {
    std::string v = readString("Введите код аэропорта (например, MSQ): ");
    try {
        g.insert_vertex(v);
        std::cout << "Аэропорт " << v << " успешно добавлен.\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void removeVertex(Graph<std::string>& g) {
    std::string v = readString("Введите код аэропорта для удаления: ");
    try {
        g.erase_vertex(v);
        std::cout << "Аэропорт " << v << " и все его маршруты удалены.\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void addEdge(Graph<std::string>& g) {
    std::string from = readString("Откуда летим (аэропорт): ");
    std::string to = readString("Куда летим (аэропорт): ");
    try {
        g.insert_edge(from, to);
        std::cout << "Маршрут " << from << " -> " << to << " успешно открыт!\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void removeEdge(Graph<std::string>& g) {
    std::string from = readString("Откуда летим (аэропорт): ");
    std::string to = readString("Куда летим (аэропорт): ");
    try {
        g.erase_edge(from, to);
        std::cout << "Маршрут " << from << " -> " << to << " закрыт.\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void printVertexInfo(Graph<std::string>& g) {
    std::string v = readString("Введите код аэропорта: ");
    if (!g.has_vertex(v)) {
        std::cout << "Аэропорт " << v << " не найден в графе.\n";
        return;
    }
    try {
        std::cout << "Аэропорт присутствует. Общая степень узла (кол-во входящих и исходящих): "
                  << g.vertex_degree(v) << "\n";
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
    }
}

void graphMenu() {
    Graph<std::string> g;
    seedGraphData(g);
    int choice = -1;
    while (choice != 0) {
        std::cout << "\n=== ЗАДАНИЕ 2: ГРАФЫ (Карта перелётов) ===\n"
                  << "1. Вывести структуру графа на экран\n"
                  << "2. Добавить аэропорт (вершину)\n"
                  << "3. Удалить аэропорт (вершину)\n"
                  << "4. Открыть маршрут (добавить ребро)\n"
                  << "5. Закрыть маршрут (удалить ребро)\n"
                  << "6. Информация об аэропорте (степень узла)\n"
                  << "7. Очистить карту перелётов полностью\n"
                  << "8. Вернуть базовые маршруты (Seed)\n"
                  << "0. Вернуться в главное меню\n";

        choice = readInt("Выберите действие: ", 0, 8);

        switch (choice) {
            case 1:
                std::cout << g;
                std::cout << "Всего аэропортов: " << g.vertex_count() << ", Всего маршрутов: " << g.edge_count() << "\n";
                break;
            case 2: addVertex(g); break;
            case 3: removeVertex(g); break;
            case 4: addEdge(g); break;
            case 5: removeEdge(g); break;
            case 6: printVertexInfo(g); break;
            case 7: g.clear(); std::cout << "Карта очищена.\n"; break;
            case 8: seedGraphData(g); break;
        }
    }
}

} // namespace cli

// ==========================================
// ГЛАВНОЕ МЕНЮ
// ==========================================

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

        switch (choice) {
            case 1: cli::sortingMenu(); break;
            case 2: cli::graphMenu(); break;
            case 0: std::cout << "До свидания!\n"; break;
        }
    }
    return 0;
}
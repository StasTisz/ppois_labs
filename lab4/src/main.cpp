/**
 * @file main.cpp
 * @brief Главный модуль консольного интерфейса (CLI) для демонстрации обобщённых алгоритмов.
 */

#include <iostream>
#include <vector>
#include <string>
#include <limits>
#include <iomanip>

#include "custom_object.h"
#include "sortings/heapsort.h"
#include "sortings/stooge_sort.h"

namespace cli {

/**
 * @brief Очищает поток ввода std::cin от некорректных символов и сбрасывает флаги ошибок.
 */
void clearInputStream() {
    std::cin.clear();
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

/**
 * @brief Безопасно считывает целое число из заданного диапазона.
 * @param prompt Текст приглашения ко вводу.
 * @param min_val Минимальное допустимое значение.
 * @param max_val Максимальное допустимое значение.
 * @return Корректное целое число.
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
 * @brief Безопасно считывает вещественное число не меньше минимального порога.
 * @param prompt Текст приглашения ко вводу.
 * @param min_val Минимально допустимое значение.
 * @return Корректное вещественное число.
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
 * @brief Считывает непустую строку из потока ввода.
 * @param prompt Текст приглашения ко вводу.
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
 * @brief Заполняет вектор базовым набором демонстрационных данных для тестов.
 * @param list Вектор для заполнения.
 */
void seedDefaultData(std::vector<FlightInfo>& list) {
    list.clear();
    list.emplace_back("B2-710", 1250.5, 2);
    list.emplace_back("SU-100", 720.0, 1);
    list.emplace_back("LH-144", 1830.0, 3);
    list.emplace_back("TK-401", 1420.0, 1);
    list.emplace_back("LO-678", 510.2, 2);
    list.emplace_back("BA-890", 2100.0, 4);
}

/**
 * @brief Выводит текущую коллекцию рейсов в консоль в виде форматированного списка.
 * @param list Коллекция рейсов.
 */
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

/**
 * @brief Запрашивает у пользователя данные пошагово и добавляет новый рейс.
 * @param list Коллекция рейсов.
 */
void addFlightInteractive(std::vector<FlightInfo>& list) {
    std::cout << "\n--- Добавление нового авиарейса (Пошагово) ---\n";
    std::string number = readString("Введите номер рейса (например, AF-112): ");
    double distance = readDouble("Введите дистанцию полёта (км, > 0): ", 0.1);
    int priority = readInt("Введите уровень приоритета (целое число от 1 до 10): ", 1, 10);

    list.emplace_back(std::move(number), distance, priority);
    std::cout << "Рейс успешно добавлен!\n";
}

/**
 * @brief Добавляет рейс, демонстрируя перегруженный оператор ввода (>>).
 * @param list Коллекция рейсов.
 */
void addFlightViaStream(std::vector<FlightInfo>& list) {
    std::cout << "\n--- Добавление рейса через поток ввода (operator>>) ---\n";
    std::cout << "Введите данные через пробел: [Номер(строка)] [Дистанция(число)] [Приоритет(целое)]\n";
    std::cout << "Пример ввода: AZ-555 1200.5 5\n> ";

    FlightInfo new_flight;
    if (std::cin >> new_flight) {
        list.push_back(new_flight);
        std::cout << "Объект успешно считан из потока и добавлен!\n";
    } else {
        std::cout << "Ошибка формата ввода! Данные не добавлены.\n";
    }
    clearInputStream(); // Очищаем буфер после чтения оператором >>
}

/**
 * @brief Удаляет рейс по указанному индексу из вектора.
 * @param list Коллекция рейсов.
 */
void removeFlight(std::vector<FlightInfo>& list) {
    if (list.empty()) {
        std::cout << "Удаление невозможно: список пуст!\n";
        return;
    }

    displayList(list);
    int index = readInt("Введите индекс рейса для удаления: ", 0, static_cast<int>(list.size() - 1));
    list.erase(list.begin() + index);
    std::cout << "Рейс с индексом " << index << " успешно удалён.\n";
}

/**
 * @brief Запускает и замеряет пирамидальную сортировку (Heapsort).
 * @param list Коллекция для сортировки.
 */
void performHeapsort(std::vector<FlightInfo>& list) {
    if (list.size() < 2) {
        std::cout << "В списке меньше двух элементов, сортировка не требуется.\n";
        return;
    }

    std::cout << "\nЗапуск Heapsort (сложность O(N log N))...\n";
    heapsort(list);
    std::cout << "Коллекция успешно отсортирована (Heapsort)!\n";
    displayList(list);
}

/**
 * @brief Запускает сортировку Студжа (Stooge sort).
 * @param list Коллекция для сортировки.
 */
void performStoogeSort(std::vector<FlightInfo>& list) {
    if (list.size() < 2) {
        std::cout << "В списке меньше двух элементов, сортировка не требуется.\n";
        return;
    }

    if (list.size() > 40) {
        std::cout << "Внимание: для N=" << list.size()
                  << " Stooge sort (O(N^2.709)) может работать долго.\n";
    }

    std::cout << "\nЗапуск Stooge sort...\n";
    stooge_sort(list);
    std::cout << "Коллекция успешно отсортирована (Stooge sort)!\n";
    displayList(list);
}

/**
 * @brief Запускает сортировку с пользовательским лямбда-выражением в качестве компаратора.
 * @param list Коллекция для сортировки.
 */
void performCustomSort(std::vector<FlightInfo>& list) {
    if (list.size() < 2) {
        std::cout << "В списке меньше двух элементов, сортировка не требуется.\n";
        return;
    }

    std::cout << "\nЗапуск кастомной сортировки (Heapsort, убывание дистанции)...\n";
    heapsort(list, [](const FlightInfo& a, const FlightInfo& b) {
        return a.get_distance() > b.get_distance();
    });
    std::cout << "Отсортировано по убыванию дистанции!\n";
    displayList(list);
}

} // namespace cli

/**
 * @brief Главная функция программы. Запускает цикл консольного меню.
 * @return 0 при успешном завершении работы программы.
 */
int main() {
    std::vector<FlightInfo> flights;
    cli::seedDefaultData(flights);

    int choice = -1;
    while (choice != 0) {
        std::cout << "\n============================================\n"
                  << "  ЛАБОРАТОРНАЯ РАБОТА №4: СОРТИРОВКИ (CLI)  \n"
                  << "============================================\n"
                  << "1. Показать текущий список рейсов\n"
                  << "2. Добавить новый рейс (пошагово)\n"
                  << "3. Добавить рейс строкой (через operator>>)\n"
                  << "4. Удалить рейс по индексу\n"
                  << "5. Сбросить данные к начальным (Seed Data)\n"
                  << "6. Очистить список полностью\n"
                  << "7. Сортировка Heapsort (по умолчанию)\n"
                  << "8. Сортировка Stooge sort (по умолчанию)\n"
                  << "9. Сортировка Heapsort (лямбда: дистанция по убыванию)\n"
                  << "0. Выход из программы\n";

        choice = cli::readInt("Выберите действие: ", 0, 9);

        switch (choice) {
            case 1: cli::displayList(flights); break;
            case 2: cli::addFlightInteractive(flights); break;
            case 3: cli::addFlightViaStream(flights); break;
            case 4: cli::removeFlight(flights); break;
            case 5:
                cli::seedDefaultData(flights);
                std::cout << "Список сброшен к базовым данным.\n";
                break;
            case 6:
                flights.clear();
                std::cout << "Список очищен.\n";
                break;
            case 7: cli::performHeapsort(flights); break;
            case 8: cli::performStoogeSort(flights); break;
            case 9: cli::performCustomSort(flights); break;
            case 0: std::cout << "Завершение программы.\n"; break;
            default: break;
        }
    }

    return 0;
}
/**
 * @file custom_object.h
 * @brief Определение пользовательского типа данных FlightInfo для проверки обобщённых алгоритмов и структур данных.
 */

#pragma once

#include <iostream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>

/**
 * @class FlightInfo
 * @brief Пользовательский класс, представляющий сведения об авиарейсе.
 *
 * Служит для демонстрации работы шаблонных сортировок (Задание 1)
 * и в качестве полезной нагрузки вершины графа (Задание 2).
 * Поддерживает полный набор операций сравнения и потоковый ввод-вывод.
 */
class FlightInfo {
private:
    static constexpr double MIN_VALID_DISTANCE = 0.0; ///< Минимальная допустимая дальность полёта
    static constexpr int DEFAULT_PRIORITY = 0;        ///< Приоритет рейса по умолчанию

    std::string flight_number;  ///< Номер рейса (например, "SU-100")
    double distance_km;         ///< Дальность полёта в километрах
    int priority_level;         ///< Приоритет рейса (чем выше число, тем выше приоритет)

public:
    /**
     * @brief Конструктор по умолчанию.
     * Инициализирует рейс со значениями "UNKNOWN", 0.0 км и нулевым приоритетом.
     */
    FlightInfo()
        : flight_number("UNKNOWN"), distance_km(MIN_VALID_DISTANCE), priority_level(DEFAULT_PRIORITY) {}

    /**
     * @brief Параметризованный конструктор.
     * @param number Идентификатор (номер) авиарейса.
     * @param distance Дистанция полёта в километрах.
     * @param priority Числовой приоритет рейса.
     */
    FlightInfo(std::string number, double distance, int priority)
        : flight_number(std::move(number)), distance_km(distance), priority_level(priority) {}

    /**
     * @brief Возвращает номер рейса.
     * @return Константная ссылка на строку с номером рейса.
     */
    const std::string& get_number() const { return flight_number; }

    /**
     * @brief Возвращает дистанцию полёта.
     * @return Дистанция в километрах.
     */
    double get_distance() const { return distance_km; }

    /**
     * @brief Возвращает приоритет рейса.
     * @return Уровень приоритета.
     */
    int get_priority() const { return priority_level; }

    /**
     * @brief Устанавливает новый номер рейса.
     * @param number Новый идентификатор рейса.
     */
    void set_number(std::string number) { flight_number = std::move(number); }

    /**
     * @brief Устанавливает дистанцию рейса.
     * @param distance Дистанция в км (не может быть отрицательной).
     * @throws std::invalid_argument если distance < 0.
     */
    void set_distance(double distance) {
        if (distance < MIN_VALID_DISTANCE) {
            throw std::invalid_argument("Дистанция не может быть отрицательной!");
        }
        distance_km = distance;
    }

    /**
     * @brief Устанавливает приоритет рейса.
     * @param priority Уровень приоритета.
     */
    void set_priority(int priority) { priority_level = priority; }

    /**
     * @brief Оператор "меньше".
     * Сравнение выполняется лексикографически: дистанция -> приоритет -> номер рейса.
     * @param other Объект для сравнения.
     * @return true, если текущий объект меньше other.
     */
    bool operator<(const FlightInfo& other) const {
        return std::tie(distance_km, priority_level, flight_number) <
               std::tie(other.distance_km, other.priority_level, other.flight_number);
    }

    /**
     * @brief Оператор проверки на равенство.
     * @param other Объект для сравнения.
     * @return true, если все поля совпадают.
     */
    bool operator==(const FlightInfo& other) const {
        return std::tie(distance_km, priority_level, flight_number) ==
               std::tie(other.distance_km, other.priority_level, other.flight_number);
    }

    /** @brief Оператор проверки на неравенство. */
    bool operator!=(const FlightInfo& other) const { return !(*this == other); }
    /** @brief Оператор "больше". */
    bool operator>(const FlightInfo& other) const { return other < *this; }
    /** @brief Оператор "меньше либо равно". */
    bool operator<=(const FlightInfo& other) const { return !(other < *this); }
    /** @brief Оператор "больше либо равно". */
    bool operator>=(const FlightInfo& other) const { return !(*this < other); }

    /**
     * @brief Выводит строковое представление объекта в выходной поток.
     * @param os Выходной поток.
     * @param flight Выводимый объект рейса.
     * @return Ссылка на выходной поток.
     */
    friend std::ostream& operator<<(std::ostream& os, const FlightInfo& flight) {
        os << "[" << flight.flight_number << " | "
           << flight.distance_km << " км | Приоритет: "
           << flight.priority_level << "]";
        return os;
    }

    /**
     * @brief Считывает данные рейса из входного потока.
     * Ожидает три значения, разделённых пробелом: номер_рейса дистанция приоритет.
     * @param is Входной поток.
     * @param flight Объект для записи результата.
     * @return Ссылка на входной поток.
     */
    friend std::istream& operator>>(std::istream& is, FlightInfo& flight) {
        std::string number;
        double distance = MIN_VALID_DISTANCE;
        int priority = DEFAULT_PRIORITY;
        if (is >> number >> distance >> priority) {
            if (distance < MIN_VALID_DISTANCE || priority < DEFAULT_PRIORITY || number.empty()) {
                is.setstate(std::ios::failbit);
                return is;
            }
            flight.flight_number = std::move(number);
            flight.distance_km = distance;
            flight.priority_level = priority;
        }
        return is;
    }
};

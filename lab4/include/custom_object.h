/**
 * @file custom_object.h
 * @brief Определение пользовательского типа данных FlightInfo для проверки обобщённых алгоритмов и структур данных.
 */

#pragma once

#include <string>
#include <iostream>
#include <tuple>
#include <utility>

/**
 * @class FlightInfo
 * @brief Пользовательский класс, представляющий сведения об авиарейсе.
 *
 * Служит для демонстрации работы шаблонных сортировок (Задание 1)
 * и в качестве полезной нагрузки вершины графа (Задание 2).
 * Поддерживает полный набор операций сравнения и потоковый вывод.
 */
class FlightInfo {
private:
    std::string flight_number;  ///< Номер рейса (например, "SU-100")
    double distance_km;         ///< Дальность полёта в километрах
    int priority_level;         ///< Приоритет рейса (чем выше число, тем выше приоритет)

public:
    /**
     * @brief Конструктор по умолчанию.
     * Инициализирует рейс со значениями "UNKNOWN", 0.0 км и нулевым приоритетом.
     */
    FlightInfo()
        : flight_number("UNKNOWN"), distance_km(0.0), priority_level(0) {}

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
     * @brief Оператор "меньше".
     *
     * Сравнение выполняется лексикографически через std::tie в следующем порядке:
     * дистанция -> приоритет -> номер рейса.
     * @param other Объект для сравнения.
     * @return true, если текущий объект меньше @p other, иначе false.
     */
    bool operator<(const FlightInfo& other) const {
        return std::tie(distance_km, priority_level, flight_number) <
               std::tie(other.distance_km, other.priority_level, other.flight_number);
    }

    /**
     * @brief Оператор проверки на равенство.
     * @param other Объект для сравнения.
     * @return true, если все поля совпадают, иначе false.
     */
    bool operator==(const FlightInfo& other) const {
        return std::tie(distance_km, priority_level, flight_number) ==
               std::tie(other.distance_km, other.priority_level, other.flight_number);
    }

    /**
     * @brief Оператор проверки на неравенство.
     * @param other Объект для сравнения.
     * @return true, если объекты отличаются хотя бы одним полем, иначе false.
     */
    bool operator!=(const FlightInfo& other) const { return !(*this == other); }

    /**
     * @brief Оператор "больше".
     * @param other Объект для сравнения.
     * @return true, если текущий объект строго больше @p other.
     */
    bool operator>(const FlightInfo& other) const { return other < *this; }

    /**
     * @brief Оператор "меньше либо равно".
     * @param other Объект для сравнения.
     * @return true, если текущий объект меньше либо равен @p other.
     */
    bool operator<=(const FlightInfo& other) const { return !(other < *this); }

    /**
     * @brief Оператор "больше либо равно".
     * @param other Объект для сравнения.
     * @return true, если текущий объект больше либо равен @p other.
     */
    bool operator>=(const FlightInfo& other) const { return !(*this < other); }

    /**
     * @brief Выводит строковое представление объекта в выходной поток.
     * Формат вывода: [Номер | Дистанция км | Приоритет: Число]
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
};
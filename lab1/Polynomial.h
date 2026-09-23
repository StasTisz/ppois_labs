/**
 * @file Polynomial.h
 * @brief Заголовочный файл с объявлением класса Polynomial для работы с математическими многочленами.
 */

#pragma once
#include <vector>
#include <iostream>

/**
 * @class Polynomial
 * @brief Класс, представляющий многочлен одной переменной.
 *
 * Хранит коэффициенты многочлена и предоставляет математические операции над ними
 * (сложение, вычитание, умножение, деление уголком).
 */
class Polynomial {
private:
    std::vector<double> coefs;

    /**
     * @brief Нормализует многочлен, удаляя старшие нулевые коэффициенты.
     */
    void normalize();

public:
    /**
     * @brief Конструктор по умолчанию. Создает нулевой многочлен: P(x) = 0.
     */
    Polynomial();

    /**
     * @brief Конструктор от вектора коэффициентов.
     * @param c Вектор коэффициентов, где индекс соответствует степени x.
     */
    Polynomial(std::vector<double> c);

    /**
     * @brief Возвращает степень многочлена.
     * @return Целое число — максимальная степень x с ненулевым коэффициентом.
     */
    int getDegree() const;

    /**
     * @brief Возвращает коэффициент при заданной степени x.
     * @param power Степень переменной x.
     * @return Значение коэффициента. Если степень выходит за пределы, возвращает 0.0.
     */
    double operator[](int power) const;

    /**
     * @brief Вычисляет значение многочлена в заданной точке x.
     * @param x Точка, для которой вычисляется значение.
     * @return Значение P(x).
     */
    double operator()(double x) const;

    /**
     * @brief Прибавляет другой многочлен к текущему.
     * @param other Многочлен-слагаемое.
     * @return Ссылка на текущий измененный объект.
     */
    Polynomial& operator+=(const Polynomial& other);

    /**
     * @brief Вычитает другой многочлен из текущего.
     * @param other Многочлен-вычитаемое.
     * @return Ссылка на текущий измененный объект.
     */
    Polynomial& operator-=(const Polynomial& other);

    /**
     * @brief Оператор сложения двух многочленов.
     * @param other Многочлен-слагаемое.
     * @return Новый многочлен, являющийся суммой.
     */
    Polynomial operator+(const Polynomial& other) const;

    /**
     * @brief Оператор вычитания двух многочленов.
     * @param other Многочлен-вычитаемое.
     * @return Новый многочлен, являющийся разностью.
     */
    Polynomial operator-(const Polynomial& other) const;

    /**
     * @brief Оператор умножения двух многочленов.
     * @param other Многочлен-множитель.
     * @return Новый многочлен, являющийся произведением.
     */
    Polynomial operator*(const Polynomial& other) const;

    /**
     * @brief Умножает текущий многочлен на другой.
     * @param other Многочлен-множитель.
     * @return Ссылка на текущий измененный объект.
     */
    Polynomial& operator*=(const Polynomial& other);

    /**
     * @brief Оператор деления многочленов "уголком".
     * @param other Многочлен-делитель.
     * @return Новый многочлен — целая часть от деления.
     * @throw std::invalid_argument Если делитель равен нулю.
     */
    Polynomial operator/(const Polynomial& other) const;

    /**
     * @brief Делит текущий многочлен на другой с сохранением целой части.
     * @param other Многочлен-делитель.
     * @return Ссылка на текущий измененный объект.
     */
    Polynomial& operator/=(const Polynomial& other);

    /**
     * @brief Проверяет два многочлена на равенство.
     * @param other Многочлен для сравнения.
     * @return true, если коэффициенты совпадают, иначе false.
     */
    bool operator==(const Polynomial& other) const;

    /**
     * @brief Проверяет два многочлена на неравенство.
     * @param other Многочлен для сравнения.
     * @return true, если многочлены не равны, иначе false.
     */
    bool operator!=(const Polynomial& other) const;

    /**
     * @brief Выводит многочлен в выходной поток в человекочитаемом виде.
     * @param os Выходной поток.
     * @param p Многочлен для вывода.
     * @return Ссылка на выходной поток.
     */
    friend std::ostream& operator<<(std::ostream& os, const Polynomial& p);

    /**
     * @brief Считывает многочлен из входного потока.
     * Запрашивает у пользователя степень и поочередно каждый коэффициент.
     * @param is Входной поток.
     * @param p Многочлен, в который запишется результат.
     * @return Ссылка на входной поток.
     */
    friend std::istream& operator>>(std::istream& is, Polynomial& p);
};
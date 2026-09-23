/**
 * @file Polynomial.cpp
 * @brief Реализация методов класса Polynomial.
 */

#include "Polynomial.h"
#include <stdexcept>

// Удаляет незначащие нули при старших степенях
void Polynomial::normalize() {
    while (coefs.size() > 1 && coefs.back() == 0.0) {
        coefs.pop_back();
    }
}

// Конструктор по умолчанию: инициализирует нулевой многочлен P(x) = 0
Polynomial::Polynomial() {
    coefs.push_back(0.0);
}

// Конструктор от вектора коэффициентов с последующей нормализацией
Polynomial::Polynomial(std::vector<double> c) {
    coefs = c;
    if (coefs.empty()) {
        coefs.push_back(0.0);
    }
    normalize();
}

// Возвращает степень многочлена (индекс старшего ненулевого коэффициента)
int Polynomial::getDegree() const {
    return coefs.size() - 1;
}

// Доступ к коэффициенту при заданной степени x (возвращает 0 при выходе за границы)
double Polynomial::operator[](int power) const {
    if (power < 0 || power >= coefs.size()) {
        return 0.0;
    }
    return coefs[power];
}

// Вычисление значения многочлена P(x) в заданной точке
double Polynomial::operator()(double x) const {
    double total_sum = 0.0;
    double current_x_power = 1.0;
    for (int i = 0; i < coefs.size(); i++) {
        total_sum += coefs[i] * current_x_power;
        current_x_power *= x;
    }
    return total_sum;
}

// Сложение многочленов с присваиванием текущему объекту
Polynomial& Polynomial::operator+=(const Polynomial& other) {
    if (other.coefs.size() > coefs.size()) {
        coefs.resize(other.coefs.size(), 0.0);
    }
    for (int i = 0; i < other.coefs.size(); i++) {
        coefs[i] += other.coefs[i];
    }
    normalize();
    return *this;
}

// Вычитание многочленов с присваиванием текущему объекту
Polynomial& Polynomial::operator-=(const Polynomial& other) {
    if (other.coefs.size() > coefs.size()) {
        coefs.resize(other.coefs.size(), 0.0);
    }
    for (int i = 0; i < other.coefs.size(); i++) {
        coefs[i] -= other.coefs[i];
    }
    normalize();
    return *this;
}

// Бинарное сложение: возвращает новый многочлен
Polynomial Polynomial::operator+(const Polynomial& other) const {
    Polynomial result = *this;
    result += other;
    return result;
}

// Бинарное вычитание: возвращает новый многочлен
Polynomial Polynomial::operator-(const Polynomial& other) const {
    Polynomial result = *this;
    result -= other;
    return result;
}

// Умножение многочленов через свертку коэффициентов
Polynomial Polynomial::operator*(const Polynomial& other) const {
    std::vector<double> result_coefs(coefs.size() + other.coefs.size() - 1, 0.0);
    for (int i = 0; i < coefs.size(); i++) {
        for (int j = 0; j < other.coefs.size(); j++) {
            result_coefs[i + j] += coefs[i] * other.coefs[j];
        }
    }
    return Polynomial(result_coefs);
}

// Умножение с присваиванием текущему объекту
Polynomial& Polynomial::operator*=(const Polynomial& other) {
    *this = *this * other;
    return *this;
}

// Деление многочленов "уголком": возвращает целую часть от деления
Polynomial Polynomial::operator/(const Polynomial& other) const {
    if (other.getDegree() == 0 && other[0] == 0.0) {
        throw std::invalid_argument("Ошибка: деление на нулевой многочлен!");
    }
    Polynomial remainder = *this;
    if (remainder.getDegree() < other.getDegree()) {
        return Polynomial();
    }
    int result_degree = remainder.getDegree() - other.getDegree();
    std::vector<double> quotient_coefs(result_degree + 1, 0.0);
    while (remainder.getDegree() >= other.getDegree() &&
          !(remainder.getDegree() == 0 && remainder[0] == 0.0)) {
        int deg_diff = remainder.getDegree() - other.getDegree();
        double lead_coef = remainder[remainder.getDegree()] / other[other.getDegree()];
        quotient_coefs[deg_diff] = lead_coef;
        for (int i = 0; i <= other.getDegree(); i++) {
            remainder.coefs[i + deg_diff] -= lead_coef * other[i];
        }
        remainder.normalize();
    }
    return Polynomial(quotient_coefs);
}

// Деление с присваиванием (сохраняет только частное)
Polynomial& Polynomial::operator/=(const Polynomial& other) {
    *this = *this / other;
    return *this;
}

// Сравнение на поэлементное равенство векторов коэффициентов
bool Polynomial::operator==(const Polynomial& other) const {
    return coefs == other.coefs;
}

// Сравнение на неравенство
bool Polynomial::operator!=(const Polynomial& other) const {
    return !(*this == other);
}

// Вывод многочлена в поток в виде P(x) = c_n*x^n + ... + c_0
std::ostream& operator<<(std::ostream& os, const Polynomial& p) {
    if (p.getDegree() == 0 && p[0] == 0) return os << "0";
    bool first = true;
    for (int i = p.getDegree(); i >= 0; i--) {
        if (p[i] == 0) continue;
        if (!first && p[i] > 0) os << "+";
        os << p[i];
        if (i > 0) os << "x^" << i << " ";
        first = false;
    }
    return os;
}

// Интерактивное чтение степени и коэффициентов из входного потока
std::istream& operator>>(std::istream& is, Polynomial& p) {
    int degree;
    std::cout << "Введите степень многочлена: ";
    is >> degree;
    std::vector<double> c(degree + 1);
    for (int i = 0; i <= degree; i++) {
        std::cout << "Коэффициент при x^" << i << ": ";
        is >> c[i];
    }
    p = Polynomial(c);
    return is;
}
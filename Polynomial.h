#pragma once
#include <vector>
#include <iostream>
#include <stdexcept>

class Polynomial {
private:
    std::vector<double> coefs;

    void normalize() {
        while (coefs.size() > 1 && coefs.back() == 0.0) {
            coefs.pop_back();
        }
    }

public:
    Polynomial() {
        coefs.push_back(0.0);
    }

    Polynomial(std::vector<double> c) {
        coefs = c;
        if (coefs.empty()) {
            coefs.push_back(0.0);
        }
        normalize();
    }

    int getDegree() const {
        return coefs.size() - 1;
    }

    double operator[](int power) const {
        if (power < 0 || power >= coefs.size()) {
            return 0.0;
        }
        return coefs[power];
    }

    double operator()(double x) const {
        double total_sum = 0.0;
        double current_x_power = 1.0;

        for (int i = 0; i < coefs.size(); i++) {
            total_sum += coefs[i] * current_x_power;
            current_x_power *= x;
        }

        return total_sum;
    }

    Polynomial& operator+=(const Polynomial& other) {
        if (other.coefs.size() > coefs.size()) {
            coefs.resize(other.coefs.size(), 0.0);
        }
        for (int i = 0; i < other.coefs.size(); i++) {
            coefs[i] += other.coefs[i];
        }
        normalize();
        return *this;
    }

    Polynomial& operator-=(const Polynomial& other) {
        if (other.coefs.size() > coefs.size()) {
            coefs.resize(other.coefs.size(), 0.0);
        }
        for (int i = 0; i < other.coefs.size(); i++) {
            coefs[i] -= other.coefs[i];
        }
        normalize();
        return *this;
    }

    Polynomial operator+(const Polynomial& other) const {
        Polynomial result = *this;
        result += other;
        return result;
    }

    Polynomial operator-(const Polynomial& other) const {
        Polynomial result = *this;
        result -= other;
        return result;
    }

    Polynomial operator*(const Polynomial& other) const {
        std::vector<double> result_coefs(coefs.size() + other.coefs.size() - 1, 0.0);
        for (int i = 0; i < coefs.size(); i++) {
            for (int j = 0; j < other.coefs.size(); j++) {
                result_coefs[i + j] += coefs[i] * other.coefs[j];
            }
        }
        return Polynomial(result_coefs);
    }

    Polynomial& operator*=(const Polynomial& other) {
        *this = *this * other;
        return *this;
    }

    Polynomial operator/(const Polynomial& other) const {
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

    Polynomial& operator/=(const Polynomial& other) {
        *this = *this / other;
        return *this;
    }

    bool operator==(const Polynomial& other) const {
        return coefs == other.coefs;
    }

    bool operator!=(const Polynomial& other) const {
        return !(*this == other);
    }

    friend std::ostream& operator<<(std::ostream& os, const Polynomial& p) {
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

    friend std::istream& operator>>(std::istream& is, Polynomial& p) {
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
};
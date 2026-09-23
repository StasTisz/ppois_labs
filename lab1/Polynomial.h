#pragma once
#include <vector>
#include <iostream>

class Polynomial {
private:
    std::vector<double> coefs;
    void normalize();

public:
    Polynomial();
    Polynomial(std::vector<double> c);

    int getDegree() const;
    double operator[](int power) const;
    double operator()(double x) const;

    Polynomial& operator+=(const Polynomial& other);
    Polynomial& operator-=(const Polynomial& other);
    Polynomial operator+(const Polynomial& other) const;
    Polynomial operator-(const Polynomial& other) const;
    Polynomial operator*(const Polynomial& other) const;
    Polynomial& operator*=(const Polynomial& other);
    Polynomial operator/(const Polynomial& other) const;
    Polynomial& operator/=(const Polynomial& other);

    bool operator==(const Polynomial& other) const;
    bool operator!=(const Polynomial& other) const;

    friend std::ostream& operator<<(std::ostream& os, const Polynomial& p);
    friend std::istream& operator>>(std::istream& is, Polynomial& p);
};
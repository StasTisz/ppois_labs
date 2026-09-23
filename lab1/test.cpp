#include <gtest/gtest.h>
#include "Polynomial.h"
#include "Set.h"
#include <sstream>
#include <stdexcept>

// ==========================================
//        ТЕСТЫ ДЛЯ МНОГОЧЛЕНОВ
// ==========================================

TEST(PolynomialTest, ConstructorsAndNormalization) {
    Polynomial p1;
    EXPECT_EQ(p1.getDegree(), 0);
    EXPECT_EQ(p1[0], 0.0);

    // Проверка нормализации (удаление незначащих нулей при старших степенях)
    Polynomial p2({1.0, 2.0, 0.0, 0.0});
    EXPECT_EQ(p2.getDegree(), 1);
    EXPECT_EQ(p2[1], 2.0);

    Polynomial p_empty(std::vector<double>{});
    EXPECT_EQ(p_empty.getDegree(), 0);
}

TEST(PolynomialTest, ElementAccessAndEvaluation) {
    Polynomial p({2.0, 3.0, 1.0}); // 2 + 3x + x^2

    // Доступ по индексу (в пределах и за пределами)
    EXPECT_EQ(p[0], 2.0);
    EXPECT_EQ(p[2], 1.0);
    EXPECT_EQ(p[10], 0.0); // За пределами вектора
    EXPECT_EQ(p[-1], 0.0); // Отрицательная степень

    // Вычисление значения: 2 + 3*2 + 2^2 = 12
    EXPECT_EQ(p(2.0), 12.0);
}

TEST(PolynomialTest, ArithmeticOperations) {
    Polynomial p1({1.0, 2.0});       // 1 + 2x
    Polynomial p2({3.0, 4.0, 1.0});  // 3 + 4x + x^2

    // Сложение
    Polynomial sum = p1 + p2;
    EXPECT_EQ(sum[0], 4.0);
    EXPECT_EQ(sum[2], 1.0);

    // Вычитание
    Polynomial diff = p2 - p1;
    EXPECT_EQ(diff[0], 2.0);
    EXPECT_EQ(diff[1], 2.0);
    EXPECT_EQ(diff[2], 1.0);

    // Умножение
    Polynomial prod = p1 * p2;
    EXPECT_EQ(prod[0], 3.0); // 1*3
    EXPECT_EQ(prod.getDegree(), 3); // x * x^2 = x^3
}

TEST(PolynomialTest, CompoundAssignments) {
    Polynomial p({1.0, 1.0});
    p += Polynomial({2.0});
    EXPECT_EQ(p[0], 3.0);

    p -= Polynomial({1.0, 1.0});
    EXPECT_EQ(p[0], 2.0);
    EXPECT_EQ(p[1], 0.0);

    p *= Polynomial({0.0, 1.0}); // Умножение на x
    EXPECT_EQ(p[1], 2.0);
}

TEST(PolynomialTest, Division) {
    // (x^2 - 1) / (x - 1) = (x + 1)
    Polynomial dividend({-1.0, 0.0, 1.0});
    Polynomial divisor({-1.0, 1.0});

    Polynomial quotient = dividend / divisor;
    EXPECT_EQ(quotient.getDegree(), 1);
    EXPECT_EQ(quotient[0], 1.0);
    EXPECT_EQ(quotient[1], 1.0);

    // Проверка деления на больший многочлен (возвращает 0)
    Polynomial zero_quot = divisor / dividend;
    EXPECT_EQ(zero_quot.getDegree(), 0);

    // Составное деление
    Polynomial p_div = dividend;
    p_div /= divisor;
    EXPECT_EQ(p_div[1], 1.0);

    // Деление на ноль должно бросать исключение
    Polynomial zero;
    EXPECT_THROW(dividend / zero, std::invalid_argument);
}

TEST(PolynomialTest, EqualityAndStreams) {
    Polynomial p1({1.0, 2.0});
    Polynomial p2({1.0, 2.0});
    Polynomial p3({1.0, 3.0});

    EXPECT_TRUE(p1 == p2);
    EXPECT_TRUE(p1 != p3);

    // Тест вывода в поток (<<)
    std::stringstream out;
    out << p1;
    // Ожидаемый формат: "2x^1 +1" (в зависимости от твоей логики вывода, просто проверяем что поток работает)
    EXPECT_FALSE(out.str().empty());

    // Тест ввода из потока (>>)
    // Симулируем ввод: степень 1, коэффициенты 5.0, 6.0
    std::stringstream in("1 5.0 6.0");
    Polynomial p_in;
    // Перехватываем cout, чтобы меню ввода не засоряло логи тестов
    std::streambuf* orig = std::cout.rdbuf();
    std::cout.rdbuf(nullptr);
    in >> p_in;
    std::cout.rdbuf(orig); // Возвращаем cout

    EXPECT_EQ(p_in.getDegree(), 1);
    EXPECT_EQ(p_in[0], 5.0);
    EXPECT_EQ(p_in[1], 6.0);
}

// ==========================================
//        ТЕСТЫ ДЛЯ МНОЖЕСТВ
// ==========================================

TEST(SetTest, BasicOperations) {
    Set<int> s;
    EXPECT_TRUE(s.isEmpty());
    EXPECT_EQ(s.cardinality(), 0);

    s.add(10);
    s.add(20);
    s.add(10); // Дубликат игнорируется

    EXPECT_FALSE(s.isEmpty());
    EXPECT_EQ(s.cardinality(), 2);
    EXPECT_TRUE(s.contains(10));
    EXPECT_FALSE(s.contains(30));

    s.remove(10);
    EXPECT_FALSE(s.contains(10));

    s.remove(999); // Удаление несуществующего (не должно крашиться)
}

TEST(SetTest, ArithmeticOperations) {
    Set<int> s1, s2;
    s1.add(1); s1.add(2);
    s2.add(2); s2.add(3);

    // Объединение (A + B)
    Set<int> s_union = s1 + s2;
    EXPECT_EQ(s_union.cardinality(), 3);
    EXPECT_TRUE(s_union.contains(3));

    // Пересечение (A * B)
    Set<int> s_intersect = s1 * s2;
    EXPECT_EQ(s_intersect.cardinality(), 1);
    EXPECT_TRUE(s_intersect.contains(2));

    // Разность (A - B)
    Set<int> s_diff = s1 - s2;
    EXPECT_EQ(s_diff.cardinality(), 1);
    EXPECT_TRUE(s_diff.contains(1));

    // Составные операции
    s1 += s2;
    EXPECT_EQ(s1.cardinality(), 3);

    s1 *= Set<int>(); // Пересечение с пустым
    EXPECT_TRUE(s1.isEmpty());
}

TEST(SetTest, EqualityAndPowerSet) {
    Set<int> s1, s2, s3;
    s1.add(1); s1.add(2);
    s2.add(2); s2.add(1);
    s3.add(1);

    EXPECT_TRUE(s1 == s2); // Порядок не должен влиять (по твоей логике operator== проверяет содержит ли)
    EXPECT_TRUE(s1 != s3);
    EXPECT_FALSE(s1 == s3);

    // Проверка булеана
    Set<Set<int>> pset = s1.powerSet();
    // Для множества из 2 элементов мощность булеана равна 2^2 = 4
    EXPECT_EQ(pset.cardinality(), 4);
}

TEST(SetTest, Streams) {
    Set<std::string> s;

    // Ввод
    std::stringstream in("{apple, banana, apple}");
    in >> s;
    EXPECT_EQ(s.cardinality(), 2);
    EXPECT_TRUE(s.contains("apple"));

    // Вывод
    std::stringstream out;
    out << s;
    EXPECT_TRUE(out.str().find('{') != std::string::npos);
    EXPECT_TRUE(out.str().find('}') != std::string::npos);
}
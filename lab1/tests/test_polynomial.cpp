#include <gtest/gtest.h>
#include "../include/Polynomial.h"
#include <sstream>
#include <stdexcept>
#include <vector>

TEST(PolynomialTest, ConstructorsAndNormalization) {
    Polynomial p1;
    EXPECT_EQ(p1.getDegree(), 0);
    EXPECT_EQ(p1[0], 0.0);

    Polynomial p2({1.0, 2.0, 0.0, 0.0});
    EXPECT_EQ(p2.getDegree(), 1);
    EXPECT_EQ(p2[1], 2.0);

    Polynomial p_empty(std::vector<double>{});
    EXPECT_EQ(p_empty.getDegree(), 0);
}

TEST(PolynomialTest, ElementAccessAndEvaluation) {
    Polynomial p({2.0, 3.0, 1.0});

    EXPECT_EQ(p[0], 2.0);
    EXPECT_EQ(p[2], 1.0);
    EXPECT_EQ(p[10], 0.0);
    EXPECT_EQ(p[-1], 0.0);

    EXPECT_EQ(p(2.0), 12.0);
}

TEST(PolynomialTest, ArithmeticOperations) {
    Polynomial p1({1.0, 2.0});
    Polynomial p2({3.0, 4.0, 1.0});

    Polynomial sum = p1 + p2;
    EXPECT_EQ(sum[0], 4.0);
    EXPECT_EQ(sum[2], 1.0);

    Polynomial diff = p2 - p1;
    EXPECT_EQ(diff[0], 2.0);
    EXPECT_EQ(diff[1], 2.0);
    EXPECT_EQ(diff[2], 1.0);

    Polynomial prod = p1 * p2;
    EXPECT_EQ(prod[0], 3.0);
    EXPECT_EQ(prod.getDegree(), 3);
}

TEST(PolynomialTest, CompoundAssignments) {
    Polynomial p({1.0, 1.0});
    p += Polynomial({2.0});
    EXPECT_EQ(p[0], 3.0);

    p -= Polynomial({1.0, 1.0});
    EXPECT_EQ(p[0], 2.0);
    EXPECT_EQ(p[1], 0.0);

    p *= Polynomial({0.0, 1.0});
    EXPECT_EQ(p[1], 2.0);
}

TEST(PolynomialTest, Division) {
    Polynomial dividend({-1.0, 0.0, 1.0});
    Polynomial divisor({-1.0, 1.0});

    Polynomial quotient = dividend / divisor;
    EXPECT_EQ(quotient.getDegree(), 1);
    EXPECT_EQ(quotient[0], 1.0);
    EXPECT_EQ(quotient[1], 1.0);

    Polynomial zero_quot = divisor / dividend;
    EXPECT_EQ(zero_quot.getDegree(), 0);

    Polynomial p_div = dividend;
    p_div /= divisor;
    EXPECT_EQ(p_div[1], 1.0);

    Polynomial zero;
    EXPECT_THROW(dividend / zero, std::invalid_argument);
}

TEST(PolynomialTest, EqualityAndStreams) {
    Polynomial p1({1.0, 2.0});
    Polynomial p2({1.0, 2.0});
    Polynomial p3({1.0, 3.0});

    EXPECT_TRUE(p1 == p2);
    EXPECT_TRUE(p1 != p3);

    std::stringstream out;
    out << p1;
    EXPECT_FALSE(out.str().empty());

    std::stringstream in("1 5.0 6.0");
    Polynomial p_in;
    std::streambuf* orig = std::cout.rdbuf();
    std::cout.rdbuf(nullptr);
    in >> p_in;
    std::cout.rdbuf(orig);

    EXPECT_EQ(p_in.getDegree(), 1);
    EXPECT_EQ(p_in[0], 5.0);
    EXPECT_EQ(p_in[1], 6.0);
}
#include <gtest/gtest.h>
#include "../include/Set.h"
#include <sstream>
#include <string>

TEST(SetTest, BasicOperations) {
    Set<int> s;
    EXPECT_TRUE(s.isEmpty());
    EXPECT_EQ(s.cardinality(), 0);

    s.add(10);
    s.add(20);
    s.add(10);

    EXPECT_FALSE(s.isEmpty());
    EXPECT_EQ(s.cardinality(), 2);
    EXPECT_TRUE(s.contains(10));
    EXPECT_FALSE(s.contains(30));

    s.remove(10);
    EXPECT_FALSE(s.contains(10));

    s.remove(999);
}

TEST(SetTest, ArithmeticOperations) {
    Set<int> s1, s2;
    s1.add(1); s1.add(2);
    s2.add(2); s2.add(3);

    Set<int> s_union = s1 + s2;
    EXPECT_EQ(s_union.cardinality(), 3);
    EXPECT_TRUE(s_union.contains(3));

    Set<int> s_intersect = s1 * s2;
    EXPECT_EQ(s_intersect.cardinality(), 1);
    EXPECT_TRUE(s_intersect.contains(2));

    Set<int> s_diff = s1 - s2;
    EXPECT_EQ(s_diff.cardinality(), 1);
    EXPECT_TRUE(s_diff.contains(1));

    s1 += s2;
    EXPECT_EQ(s1.cardinality(), 3);

    s1 *= Set<int>();
    EXPECT_TRUE(s1.isEmpty());
}

TEST(SetTest, EqualityAndPowerSet) {
    Set<int> s1, s2, s3;
    s1.add(1); s1.add(2);
    s2.add(2); s2.add(1);
    s3.add(1);

    EXPECT_TRUE(s1 == s2);
    EXPECT_TRUE(s1 != s3);
    EXPECT_FALSE(s1 == s3);

    Set<Set<int>> pset = s1.powerSet();
    EXPECT_EQ(pset.cardinality(), 4);
}

TEST(SetTest, Streams) {
    Set<std::string> s;

    std::stringstream in("{apple, banana, apple}");
    in >> s;
    EXPECT_EQ(s.cardinality(), 2);
    EXPECT_TRUE(s.contains("apple"));

    std::stringstream out;
    out << s;
    EXPECT_TRUE(out.str().find('{') != std::string::npos);
    EXPECT_TRUE(out.str().find('}') != std::string::npos);
}
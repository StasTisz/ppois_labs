#pragma once
#include <vector>
#include <string>
#include <sstream>
#include <type_traits>
#include <iostream>

template <typename T>
class Set {
private:
    std::vector<T> elements;

    void parseAndAddToken(std::string s) {
        size_t first = s.find_first_not_of(" \t");
        size_t last = s.find_last_not_of(" \t");
        if (first == std::string::npos) return;
        s = s.substr(first, last - first + 1);

        T value;
        if constexpr (std::is_same_v<T, std::string>) {
            value = s;
        } else {
            std::stringstream ss(s);
            ss >> value;
        }
        add(value);
    }

public:
    Set() {}

    bool contains(T value) const {
        for (int i = 0; i < elements.size(); i++) {
            if (elements[i] == value) return true;
        }
        return false;
    }

    void add(T element) {
        if (!contains(element)) {
            elements.push_back(element);
        }
    }

    void remove(T element) {
        for (int i = 0; i < elements.size(); i++) {
            if (elements[i] == element) {
                elements.erase(elements.begin() + i);
                return;
            }
        }
    }

    Set<T> operator+(const Set<T>& other) const {
        Set<T> result;
        for (int i = 0; i < elements.size(); i++) result.add(elements[i]);
        for (int i = 0; i < other.elements.size(); i++) result.add(other.elements[i]);
        return result;
    }

    Set<T>& operator+=(const Set<T>& other) {
        *this = *this + other;
        return *this;
    }

    Set<T> operator*(const Set<T>& other) const {
        Set<T> result;
        for (int i = 0; i < elements.size(); i++) {
            for (int j = 0; j < other.elements.size(); j++) {
                if (elements[i] == other.elements[j]) result.add(elements[i]);
            }
        }
        return result;
    }

    Set<T>& operator*=(const Set<T>& other) {
        *this = *this * other;
        return *this;
    }

    Set<T> operator-(const Set<T>& other) const {
        Set<T> result;
        for (int i = 0; i < elements.size(); i++) {
            if (!other.contains(elements[i])) result.add(elements[i]);
        }
        return result;
    }

    Set<T>& operator-=(const Set<T>& other) {
        *this = *this - other;
        return *this;
    }

    bool operator==(const Set<T>& other) const {
        if (elements.size() != other.elements.size()) return false;
        for (int i = 0; i < elements.size(); i++) {
            if (!other.contains(elements[i])) return false;
        }
        return true;
    }

    bool operator!=(const Set<T>& other) const {
        return !(*this == other);
    }

    int cardinality() const {
        return elements.size();
    }

    bool isEmpty() const {
        return elements.empty();
    }

    // Построение булеана
    Set<Set<T>> powerSet() const {
        std::vector<Set<T>> subsets;
        // Начинается с одного пустого подмножества
        subsets.push_back(Set<T>());

        // По очереди перебираются каждый элемент множества
        for (int i = 0; i < elements.size(); i++) {
            int current_size = subsets.size();
            for (int j = 0; j < current_size; j++) {
                Set<T> new_subset = subsets[j];
                new_subset.add(elements[i]);
                subsets.push_back(new_subset);
            }
        }

        Set<Set<T>> result;
        for (int i = 0; i < subsets.size(); i++) {
            result.add(subsets[i]);
        }

        return result;
    }

    friend std::ostream& operator<<(std::ostream& os, const Set<T>& set) {
        os << "{";
        for (int i = 0; i < set.elements.size(); i++) {
            os << set.elements[i];
            if (i < set.elements.size() - 1) os << ", ";
        }
        os << "}";
        return os;
    }

    friend std::istream& operator>>(std::istream& is, Set<T>& set) {
        std::string line;
        std::getline(is >> std::ws, line);

        size_t start = line.find('{');
        size_t end = line.find_last_of('}');

        if (start == std::string::npos || end == std::string::npos || end <= start) {
            return is;
        }

        std::string inner = line.substr(start + 1, end - start - 1);
        int brace_count = 0;
        std::string token = "";

        for (char c : inner) {
            if (c == '{') brace_count++;
            else if (c == '}') brace_count--;

            if (c == ',' && brace_count == 0) {
                set.parseAndAddToken(token);
                token = "";
            } else {
                token += c;
            }
        }
        set.parseAndAddToken(token);
        return is;
    }
};
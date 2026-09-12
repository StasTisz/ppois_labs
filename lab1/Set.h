#pragma once
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include <type_traits>

template <typename T>
class Set {
private:
    std::vector<T> elements;

    // Вспомогательный метод: чистит токен и добавляет в множество
    void parseAndAddToken(std::string s) {
        size_t first = s.find_first_not_of(" \t"); // первый и последний индекс строки
        size_t last = s.find_last_not_of(" \t");
        if (first == std::string::npos) return;      // проверка на пустоту
        s = s.substr(first, last - first + 1); // чистая строка без внешних пробелов и \t

        T value;
        if constexpr (std::is_same_v<T, std::string>) { // проверка на этапе компиляции на соответствие типа
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

    Set<T> operator&(const Set<T>& other) const {
        Set<T> result;
        for (int i = 0; i < elements.size(); i++) {
            for (int j = 0; j < other.elements.size(); j++) {
                if (elements[i] == other.elements[j]) result.add(elements[i]);
            }
        }
        return result;
    }

    Set<T> operator-(const Set<T>& other) const {
        Set<T> result;
        for (int i = 0; i < elements.size(); i++) {
            if (!other.contains(elements[i])) result.add(elements[i]);
        }
        return result;
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

        // очистка потока ввода и чтение
        std::getline(is >> std::ws, line);

        size_t start = line.find('{');
        size_t end = line.find_last_of('}');

        if (start == std::string::npos || end == std::string::npos || end <= start) {
            return is;
        }

        // вырезание строки
        std::string inner = line.substr(start + 1, end - start - 1);

        int brace_count = 0;   // глубина вложенности
        std::string token = ""; // Буфер для накопления символов текущего элемента

        // Посимвольный проход по всей внутренней строке
        for (char c : inner) {
            if (c == '{') brace_count++;       // Вошли во вложенное подмножество — увеличили глубину
            else if (c == '}') brace_count--;  // Вышли — уменьшили глубину

            // режем по запятой ТОЛЬКО если мы на нулевом уровне вложенности
            if (c == ',' && brace_count == 0) {
                set.parseAndAddToken(token); // Отправляем накопленный сырой элемент на очистку и добавление
                token = "";                  // Сбрасываем буфер для следующего элемента
            } else {
                token += c; 
            }
        }

        // После последней запятой цикл завершится, но в token останется последний элемент
        set.parseAndAddToken(token);

        return is;
    }
};
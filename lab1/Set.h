/**
 * @file Set.h
 * @brief Заголовочный файл с реализацией шаблонного класса Set, представляющего Канторовское множество.
 */

#pragma once
#include <vector>
#include <string>
#include <sstream>
#include <type_traits>
#include <iostream>

/**
 * @class Set
 * @brief Шаблонный класс для работы с математическими множествами.
 *
 * Гарантирует уникальность хранимых элементов. Поддерживает операции
 * объединения, пересечения, разности и построения булеана.
 * @tparam T Тип элементов, хранящихся в множестве.
 */
template <typename T>
class Set {
private:
    std::vector<T> elements;

    /**
     * @brief Вспомогательный метод для парсинга строковых токенов при вводе множества.
     * @param s Строковый токен для добавления.
     */
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
    /**
     * @brief Конструктор по умолчанию. Создает пустое множество.
     */
    Set() {}

    /**
     * @brief Проверяет наличие элемента в множестве.
     * @param value Искомый элемент.
     * @return true, если элемент присутствует, иначе false.
     */
    bool contains(T value) const {
        for (int i = 0; i < elements.size(); i++) {
            if (elements[i] == value) return true;
        }
        return false;
    }

    /**
     * @brief Добавляет новый элемент в множество.
     * Если элемент уже существует, добавление игнорируется.
     * @param element Элемент для добавления.
     */
    void add(T element) {
        if (!contains(element)) {
            elements.push_back(element);
        }
    }

    /**
     * @brief Удаляет элемент из множества.
     * @param element Элемент для удаления.
     */
    void remove(T element) {
        for (int i = 0; i < elements.size(); i++) {
            if (elements[i] == element) {
                elements.erase(elements.begin() + i);
                return;
            }
        }
    }

    /**
     * @brief Оператор объединения двух множеств (A + B).
     * @param other Второе множество.
     * @return Новое множество, содержащее элементы из обоих множеств без дубликатов.
     */
    Set<T> operator+(const Set<T>& other) const {
        Set<T> result;
        for (int i = 0; i < elements.size(); i++) result.add(elements[i]);
        for (int i = 0; i < other.elements.size(); i++) result.add(other.elements[i]);
        return result;
    }

    /**
     * @brief Объединяет текущее множество с другим.
     * @param other Второе множество.
     * @return Ссылка на текущее измененное множество.
     */
    Set<T>& operator+=(const Set<T>& other) {
        *this = *this + other;
        return *this;
    }

    /**
     * @brief Оператор пересечения двух множеств (A * B).
     * @param other Второе множество.
     * @return Новое множество, содержащее только общие элементы.
     */
    Set<T> operator*(const Set<T>& other) const {
        Set<T> result;
        for (int i = 0; i < elements.size(); i++) {
            for (int j = 0; j < other.elements.size(); j++) {
                if (elements[i] == other.elements[j]) result.add(elements[i]);
            }
        }
        return result;
    }

    /**
     * @brief Пересекает текущее множество с другим.
     * @param other Второе множество.
     * @return Ссылка на текущее измененное множество.
     */
    Set<T>& operator*=(const Set<T>& other) {
        *this = *this * other;
        return *this;
    }

    /**
     * @brief Оператор разности двух множеств (A - B).
     * @param other Множество вычитаемых элементов.
     * @return Новое множество с элементами A, которых нет в B.
     */
    Set<T> operator-(const Set<T>& other) const {
        Set<T> result;
        for (int i = 0; i < elements.size(); i++) {
            if (!other.contains(elements[i])) result.add(elements[i]);
        }
        return result;
    }

    /**
     * @brief Вычитает элементы другого множества из текущего.
     * @param other Множество вычитаемых элементов.
     * @return Ссылка на текущее измененное множество.
     */
    Set<T>& operator-=(const Set<T>& other) {
        *this = *this - other;
        return *this;
    }

    /**
     * @brief Проверяет два множества на равенство (совпадение элементов).
     * @param other Второе множество.
     * @return true, если мощности равны и все элементы совпадают.
     */
    bool operator==(const Set<T>& other) const {
        if (elements.size() != other.elements.size()) return false;
        for (int i = 0; i < elements.size(); i++) {
            if (!other.contains(elements[i])) return false;
        }
        return true;
    }

    /**
     * @brief Проверяет два множества на неравенство.
     * @param other Второе множество.
     * @return true, если множества не равны.
     */
    bool operator!=(const Set<T>& other) const {
        return !(*this == other);
    }

    /**
     * @brief Возвращает мощность множества.
     * @return Количество элементов в множестве.
     */
    int cardinality() const {
        return elements.size();
    }

    /**
     * @brief Проверяет множество на пустоту.
     * @return true, если множество не содержит элементов.
     */
    bool isEmpty() const {
        return elements.empty();
    }

    /**
     * @brief Строит булеан (множество всех подмножеств) для текущего множества.
     * @return Множество, содержащее множества-подмножества типа Set<Set<T>>.
     */
    Set<Set<T>> powerSet() const {
        std::vector<Set<T>> subsets;
        subsets.push_back(Set<T>());

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

    /**
     * @brief Выводит множество в выходной поток в формате {a, b, c}.
     * @param os Выходной поток.
     * @param set Множество для вывода.
     * @return Ссылка на выходной поток.
     */
    friend std::ostream& operator<<(std::ostream& os, const Set<T>& set) {
        os << "{";
        for (int i = 0; i < set.elements.size(); i++) {
            os << set.elements[i];
            if (i < set.elements.size() - 1) os << ", ";
        }
        os << "}";
        return os;
    }

    /**
     * @brief Считывает множество из входного потока.
     * Ожидает формат ввода, заключенный в фигурные скобки: {a, b, c}.
     * @param is Входной поток.
     * @param set Множество, в которое добавятся элементы.
     * @return Ссылка на входной поток.
     */
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
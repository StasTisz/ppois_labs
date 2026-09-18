#include <iostream>
#include <string>
#include "Set.h"
#include "Polynomial.h"

using namespace std;

void runSetDemo() {
    Set<string> setA;
    Set<string> setB;
    int choice = -1;

    while (choice != 0) {
        cout << "\n=== УПРАВЛЕНИЕ МНОЖЕСТВАМИ ===\n"
             << "1. Задать множество A (формат {a, b, {c}})\n"
             << "2. Задать множество B (формат {a, b, {c}})\n"
             << "3. Показать множества A и B\n"
             << "4. Объединить (A + B)\n"
             << "5. Пересечь (A * B)\n" // ВНИМАНИЕ: ЗАМЕНЕНО НА * ПО ТРЕБОВАНИЮ 1.4
             << "6. Разность (A - B)\n"
             << "7. Проверить на равенство (A == B)\n"
             << "8. Добавить элемент в множество A\n"
             << "9. Мощность множества А\n"
             << "10. Построить булеан множества A\n"
             << "0. Выход в главное меню\n"
             << "Выберите действие: ";
        cin >> choice;

        switch (choice) {
            case 1: cout << "Введите множество A:\n"; cin >> setA; break;
            case 2: cout << "Введите множество B:\n"; cin >> setB; break;
            case 3: cout << "A: " << setA << "\nB: " << setB << "\n"; break;
            case 4: cout << "A + B = " << (setA + setB) << "\n"; break;
            case 5: cout << "A * B = " << (setA * setB) << "\n"; break;
            case 6: cout << "A - B = " << (setA - setB) << "\n"; break;
            case 7: cout << (setA == setB ? "Равны\n" : "Не равны\n"); break;
            case 8: {
                string val;
                cout << "Введите значение: ";
                cin >> val;
                setA.add(val);
                break;
            }
            case 9: cout << "|A| = " << setA.cardinality() << endl; break;
            case 10: {
                Set<Set<string>> boolean_A = setA.powerSet();
                cout << "Булеан множества A: " << boolean_A << "\n";
                cout << "Мощность булеана: " << boolean_A.cardinality() << "\n";
                break;
            }
            case 0: break;
            default: cout << "Неверный пункт!\n"; break;
        }
    }
}

void runPolyDemo() {
    Polynomial pA;
    Polynomial pB;
    int choice = -1;

    while (choice != 0) {
        cout << "\n=== УПРАВЛЕНИЕ МНОГОЧЛЕНАМИ ===\n"
             << "1. Задать многочлен A\n"
             << "2. Задать многочлен B\n"
             << "3. Показать многочлены A и B\n"
             << "4. Сложить (A + B)\n"
             << "5. Вычесть (A - B)\n"
             << "6. Умножить (A * B)\n"
             << "7. Разделить (A / B)\n"
             << "8. Вычислить значение A(x)\n"
             << "0. Выход в главное меню\n"
             << "Выберите действие: ";
        cin >> choice;

        switch (choice) {
            case 1: cin >> pA; break;
            case 2: cin >> pB; break;
            case 3: cout << "A(x) = " << pA << "\nB(x) = " << pB << "\n"; break;
            case 4: cout << "A + B = " << (pA + pB) << "\n"; break;
            case 5: cout << "A - B = " << (pA - pB) << "\n"; break;
            case 6: cout << "A * B = " << (pA * pB) << "\n"; break;
            case 7:
                try {
                    cout << "A / B = " << (pA / pB) << "\n";
                } catch (const exception& e) {
                    cout << e.what() << "\n";
                }
                break;
            case 8: {
                double x;
                cout << "Введите x: ";
                cin >> x;
                cout << "A(" << x << ") = " << pA(x) << "\n";
                break;
            }
            case 0: break;
            default: cout << "Неверный пункт!\n"; break;
        }
    }
}

int main() {
    int mainChoice = -1;
    while (mainChoice != 0) {
        cout << "\n========== ГЛАВНОЕ МЕНЮ ==========\n"
             << "1. Работа с Канторовскими множествами\n"
             << "2. Работа с Многочленами\n"
             << "0. Выход из программы\n"
             << "Выберите предметную область: ";
        cin >> mainChoice;

        if (mainChoice == 1) {
            runSetDemo();
        } else if (mainChoice == 2) {
            runPolyDemo();
        }
    }
    cout << "Завершение работы.\n";
    return 0;
}
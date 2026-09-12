#include <iostream>
#include <string>
#include "Set.h"

using namespace std;

void showMenu() {
    cout << "\n=== УПРАВЛЕНИЕ МНОЖЕСТВАМИ ===\n"
         << "1. Задать множество A (ввод Канторовского множества)\n"
         << "2. Задать множество B (ввод Канторовского множества)\n"
         << "3. Показать множества A и B\n"
         << "4. Объединить (A + B)\n"
         << "5. Пересечь (A & B)\n"
         << "6. Разность (A - B)\n"
         << "7. Проверить на равенство (A == B)\n"
         << "8. Добавить элемент в множество A\n"
         << "9. Мощность множества А\n"
         << "10. Мощность множества B\n"
         << "0. Выход\n"
         << "Выберите действие: ";
}

int main() {
    Set<string> setA;
    Set<string> setB;
    int choice = -1;

    while (choice != 0) {
        showMenu();
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Введите множество в формате {a, b, {c, d}}:\n";
                cin >> setA;
                break;
            case 2:
                cout << "Введите множество в формате {a, b, {c, d}}:\n";
                cin >> setB;
                break;
            case 3:
                cout << "Множество A: " << setA << "\n";
                cout << "Множество B: " << setB << "\n";
                break;
            case 4: {
                Set<string> res = setA + setB;
                cout << "A + B = " << res << "\n";
                break;
            }
            case 5: {
                Set<string> res = setA & setB;
                cout << "A & B = " << res << "\n";
                break;
            }
            case 6: {
                Set<string> res = setA - setB;
                cout << "A - B = " << res << "\n";
                break;
            }
            case 7:
                if (setA == setB) cout << "Множества равны.\n";
                else cout << "Множества не равны.\n";
                break;
            case 8: {
                string val;
                cout << "Введите значение: ";
                cin >> val;
                setA.add(val);
                break;
            }
            case 9:
                cout << "|A| = " << setA.cardinality() << endl;
                break;
            case 10:
                cout << "|B| = " << setB.cardinality() << endl;
                break;
            case 0:
                cout << "Завершение программы.\n";
                break;
            default:
                cout << "Неверный пункт меню, попробуйте снова.\n";
                break;
        }
    }
    return 0;
}
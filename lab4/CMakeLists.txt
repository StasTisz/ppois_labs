cmake_minimum_required(VERSION 3.14)
project(ppois_lab4)

# Включаем современный стандарт C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 1. Основной исполняемый файл (Консольное меню)
add_executable(lab4_run main.cpp)

# 2. Автоматическое скачивание и подключение Google Test
include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
# Отключаем предупреждения и переопределение настроек компилятора от GTest
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# 3. Исполняемый файл для unit-тестов
add_executable(lab4_test tests.cpp)
target_link_libraries(lab4_test GTest::gtest_main)

# Включаем обнаружение тестов для панели тестирования в CLion
include(GoogleTest)
gtest_discover_tests(lab4_test)
cmake_minimum_required(VERSION 3.20)
project(ppois_lab1)

set(CMAKE_CXX_STANDARD 17)

# Основная программа с меню (Переименовано в lab1_app)
add_executable(lab1_app
        app/main.cpp
        src/Polynomial.cpp
)

target_include_directories(lab1_app PRIVATE include)

# Автоматическое скачивание Google Test
include(FetchContent)
FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG        v1.14.0
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Отдельная программа-тестировщик (Переименовано в lab1_tests)
add_executable(lab1_tests tests/test.cpp src/Polynomial.cpp)

target_link_libraries(lab1_tests gtest_main)

# Интеграция со встроенным окном тестов CLion
include(GoogleTest)
gtest_discover_tests(lab1_tests)
cmake_minimum_required(VERSION 3.20)
project(ppois_lab1)

set(CMAKE_CXX_STANDARD 17)

# Основная программа с меню
add_executable(ppois_lab1 main.cpp Polynomial.cpp)

# Автоматическое скачивание Google Test
include(FetchContent)
FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG        v1.14.0
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Отдельная программа-тестировщик
add_executable(run_tests test.cpp Polynomial.cpp)

target_link_libraries(run_tests gtest_main)

# Интеграция со встроенным окном тестов CLion
include(GoogleTest)
gtest_discover_tests(run_tests)
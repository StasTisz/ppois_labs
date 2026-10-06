cmake_minimum_required(VERSION 3.20)
project(ppois_lab4 CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

# Исполняемый файл CLI
add_executable(lab4_app
        src/main.cpp
)

# Модульные тесты Google Test
enable_testing()

include(FetchContent)
FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG        v1.15.2
)
# Предотвращает конфликт настроек рантайма на Windows
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(lab4_tests
        tests/test_sortings.cpp
        tests/test_graph.cpp
)

target_link_libraries(lab4_tests PRIVATE GTest::gtest GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(lab4_tests)
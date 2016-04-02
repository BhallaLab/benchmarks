cmake_minimum_required(VERSION 2.8)

find_package( GSL REQUIRED)
include_directories( ${GSL_INCLUDE_DIR} )
add_definitions( -std=c++11 )
add_executable( benchmark_rng 
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
    )

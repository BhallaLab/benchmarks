cmake_minimum_required(VERSION 2.8)

option(WITH_MPI "Enable OpenMPI" ON)
option(WITH_OPENMP "Enable OpenMPI" ON)
option(WITH_GSL "Use gsl RNG" OFF)
option(WITH_BOOST "Use boost RNG" OFF)

set(CMAKE_BUILD_TYPE Release)

add_definitions( -std=c++11 )

add_executable( benchmark_rng_mpi 
    ${CMAKE_CURRENT_SOURCE_DIR}/main_mpi.cpp
    )

add_executable( benchmark_rng_openmp 
    ${CMAKE_CURRENT_SOURCE_DIR}/main_openmp.cpp
    )

if(WITH_GSL)
    find_package( GSL REQUIRED )
    include_directories( ${GSL_INCLUDE_DIR} )
    target_link_libraries( benchmark_rng_mpi ${GSL_LIBRARIES} )
    target_link_libraries( benchmark_rng_openmp ${GSL_LIBRARIES} )
    add_definitions( -DUSE_GSL )
endif(WITH_GSL)


if(WITH_MPI)
    find_package( MPI REQUIRED )
    set_target_properties( benchmark_rng_mpi PROPERTIES 
        COMPILE_FLAGS "${MPI_CXX_COMPILE_FLAGS}"
        INCLUDE_DIRECTORIES "${MPI_CXX_INCLUDE_PATH}"
        LINK_FLAGS ${MPI_CXX_LINK_FLAGS}
        )
    target_link_libraries( benchmark_rng_mpi ${MPI_CXX_LIBRARIES} )
endif(WITH_MPI)

if(WITH_OPENMP)
    find_package(OpenMP REQUIRED)
    set_target_properties( benchmark_rng_openmp PROPERTIES 
        COMPILE_FLAGS "${OpenMP_CXX_FLAGS}"
        LINK_FLAGS "${OpenMP_CXX_FLAGS}" 
        )
endif()

FILE(GLOB LATEX_SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.tex)

add_custom_target( docs 
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/report.pdf
    SOURCES ${LATEX_SRCS}
    )

add_custom_command( 
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/report.pdf
    COMMAND xelatex -output-directory=${CMAKE_CURRENT_BINARY_DIR} 
        ${CMAKE_CURRENT_SOURCE_DIR}/report.tex
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    DEPENDS ${LATEX_SRCS}
    VERBATIM
    )

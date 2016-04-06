cmake_minimum_required(VERSION 2.8)

option(WITH_MPI "Enable OpenMPI" ON)
option(WITH_OPENMP "Enable OpenMPI" ON)
option(WITH_GSL "Use gsl RNG" ON)
option(NUMTHREADS "No of threads to launch" 10)

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
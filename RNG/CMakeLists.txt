cmake_minimum_required(VERSION 2.8)

add_executable( benchmark_rng 
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
    )

option(WITH_MPI "Enable OpenMPI" ON)
option(WITH_GSL "Use gsl RNG" ON)

if(WITH_GSL)
    find_package( GSL REQUIRED )
endif(WITH_GSL)

if(WITH_MPI)
    find_package( MPI REQUIRED )
endif(WITH_MPI)

if(MPI_CXX_FOUND)
    message(STATUS "Using MPI: ${MPI_CXX_COMPILE_FLAGS} ${MPI_CXX_LINK_FLAGS}")
    #set(CMAKE_CXX_COMPILER ${MPI_CXX_COMPILER})
    add_definitions( -DUSE_MPI )
    include_directories( ${MPI_CXX_INCLUDE_PATH} )
    set_target_properties( benchmark_rng 
        PROPERTIES 
        COMPILE_FLAGS "${CMAKE_CXX_COMPILE_FLAGS} -fopenmp"
        LINK_FLAGS "${CMAKE_CXX_LINK_FLAGS} -fopenmp"
        )
endif(MPI_CXX_FOUND)
include_directories( ${GSL_INCLUDE_DIR} )
add_definitions( -std=c++11 )

if(WITH_GSL)
    target_link_libraries( benchmark_rng ${GSL_LIBRARIES} )
endif(WITH_GSL)

if(WITH_MPI)
    target_link_libraries( benchmark_rng ${MPI_LIBRARIES} )
endif(WITH_MPI)

## Add custom command
add_custom_command( TARGET benchmark_rng 
    POST_BUILD 
    COMMAND ${MPIEXEC} ${MPIEXEC_NUMPROC_FLAG} 4 ${MPIEXEC_PREFLAGS} benchmark_rng ${MPIEXEC_POSTFLAGS}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running benchmark"
    VERBATIM 
    )

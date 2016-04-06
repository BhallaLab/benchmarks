In this project, we compare following random number generators with when
multiple instances are launched using MPI.

- boost
- C++11 STL
- GSL
- MOOSE

## Implementation

In `CMakeLists.txt` file, two targets are declared: one for MPI and other for
OpenMP. For both of them, appropriate cpp file is created: `./main_mpi.cpp` and
`./main_openmp.cpp`. CMake builds binaries which can be launched in terminal.

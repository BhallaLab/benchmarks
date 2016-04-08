/***
 *       Filename:  main.cpp
 *
 *    Description:  Benchmark three random number generators with OpenMPI.
 *
 *        Version:  0.0.1
 *        Created:  2016-04-02

 *       Revision:  none
 *
 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 *
 *        License:  GNU GPL2
 */

#include <iostream>
#include <ctime>
#include <chrono>
#include <cmath>

#include <vector>

#ifdef  USE_GSL
#include <gsl/gsl_rng.h>
#else      /* -----  not USE_GSL  ----- */

#endif     /* -----  not USE_GSL  ----- */

#include <mpi.h>

using namespace std;
using namespace std::chrono;


double d_t (struct timespec t1, struct timespec t2)
{
    return (t2.tv_sec-t1.tv_sec)+(double)(t2.tv_nsec-t1.tv_nsec)/1000000000.0;
}

int main(int argc, char *argv[])
{

    MPI_Init( &argc, &argv);
    // Number of processors
    int worldSize;
    MPI_Comm_size( MPI_COMM_WORLD, &worldSize);

    // Rank of process
    int worldRank;
    MPI_Comm_rank( MPI_COMM_WORLD, &worldRank);

    // Get the processor name 
    char processorName[MPI_MAX_PROCESSOR_NAME];
    int nameLen;
    MPI_Get_processor_name( processorName, &nameLen);

    // Print off a hellow world msg.
    printf("Hello from %s rank %d out of total %d\n", processorName, worldRank, worldSize);

    high_resolution_clock::time_point t1 = high_resolution_clock::now();
    high_resolution_clock::time_point t2 = high_resolution_clock::now();

#ifdef  USE_GSL
    gsl_rng* r;
    const gsl_rng_type * T;
    gsl_rng_env_setup(); // b default it assumes mt19937 with seed 0.
    T = gsl_rng_default;
    r = gsl_rng_alloc( T );
    cerr << "RNG " << r << endl;
    gsl_rng_set( r, worldRank );

    cerr << "GSL random number generator: " << gsl_rng_name( r ) << endl;

    // Before doing benchmarking, we generate few numbers to show the user that
    // everything is all right.
    for(int i = 0; i < 5; i ++ )
    {
#if 0
        cerr << "STL=" << rng();
#ifdef MOOSE
        cerr  << ",MOOSE=" << genrand_int32(); 
#endif

#ifdef BOOST 
        cerr << ",BOOST=" << brng();
#endif
#endif
        printf("\nGSL=(%d) %d", worldRank, gsl_rng_get( r ));
#if 0
        cerr << ",TNMM=" << tnmm::genrand_int32() << endl;
#endif
    }


#if 0
    for( unsigned int i = 0; i < 9 ; i ++ )
    {
        size_t  N = pow(10, i);
        vector<int> store(N);

        //dataF << SETW << N;
        double baselineT = 0.0;

        cout << "N = " << N << endl;

        cout  << "\tBaseline (vector storage time) ";
        t1 = chrono::high_resolution_clock::now();
        for(size_t i = 0; i < N; i ++)
            store[i] = 1222; // just store some number.
        t2 = chrono::high_resolution_clock::now();
        baselineT = duration_cast<duration<double>>(t2 - t1 ).count();
        cout << "  ends. Time " << baselineT << endl;

#if 0
        // Using c++ library
        cout << "\tSTL starts .. ";
        t1 = high_resolution_clock::now();
        for( unsigned int i = 0; i < N; ++i )
            store[i] = rng();
        t2 = high_resolution_clock::now();

        // Get at least some numbers generated for sanity test.
        print_array( store, 10);

        double stlT = duration_cast<duration<double> >(t2 - t1).count();
        cout << " ends. Time " << stlT - baselineT << endl;
        dataF << "," << stlT - baselineT;

#ifdef MOOSE
        cout << "\tMOOSE start.. ";
        t1 = chrono::high_resolution_clock::now();
        for( size_t i = 0; i < N; ++i )
            store[i] = mtrand();
        t2 = chrono::high_resolution_clock::now();

        // Get at least some numbers generated for sanity test.
        print_array( store, 10);
        double mooseT = duration_cast<duration<double>>(t2 - t1 ).count();
        cout << "  ends. Time " << mooseT - baselineT << endl;
        dataF << "," << mooseT - baselineT;
        dataF << "," << 1.0 / (mooseT - baselineT) * (stlT - baselineT);
#endif

#ifdef BOOST
        t1 = high_resolution_clock::now();
        cout << "\tBOOST starts ..";
        for( size_t i = 0; i < N; ++i )
            store[i] = brng();
        t2 = high_resolution_clock::now();

        // Get at least some numbers generated for sanity test.
        print_array( store, 10);

        double boostT = duration_cast<duration<double> >(t2 - t1).count();
        cout << "  ends. Time " <<  boostT - baselineT << endl;
        dataF << "," << boostT - baselineT;
        dataF << "," << 1 / (boostT - baselineT) * (stlT - baselineT);
#endif
#endif

        t1 = high_resolution_clock::now();
        printf("\tGSL starts ..");
        for( unsigned int i =0; i < N; ++i)
            store[i] = gsl_rng_get( r );
        t2 = high_resolution_clock::now();

        double gslT = duration_cast<duration<double> >(t2 - t1).count();
        cout << "  ends. Time " <<  gslT - baselineT << endl;
        //cout << "," << gslT - baselineT;
        //cout << "," << 1.0 / (gslT - baselineT) * (stlT - baselineT);

#if 0
        t1 = high_resolution_clock::now();
        cout << "\t TNMM starts ..";
        for( unsigned int i =0; i < N; ++i)
            store[i] = tnmm::genrand_int32( );
        t2 = high_resolution_clock::now();

        print_array(store, 10);

        double tnmmT = duration_cast<duration<double> >(t2 - t1).count();
        cout << "  ends. Time " << tnmmT - baselineT << endl;
        dataF << "," << tnmmT - baselineT;
        dataF << "," << 1/(tnmmT - baselineT) * (stlT - baselineT);
        dataF << endl;
#endif

    }
#endif

    // Now let's time the GSL performance.

    double a, b;
    int i,j,k;
    MPI_Finalize();
    return 0;
#else      /* -----  not USE_GSL  ----- */

#endif     /* -----  not USE_GSL  ----- */

#if 0

        struct timespec t1, t2, t3, t4;

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t1);

    //initialize gsl random number generator
    const gsl_rng_type *rng_t;
    gsl_rng **rng;
    gsl_rng_env_setup();
    rng_t = gsl_rng_default;

    rng = (gsl_rng **) malloc(nt * sizeof(gsl_rng *));

#pragma omp parallel for num_threads(nt)
    for(i=0;i<nt;i++)
    {
        rng[i] = gsl_rng_alloc (rng_t);
        gsl_rng_set(rng[i],seed*i);
    }

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t2);

    for (i=0;i<n;i++)
    {
        a = gsl_rng_uniform(rng[0]);
    }

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t3);

    omp_set_num_threads(nt);
#pragma omp parallel private(j,a)
    {
        j = omp_get_thread_num();
#pragma omp for
        for(i=0;i<n;i++){
            a = gsl_rng_uniform(rng[j]);
        }
    }

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t4);

    printf("\n\ninitializing:\t\tt1 = %f seconds", d_t(t1,t2));
    printf("\nsequencial for loop:\tt2 = %f seconds", d_t(t2,t3));
    printf("\nparalel for loop:\tt3 = %f seconds (%f * t2)", d_t(t3,t4), (double)d_t(t3,t4)/(double)d_t(t2,t3));
    printf("\nnumber of threads:\tnt = %d\n", nt);

    //free random number generator
    for (i=0;i<nt;i++)
        gsl_rng_free(rng[i]);
    free(rng);

    return 0;
#endif 
}

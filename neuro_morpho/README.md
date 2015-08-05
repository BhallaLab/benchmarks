1. Run nrnivmodl to compile the channels.

2. Run ./run_benchmark.sh to generate the benchmarks. You can pass the number of
   models for which benchmark needs to be run. DEFAULT=ALL.

3. Run ./plot_benchmark.py to generate a plot out of sqlite database generated
   in step 2. This plot show model on x-axis, and on y-axis comparison of
   different simulator.

4. Run ./plot_benchmark_runtime_vs_compt.py to generate csv file from data.
   These files can be compared in Excel or OpenOffice.

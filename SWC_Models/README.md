1. Run nrnivmodl to compile the channels.

2. Run ./run_benchmark.sh to generate the benchmarks. You can pass the number of
   models for which benchmark needs to be run. DEFAULT=ALL.

3. Run ./plot_benchmark.py to generate a plot out of sqlite database generated
   in step 2. This plot show model on x-axis, and on y-axis comparison of
   different simulator.

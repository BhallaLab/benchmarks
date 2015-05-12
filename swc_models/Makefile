all : moose neuron compare
	echo "All done"


moose : loader_moose.py 
	./test_moose.sh 

neuron : loader_neuron.py
	./test_nrn.sh 

compare : 
	echo "Plotting differences"
	./plot_gnuplot.sh _data/*.csv

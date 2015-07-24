DATAFILE:=../../swc_models/wu/CNG_version/ko20x-07.CNG.swc
HOCFILE:=$(shell basename $(DATAFILE).hoc)
PYSCRIPT:= ./check_equivalence.py

all : $(DATAFILE) $(PYSCRIPT) compare

$(HOCFILE) : $(DATAFILE) $(PYSCRIPT) ./moose_to_neuron.py
	python $(PYSCRIPT) $< 

compare :  $(HOCFILE) 
	nrniv  $(HOCFILE)
	./xplot.py -i ./nrn_out.dat -o nrnout.png -t "NRN"
	./xplot.py -i ./moose_results.csv -o moose_results.png -t "MOOSE"
	

SWCFILE= ../../swc_models/wu/CNG_version/ko20x-07.CNG.swc
MOOSEOUT=moose_results.csv
HOCOUT=$(shell basename $(SWCFILE)).hoc
NRNOUT=nrn_out.dat
PYSCRIPTS= ./check_equivalence.py ./loader_moose.py ./moose_to_neuron.py

all: $(MOOSEOUT) $(NRNOUT)

$(HOCOUT) $(MOOSEOUT) : $(SWCFILE) $(PYSCRIPTS)
	./check_equivalence.py $(SWCFILE)

$(NRNOUT) : $(MOOSEOUT) 
	nrnivmodl chans
	nrniv $(HOCOUT)

plot : $(MOOSEOUT) $(NRNOUT)
	./xplot.py -i $(MOOSEOUT) -o moose_results.png
	./xplot.py -i $(NRNOUT) -o nrn_out.png

somaplot : $(MOOSEOUT) $(NRNOUT)
	./csv_extract_columns.py -in $(MOOSEOUT) -c time -c "some\[0\]" -out moose_soma.csv
	./csv_extract_columns.py -in $(NRNOUT) -c time -c ".*table_soma$" -out moose_soma.csv
	./xplot.py -i moose_soma.csv nrn_soma.csv -m ./modifiers.txt

clean:
	git clean -fxd


.PHONY : clean

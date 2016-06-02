SAMPLES = 500.h

all: default

default:
	echo CS 229 Project H Teo, Y Wang, J Zhu

data:
	python3.5 generate_data.py 400

count:
	python3.5 how_many_points.py

%.train_st: %.hssample
	python3 train_models.py st_fs_resource_$@ $<
	python3 train_models.py st_fs_neural_$@ $<
	python3 train_models.py st_fs_deep_neural_$@ $<
	echo Done > $@

%.hssample:
	echo Training

%.test: %.train_st
	python3 agent_test.py st_fs_resource_$<
	python3 agent_test.py st_fs_neural_$<
	python3 agent_test.py st_fs_deep_neural_$<

test: $(SAMPLES:%.h=%.test)
	echo Done

train: $(SAMPLES:%.h=%.train_st)#, $(SAMPLES:%.h=%.train_ql)
	echo Done

sample: data.hsdat
	python3.5 sample_data.py -d 500 #25
	python3.5 sample_data.py -d 1000 #50
	python3.5 sample_data.py -d 2000 #100
	python3.5 sample_data.py -d 4000 #200
	python3.5 sample_data.py -d 8000 #400
	python3.5 sample_data.py -d 12000 #
	python3.5 sample_data.py -d 16000
	python3.5 sample_data.py -d 20000
	python3.5 sample_data.py -d 25000
	python3.5 sample_data.py -d 30000
	python3.5 sample_data.py -d 40000


clean:
	rm -f *.hssample $(SAMPLES:%.h=%.train_st)

.PHONY: all default generate_data clean count sample train test
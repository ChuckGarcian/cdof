TEST ?= memchase_test
SAMPLE_N ?= 20
test_args ?= 12
default: build

# Build test
build:
	gcc $(TEST).c -o $(TEST).o -g -O0

# Dry Run 
run: build
	./$(TEST).o $(test_args)

cwd = $(shell pwd)

# Run cdof
cdof: build
	sudo docker run --rm -v $(cwd):/tmp/work grammatech/ddisasm ddisasm /tmp/work/$(TEST).o --ir /tmp/work/$(TEST).gtirb
	sudo docker run --rm -v $(cwd):/tmp/work grammatech/ddisasm gtirb-pprinter /tmp/work/$(TEST).gtirb --asm /tmp/work/$(TEST).s	
	cdof $(TEST)_runs.txt $(TEST).s

# Measure Before Optimization
measure_nop:
	perf stat -e cache-references,cache-misses,LLC-loads,LLC-load-misses ./$(TEST).o $(test_args)

# Measure After Optimization
measure_op:
	perf stat  -e cache-references,cache-misses,LLC-loads,LLC-load-misses ./$(TEST).owith_prefetch $(test_args)

measure: 
	python3 average.py $(TEST) $(TEST)_experiments.csv $(SAMPLE_N)

graph: 
	python3 graph.py $(TEST)

clean:
	rm -rf $(TEST).o $(TEST).owith_prefetch $(TEST).swith_prefetch.s $(TEST).s $(TEST).gtirb output.txt 

clean_measure:
	rm -rf ./*_measurements

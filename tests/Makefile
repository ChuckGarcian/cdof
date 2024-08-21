# Directories
BENCHMARK := benchmark_scripts
EXPERIMENT := experiment_csv
WP := workload_profiles
BIN := _bin

# Arguments
TEST ?= memchase_test
SAMPLE_N ?= 20
test_args ?= 12
default: build

# Build test
build:
	mkdir -p $(BIN)
	gcc $(BENCHMARK)/$(TEST).c -o $(BIN)/$(TEST).o -g 

# Dry Run 
run: build
	./$(TEST).o $(test_args)

cwd = $(shell pwd)

# Run cdof
cdof: build
	mkdir -p $(BIN)
	sudo docker run --rm -v $(cwd):/tmp/work grammatech/ddisasm ddisasm /tmp/work/$(BIN)/$(TEST).o --ir /tmp/work/$(BIN)/$(TEST).gtirb
	sudo docker run --rm -v $(cwd):/tmp/work grammatech/ddisasm gtirb-pprinter /tmp/work/$(BIN)/$(TEST).gtirb --asm /tmp/work/$(BIN)/$(TEST).s	
	cdof $(WP)/$(TEST)_runs.txt $(BIN)/$(TEST).s

# Measure Before Optimization
measure_nop:
	perf stat -e cache-references,cache-misses,LLC-loads,LLC-load-misses ./$(TEST).o $(test_args)

# Measure After Optimization
measure_op:
	perf stat  -e cache-references,cache-misses,LLC-loads,LLC-load-misses ./$(TEST).owith_prefetch $(test_args)

measure: 
	python3 average.py $(TEST) $(EXPERIMENT)/$(TEST)_experiments.csv $(SAMPLE_N)

graph: 
	python3 graph.py $(TEST)

clean:
	rm -rf $(BIN) output.txt 

clean_measure:
	rm -rf ./*_measurements

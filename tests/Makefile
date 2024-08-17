TEST ?= gemv_test
test_run ?= test_run.txt
M ?= 10000
N ?= 100

# Build test
all:
	gcc $(TEST).c -o $(TEST).o

# Dry Run 
run:
	./$(TEST).o $(M) $(N)

cwd = $(shell pwd)

# Run cdof
cdof: all
	sudo docker run --rm -v $(cwd):/tmp/work grammatech/ddisasm ddisasm /tmp/work/$(TEST).o --ir /tmp/work/$(TEST).gtirb
	sudo docker run --rm -v $(cwd):/tmp/work grammatech/ddisasm gtirb-pprinter /tmp/work/$(TEST).gtirb --asm /tmp/work/$(TEST).s	
	cdof $(test_run) $(TEST).s

# Measure Before Optimization
measure_nop:
	perf stat  -e cache-references,cache-misses ./$(TEST).o $(M) $(N)

# Measure After Optimization
measure_op:
	perf stat  -e cache-references,cache-misses ./$(TEST).owith_prefetch $(M) $(N)

clean:
	rm -f $(TEST).o $(TEST).owith_prefetch $(TEST).swith_prefetch.s $(TEST).s $(TEST).gtirb 

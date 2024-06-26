#define _GNU_SOURCE 1

#include <stdlib.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/perf_event.h>
#include <asm/unistd.h>
#include <sys/mman.h>

#include <fcntl.h>
#include <signal.h>
#include <assert.h>

#define PAGE_SIZE (4*1024)

#define UNCORE_IMC_TYPE 12
#define UNCORE_IMC_EVENT_READ 0x01
#define UNCORE_IMC_EVENT_WRITE 0x02

static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
			    int cpu, int group_fd, unsigned long flags)
{
	int ret;

	ret = syscall(__NR_perf_event_open, hw_event, pid, cpu,
	               group_fd, flags);
	return ret;
}

static print_perf_macros()
{
	printf("perf_event_attr->type:\n");
	printf(" - PERF_TYPE_HARDWARE: %d\n", PERF_TYPE_HARDWARE);
	printf(" - PERF_TYPE_SOFTWARE: %d\n", PERF_TYPE_SOFTWARE);
	printf(" - PERF_TYPE_TRACEPOINT: %d\n", PERF_TYPE_TRACEPOINT);
	printf(" - PERF_TYPE_HW_CACHE: %d\n", PERF_TYPE_HW_CACHE);
	printf(" - PERF_TYPE_RAW: %d\n", PERF_TYPE_RAW);
	printf(" - PERF_TYPE_BREAKPOINT: %d\n", PERF_TYPE_BREAKPOINT);

	printf("perf_event_mmap-page->type:\n");
	printf(" - PERF_RECORD_MMAP: %d\n", PERF_RECORD_MMAP);
	printf(" - PERF_RECORD_LOST: %d\n", PERF_RECORD_LOST);
	printf(" - PERF_RECORD_COMM: %d\n", PERF_RECORD_COMM);
	printf(" - PERF_RECORD_EXIT: %d\n", PERF_RECORD_EXIT);
	printf(" - PERF_RECORD_THROTTLE: %d\n", PERF_RECORD_THROTTLE);
	printf(" - PERF_RECORD_UNTHROTTLE: %d\n", PERF_RECORD_UNTHROTTLE);
	printf(" - PERF_RECORD_FORK: %d\n", PERF_RECORD_FORK);
	printf(" - PERF_RECORD_READ: %d\n", PERF_RECORD_READ);
	printf(" - PERF_RECORD_SAMPLE: %d\n", PERF_RECORD_SAMPLE);
	printf(" - PERF_RECORD_MMAP2: %d\n", PERF_RECORD_MMAP2);
#ifdef PERF_RECORD_AUX
	printf(" - PERF_RECORD_AUX: %d\n", PERF_RECORD_AUX);
#endif
#ifdef PERF_RECORD_ITRACE_START
	printf(" - PERF_RECORD_ITRACE_START: %d\n", PERF_RECORD_ITRACE_START);
#endif
#ifdef PERF_RECORD_LOST_SAMPLES
	printf(" - PERF_RECORD_LOST_SAMPLES: %d\n", PERF_RECORD_LOST_SAMPLES);
#endif
#ifdef PERF_RECORD_SWITCH
	printf(" - PERF_RECORD_SWITCH: %d\n", PERF_RECORD_SWITCH);
#endif
#ifdef PERF_RECORD_SWITCH_CPU_WIDE
	printf(" - PERF_RECORD_SWITCH_CPU_WIDE: %d\n", PERF_RECORD_SWITCH_CPU_WIDE);
#endif
	printf("\n");
}

void print_sampling_info(struct perf_event_mmap_page *samp_info)
{
	printf("perf_event_mmap-page (not complete):\n");
	printf("  - version: %u\n", samp_info->version);
	printf("  - compat version: %u\n", samp_info->compat_version);
	printf("  - index: %u\n", samp_info->index);
	printf("  - offset: %lld\n", samp_info->offset);
	printf("  - time enabled: %llu\n", samp_info->time_enabled);
	printf("  - time running: %llu\n", samp_info->time_running);
	printf("  - cap_usr_time: %d\n", samp_info->cap_user_time);
	printf("  - cap_usr_rdpmc: %d\n", samp_info->cap_user_rdpmc);
	printf("  - pmc_width: %x\n", samp_info->pmc_width);
	printf("  - data_head: %lld\n", samp_info->data_head);
	printf("  - data_tail: %lld\n", samp_info->data_tail);
	printf("\n");
}

void compute_stuff()
{
	// const size_t buf_size = 1024*1024*1024;
	const size_t buf_size = 1024;
	char * buf;
	int sum, i;

	buf = (char *)malloc(buf_size);
	if (!buf) {
		perror("Cannot mmap memory");
		exit(EXIT_FAILURE);
	}

	for (i = 0; i < buf_size; i++) {
		if (!buf) 


		sum += buf[i];
	}

	// this is to avoid compiler optimizations
	printf("sum: %d\n", sum);
}

/* Print record sample of type branch record */
static void branch_stack_print(struct {
																			struct perf_event_header hdr;
																			uint64_t nr;
																			struct perf_branch_entry lbr[];} *data)
{
  uint64_t lbr_size = data->nr;
	uint32_t type = data->hdr.type;
	struct perf_branch_entry *lbr = data->lbr;
	
	assert (type == PERF_RECORD_SAMPLE);

  
	/* For each branch entry */
	int idx = 0;
	while (idx < lbr_size)
	{
	  /* Print out it's event data */
		uint64_t from = lbr[idx].from;
		uint64_t to = lbr[idx].to;
		int mispred = lbr[idx].mispred;
		int pred = lbr[idx].predicted;
		int cycles = lbr[idx].cycles;
		printf ("from %lx \n", from);
		printf ("to %lx  \n", to);
		printf("mispred %u \n", mispred);
		printf("predicted %u \n", pred);
		printf("\n");
		
		idx ++;
	}
	
}

void print_header(struct perf_event_header *header)
{
	printf("perf_event_header:\n");
	printf(" - type:%u\n", header->type);
	printf(" - misc:%x\n", header->misc);
	printf(" - size:%u\n", header->size);
	
	// branch_stack_print (header);
}

void print_raw_data(struct perf_event_header *header)
{
	void *post_header;
	uint32_t raw_size;
	char * raw_data;
	int i;

	post_header = (char *)header + sizeof(struct perf_event_header);
	raw_size = *((uint32_t *)post_header);
	raw_data = (char *)(post_header+sizeof(uint32_t));
	printf (" - raw_size:%d\n", raw_size);
	printf (" - raw_data: ");
	for (i = 0; i < raw_size; i++) {
		printf("%u ", raw_data[i]);
	}
	printf("\n");
}

void sigio_handler (int signum)
{
 printf("signal recieved!\n");
}

#define BUF_SIZE_SHIFT 12
#define BUF_SIZE (1ULL << BUF_SIZE_SHIFT)

int perf_sampling_example()
{
	int fd;
	struct perf_event_attr pe;
	struct perf_event_mmap_page *samp_info;
	struct perf_event_header *header;
	const size_t mmap_size = 2*PAGE_SIZE;
	void *buffer;
	char *iter, *samples_end;
	unsigned long nrecords = 0;
	void *post_header;
	pid_t pid;
	int cpu;
	uint64_t *value;

	memset(&pe, 0, sizeof(struct perf_event_attr));
	pe.size        = sizeof(struct perf_event_attr);
	pe.type        = PERF_TYPE_HARDWARE;
	pe.config      = PERF_COUNT_HW_BRANCH_INSTRUCTIONS;
	pe.sample_period = 32;
	pe.exclude_kernel = 1;
	pe.wakeup_events = 64;
	pe.exclude_hv = 1;
	pe.disabled    = 1;
	// pe.precise_ip = 3; // Precise skidperf record --call-graph lbr        
	pe.exclude_user = 0;
	pe.sample_type = PERF_SAMPLE_BRANCH_STACK; 
	pe.branch_sample_type = PERF_SAMPLE_BRANCH_USER | PERF_SAMPLE_BRANCH_ANY;
  pe.mmap        = 1;
	pe.watermark = 0;

	pid = 0;
	cpu = -1;
	fd = perf_event_open(&pe, pid, cpu, -1, 0);

  // fcntl(fd, F_SETFL, O_NONBLOCK|O_ASYNC);
  // fcntl(fd, F_SETSIG, SIGIO);
  // fcntl(fd, F_SETOWN, getpid());
  
	// struct sigaction sact = {0};
  // sact.sa_handler = sigio_handler;
  // sigaction(SIGIO, &sact, NULL);

  if (fd == -1) {
		fprintf(stderr, "Error opening leader %llx: %d: %s\n",
			pe.config, errno, strerror(errno));
		exit(EXIT_FAILURE);
	}

	buffer = mmap(NULL, mmap_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
	if (buffer == MAP_FAILED) {
		perror("Cannot memory map sampling buffer\n");
		exit(EXIT_FAILURE);
	}

	samp_info = (struct perf_event_mmap_page *)buffer;
  printf ("about to computer \n");
	
	ioctl(fd, PERF_EVENT_IOC_RESET, 0);
	
	ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
  printf ("about to computer \n");
	

	compute_stuff();
	ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
	// printf ("done!\n");
	// return;
	

	print_sampling_info(samp_info);

	samples_end = buffer + PAGE_SIZE + samp_info->data_head;
	//TODO memory barrier rmb

	iter = ((char *)buffer + PAGE_SIZE);
	while (iter < samples_end) {
		header = (struct perf_event_header *)iter;
		post_header = (char *)header + sizeof(struct perf_event_header);

		print_header(header);
		value = (uint64_t *)post_header;
		printf("   {value: %"PRIu64"}\n", *value);

		iter += header->size;
		nrecords++;
	}

	printf("total number of records: %lu\n", nrecords);

	if (munmap(buffer, mmap_size)) {
		perror("Cannot unmmap sampling buffer\n");
	}
	close(fd);

	return 0;
}
int main(int argc, char **argv)
{
	print_perf_macros();

	printf("\n################\n");
	printf("sampling example\n");
	printf("################\n\n");
	perf_sampling_example();

	

}
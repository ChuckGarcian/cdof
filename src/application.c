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

static int perf_event_open (struct perf_event_attr *attr, pid_t pid, int cpu, int group_fd, unsigned long flags);
static int setup_perf (void);
static void setup_overflow_handler (int fd);
static void *setup_buffer (int fd);

static void cdof_enable(int fd);
static void cdof_disable (int fd);

static void printf_results (void *buffer);

void print_sampling_info (struct perf_event_mmap_page *samp_info);
void compute_stuff (void);
void print_header(struct perf_event_header *header);

int main(void)
{
  int fd;
  void *buf;
  char *iter, *samples_end;
  struct perf_event_mmap_page *samp_info;
  struct perf_event_header *header;
  
  fd = setup_perf ();
  buf = setup_buffer (fd);
  printf ("about to computer \n");
  
  cdof_enable(fd);  
  compute_stuff();
	cdof_disable(fd);
	
  printf_results(buf);
}

/* Setup linux profiling API */
static int setup_perf (void)
{
  struct perf_event_attr pe;
	int pid, cpu, tfd;
  
  /* Setup perf for branch event profiling */
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
  
  /* Setup Environment Metadata */
  pid = 0;
  cpu = -1;
  
  return perf_event_open(&pe, pid, cpu, -1, 0);
}

static int perf_event_open(struct perf_event_attr *attr, pid_t pid, int cpu, int group_fd, unsigned long flags)
{
return syscall(__NR_perf_event_open, attr, pid, cpu, group_fd, flags);
}


static void setup_overflow_handler (int fd);

static void *setup_buffer (int fd)
{
  
  void * buffer;
  const size_t mmap_size = 2*PAGE_SIZE;
  buffer = mmap(NULL, mmap_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
	
  if (buffer == MAP_FAILED) {
		perror("Cannot memory map sampling buffer\n");
		exit(EXIT_FAILURE);
	}
  return buffer;
}

static void cdof_enable(int fd)
{
  ioctl(fd, PERF_EVENT_IOC_RESET, 0);

	ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
}

static void cdof_disable (int fd)
{
  ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
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
	
	if (header->type == PERF_RECORD_SAMPLE)
    
		branch_stack_print (header);
}


static void printf_results (void *buf)
{
	struct perf_event_mmap_page *samp_info;
	struct perf_event_header *header;
	char *iter, *samples_end;
  unsigned long nrecords = 0;
	void *post_header;
	uint64_t *value; 
  
  samp_info = (struct perf_event_mmap_page *)buf;
  print_sampling_info(samp_info);
 
	samples_end = buf + PAGE_SIZE + samp_info->data_head;
	iter = ((char *)buf + PAGE_SIZE);
	
  while (iter < samples_end)
  {
		header = (struct perf_event_header *)iter;
		post_header = (char *)header + sizeof(struct perf_event_header);

		print_header(header);
		value = (uint64_t *)post_header;
		printf("   {value: %"PRIu64"}\n", *value);

		iter += header->size;
		nrecords++;
	}
	
}
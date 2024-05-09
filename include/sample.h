/* Based Off perf - 'sample.h' */

#include <linux/perf_event.h>
#include <inttypes.h>

typedef uint64_t u64;
typedef int64_t s64;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t u8;

struct perf_branch_entry {
	__u64	from;
	__u64	to;
	__u64	mispred:1,  /* target mispredicted */
		predicted:1,/* target predicted */
		in_tx:1,    /* in transaction */
		abort:1,    /* transaction abort */
		cycles:16,  /* cycle count to last branch */
		type:4,     /* branch type */
		reserved:40;
};

struct read_format 
{
  u64		value;
  u64		time_enabled; 
  u64		time_running;
  u64		id;          
  u64		lost;        
};

struct ip_callchain 
{
	u64 nr;
	u64 ips[];
};

struct branch_stack {
	u64			nr;
	u64			hw_idx;
	struct branch_entry	entries[];
};


struct perf_record_sample
{
  struct perf_event_header header;
  u64    sample_id;   /* if PERF_SAMPLE_IDENTIFIER */
  u64    ip;          /* if PERF_SAMPLE_IP */
  u32    pid, tid;    /* if PERF_SAMPLE_TID */
  u64    time;        /* if PERF_SAMPLE_TIME */
  u64    addr;        /* if PERF_SAMPLE_ADDR */
  u64    id;          /* if PERF_SAMPLE_ID */
  u64    stream_id;   /* if PERF_SAMPLE_STREAM_ID */
  u32    cpu, res;    /* if PERF_SAMPLE_CPU */
  u64    period;      /* if PERF_SAMPLE_PERIOD */
  struct read_format v;
                      /* if PERF_SAMPLE_READ */
  u64    nr;          /* if PERF_SAMPLE_CALLCHAIN */
  u64    ips;         /* if PERF_SAMPLE_CALLCHAIN */
  
  u32    size;        /* if PERF_SAMPLE_RAW */
  char   data;        /* if PERF_SAMPLE_RAW */
  u64    bnr;         /* if PERF_SAMPLE_BRANCH_STACK */
  struct perf_branch_entry lbr[];
};

struct perf_sample {
	u64 ip;
	u32 pid, tid;
	u64 time;
	u64 addr;
	u64 id;
	u64 stream_id;
	u64 period;
	u64 weight;
	u64 transaction;
	u64 insn_cnt;
	u64 cyc_cnt;
	u32 cpu;
	u32 raw_size;
	u64 data_src;
	u64 phys_addr;
	u64 data_page_size;
	u64 code_page_size;
	u64 cgroup;
	u32 flags;
	u32 machine_pid;
	u32 vcpu;
	u16 insn_len;
	u8  cpumode;
	u16 misc;
	u16 ins_lat;
	union {
		u16 p_stage_cyc;
		u16 retire_lat;
	};
	bool no_hw_idx;		/* No hw_idx collected in branch_stack */
	char insn[MAX_INSN]
	void *raw_data;
	struct ip_callchain *callchain;
	struct branch_stack *branch_stack;
	u64 *branch_stack_cntr;
	struct regs_dump  user_regs;
	struct regs_dump  intr_regs;
	struct stack_dump user_stack;
	struct sample_read read;
	struct aux_sample aux_sample;
	struct simd_flags simd_flags;
};
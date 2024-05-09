# 3/21 - Understanding How to Profile a Running Program
Initially, when I was writing the proposal for this project, I underestimated how difficult it would be to get the profiling aspect of the project to work. After doing some reading, I learned that profiling is a method of measuring events in a system. These events can either be hardware or software-sourced events. 

According to the man pages for perf_event: 
  "
  There are two different flavors of events: counting and sampled. A counting event is one that is used for counting the aggregate number of events that occur. In general, counting event results are gathered with a read(2) call. A sampling event periodically writes measurements to a buffer that can then be accessed via mmap(2).
  "

At first, I assumed I was going to use Intel's PCM API. However, it seems like it only offers counting events and, in general, is pretty complex to use. After searching around a bit more, if I understand correctly, I will need a kernel-level profiling tool, which PCM is not. Linux has a system call just for this called 'perf_event_open', and it seems like it has everything that I need.

For this project, I will need sample-based events. Specifically, I need to use 'perf_event_open' to group events into one sample that is later read into a buffer.

Lastly, during my reading, I found these websites that may prove useful in the future:
  - https://www.brendangregg.com/perf.html#Usage
  - https://jvns.ca/blog/2016/03/12/how-does-perf-work-and-some-questions/
  - https://www.man7.org/linux/man-pages/man2/perf_event_open.2.html

## Sample Event
The following is from the `perf_event_open` man page:
    sample_period, sample_freq: A "sampling" event is one that generates an overflow notification every N events, where N is given by sample_period. A sampling event has sample_period > 0. When an overflow occurs, requested data is recorded in the mmap buffer. The sample_type field controls what data is recorded on each overflow.

So it seems like for our purposes we will need to

## Perf-event-open Man Page Notes
The perf-event-open system call takes a 'perf_event_attr' struct that describes information on how the kernel should sample the PMU and deliver to the us (us being the calling thread).

struct members:  

- sample_type:
  - Specifies what the sample contains
  - Our case it will be PERF_SAMPLE_BRANCH_STACK 

- execlude_kernel:
  - execlude kernel events
  - = 1
- execlude_hv:
  - execlude hypervisor
  - = 1


# PERF_RECORD_MMAP
To understand what cases this flag is used for consider an application, and our exernal optimizer thread. The external optimizer thread is agnostic to any application so it is not explicitly aware of certain events needs to be notified. In the case of mmap() system calls, like when an application links to a dynamicaly shared library, our external optimizer thread needs to know about it. 

The perf_record_mmap is a perf event that records information about mmap calls. In theory, if CDOF needed this information, we would use this flag. According to man pages: 
        The mmap bit enables generation of PERF_RECORD_MMAP
        samples for every mmap(2) call that has PROT_EXEC set.
        This allows tools to notice new executable code being
        mapped into a program (dynamic shared libraries for
        example) so that addresses can be mapped back to the
        original code.

## My Laptop Nova 15 - Determining if it supports LBR
I need to know if my laptop supports LBR (last branch retired).
The specs of my laptop as per 'lscpu':
      Model name:            Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
      CPU family:          6
      Model:               158
After a google search, it seems like the codename for my cpu is coffee lake. Moreover according to intel software development manual section 20.3.8 '6th Generation, 7th Generation and 8th Generation Intel® Core™ Processor Performance Monitoring facility' the coffee lake microarchitecture family has LBR with support for 32 entries. 

## Fixed issue
The example code on man page would give an invalid argument error when I modified it to branch stack sampling, turns out I was not correctly setting the branch sample type. You need to or two different enums: 
    - First enum is the privilege level
    - Second filters the branch type
So in our case its user privilege level and branch type is all. Branch type shall change in the future (maybe).

# 3/23 - Remark On Intel LBRs
# Understanding Last Branch Records Collection

There has been some confusion about the overall flow of collecting Last Branch Records (LBR). Specifically, the process of monitoring LBR with `perf_event_open()` and the notification system can be perplexing. After some research, the following details have been clarified:

## Performance Event Based Sampling (PEBS)

Intel machines support Performance Event Based Sampling (PEBS). PEBS allows the hardware, not the software, to write to a buffer when a particular counter of interest overflows. This process also initiates a Performance Monitor Interrupt (PMI). In our case, we want to initiate a PMI by monitoring the number of branch instructions taken.

## Key Components of `perf_event_open` Struct

There are two components in the `perf_event_open` struct that were initially confusing:

### 1. Sampling Period

The man pages state that this value determines how often an overflow notification occurs. However, this does not actually change the maximum value at which a counter overflows. Instead, it determines how often the data we are interested in gets written to a buffer. This implies that some counters may be lost, as we could sample after they have overflowed. 

### 2. Wakeup Event/Wakeup Watermark

This component determines how often the thread is woken up. 

## Last Branch Records (LBR)

According to the Intel Manual, LBR is a model-specific register (MSR), specifically a circular buffer, that stores metadata on the last 32 branches (Coffee Lake architecture). We can configure it so that when a PMI occurs, the processor will write the LBR record sample to a memory buffer. The Wakeup Event/Wakeup Watermark events seem to be a software/kernel-backed component, not a hardware one. It appears to refer to the number of PEBS that can occur before waking up the thread.


# 3/24
I found a textbook that greatly helps with some of the issues and confusion I've been dealing with in the perf kernel API. The textbook is titled 'Power_and_Performance_Software_Analysis_and_Optimization'. Specifically, it has helped with an issue regarding how data should be read from the ring buffer. The man pages seemed unclear on how the data was organized. However, the following excerpt from the book clears it up:
  The perf_attr.sample_type field specifies what information should
  be recorded for each event.
Moreover, the book provides an example confirming how data is read from the ring buffer.

## Reading Sampling Events
Expanding on what was said above, when we first initialize the `perf_event_open()` API, we pass it a struct containing the desired event data we want from the PMU. If the event is a sampling event, then the struct member `attr.sample_type` is set to the list of all the event types we want. When the kernel writes to the ring buffer, **the only** contents written to the buffer are the ones specified by the list we originally passed.
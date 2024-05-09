To help you in your project we recommend taking the following steps:

# Stage 1

TODO:
  -Create a short C program with Second thread containing code to routinely profile the first thread. 
  - Specifically the second thread should be periodically sampling the branch events of the first thread.
  - For now events should only be printed to console. Do not bother with buffering or saving them; That will be the next stage.

DONOT:
- Don't focus on shared library or execution environment initialization (libc_start).

Purpose: 
  - To understand how to interface with Intel's PCM API to acquire certain program counter values and events
  

# Stage 2

TODO:
  - Implement *window profiling* so that events are saved in a buffer.
  - Learn how to detect phases using window profiling
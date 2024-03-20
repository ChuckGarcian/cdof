CC = gcc
CC_OPTIONS = -Wall -O2 -c
LDFLAGS = -L/home/chuckg/Packages/pcm/build/lib/libpcm -DPCM_DYNAMIC_LIB
LDLIBS = -llibpcm
RM = /bin/rm -f

BINARY_DIR = /home/chuckg/Packages/pcm/build
INSTALL_RPATH = /home/chuckg/Packages/pcm/build/lib/libpcm.so

SRCS := main.c
OBJS := $(SRCS:%.c=%.o)
EXEC := driver

# Compile the source file into an object file


# Link the object file with the library to create an executable
# -Wl,-rpath,... sets the runtime library search path
# -ldl links against the dynamic linking library
# -lpthread links against the POSIX threads library

# gcc -o c_example c_example.o -L${BINARY_DIR}/lib -Wl,-rpath,${BINARY_DIR}/lib:${INSTALL_RPATH} -ldl -lpthread

all: $(EXEC)

build:
		gcc -c -DPCM_DYNAMIC_LIB -o exec.o main.c

link: build
		gcc -o exec exec.o -L/home/chuckg/Packages/pcm/build/lib -Wl,-rpath,/home/chuckg/Packages/pcm/build/lib:/home/chuckg/Packages/pcm/build/lib/libpcm.so -ldl -lpthread




$(EXEC): $(OBJS)
	$(CC) $(LDFLAGS) $(OBJS) $(LDLIBS) -o $(EXEC)

%.o: %.c
	$(CC) $(CC_OPTIONS) $< -o $@

clean:
	$(RM) $(OBJS) $(EXEC)

.PHONY: all clean
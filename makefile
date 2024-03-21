CC = gcc
CC_OPTIONS = -Wall -O2 -c
LDFLAGS = -L/home/chuckg/Packages/pcm/build/lib
LDLIBS = -lpcm
RM = rm -f

BINARY_DIR = /home/chuckg/Packages/pcm/build
INSTALL_RPATH = /home/chuckg/Packages/pcm/build/lib/libpcm.so

SRCS := main.c
OBJS := $(SRCS:%.c=%.o)
EXEC := driver

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(LDFLAGS) $(OBJS) $(LDLIBS) -Wl,-rpath,$(BINARY_DIR)/lib:$(INSTALL_RPATH) -ldl -lpthread -o $(EXEC)

%.o: %.c
	$(CC) $(CC_OPTIONS) -DPCM_DYNAMIC_LIB $< -o $@

clean:
	$(RM) $(OBJS) $(EXEC)

run: all
	sudo ./$(EXEC) 

.PHONY: all clean run
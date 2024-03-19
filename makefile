CC = gcc
CC_OPTIONS = -Wall -O2 -c
RM = /bin/rm -f

SRCS := main.c
OBJS := $(SRCS:%.c=%.o)
EXEC := driver

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CC) $(OBJS) -o $(EXEC)

%.o: %.c
	$(CC) $(CC_OPTIONS) $< -o $@

clean:
	$(RM) $(OBJS) $(EXEC)

.PHONY: all clean




CPPCHECK = cppcheck
CPPCHECKFLAG = --std=c99 --verbose --bug-hunting 

CC = gcc
CFLAGS = -Wall -Wextra -g
BIN = bin
DIRS = src tests include
DIRPATHS = $(foreach DIR, $(DIRS), $(shell find $(DIR) -type d))
FILEPATHS = $(foreach DIR, $(DIRPATHS), $(shell find $(DIR) -type f -name *.c))
IFLAGS = $(DIRPATHS:%=-I%)
VPATH = $(DIRPATHS)

all:
	@echo $(DIRPATHS)

%_test : %_test.c
	@$(CC) $(CFLAGS) $(IFLAGS) -o $(BIN)/$@ $<

test_%: %_test
	@$(BIN)/$<

check_%: %.c
	@$(CPPCHECK) $(CPPCHECKFLAG) $<

compile_%: %.c
	@$(CC) $(CFLAGS) $(IFLAGS) -o $(BIN)/$* $<
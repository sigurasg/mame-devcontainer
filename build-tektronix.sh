#!/usr/bin/env bash

export DEBUG=1
export SYMBOLS=1
export LDFLAGS=-lfontconfig 

time \
make -C mame SUBTARGET=tektronix SOURCES=src/mame/tektronix TOOLS=1 -j5

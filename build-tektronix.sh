#!/usr/bin/env sh

export LDFLAGS=-lfontconfig 

make -C mame SUBTARGET=tektronix SOURCES=src/mame/tektronix TOOLS=1 -j5

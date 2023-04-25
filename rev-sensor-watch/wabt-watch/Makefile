# Use implicit rules for compiling C files.
CFLAGS=-I../.. -I.

all: watch

clean:
	rm -rf watch watch.wasm watch.c *.o

watch: main.o watch.o ../../wasm-rt-impl.o -lm

watch.wasm: watch.wat ../../../bin/wat2wasm
	../../../bin/wat2wasm $< -o $@

watch.c: watch.wasm ../../../bin/wasm2c
	../../../bin/wasm2c $< -o $@

.PHONY: all clean

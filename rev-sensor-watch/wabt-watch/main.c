#include <stdio.h>
#include <stdlib.h>

#include "watch.h"

int main(int argc, char** argv) {
  /* Make sure there is at least one command-line argument. */
  if (argc < 2) {
    printf("Invalid argument. Expected '%s NUMBER'\n", argv[0]);
    return 1;
  }

  /* Convert the argument from a string to an int. We'll implicitly cast the int
  to a `u32`, which is what `fac` expects. */
  u32 x = atoi(argv[1]);

  /* Initialize the Wasm runtime. */
  wasm_rt_init();

  /* Declare an instance of the `fac` module. */
  w2c_watch watch;
  struct w2c_env* env;
  struct w2c_wasi__snapshot__preview1* wasi;

  /* Construct the module instance. */
  wasm2c_watch_instantiate(&watch, env, wasi);

  /* Call `fac`, using the mangled name. */
  u32 result = w2c_watch_main(&watch, x, x);

  /* Print the result. */
  printf("watch(%u) -> %u\n", x, result);

  /* Free the fac module. */
  wasm2c_watch_free(&watch);

  /* Free the Wasm runtime state. */
  wasm_rt_free();

  return 0;
}

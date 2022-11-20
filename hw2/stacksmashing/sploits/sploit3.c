#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

/*
 * Construct your exploit string in the main function and print it.
 * You can pass it into a target binary <target> by running"<target> $(sploit)"
 * in your terminal.
 */

struct widget_t {
  double x;
  double y;
  int count;
};

int main(void)
{
  char exploit[] = "Your exploit goes here!";

  printf("%lu\n", sizeof(struct widget_t));
  printf("%s", exploit);

  return 0;
}

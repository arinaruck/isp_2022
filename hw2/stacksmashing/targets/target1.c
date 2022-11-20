#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int bar(char *arg, char *out)
{
  strcpy(out, arg);
}

int foo(char *argv[])
{
  char buf[240];
  bar(argv[1], buf);
}

int main(int argc, char *argv[])
{
  setuid(0);
  if (argc != 2)
    {
      fprintf(stderr, "target1: argc != 2\n");
      exit(EXIT_FAILURE);
    }
  foo(argv);
  return 0;
}

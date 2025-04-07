#include <stdio.h>

/*
This program is for testing gdb-mcp by loading this program into gdb and then using the MCP server to interact with it.

Compile with:
gcc -g -o example example.c
*/

int add(int a, int b) {
    return a + b;
}

void crash() {
    int* ptr = NULL;
    *ptr = 42;  // Will trigger a seg fault
}

int main() {
    printf("Starting test program...\n");

    int result = add(10, 20);
    printf("10 + 20 = %i\n", result);

    crash();

    return 0;
}
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
This program is for testing gdb-mcp by loading this program into gdb and then using the MCP server to interact with it.

Compile with:
gcc -g -o example example.c
*/

// Global variables for memory operations
char* global_buffer = NULL;
int global_value = 42;

// Function to demonstrate stack operations
void stack_operation(int depth) {
    if (depth <= 0) return;
    printf("Stack depth: %d\n", depth);
    stack_operation(depth - 1);
}

// Function to demonstrate memory operations
void memory_operation() {
    // Allocate and use memory
    global_buffer = malloc(100);
    strcpy(global_buffer, "Hello, GDB!");
    printf("Buffer content: %s\n", global_buffer);

    // Intentionally cause a memory issue
    global_buffer[100] = 'X';  // Buffer overflow
}

// Function to demonstrate register operations
int register_operation(int a, int b) {
    int result = a + b;
    printf("Register operation: %d + %d = %d\n", a, b, result);
    return result;
}

// Function to demonstrate conditional breakpoints
void conditional_operation(int value) {
    if (value > 100) {
        printf("Value is greater than 100\n");
    } else {
        printf("Value is less than or equal to 100\n");
    }
}

int main() {
    printf("Starting test program...\n");

    // Demonstrate stack operations
    stack_operation(3);

    // Demonstrate register operations
    int sum = register_operation(10, 20);
    printf("Sum result: %d\n", sum);

    // Demonstrate conditional operations
    conditional_operation(150);
    conditional_operation(50);

    // Demonstrate memory operations (will crash)
    memory_operation();

    // Cleanup (won't be reached due to crash)
    free(global_buffer);


    return 0;
}
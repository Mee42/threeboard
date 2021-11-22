// predefs

#define true 1
#define false 0

// so it goes first
__attribute__((section(".text.main"))) void main();
void halt();
void delay();

extern char foo;

// sizeof(long)      = 4
// sizeof(int)       = 4
// sizeof(long long) = 8

// memory arangement
// stack starts at 0x20003FFF and grows down

// guess we start the heap at 0x20000000 and go up? hopefully I don't need to write an allocator
// wonder where we put static variables 


volatile int* const post_tables  = (int*)0x41004400;
volatile int* start_of_mem = (int*)0x20000000;


// USEFUL LINK https://www.bravegnu.org/gnu-eprog/data-in-ram.html
//
//
int x = 0xDEADBEAF; // goes into .data
int const y = 0xBABEDEAD; // goes into .rwdata

// do not return from main
void main() {
    *start_of_mem = x;
    *start_of_mem = y;

    int bit_27_high = 1 << 27;
    post_tables[0x08 / sizeof(int*)] = bit_27_high; // set the 27th bit of DIRSET
    post_tables[0x18 / sizeof(int*)] = bit_27_high; // set the 27th bit of OUTSET
    while(true) {
        post_tables[0x1C / sizeof(int*)] = bit_27_high; // set the 27th bit of OUTTGL 
        delay();
    }
    halt();
}

__attribute__((noinline)) void delay() {
    // delays 1-2 seconds
    int i = 0;
    while(i < 30000) {
        i++;
        asm("");
    }
}


// busyloop the CPU, never exit
void halt() {
    while(1) {}
}

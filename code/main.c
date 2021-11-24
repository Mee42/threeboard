#define true 1
#define false 0

// so it goes first, for linking
__attribute__((section(".text.main"))) void main();
void halt();
void setup_global_variables();
void delay(int);
void blinkN(int, int);

extern char l_flash_data; // where the .data segment is in flash
extern char l_mem_data; // where the .data segment is in memory
extern char l_mem_data_end;  // the end of the .data segment in memory
 
// sizeof(long)      = 4
// sizeof(int)       = 4
// sizeof(long long) = 8

// memory
// stack starts at 0x20003FFF and grows down
// global variables start at 0x20000000 go up until l_mem_data_end
// heap starts at l_mem_data_end and grows up

volatile int* const post_tables  = (int*)0x41004400; // place we can configure the pins
volatile char* start_of_mem = (char*)(&l_mem_data_end); // where the heap (should) start


int x = 0xDEADBEAF; // goes into .data. Remove once we have actual rw data
int const y = 0xBABEDEAD; // goes into .rodata, read only

// do not return from main
// you will segfault
void main() {
    // this is needed to reset the stackpointer when debugging (otherwise it trends downwards)
    asm("ldr r0, =0x20003FFF");
    asm("mov sp, r0");
    delay(30000); // seems like the sram needs time to boot...
    // NEEDED, all global variables are garbage until this is called
    setup_global_variables();

    asm("debug_label:");
    ((int*)start_of_mem)[0] = x;
    asm("debug_label_2:");

    blinkN(5, 30000);
    blinkN(10000, 3000);
    // do not remove
    halt();
}

void blinkN(int n, int delayTime) {
    int const bit_27_high = 1 << 27;
    post_tables[0x08 / sizeof(int*)] = bit_27_high; // set the 27th bit of DIRSET
    post_tables[0x18 / sizeof(int*)] = bit_27_high; // set the 27th bit of OUTSET
    int i = 0;
    while(i < n*2) {
        i++;
        post_tables[0x1C / sizeof(int*)] = bit_27_high; // set the 27th bit of OUTTGL, toggle pin
        delay(delayTime);
    }
}


void setup_global_variables() {
    int* start = (int*)(&l_flash_data);
    int* dest  = (int*)(&l_mem_data);
    int* end_dest = (int*)(&l_mem_data_end);
    do { // might be off-by-one error, should we do <=?
        asm("mov r7, r7");
        *dest = *start;
        dest++;
        start++;
    }while(dest != end_dest);
}

__attribute__((noinline)) void delay(int delayTime) {
    // delays ~0.5 seconds
    register int i = 0;
    while(i < delayTime) {
        i++;
        asm("");
    }
}


// busyloop the CPU, never exit
void halt() {
    while(1) {}
}

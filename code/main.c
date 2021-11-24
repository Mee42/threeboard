
#define true 1
#define false 0
#define bool _Bool

// so it goes first, for linking
__attribute__((section(".text.main"))) void main();
void halt();
void setup_global_variables();
void delay(int);
void blinkN(int, int);
void initGPIO();
void setLED(bool);
bool readPin();

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
    initGPIO();

    blinkN(5, 30000);
    while(true) {
        setLED(readPin());
    }
//    while(true) {
//        if(readPin()) {
//            blinkN(1, 100000);
//        } else {
//            blinkN(1, 10000);
//        }
//    }

    // do not remove
    halt();
}

// led  PA27
// key3 PA05
volatile char* const pincfg5 = ((char*)post_tables) + 0x40/*starting offset*/ + 0x5/*pin num*/;
void initGPIO() {
    post_tables[0x08 / sizeof(int*)] = 1 << 27; // DIRSET[27] = 1

    // the keys are configured with internal pull-up resistors, with the key connecting the pin to ground
    post_tables[0x04/sizeof(int*)] = 1 << 5; // DIRCLR[5] = 0
    post_tables[0x18/sizeof(int*)] = 1 << 5; // OUTSET[5] = 1
    *pincfg5 = 1 << 2; // pincfg5 bit 2 (PULLEN) = 1
    *pincfg5 |= 1 << 1; // pincfg5 bit 1 (INEN) = 1

    // DIR: 0     input pin
    // PULLEN: 1  pull pin
    // OUT: 1     pull up
    // INEN: 1    buffered
    
    // read state out of IN[bit y]
}
bool readPin() {
    return (post_tables[0x20/sizeof(int*)] & 0x20) != 0; // IN[5];
}

void setLED(bool state) {
    if(state) {
        post_tables[0x14 / sizeof(int*)] = 1 << 27;// OUTCLR[27]
    } else {
        post_tables[0x18 / sizeof(int*)] = 1 << 27; // OUTSET[27]
    }
}



void blinkN(int n, int delayTime) {
    int i = 0;
    while(i < n) {
        i++;
        setLED(true);
        delay(delayTime);
        setLED(false);
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

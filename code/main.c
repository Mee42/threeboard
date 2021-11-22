
// memory arangement
// stack starts at 0x20003FFF and grows down

// guess we start the heap at 0x20000000 and go up? hopefully I don't need to write an allocator
// wonder where we put static variables 
void main() {
    while(true) {} // DO NOT RETURN, the assembly WILL NOT WORK
}

int getNumber() {
    return 0xBABEBABE;
}

int getNumber2() {
    return getNumber() + 1;
}

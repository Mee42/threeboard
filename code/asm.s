
.global _start


.thumb
.section .text

_start:


// r15 = PC program counter
// r14 = LR link register 
// r13 = SP stack pointer
// r12 = IP intra-procedure-call scratch register
// r11 = FP frame pointer

// r0-r3   argument registers
// r4-r8   callee-saved
// r9      is cringe
// r10-r11 callee-saved
// r12-15  special

// working memory starts at 0x20000000
// and              ends at 0x20003FFF
// so I supposed we will set the stack pointer
// to 0x20003FFF and see how it goes. Maybe we want 0x200003FF0 to pad for qwords, or 0x200004000 cause it subrtacts then moves down
ldr r0, =0x20003FF
mov sp, r0

mov r0, #0x77
mov r1, #0x77
mov r2, #0x77

push {r0}
push {r1}
push {r2}

mov r0, r0
mov r0, r0
blinkLight:

@ set PA27 to OUT
ldr r0, =0x41004400 @ this is the location of the POST tables
add r0, r0, #0x08   @ this is the offset for DIRSET

ldr r1, =0x08000000 @ this is the 1 << 27, the bit we need to set

str r1, [r0]        @ set the 27th bit of DIRSET


ldr r3, =300000 @ counter max
loop1:

@ drive PA27 to HIGH
ldr r0, =0x41004400 @ location of the POST table
add r0, r0, #0x18   @ offset of OUTSET
ldr r1, =0x08000000 @ 1 << 27
str r1, [r0]        @ set the 27th bit of OUTSET

@ busywait
mov r2, #0
tmploop:
add r2, r2, #1
cmp r2, r3
bne tmploop

@ drive PA27 to LOW
ldr r0, =0x41004400 @ location of the POST table
add r0, r0, #0x1C   @ offset of OUTTGL
ldr r1, =0x08000000 @ 1 << 27
str r1, [r0]        @ set the 27th bit of OUTCLR

@ busywait
mov r2, #0
tmploop2:
add r2, r2, #1
cmp r2, r3
bne tmploop2

b loop1

exit: @ spin exit
b exit


@ halt exit?
halt_exit:
ldr r0, =0x21000000 @ out of bounds memory
ldr r0, [r0]

constants:

.section .data

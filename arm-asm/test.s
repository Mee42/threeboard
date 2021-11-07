
.global _start

.section .text

_start:

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

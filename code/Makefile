
.PHONY: enterance asm clean

enterance: out.bin

asm: out.bin main
	arm-none-eabi-objdump -S main
	arm-none-eabi-objdump -s main

main.o: main.c
	arm-none-eabi-gcc main.c -mcpu=cortex-m0 -c -o main.o -O3

main: main.o linkerscript.txt
	arm-none-eabi-ld -o main main.o -T linkerscript.txt

out.text.bin: main
	arm-none-eabi-objcopy -O binary -S main --only-section=.text out.text.bin

out.bin: out.text.bin # this needs to be put at a 0x20 offset
	cat out.text.bin > out.bin 

zeros.bin: # this is 0x20 bytes of zeros
	dd if=/dev/zero of=/dev/stdout count=32 bs=1 >> zeros.bin



clean:
	rm -f test.o test out.text.bin out.bin asm.o main.o main

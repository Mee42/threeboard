
.PHONY: main0 main clean

main0: main

test.o: test.s
	arm-none-eabi-as test.s -mcpu=cortex-m0 -o test.o

test: test.o linkerscript.txt
	arm-none-eabi-ld -o test test.o -T linkerscript.txt

out.text.bin: test
	arm-none-eabi-objcopy -O binary -S test --only-section=.text out.text.bin

out.bin: out.text.bin # this needs to be put at a 0x20 offset
	cat out.text.bin > out.bin 

zeros.bin: # this is 0x20 bytes of zeros
	dd if=/dev/zero of=/dev/stdout count=32 bs=1 >> zeros.bin

main: clean out.bin
	arm-none-eabi-objdump -S test


clean:
	rm -f test.o test out.text.bin out.bin

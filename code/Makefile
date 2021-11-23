
.PHONY: enterance asm help clean

enterance: out.bin

help:
	@echo Use \'make out.bin\' or \'make\' to produce the final out.bin binary
	@echo Use \'make asm\' to print debugging information about produced binary
	@echo You can find out.bin in the current directory, and build artifacts in build/
	@echo You can use \'make clean\' to delete all built files, including out.bin

asm: out.bin build/main
	@arm-none-eabi-objdump -S build/main
	@arm-none-eabi-objdump -s build/main
	@echo -e "\nGlobal Symbol Table:\n"
	@arm-none-eabi-nm build/main

build/main.o: main.c
	@mkdir -p build
	arm-none-eabi-gcc main.c -mcpu=cortex-m0 -c -o build/main.o

build/main: build/main.o linkerscript.txt
	arm-none-eabi-ld -o build/main build/main.o -T linkerscript.txt

build/out.text.bin: build/main
	arm-none-eabi-objcopy -O binary -S build/main --only-section=.text build/out.text.bin

build/out.rodata.bin: build/main
	arm-none-eabi-objcopy -O binary -S build/main --only-section=.rodata build/out.rodata.bin

build/out.data.bin: build/main
	arm-none-eabi-objcopy -O binary -S build/main --only-section=.data build/out.data.bin

out.bin: bootload.bin build/out.text.bin build/out.rodata.bin build/out.data.bin build/zeros.bin
	cat bootload.bin build/out.text.bin build/out.rodata.bin build/out.data.bin build/zeros.bin > out.bin 

build/zeros.bin: # this is 0x20 bytes of zeros
	dd if=/dev/zero of=/dev/stdout count=32 bs=1 status=none >> build/zeros.bin


clean:
	@rm -fr build/
	@rm -f out.bin
	@echo "Cleaned"

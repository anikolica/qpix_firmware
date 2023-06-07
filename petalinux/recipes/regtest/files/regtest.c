#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <fcntl.h>

/* Example code:
 * Build with gcc reg_test.c -o reg_test
 * Call with one or two arguments:
 * reg_test [reg num] reads the register
 * reg_test [reg_num] [reg_data] writes the register
 * Refer to AXI register map for assignments.
 */

int main (int argc, char *argv[]) {
        int mem_fd = 0;                 // /dev/mem memory file descriptor
        int *reg_ptr;                   // pointer to AXI register
        int AXI_reg_base = 0x43c00000;  // from Vivado
        int reg_size = 0x80;            // 128 registers
					// NOTE: no provision to check RW/RO!
        int reg_offset = 0;
        int reg_data = 0;
        long arg = 0;
        int rw = 0;

        if (argc == 2){                 // read reg
                rw = 0;
                arg = strtol(argv[1], NULL, 16);
                reg_offset = (int)arg;  // conv str to 32-bit int
        }
        else if (argc == 3){            // write reg
                rw = 1;
                arg = strtol(argv[1], NULL, 16);
                reg_offset = (int)arg;
                arg = strtol(argv[2], NULL, 16);
                reg_data = (int)arg;
        }
        else{
                printf ("Incorrect number of arguments!\n");
                return 0;
        }

        printf("Opening /dev/mem.\n");
        mem_fd = open("/dev/mem", O_RDWR);
        if (mem_fd == -1)
                printf ("Error! mem_fd: 0x%x\n", mem_fd);

        printf("Memory mapping AXI register from /dev/mem to user space.\n");
        reg_ptr = mmap(NULL, reg_size, PROT_READ|PROT_WRITE, MAP_SHARED, mem_fd, AXI_reg_base);
        if (*reg_ptr == -1)
                printf ("Error! reg_ptr: 0x%x\n", *reg_ptr);


        if (rw == 0){
                printf("Reading AXI register %d.\n", reg_offset);
                printf ("AXI register %d contents: 0x%x\n", reg_offset, *(reg_ptr+reg_offset));
        }
        if (rw == 1){
                printf("Writing AXI register %d with data 0x%x\n", reg_offset, reg_data);
                *(reg_ptr+reg_offset) = reg_data;
                printf ("AXI register %d contents: 0x%x\n", reg_offset, *(reg_ptr+reg_offset));
        }

        printf("Unmapping memory.\n");
        munmap(reg_ptr, reg_size);

        printf("Exit.\n");
        return 0;
}

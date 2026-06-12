#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <errno.h>
#include <string.h>

// Compile: make setVcm
// Usage: ./setVcm <wanted Vcm> <channel>
// Usage example (1.8 V in Vcm2): ./setVcm 1.8 0x01

const float V_REF = 1.8f;
const int DAC_MAX = 4095;

int main(int argc, char* argv[])
{
    if (argc != 3) {
       //Yes, 0x01 is Vcm2
       printf("Error: 2 and only 2 arguments accepted: Vcm [0 to 1.8 V], Channel [0x01 (Vcm2), 0x02 (Vcm), 0x03 (both)]\n");
       return 1;
    }

    char* endptr;
    float targetVcm = strtof(argv[1], &endptr);
    if (endptr == argv[1]) {
       printf("Conversion of targetVcm to float failed\n");
       return 1;
    }

    if (targetVcm < 0.0f || targetVcm > 1.8f) {
       printf("Error: Wrong Vcm value (%f). Accepted values: 0 to 1.8 V\n", targetVcm);
       return 1;
    }

    char* endptr2;
    long channelHex = strtol(argv[2], &endptr2, 0);
    
    if (endptr2 == argv[2] || *endptr2 != '\0') {
       printf("Invalid hex format for channel: %s\n", argv[2]);
       return 1;
    }
    
    if (channelHex != 0x01 && channelHex != 0x02 && channelHex != 0x03) {
       //Yes, 0x01 is Vcm2
       printf("Error: Wrong channel (0x%02lX). Accepted: 0x01 (Vcm2), 0x02 (Vcm), 0x03 (both)\n", channelHex); 
       return 1;
    }
    
    uint8_t channelCmd = (uint8_t)channelHex;

    // Open I2C device
    int file = open("/dev/i2c-1", O_RDWR);
    if (file < 0) {
       perror("open");
       return 1;
    }

    if (ioctl(file, I2C_SLAVE, 0x0D) < 0) {
       perror("ioctl");
       close(file);
       return 1;
    }

    // 12-bit DAC value: 0 to 4095, for AD5339ARMZ-REEL7 DAC
    uint16_t dacValue = (uint16_t)(DAC_MAX * (targetVcm / V_REF) + 0.5f);
    if (dacValue > DAC_MAX) dacValue = DAC_MAX;

    /*
     * Pointer byte:
     * bit 1 = DACB
     * bit 0 = DACA

     * First data byte:
     * bit 7   = PD1
     * bit 6   = PD0
     * bit 5   = CLR
     * bit 4   = LDAC
     * bit 3-0 = D11:D8
    */
    uint8_t data_msb =
          (0 << 7)                      // PD1 = 0 (normal operation)
        | (0 << 6)                      // PD0 = 0 (normal operation)
        | (1 << 5)                      // CLR = 1 (don't clear)
        | (0 << 4)                      // LDAC = 0 (update immediately)
        | ((dacValue >> 8) & 0x0F);     // D11:D8

    uint8_t data_lsb = dacValue & 0xFF; // D7:D0

    uint8_t buffer[3] = {
        channelCmd,
        data_msb,
        data_lsb
    };

    ssize_t ret = write(file, buffer, sizeof(buffer));
    if (ret != sizeof(buffer)) {
        if (ret < 0)
            perror("write");
        else
            fprintf(stderr, "Incomplete write: %zd bytes written\n", ret);

        close(file);
        return 1;
    }

    printf("Successfully wrote DAC value %u (0x%03X) for %.3f V\n", 
           dacValue, dacValue, targetVcm);

    close(file);
    return 0;
}

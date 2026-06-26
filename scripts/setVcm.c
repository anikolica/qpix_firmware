#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <errno.h>
#include <string.h>

// AD5339ARMZ-REEL7 12 bits
// https://www.analog.com/media/en/technical-documentation/data-sheets/ad5337_5338_5339.pdf

// Compile: make setVcm
// Usage: ./setVcm <channel> <wanted Vcm>
// Usage example (Vcm1 1.5 V): ./setVcm 1 1.5 
// Usage example (Vcm2 1.8 V): ./setVcm 2 1.8 
// Usage example (Both 1.3 V): ./setVcm 3 1.3 

const float V_REF = 1.8f;
const int DAC_MAX = 4095; // 12-bit DAC

// Map user input (1, 2, 3) to channel commands
// 1 -> 0x02 (Vcm1), 2 -> 0x01 (Vcm2), 3 -> 0x03 (both)
uint8_t map_channel(int channel)
{
   switch(channel) {
      case 1: return 0x02;  // Vcm1
      case 2: return 0x01;  // Vcm2
      case 3: return 0x03;  // Both
      default: return 0x00;  // Error
   }
}

void i2c_write(int channel, uint16_t dacValue)
{
   const char* i2c_device = "/dev/i2c-1";
   const int i2c_address = 0x0D;
   
   // Open I2C device
   int i2c_fd = open(i2c_device, O_RDWR);
   if (i2c_fd < 0) {
      fprintf(stderr, "Failed to open %s: %s\n", i2c_device, strerror(errno));
      return;
   }
   
   // Set I2C slave address
   if (ioctl(i2c_fd, I2C_SLAVE, i2c_address) < 0) {
      fprintf(stderr, "Failed to set I2C address 0x%02X: %s\n", i2c_address, strerror(errno));
      close(i2c_fd);
      return;
   }
   
   // Get channel command
   uint8_t channelCmd = map_channel(channel);
   if (channelCmd == 0x00) {
      fprintf(stderr, "Error: Invalid channel %d\n", channel);
      close(i2c_fd);
      return;
   }
   
   /*
    * Pointer byte:
    * bit 1 = DACB
    * bit 0 = DACA
    *
    * First data byte:
    * bit 7   = PD1
    * bit 6   = PD0
    * bit 5   = CLR
    * bit 4   = LDAC
    * bit 3-0 = D11:D8
    */
   
   // Prepare buffer
   uint8_t data_msb =
        (0 << 7)                       // PD1 = 0 (normal operation)
      | (0 << 6)                       // PD0 = 0 (normal operation)
      | (1 << 5)                       // CLR = 1 (don't clear)
      | (0 << 4)                       // LDAC = 0 (update immediately)
      | ((dacValue >> 8) & 0x0F);      // D11:D8
   uint8_t data_lsb = dacValue & 0xFF; // D7:D0
   
   uint8_t buffer[3];
   buffer[0] = channelCmd;
   buffer[1] = data_msb;
   buffer[2] = data_lsb;
   
   // Write to I2C device
   ssize_t ret = write(i2c_fd, buffer, sizeof(buffer));
   if (ret != sizeof(buffer)) {
      if (ret < 0) {
         fprintf(stderr, "I2C write failed: %s\n", strerror(errno));
      } else {
         fprintf(stderr, "Incomplete I2C write: %zd bytes written (expected %zu)\n", ret, sizeof(buffer));
      }
      close(i2c_fd);
      return;
   }
   
   // Close the file
   close(i2c_fd);
   
   const char* channel_names[] = {"", "Vcm1", "Vcm2", "Vcm1 and Vcm2"};
   printf("Wrote %d to %s\n", dacValue, channel_names[channel]);
}

int main(int argc, char *argv[])
{
   // usage
   if (argc != 3) {
      printf("Usage: %s <channel> <Vcm voltage>\n", argv[0]);
      printf("argv[1]:  channel [1 = Vcm1, 2 = Vcm2, 3 = both]\n");
      printf("argv[2]:  Vcm [0.0 to 1.8 V]\n");
      return 1;
   }
   
   // channel selection
   char* endptrC;
   int channel = strtol(argv[1], &endptrC, 10);
   if (*endptrC != '\0' || endptrC == argv[1]) {
      fprintf(stderr, "Wrong channel format (%s). Please provide a valid one: 1 (Vcm1), 2 (Vcm2), 3 (both)\n", argv[1]);
      return 1;
   }
   if (channel < 1 || channel > 3) {
      fprintf(stderr, "Error: Wrong channel. Accepted values: 1 (Vcm1), 2 (Vcm2), 3 (both)\n");
      return 1;
   }
   
   // target Vcm voltage
   char* endptrV;
   float targetVcm = strtof(argv[2], &endptrV);
   if (endptrV == argv[2] || *endptrV != '\0') {
      fprintf(stderr, "Conversion of targetVcm to float failed\n");
      return 1;
   }
   if (targetVcm < 0.0f || targetVcm > 1.8f) {
      fprintf(stderr, "Error: Wrong Vcm value (%f). Accepted values: 0 to 1.8 V\n", targetVcm);
      return 1;
   }
   
   // translate voltage to DAC value with rounding
   uint16_t dacValue = (uint16_t)(DAC_MAX*(targetVcm/V_REF)+0.5f);
   if (dacValue > DAC_MAX) dacValue = DAC_MAX;
   
   // write to the chosen device
   i2c_write(channel, dacValue);
   
   return 0;
}

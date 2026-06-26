#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

// MCP4911-E/P 10 bits 
// https://ww1.microchip.com/downloads/en/DeviceDoc/22248a.pdf

// Compile: make setVcomp
// Usage: ./setVcomp <channel> <wanted Vcomp> 
// Usage example (Vcomp1, 0.78 V): ./setVcomp 1 0.78 
// Usage example (Vcomp2, 0.90 V): ./setVcomp 2 0.9 
// Usage example (Both,   0.80 V): ./setVcomp 3 0.8 

const int SPI_SPEED = 1000000;
const float V_REF = 1.0f;
const int DAC_MAX = 1023; // 10-bit DAC

void spi_write(int device, uint16_t dacValue)
{
   const char* dev_path;
   // Select device path
   if (device == 1) {
      dev_path = "/dev/spidev1.0";
   } else if (device == 2) {
      dev_path = "/dev/spidev1.1";
   } else {
      fprintf(stderr, "Error: Invalid device %d\n", device);
      return;
   }

   // Open SPI device
   int spi_fd = open(dev_path, O_RDWR);
   if (spi_fd < 0) {
      fprintf(stderr, "Failed to open %s: %s\n", dev_path, strerror(errno));
      return;
   }

   // SPI_CS_HIGH forces CS low during the transaction
   uint8_t mode = SPI_MODE_0 | SPI_CS_HIGH;
   if (ioctl(spi_fd, SPI_IOC_WR_MODE, &mode) < 0) {
      fprintf(stderr, "Failed to set SPI mode: %s\n", strerror(errno));
      close(spi_fd);
      return;
   }

	// set speed
   uint32_t speed = SPI_SPEED;
   if (ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed) < 0) {
      fprintf(stderr, "Failed to set SPI speed: %s\n", strerror(errno));
      close(spi_fd);
      return;
   }


   // MCP4911 frame: GA=1, active, unbuffered
   uint16_t cmd = 0x3000 | ((dacValue & 0x03FF) << 2);

   uint8_t tx[2];
   tx[0] = (cmd >> 8) & 0xFF;
   tx[1] = cmd & 0xFF;

   struct spi_ioc_transfer tr = {0};
   tr.tx_buf = (unsigned long)tx;
   tr.len = 2;
   tr.speed_hz = SPI_SPEED;
   tr.bits_per_word = 8;

	// write to SPI device
   if (ioctl(spi_fd, SPI_IOC_MESSAGE(1), &tr) < 1) {
      fprintf(stderr, "SPI write failed: %s\n", strerror(errno));
      close(spi_fd);
      return;
   }

	// close the file
   close(spi_fd);

   if (device == 1)
       printf("Wrote %d to spidev1.0\n", dacValue);
   else if (device == 2)
       printf("Wrote %d to spidev1.1\n", dacValue);
}

int main(int argc, char *argv[])
{
    // usage
    if (argc != 3) {
       printf("Usage: %s <device> <Vcomp voltage>\n", argv[0]);
       printf("argv[1]:  device [1 = Vcomp1, 2 = Vcomp2, 3 = both]\n");
       printf("argv[2]:  Vcomp [0.0 to 1.0 V]\n");
       return 1;
    }

    // device selection
    char *endptrD;
    int device = strtol(argv[1], &endptrD, 10);
    if (*endptrD != '\0' || endptrD == argv[1]) {
        fprintf(stderr, "Wrong device format (%s). Please provide a valid one: 1 (Vcomp1), 2 (Vcomp2), 3 (both)\n", argv[1]);
        return 1;
    }
    if (device < 1 || device > 3) {
       fprintf(stderr, "Error: Wrong device. Accepted values: 1 (Vcomp1), 2 (Vcomp2), 3 (both)\n");
       return 1;
    }

    // target Vcomp voltage
    char* endptrV;
    float targetVcomp = strtof(argv[2], &endptrV);
    if (endptrV == argv[2] || *endptrV != '\0') {
       fprintf(stderr, "Conversion of targetVcomp to float failed\n");
       return 1;
    }
    if (targetVcomp < 0.0f || targetVcomp > 1.0f) {
       fprintf(stderr, "Error: Wrong Vcomp value (%f). Accepted values: 0 to 1.0 V\n", targetVcomp);
       return 1;
    }
    
    // translate voltage to DAC value
    uint16_t dacValue = (uint16_t)(DAC_MAX*(targetVcomp/V_REF)+0.5f);
    if (dacValue > DAC_MAX) dacValue = DAC_MAX;

    // write to the chosen device
    if (device == 3) { // Both devices
       spi_write(1, dacValue);
       spi_write(2, dacValue);
    } 
	 else {
	    spi_write(device, dacValue);
    }

    return 0;
}

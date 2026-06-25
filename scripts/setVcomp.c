#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <stdlib.h>
#include <string.h>

#define SPI_SPEED  1000000

const float V_REF = 1.0f;
const int DAC_MAX = 1023;
static int spi_fd;

void spi_write(uint16_t value)
{
   uint8_t tx[2];
   struct spi_ioc_transfer tr = {0};

   // MCP4911 frame: GA=1, active, unbuffered
   uint16_t cmd = 0x3000 | ((value & 0x03FF) << 2);

   tx[0] = (cmd >> 8) & 0xFF;
   tx[1] = cmd & 0xFF;

   tr.tx_buf = (unsigned long)tx;
   tr.len = 2;
   tr.speed_hz = SPI_SPEED;
   tr.bits_per_word = 8;

   if (ioctl(spi_fd, SPI_IOC_MESSAGE(1), &tr) < 1) {
      perror("SPI write failed");
      exit(1);
   }
}

int open_spi_device(const char *device_path)
{
   int fd = open(device_path, O_RDWR);
   if (fd < 0) {
      perror("Cannot open SPI device");
      return -1;
   }

   // SPI_CS_HIGH forces CS low during the transaction
   uint8_t mode = SPI_MODE_0 | SPI_CS_HIGH;
   if (ioctl(fd, SPI_IOC_WR_MODE, &mode) < 0) {
      perror("Failed to set SPI mode");
      close(fd);
      return -1;
   }

   uint32_t speed = SPI_SPEED;
   if (ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed) < 0) {
      perror("Failed to set SPI speed");
      close(fd);
      return -1;
   }

   return fd;
}

int main(int argc, char *argv[])
{
    if (argc < 2 || argc > 3) {
       printf("Usage: %s <voltage value> [device]\n", argv[0]);
       printf("  Vcomp [0.0 to 1.0 V]\n");
       printf("  device [0 = spidev1.0, 1 = spidev1.1, 2 = both (default: 0)]\n");
       return 1;
    }

    char* endptr;
    float targetVcomp = strtof(argv[1], &endptr);
    if (endptr == argv[1]) {
       printf("Conversion of targetVcomp to float failed\n");
       return 1;
    }

    if (targetVcomp < 0.0f || targetVcomp > 1.0f) {
       printf("Error: Wrong Vcomp value (%f). Accepted values: 0 to 1.0 V\n", targetVcomp);
       return 1;
    }
    uint16_t dacValue = (uint16_t)(DAC_MAX*(targetVcomp/V_REF));
    if (dacValue > DAC_MAX) dacValue = DAC_MAX;

    int device_choice = 0;
    if (argc == 3) {
       device_choice = atoi(argv[2]);
    }

    const char *devices[3] = {
       "/dev/spidev1.0",
       "/dev/spidev1.1",
       NULL  // both
    };

    if (device_choice == 0) { // Single device: spidev1.0
       spi_fd = open_spi_device(devices[0]);
       if (spi_fd < 0) return 1;
        
       spi_write(dacValue);
       close(spi_fd);
       printf("Wrote %d to spidev1.0\n", dacValue);
    } 
    else if (device_choice == 1) { // Single device: spidev1.1
       spi_fd = open_spi_device(devices[1]);
       if (spi_fd < 0) return 1;
        
       spi_write(dacValue);
       close(spi_fd);
       printf("Wrote %d to spidev1.1\n", dacValue);
    } 
    else if (device_choice == 2) { // Both devices
       for (int i = 0; i < 2; i++) {
          spi_fd = open_spi_device(devices[i]);
          if (spi_fd < 0) {
             fprintf(stderr, "Failed to open %s, continuing...\n", devices[i]);
             continue;
          }
            
          spi_write(dacValue);
          close(spi_fd);
          printf("Wrote %d to %s\n", dacValue, devices[i]);
       }
    } 
    else {
       fprintf(stderr, "Invalid device choice: %d. Use 0, 1, or 2.\n", device_choice);
       return 1;
    }

    return 0;
}

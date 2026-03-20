#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>

# with help from ML/AI ...
int main() {
        int fd = open("/dev/spidev1.0", O_RDWR);

        uint8_t tx[] = {0xAA, 0x55};
        uint8_t rx[2] = {0};

        struct spi_ioc_transfer tr = {
                .tx_buf = (unsigned long)tx,
                .rx_buf = (unsigned long)rx,
                .len = 2,
                .speed_hz = 1000000,
                .bits_per_word = 8,
        };

        ioctl(fd, SPI_IOC_MESSAGE(1), &tr);

        printf("RX: %02X %02X\n", rx[0], rx[1]);

        close(fd);
        return 0;
}
# QPix Tester Firmware

## Maintainer

Adrian Nikolica (nikolica@hep.upenn.edu)

## Contributors

* Adrian Nikolica
* Nandor Dressnandt

## Documentation

* [Z-turn V2](https://www.myirtech.com/list.asp?id=708)

## Description
This respository contains firmware, software, test scripts, and Petalinux build configurations for a MYiR Z-turn v2 board. The Z-turn plugs into a carrier card with 5V supply and associated test circuitry (level translators, DACs, etc.) to interface with QPix. The QPix ASIC is on a separate PCB connected via cables to the carrier board. Primary means of interacting with the firmware is the register map, which is accessed from Petalinux user space addresses. The Z-turn is accessed via a serial UART or Ethernet RJ-45 interface.

The firmware allows control of the QPix serial interface, and also registers QPix event data that has been captured on input pins to the Z-turn. At powerup, certain pins can be set to a low or high level for reset and control. A 3.3V level can be generated on a TRIGGER pin which triggers an external function generator. The function generator produces an artibrary pulse which stimulates an input channel on the QPix ASIC. The firmware marks the time the trigger was sent out by capturing a 64-bit timestamp which has been running since power-up. The timestamp is manually resettable to zero at an arbitrary time. 

Each of 16 QPix output channels is sampled on a 200MHz internal clock and synchronized into the that domain. An pulse from QPix causes the current timestamp to be written into a FIFO (one for each channel). Each FIFO is 64b wide by 4k deep, enough for approximately 20 microseconds of QPix data even if events occurred on every single clock edge. Since QPix pulses are expected to be at least 10ns wide (2x 200MHz clock cycles), all pulses from an "event" (pulse train) should be catpured, since even if the leading edge of an event violates the setup time of a Xilinx flip flop, the next 200MHz clock cycle should capture the still-high level. It is not expected that a single channel's FIFO will fill after a single triggered event on a test bench. There is a known, fixed delay of 5x 200MHz clocks between when a given pulse is registered and when the timestamp is written, which can be accounted for in post-processing. This can be seen in simulation. 

After a triggered event, the FIFO can be read out until empty, and the output is a series of 64b timestamps indicating when QPix pulses were registered for that channel. These timestamps can be compared to the outgoing trigger timestamp to get a relative time between all channel events, and this gives a reconstruction of the all the events. The FIFOs can then reset manually for the next events.

### Directory Structure

|      |      |
| :--- | :--- |
| qpix_tester/ | Contains the recreated Vivado project. Does not need to be source controlled. |
| firmware/src/ | Verilog source files |
| firmware/constr/ | Pin/timing constraint files |
| firmware/sim/ | Simple Verilog testbench |
| firmware/ip/ | Xilinx-specific IP e.g. AXI peripherals and Vivado-generated FIFOs |
| petalinux/config/ | PetaLinux configuration files (not build products) |
| petalinux/recipes/ | C/C++ code intended to be compiled into the PetaLinux distribution |
| scripts/ | Python and shell scripts to use at runtime |
| doc/ | Register map |

### Git Instructions
This project uses Vivado 2020.1 and petalinux 2020.1 in a Linux environment (Ubuntu 16.04.6 LTS is used for development). Ensure you have the third party Z-turn [board definition files](https://github.com/q3k/zturn-stuff/tree/master/boards/board_files/zturn-7z020/2.1) added to your Vivado install. Ensure you have the [PetaLinux dependencies (p10)](https://docs.xilinx.com/v/u/2020.1-English/ug1144-petalinux-tools-reference-guide) installed on your system. 

1. `git pull` changes from remote.
2. Open `vivado` from the `firmware/` directory.
3. In tcl console, run `source ./create_project.tcl`. A new `qpix_tester/` directory will be created.
4. `top_rtl.v` is effectively the top of the design and be altered with any text editor. Other Verilog files can be added to the project in the `src/` directory. (When saving, the design must be refreshed, as Vivado sees the RTL block as an IP.)
5. If the Zynq or AXI peripherals are changed, or any new AXI peripherals added, the .tcl file must be re-written so that the block design can be re-created from a fresh git pull. Go to **File - Project - Write Tcl**. Set the output file to `create_project.tcl`. Check *Write all properties*, *Recreate Block Designs using Tcl*, and *Write object values*. Uncheck *Copy sources to new project*. Check the `git diff` output and ensure no files path names are corrupted before comitting changes.
6. `git commit` all changes and `git push`.


### Simulation
1. The rudimentary simulation is run in Vivado by clicking **Run Simulation - Run Behavioral Simulation** and then running for 8000ns from the top toolbar. An example of serial reigster write, one FIFO event write and read, is provided.

### Building PetaLinux and software
1. First, from Vivado: **File - Export - Export Hardware - Fixed - Include Bitstream** and export a file called *qpix_tester.xsa* to the `qpix_tester/` directory.
2. **File - Export - Export Hardware - Export Bitstream File** and choose the same directory as above. Name the file *qpix_tester.bit*.
3. From the `firmware/` directory on the Linux machine:`petalinux-create -t project -n qpix.linux --template zynq`
4. From the `petalinux/configs/` directory in this repo, copy the `config` and `rootfs_config` files to the `qpix.linux/project-spec/configs/` folder. 
5. `petalinux-config -p qpix.linux/ --get-hw-description qpix_tester/`. This will grab the exported .xsa and .bit files from before. In the graphical menu that pops up, confirm **Image Packaging Configuration - Root filesystem type - EXT4** has been selected properly from the configuration files. (This ensures the image will boot from an ext4 partition on the SD card.)
6. `petalinux-config -p qpix.linux/ -c rootfs` will bring up a graphical menu, and you can confirm that the choices in the `rootfs_config` file are reflected here. (There are several filesystem utilities that will be marked for install based on the file.)
7. The `system-user.dtsi` file in `project-spec/meta-user/recipes-bsp/device-tree/files/` should be empty. If custom device drivers are desired, or if a proprty of an existing hardware device (e.g. the SD card controller) needs to be modified, this file can be modified.
8. From the `petalinux/recipes/` directory, copy the `regtest/` directory to `qpix.linux/project-spec/meta-user/recipes-apps/`. This adds a simple user application to the build <sup>1</sup>. Also copy `petalinux/config/user-rootfsconfig` to `project-spec/meta-user/conf/` (this ensures that user applications are included in the root filesystem).
9. `petalinux-build -p qpix.linux` will take many tens of minutes to build the first time.
10. `petalinux-package -p qpix.linux/ --boot --u-boot --fsbl qpix.linux/images/linux/zynq_fsbl.elf --fpga qpix.linux/images/linux/system.bit -o qpix.linux/images/linux/BOOT.bin` will package the output into a bootable image.
11. From the `qpix.linux/` directory, you can test the build by using `petalinux-boot --qemu --u-boot`. The image will boot virtually, and you can login with password `root` (change this in the config menu from step 5). You can test if simple command line utilities like `peek` were built into the image correctly by typing them at the prompt after logging in. CTRL+A, and then X, will exit a QEMU session.

### Booting
1. Using your favorite partition editor (e.g. `gparted`), create two partitions on an SDHC micro-SD card: a 256MB FAT32 partition named `BOOT`, and the remainder of the disk should be an EXT4 partition called `ROOT`.
2. Copy the following files from `qpix.linux/images/linux/` to the `BOOT` partition: `BOOT.bin`, `image.ub`, `boot.scr`
3. Copy the file `rootfs.tar.gz` to the `ROOT` partition. `gunzip` and then `tar -xvf` the file to uncompress the entire contents.
4. Install the SD card into the Z-turn. Ensure jumper settings are set to boot from SD. After the QPix carrier PCB is turned on, the 5V to Z-turn will power it on and start the boot process (LEDs will go on). After this, connect a mini USB cable to the front panel UART connector (not JTAG connector), and open a connection to the COM port that comes up at 115kbaud.
5. If a roo console does not appear, press the reset button on Z-turn and and stop the boot when the message `Hit any key to stop autoboot` appears. This will show the `Zynq` prompt. You may have to set the correct root partition in U-Boot with `setenv bootargs root=/dev/mmcblk1p2` and `saveenv`. Then `boot` will continue the boot process. 

### Register reads and writes
At the root prompt, registers can be manually written using `poke [addr] [data]` from the table below. For example `poke 0x43c00000 0x00000020` will assert opad\_EXT\_RST. Test scripts (below) initiate sequences of register writes.

1. Control registers (R/W)

| reg. no. | AXI addr. | bit(s) | name | description |
| ------ | ------ | ------ | ------ | ------ |
| 0 | 0x43c00000 | [25:24] | opad2_startup, opad_startup | asserts pads |
| 0 | 0x43c00000 |  [17:16] | clk2_repl_en, clk_repl_en | enables |
| 0 | 0x43c00000 |  [11:10] | opad2_control, opad_control | asserts pads |
| 0 | 0x43c00000 |  [9:8] | opad2_cal_control, opad_cal_control | asserts pads |
| 0 | 0x43c00000 |  [7] | rst_and_trig | asserts both RST_EXT pads for 5us, then sends TRIGGER on falling edge of de-assert |
| 0 | 0x43c00000 |  [6:5] | rst_ext2, rst_ext | asserts pads |
| 0 | 0x43c00000 |  [4] | calibrate | asserts both RST_EXT and cal_control pads, de-asserts RST_EXT and then de-asserts cal_control 100ns after |
| 0 | 0x43c00000 |  [3:2] | pulse_rst_ext2, pulse_rst_ext | sends 5us pulse on pads |
| 0 | 0x43c00000 |  [1] | opad_ext_POR | asserts pad |
| 0 | 0x43c00000 |  [0] | sys_rst | resets internal FPGA logic |
| - | - | - | - | - |
| 1 | 0x43c00004 |  [9] | opad_selDefData | asserts pad |
| 1 | 0x43c00004 |  [8] | load_data | sends 100us pulse on pad |
| 1 | 0x43c00004 |  [2] | xmit | shift data out to pad | 
| 1 | 0x43c00004 |  [1] | load | load 32-bit data word from AXI reg to FPGA shift reg |
| 1 | 0x43c00004 |  [0] | rst | reset FPGA shift reg |
| - | - | - | - | - |
| 2 | 0x43c00008 |  [31:0] | data | 32-bit data to send to QPix |
| - | - | - | - | - |
| 3 | 0x43c0000c |  [9] | opad2_selDefData | asserts pad |
| 3 | 0x43c0000c |  [8] | load_data2 | sends 100us pulse on pad |
| 3 | 0x43c0000c |  [2] | xmit2 | shift data out to pad | 
| 3 | 0x43c0000c |  [1] | load2 | load 32-bit data word from AXI reg to FPGA shift reg |
| 3 | 0x43c0000c |  [0] | rst2 | reset FPGA shift reg |
| - | - | - | - | - |
| 4 | 0x43c00010 |  [31:0] | data2[31:0] | 32-bit data to send to QPix |
| - | - | - | - | - |
| 5 | 0x43c00014 |  [1] | counter_reset | reset FPGA 64-bit counter |
| 5 | 0x43c00014 |  [0] | trigger | assert pad |  
| - | - | - | - | - |
| 6 | 0x43c00018 |  [15:0] | read_fifo[15:0] | trigger read of one of 16 FPGA FIFOs holding timestamped QPix pulse output |

2. Read only registers

| reg. no. | AXI addr. | bit(s) | name | description |
| ------ | ------ | ------ | ------ | ------ |
| 64 | 0x43c00100 | [31:0] | trig_ts[63:32] | high bits of 64-bit timestamp when trigger was issued |
| - | - | - | - | - |
| 65 | 0x43c00104 | [31:0] | trig_ts[31:0] | low bits of 64-bit timestamp when trigger was issued |
| - | - | - | - | - |
| 66 | 0x43c00108 | [31:0] | event_ts[63:32] | current FIFO word, high bits of 64-bit event timestamp from port 0 |
| - | - | - | - | - |
| 67 | 0x43c0010c | [31:0] | event_ts[31:0] | current FIFO word, low bits of 64-bit event timestamp from port 0 |
| - | - | - | - | - |
| - | - | - | - | (continue thru reg 97 for ports 2-15) |
| - | - | - | - | - |
| 109 | 0x43c001b4 | [10] | wr_rst_busy | Port 0 FIFO writing |
| 109 | 0x43c001b4 | [9] | almost_full | Port 0 FIFO almost full |
| 109 | 0x43c001b4 | [8] | full | Port 0 FIFO full |
| 109 | 0x43c001b4 | [2] | rd_rst_busy | Port 0 FIFO reading |
| 109 | 0x43c001b4 | [1] | almost_empty | Port 0 FIFO almost full |
| 109 | 0x43c001b4 | [0] | empty | Port 0 FIFO full |
| - | - | - | - | - |
| - | - | - | - | (continue thru reg 124 for ports 2-15) |
| - | - | - | - | - |
| 127 | 0x43c001fc | [31:0] | `0xdeadbeef` | test word |


### Running test scripts
1. Run `python3 startup.py` to reset internal FPGA logic. (All user scripts are in `scripts/`.)
2. Run `python3 Kickstart.py` to set the two startup pads to logic high and keep then high.
3. Run `python3 set_Thresholds.py [TP|VCOMP] [1|2] [voltage]` to program the 4 DAC channels from 0 - 3.3V.
4. Run `python3 Serial_Interface_rst.py` to assert selDefData and pulse loadData on both QPix serial interfaces.
5. Run `python3 Serial_Interface.py [1|2] [data]` where `1|2` is the interface, and `data` is a 32 bit word in hex format (`0x12345678`). This will shift the word out of the Datain pin to QPix, along with 32 clock pulses on the CLKin pin, an then pulse loadData.
6. Run `python3 Integrator_rst.py [1|2]` to send a 5us pulse on opad_RST_EXT or opad2_RST_EXT.
7. Run `python3 Clock_50MHz.py [on|off]` to enable/disable a 50MHz clock to opad_CLK and opad2_CLK. 
8. Run `python3 Calibrate.py` to assert opad_RST_EXT1,2 high, send a 5us pulse on opad_cal_control1,2, and then deassert the reset pads 100ns after the cal pads deassert.
9. Run `python3 hold_reset.py [1|2] [on|off]` to assert opad_RST_EXT1,2 high or low.
10. Run `python3 send_trigger.py` to assert opad_RST_EXT1,2 for 5us, then send TRIGGER on the falling edge of reset de-assert.
 
## Footnotes
1. This is done by creating an app template as in the [PetaLinux Yocto documentation](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842475/PetaLinux+Yocto+Tips#PetaLinuxYoctoTips-CreatingApps(whichuseslibraries)inPetaLinuxProject)

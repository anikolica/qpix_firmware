#!/bin/bash

# Usage: 
# 1. Upload BOOT.bin, boot.scr and image.ub to /home/root/fw_tmp in the Z-Turn
# 2. From /home/root/software on the Z-Turn, do `bash qpix_remote_fw_upgrade.sh`
# 3. The Z-Turn will reboot. Wait a few seconds before logging back in. The fw
#    will be now upgraded.
echo "---------------------------------------------"
echo "<<<<<<<<< CHECK FIRMWARE BOOT FILES >>>>>>>>>"
echo "---------------------------------------------"

# enable extglob
shopt -s extglob

TMP_DIR=/home/root/fw_tmp
# check if /home/root/fw_tmp exist
# if not, create it
if [ -d "${TMP_DIR}" ]; then
  echo "${TMP_DIR} exist"
else
	echo "${TMP_DIR} created!"
	mkdir ${TMP_DIR}
fi
cd ${TMP_DIR}
# check if BOOT.bin can be found in /home/root/fw_tmp
# if not, exit
if [ -f "BOOT.bin" ]; then
	echo "BOOT.bin found"
else
	echo -e "\033[0;33mBOOT.bin not found!"
	echo -e "Please copy BOOT.bin to ${TMP_DIR} and re-try!\033[0m"
	exit 1
fi
# check if boot.scr can be found in /home/root/fw_tmp
# if not, exit
if [ -f "boot.scr" ]; then
	echo "boot.scr found"
else
	echo -e "\033[0;33mboot.scr not found!"
	echo -e "Please copy boot.scr to ${TMP_DIR} and re-try!\033[0m"
	exit 1
fi
# check if image.ub can be found in /home/root/fw_tmp
# if not, exit
if [ -f "image.ub" ]; then
	echo "image.ub found"
else
	echo -e "\033[0;33mimage.ub not found!"
	echo -e "Please copy image.ub to ${TMP_DIR} and re-try!\033[0m"
	exit 1
fi
# check that only BOOT.bin, boot.scr and image.ub can be found in /home/root/fw_tmp
N_FILE=$(ls -1 | wc -l)
if [[ ${N_FILE} -gt 3 ]]; then
	echo "Other files except BOOT.bin, boot.scr and image.ub found in ${TMP_DIR}!"
	echo "Removing other files except BOOT.bin, boot.scr and image.ub in ${TMP_DIR} ..."
	rm -v !(BOOT.bin|boot.scr|image.ub)
fi

# disable extglob
shopt -u extglob

echo ""

echo "---------------------------------------------"
echo "<<<<<<<<<<< CHECK MOUNT DIRECTORY >>>>>>>>>>>"
echo "---------------------------------------------"

MNT_DIR=/home/root/fw_mnt
# check if /home/root/fw_mnt exist
# if not, create it
if [ -d "${MNT_DIR}" ]; then
  echo "${MNT_DIR} exist"
else
	echo "${MNT_DIR} created!"
	mkdir ${MNT_DIR}
fi

echo ""

echo "--------------------------------------------"
echo "<<<<<<<< UPDATE FIRMWARE BOOT FILES >>>>>>>>"
echo "--------------------------------------------"

cd /home/root
# mount /dev/mmcblk0p1 to /home/root/fw_mnt
echo "Mount /dev/mmcblk0p1 to ${MNT_DIR}"
sudo mount /dev/mmcblk0p1 ${MNT_DIR}
# move firmware boot files from /home/root/fw_tmp to /home/root/fw_mnt
echo "Move firmware boot files from ${TMP_DIR} to ${MNT_DIR}"
sudo mv ${TMP_DIR}/* ${MNT_DIR}/.
echo "IGNORE MESSAGE => mv: failed to preserve ownership for '/home/root/fw_mnt/./BOOT.bin': Operation not permitted"
echo "IGNORE MESSAGE => mv: failed to preserve ownership for '/home/root/fw_mnt/./boot.scr': Operation not permitted"
echo "IGNORE MESSAGE => mv: failed to preserve ownership for '/home/root/fw_mnt/./image.ub': Operation not permitted"

echo ""

echo "--------------------------------------------"
echo "<<<<<<<<< FIRMWARE UPDATE COMPLETE >>>>>>>>>"
echo "--------------------------------------------"

# reboot z-turn
echo "Reboot Z-Turn"
sudo shutdown -r now


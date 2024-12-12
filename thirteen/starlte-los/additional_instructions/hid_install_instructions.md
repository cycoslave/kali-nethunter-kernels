After flashing Nethunter ZIP in Magisk, reboot and follow these step :

1. Go to files, and extract ramdisk-patch from nethunter zip file.

2. Reboot to TWRP

3. Mount System and Vendor partition (or everything to be sure)

4. Enter into a terminal

```
rm /system_root/system/vendor/etc/ueventd.rc
cp /sdcard/ramdisk-patch/ueventd.rc /system_root/system/vendor/etc/
cp /sdcard/ramdisk-patch/init.nethunter.rc /system_root/system/vendor/etc/
chmod 644 /system_root/system/vendor/etc/ueventd.rc
chmod 644 /system_root/system/vendor/etc/init.nethunter.rc
```

5. Reboot to System

6. Open Root Shell Terminal (Android, not nethunter)

Repeat this each time you which to use hid gadget stuff :

```bash
mknod -m 666 /dev/hidg0 c 240 0
mknod -m 666 /dev/hidg1 c 240 1
setprop sys.usb.config win,hid
```

Note : If you was already plugged in the target computer, unplug and plug again the phone)

Done.

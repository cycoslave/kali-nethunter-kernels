# ⚡ Miatoll NetHunter Kernel  
### 🔹 Xiaomi Redmi Note 9S/Pro (miatoll) | Android 15 | Linux Kernel 4.14.336  

[![Kernel Source](https://img.shields.io/badge/Kernel%20Source-GitHub-blue?logo=github)](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250/tree/15.0)  
[![Author](https://img.shields.io/badge/Author-jolucas245-green?logo=github)](https://github.com/jolucas245)  

---

## 📌 Overview  
This is a **custom kernel for Kali NetHunter** on the **Xiaomi Redmi Note 9S/Pro (miatoll)**.  
Based on **Linux Kernel 4.14.336**, built for **Android 15**.  

---

## 🛠️ Build Information  
- **Source:** [crDroid Kernel Source](https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250/tree/15.0)  
- **Base defconfig:** `miatoll_defconfig`  
- **Build system:** Standard **NetHunter Kernel Builder**  

---

## ⚠️ Important Notes  
1. The kernel is provided as **`Image.gz` only**, with **no appended DTB/DTBO**.  
2. DTB/DTBO compilation from this source fails with standard toolchains.  
3. Flashing method must:  
   - **Preserve the original DTB/DTBO** from the stock boot image  
   - **Replace only the kernel image (`Image.gz`)**  
   - Follow logic similar to **AnyKernel3**  
4. This build is intended for **non-A/B variants only**.  

---

## 📦 Installation  
Use a flashing method that respects the requirements above (e.g., modified **AnyKernel3**).  
- Extract the **kernel `Image.gz`**  
- Flash into the **boot.img**, keeping the stock DTB/DTBO intact  

---

## ✅ Status  
- [x] Successful compilation  
- [x] Boot confirmed on Android 15  
- [x] NetHunter installed and Working External Wireless Adapter and Bluetooth

---

✨ Designed for **NetHunter power users** who want to use the miatoll device as an advanced testing platform. 

import os
import shutil

# --- PATHS ---
base_dir = "/root/twrp-source/device/lenovo/TB330FU"
print(f"--- RESETTING TO TWRP 12.1 CONFIG ---")

# 1. ENSURE DIRECTORY EXISTS
if not os.path.exists(base_dir):
    print(f"Error: {base_dir} does not exist!")
    exit(1)

# 2. LOCATE KERNEL BINARIES (Handle 'prebuilts' subfolder)
# We need to find where the kernel is to point the makefile correctly
kernel_path = "$(LOCAL_PATH)/kernel"
dtbo_path = "$(LOCAL_PATH)/dtbo.img"
dtb_path = "$(LOCAL_PATH)/dtb"

if os.path.exists(os.path.join(base_dir, "prebuilts", "kernel")):
    print("Detected kernel in 'prebuilts' subfolder.")
    kernel_path = "$(LOCAL_PATH)/prebuilts/kernel"
    dtbo_path = "$(LOCAL_PATH)/prebuilts/dtbo.img"
    dtb_path = "$(LOCAL_PATH)/prebuilts/dtb.img" # Often renamed to .img

# 3. WRITE omni_TB330FU.mk (The Entry Point)
omni_mk = """$(call inherit-product, $(SRC_TARGET_DIR)/product/languages_full.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device
$(call inherit-product, device/lenovo/TB330FU/device.mk)

PRODUCT_NAME := omni_TB330FU
PRODUCT_DEVICE := TB330FU
PRODUCT_MANUFACTURER := lenovo
PRODUCT_BRAND := lenovo
PRODUCT_MODEL := TB330FU
"""
with open(os.path.join(base_dir, "omni_TB330FU.mk"), "w") as f:
    f.write(omni_mk)
print(" - Wrote omni_TB330FU.mk")

# 4. WRITE AndroidProducts.mk
products_mk = """PRODUCT_MAKEFILES := \\
    $(LOCAL_DIR)/omni_TB330FU.mk

COMMON_LUNCH_CHOICES := \\
    omni_TB330FU-eng
"""
with open(os.path.join(base_dir, "AndroidProducts.mk"), "w") as f:
    f.write(products_mk)
print(" - Wrote AndroidProducts.mk")

# 5. WRITE BoardConfig.mk (Specific to TB330FU)
board_config = f"""
# Architecture
TARGET_ARCH := arm64
TARGET_ARCH_VARIANT := armv8-a
TARGET_CPU_ABI := arm64-v8a
TARGET_BOARD_PLATFORM := mt6768

# Boot & Kernel
BOARD_KERNEL_CMDLINE := bootopt=64S3,32N2,64N2
BOARD_KERNEL_BASE := 0x40078000
BOARD_KERNEL_PAGESIZE := 4096
TARGET_PREBUILT_KERNEL := {kernel_path}
BOARD_PREBUILT_DTBOIMAGE := {dtbo_path}
BOARD_INCLUDE_DTB_IN_BOOTIMG := true
BOARD_MKBOOTIMG_ARGS += --header_version 2

# Partitions
BOARD_BOOTIMAGE_PARTITION_SIZE := 33554432
BOARD_USERDATAIMAGE_PARTITION_SIZE := 9122611200 # Approx from logs

# Recovery-as-Boot (CRITICAL)
BOARD_USES_RECOVERY_AS_BOOT := true
TARGET_NO_RECOVERY := true
TARGET_RECOVERY_FSTAB := $(LOCAL_PATH)/recovery.fstab

# TWRP UI & Flags
TW_THEME := portrait_hdpi
TARGET_SCREEN_WIDTH := 1200
TARGET_SCREEN_HEIGHT := 1920
TW_NO_REBOOT_BOOTLOADER := true
TW_INCLUDE_NTFS_3G := true
"""
with open(os.path.join(base_dir, "BoardConfig.mk"), "w") as f:
    f.write(board_config)
print(" - Wrote BoardConfig.mk")

# 6. WRITE device.mk
device_mk = """$(call inherit-product, $(SRC_TARGET_DIR)/product/languages_full.mk)
PRODUCT_COPY_FILES += \\
    $(LOCAL_PATH)/recovery.fstab:$(TARGET_COPY_OUT_RECOVERY)/root/system/etc/recovery.fstab
"""
with open(os.path.join(base_dir, "device.mk"), "w") as f:
    f.write(device_mk)
print(" - Wrote device.mk")

print("SUCCESS: Configuration normalized.")

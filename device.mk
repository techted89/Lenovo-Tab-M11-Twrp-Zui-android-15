$(call inherit-product, $(SRC_TARGET_DIR)/product/languages_full.mk)
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/recovery.fstab:$(TARGET_COPY_OUT_RECOVERY)/root/system/etc/recovery.fstab

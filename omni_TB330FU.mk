$(call inherit-product, $(SRC_TARGET_DIR)/product/languages_full.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device
$(call inherit-product, device/lenovo/TB330FU/device.mk)

PRODUCT_NAME := omni_TB330FU
PRODUCT_DEVICE := TB330FU
PRODUCT_MANUFACTURER := lenovo
PRODUCT_BRAND := lenovo
PRODUCT_MODEL := TB330FU

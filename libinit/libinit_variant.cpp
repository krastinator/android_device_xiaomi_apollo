/*
 * Copyright (C) 2021 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <android-base/logging.h>
#include <android-base/properties.h>
#include <libinit_utils.h>

#include <libinit_variant.h>

using android::base::GetProperty;

#define HWC_PROP "ro.boot.hwc"
#define SKU_PROP "ro.boot.product.hardware.sku"

void search_variant(const std::vector<variant_info_t> variants) {
    std::string hwc_value = GetProperty(HWC_PROP, "");
    std::string sku_value = GetProperty(SKU_PROP, "");

    for (const auto& variant : variants) {
        if ((variant.hwc_value == "" || variant.hwc_value == hwc_value) &&
            (variant.sku_value == "" || variant.sku_value == sku_value)) {
            set_variant_props(variant);
            break;
        }
    }
}

void set_variant_props(const variant_info_t variant) {
    // Older devices don't have marketname
    auto marketname = !variant.marketname.empty() ? variant.marketname : variant.model;

    set_ro_build_prop("brand", variant.brand, true);
    set_ro_build_prop("device", variant.device, true);
    set_ro_build_prop("name", variant.name, true);
    set_ro_build_prop("marketname", variant.marketname, true);
    set_ro_build_prop("mod_device", variant.mod_device, true);
    set_ro_build_prop("model", variant.model, true);
    property_override("vendor.usb.product_string", marketname, true);

    if (access("/system/bin/recovery", F_OK) != 0) {
        property_override("bluetooth.device.default_name", marketname, true);
        set_ro_build_prop("fingerprint", variant.build_fingerprint);
        property_override("ro.bootimage.build.fingerprint", variant.build_fingerprint);

        property_override("ro.build.description", fingerprint_to_description(variant.build_fingerprint));
    }

    if (variant.nfc)
        property_override(SKU_PROP, "nfc");
}

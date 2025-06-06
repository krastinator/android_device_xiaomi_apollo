#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/camera/camxoverridesettings.txt': blob_fixup()
        .regex_replace('0x10098', '0')
        .regex_replace('0x1F', '0x0'),
    'vendor/etc/init/init.batterysecret.rc': blob_fixup()
        .regex_replace('.*seclabel u:r:batterysecret:s0\n', ''),
    'vendor/etc/libnfc-nci.conf': blob_fixup()
        .add_line_if_missing('LEGACY_MIFARE_READER=1'),
    'vendor/lib64/camera/components/com.mi.node.watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    (
        'vendor/lib64/libMIAIHDRhvx_interface.so',
        'vendor/lib64/libarcsoft_hdrplus_hvx_stub.so',
        'vendor/lib64/libarcsoft_super_night_raw.so',
        'vendor/lib64/libmialgo_rfs.so',
    ): blob_fixup()
        .clear_symbol_version('remote_handle_close')
        .clear_symbol_version('remote_handle_invoke')
        .clear_symbol_version('remote_handle_open')
        .clear_symbol_version('remote_register_buf')
        .clear_symbol_version('remote_register_buf_attr'),
    (
        'vendor/lib64/libalAILDC.so',
        'vendor/lib64/libalLDC.so',
        'vendor/lib64/libalhLDC.so',
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/lib64/vendor.qti.hardware.camera.postproc@1.0-service-impl.so': blob_fixup()
        .binary_regex_replace(b'\x9A\x0A\x00\x94', b'\x1F\x20\x03\xD5'),
    'system_ext/lib64/libwfdmmsrc_system.so': blob_fixup()
        .add_needed('libgui_shim.so'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .add_needed('libbinder_shim.so')
        .add_needed('libinput_shim.so'),
    'vendor/etc/init/init.mi_thermald.rc': blob_fixup()
        .regex_replace('.*seclabel u:r:mi_thermald:s0\n', ''),
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': blob_fixup()
        .add_line_if_missing('gettid: 1'),
    'vendor/etc/seccomp_policy/codec2.vendor.base-arm.policy': blob_fixup()
        .regex_replace('futex: 1', '')
        .add_line_if_missing('futex: 1'),
    'vendor/etc/seccomp_policy/codec2.vendor.ext-arm.policy': blob_fixup()
        .regex_replace('_llseek: 1', '')
        .regex_replace('getdents64: 1', ''),
    'vendor/lib64/libril-qc-hal-qmi.so': blob_fixup()
        .binary_regex_replace(b'ro.product.vendor.device', b'ro.vendor.radio.midevice'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'vendor/lib64/mediadrm/libwvdrmengine.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
    (
     'vendor/lib/libstagefright_soft_ac4dec.so',
     'vendor/lib/libstagefright_soft_ddpdec.so',
     'vendor/lib/libstagefrightdolby.so',
     'vendor/lib64/libdlbdsservice.so',
     'vendor/lib64/libstagefright_soft_ac4dec.so',
     'vendor/lib64/libstagefright_soft_ddpdec.so',
     'vendor/lib64/libstagefrightdolby.so'
     ): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
}  # fmt: skip


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libmmosal',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
}

namespace_imports = [
    'device/xiaomi/apollo',
    'hardware/qcom-caf/sm8250',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

module = ExtractUtilsModule(
    'apollo',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

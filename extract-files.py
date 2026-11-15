#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'vendor/infinix/X6840'
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('vendor.mediatek.hardware.videotelephony@1.0',): lib_fixup_vendor_suffix,
    ('libsink',): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/lib64/libsink.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    'system_ext/lib64/libsource.so': blob_fixup()
        .add_needed('libui_shim.so'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so': blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    'vendor/bin/hw/vendor.mediatek.hardware.mtkpower@1.0-service': blob_fixup()
        .replace_needed('android.hardware.power-V2-ndk_platform.so', 'android.hardware.power-V2-ndk.so'),
    ('vendor/bin/mnld', 'vendor/lib64/libaalservice.so'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/libmnl.so' : blob_fixup()
        .add_needed('libcutils.so'),
    'vendor/lib64/android.hardware.sensors@2.X-subhal-mediatek.so' : blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),
    ('vendor/lib/libnvram.so', 'vendor/lib64/libnvram.so', 'vendor/lib64/libsysenv.so') : blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/bin/hw/android.hardware.usb@1.2-service-mediatekv2'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/bin/ccci_rpcd'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/bin/hw/mtkfusionrild'): blob_fixup()
        .add_needed('libbase_shim.so'),
    'vendor/lib64/hw/hwcomposer.mt6768.so' : blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    # Transsion libs not carried (no symbols imported, verified with nm)
    'vendor/lib64/libmtkcam_3rdparty.customer.so': blob_fixup()
        .remove_needed('libcam3_transerverengine.so')
        .remove_needed('libTran_mtkPowerAPI.so'),
    'vendor/lib64/libcodec2_mtk_vdec.so': blob_fixup()
        .remove_needed('libcodec2_vpp_rs_tran_shju_plugin.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'X6840',
    'infinix',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

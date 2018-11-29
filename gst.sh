#!/bin/bash

export CONAN_DATA=${HOME}/.conan/data
export GST_VERSION=1.14.3
export GLIB_ROOT=${CONAN_DATA}/glib/2.54.3/user/channel/package/cd8ad4ab2d0b217066651b0b2282a98a5c61f2a2
export GST_ROOT=${CONAN_DATA}/gstreamer/${GST_VERSION}/user/channel/package/dd3a1ce7318b5ad4b4a01d10c038af489a93a69d
export GST_BASE_ROOT=${CONAN_DATA}/gst-plugins-base/${GST_VERSION}/user/channel/package/eaf1e6e9a26e8dac0758f74a2454cf192b5fe979
export GST_GOOD_ROOT=${CONAN_DATA}/gst-plugins-good/${GST_VERSION}/user/channel/package/00f62a56f221379aa147b360d636c1e1a9341031
export GST_BAD_ROOT=${CONAN_DATA}/gst-plugins-bad/${GST_VERSION}/user/channel/package/132e83b9bca843e4e525d7eadad6dbd9a7d6cc95
export GST_UGLY_ROOT=${CONAN_DATA}/gst-plugins-ugly/${GST_VERSION}/user/channel/package/436084e19fe0108fda079b4c6011f87ecbf8869d
export GST_PLUGIN_SYSTEM_PATH_1_0=${GST_ROOT}/lib/gstreamer-1.0:${GST_BASE_ROOT}/lib/gstreamer-1.0:${GST_GOOD_ROOT}/lib/gstreamer-1.0:${GST_BAD_ROOT}/lib/gstreamer-1.0:${GST_UGLY_ROOT}/lib/gstreamer-1.0
export GST_REGISTRY_1_0=${CONAN_DATA}/.cache/gstreamer-1.0/registry
export GST_PLUGIN_SCANNER_1_0=${GST_ROOT}/libexec/gstreamer-1.0/gst-plugin-scanner
export PATH=$GST_ROOT/bin:$GST_BASE_ROOT/bin:$GST_GOOD_ROOT/bin:$GST_BAD_ROOT/bin:$GST_UGLY_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$GST_ROOT/lib:$GST_BASE_ROOT/lib:$GST_GOOD_ROOT/lib:$GST_BAD_ROOT/lib:$GST_UGLY_ROOT/lib:$GLIB_ROOT/lib

$SHELL "$@"
from conans import ConanFile, CMake, tools
import os

class WebrtcaudioprocessingConan(ConanFile):
    name = "webrtc-audio-processing"
    version = "0.2"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Webrtcaudioprocessing here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://172.16.64.65:8081/artifactory/gstreamer/{0}-{1}.tar.xz'.format(name, version)
    patches = [ 'webrtc-audio-processing/0000-Add-sal.h-as-it-s-missing-in-cerbero-mingw.patch',
                'webrtc-audio-processing/0000-Add-fix_interlocked_exchange_pointer_win.h.patch',
                'webrtc-audio-processing/0001-build-enforce-linking-with-no-undefined-add-explicit.patch',
                'webrtc-audio-processing/0002-build-Make-sure-files-with-SSE2-code-are-compiled-wi.patch',
                'webrtc-audio-processing/0003-Don-t-include-execinfo.h-for-windows.patch',
                'webrtc-audio-processing/0004-Don-t-use-MSVC-specific-exception-handler-for-MINGW.patch',
                'webrtc-audio-processing/0005-Add-missing-throw-in-destructor-override.patch',
                'webrtc-audio-processing/0006-lrint-is-available-with-mingw.patch',
                'webrtc-audio-processing/0007-Fix-case-sensitivity-issue-with-MinGW-cross-build.patch',
                'webrtc-audio-processing/0008-Add-missing-windows-specific-headers.patch',
                'webrtc-audio-processing/0009-Fix-build-on-win64.patch',
                'webrtc-audio-processing/0010-Add-cerbero-gnustl-support-for-Android.patch',
                'webrtc-audio-processing/0011-Disable-backtrace-on-android.patch',
                'webrtc-audio-processing/0012-Don-t-blindly-link-to-pthread.patch',
                'webrtc-audio-processing/0013-Add-required-define-for-Windows.patch',
                'webrtc-audio-processing/0014-Properly-select-the-right-system-wrappers.patch',
                'webrtc-audio-processing/0015-Fix-case-sensitivity-in-windows-include.patch',
                'webrtc-audio-processing/0016-Define-MSVC-_WIN32-so-we-can-build-on-mingw.patch',
                'webrtc-audio-processing/0017-Add-missing-windows-conditions-variable.patch',
                'webrtc-audio-processing/0018-Protect-against-unsupported-CPU-types.patch',
                'webrtc-audio-processing/0019-osx-Fix-type-OS_FLAGS-instead-of-OS_CFLAGS.patch',
                'webrtc-audio-processing/0020-Sync-defines-and-libs-with-build.gn.patch',
                'webrtc-audio-processing/0021-Use-no-undefined-to-support-both-clang-and-gcc.patch',
                'webrtc-audio-processing/0022-Re-add-pthread-linking-on-linux.patch',
                'webrtc-audio-processing/0023-Add-ARM-64bit-support.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        self.run("autoreconf -f -i")
        self.run('./configure --prefix %s/build --libdir %s/build/lib --enable-introspection'%(os.getcwd(),os.getcwd()))
        self.run('make -j4')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["webrtc-audio-processing"]


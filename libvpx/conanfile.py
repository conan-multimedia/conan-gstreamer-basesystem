from conans import ConanFile, CMake, tools
import os

class LibvpxConan(ConanFile):
    name = "libvpx"
    version = "v1.6.0"
    license = "BSD"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libvpx here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    patches = ['libvpx/0001-build-Fix-the-min-version-flag-for-iOS-simulator-bui.patch',
               'libvpx/0002-Include-Android-cpu-features.c-instead-of-.h.patch',
               'libvpx/0003-configure-Add-back-the-armv5te-android-gcc-target.patch',
               'libvpx/0004-build-Remove-broken-custom-android-toolchain-usage.patch',
               'libvpx/0005-configure-Add-Android-ARM64-support.patch',
               'libvpx/0006-Don-t-embed-bitcode-on-iOS-until-we-support-that-pro.patch',
               'libvpx/0001-Add-visibility-protected-attribute-for-global-variab.patch',
               ]
    remotes = {'origin': 'https://github.com/webmproject/libvpx.git'}
    commit = 'v1.6.0'
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("git init")
        for key, val in self.remotes.items():
            self.run("git remote add %s %s"%(key, val))
        self.run("git fetch --all")
        self.run("git reset --hard %s"%(self.version))
        self.run("git submodule init && git submodule sync && git submodule update")
        self.run("git reset --hard %s"%(self.version))
        self.run("git branch cerbero_build && git checkout cerbero_build")
        self.run("git reset --hard %s"%(self.version))
        self.run("git config user.email")
        self.run("git config user.name")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        self.run('./configure --prefix=%s/build --libdir=%s/build/lib --enable-pic --as=yasm --disable-unit-tests'
        ' --size-limit=16384x16384 --enable-postproc --enable-multi-res-encoding --enable-temporal-denoising'
        ' --enable-vp9-temporal-denoising --enable-vp9-postproc --enable-shared  --disable-examples --target=x86_64-linux-gcc'
        %(os.getcwd(),os.getcwd()))
        self.run('make HAVE_GNU_STRIP=no -j4')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libvpx"]


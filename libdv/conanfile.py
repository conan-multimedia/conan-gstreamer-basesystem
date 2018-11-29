from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibdvConan(ConanFile):
    name = "libdv"
    version = "1.0.0"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libdv here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://sourceforge.net/projects/libdv/files/libdv/1.0.0/libdv-1.0.0.tar.gz'
    patches = ['libdv/0001-Check-properly-for-sched_setscheduler.patch',
               'libdv/0003-Don-t-build-test-programs.patch',
               'libdv/0004-Fix-compilation-on-Android.patch',
               'libdv/0005-Fix-compilation-on-Windows-some-more.patch',
               'libdv/0006-Add-the-pthread-libs-to-pkg-config.patch',
               'libdv/0007-Don-t-require-libsdl-to-be-installed-for-autoreconf.patch',
               'libdv/0012-Build-a-DLL-on-Windows.patch',
               'libdv/0013-Fix-endianess-detection-with-mingw-w64.patch',
               'libdv/0014-libdv-fix-build-of-gasmoff-after-autoreconf.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name, self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        self.run("autoreconf -f -i")
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
            ' --disable-silent-rules --enable-introspection'%(os.getcwd(),os.getcwd()))
        self.run("make -j4")
        self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libdv"]


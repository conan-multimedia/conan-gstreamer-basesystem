from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibvisualConan(ConanFile):
    name = "libvisual"
    version = "0.4.0"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libvisual here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://sourceforge.net/projects/libvisual/files/libvisual/libvisual-0.4.0/libvisual-0.4.0.tar.bz2'
    patches = ['libvisual/0001-Check-properly-for-sched_setshceduler.patch',
               'libvisual/0003-Add-long-long-check-for-win64.patch',
               'libvisual/0005-Fix-compilation-in-win64.patch',
               'libvisual/0006-Fix-build-in-PPC.patch',
               'libvisual/0007-Fix-build-on-debian-squeeze.patch',
               'libvisual/0008-Remove-malloc-realloc-configure-checks-they-re-broke.patch',
               'libvisual/0009-Fix-build-for-Android-X86.patch',
               'libvisual/0010-Only-define-inline-and-friends-if-they-re-not-define.patch',
               'libvisual/0011-Fix-autoreconf-when-using-our-gettext-version.patch',
               'libvisual/0012-configure-gettext-0.18-is-enough-no-0.18.2-needed.patch',
               'libvisual/0013-Include-lv_cpu.h-for-visual_cpu_initialize.patch',
               'libvisual/0014-Add-forward-declaration-of-visual_transform_init-as-.patch',
               'libvisual/0015-Include-lv_cpu.h-in-another-place-too.patch',
               'libvisual/0016-configure.ac-Use-gettext-0.19.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -jxvf %s-%s.tar.bz2 --strip-components 1"%(self.name, self.version))

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
        self.run('./configure --prefix %s/build --libdir %s/build/lib'
            ' --disable-maintainer-mode --disable-silent-rules --enable-introspection --enable-static'%(os.getcwd(), os.getcwd()))
        self.run('make -j2')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libvisual"]


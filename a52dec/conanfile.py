from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class A52decConan(ConanFile):
    name = "a52dec"
    version = "0.7.4"
    license = "GPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of A52dec here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://liba52.sourceforge.net/files/a52dec-0.7.4.tar.gz'
    patches = ['a52dec/0002-Fix-link-cross-compiling-to-x86-in-darwin-platforms.patch',
               'a52dec/0003-Disable-AC_C_ALWAYS_INLINE.patch',
               'a52dec/0004-configure-let-us-decide-if-we-really-want-PIC-or-not.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name,self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))

    def build(self):
        vars = {'LIBS' : "-lm"}

        with tools.environment_append(vars):
            self.run("autoreconf -f -i")
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/autotools/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/autotools/config.sub"%(os.getcwd()))
            self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
            ' --disable-silent-rules --enable-introspection --with-pic --enable-shared'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["a52dec"]


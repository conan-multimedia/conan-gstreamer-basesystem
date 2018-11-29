from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class Libtasn1Conan(ConanFile):
    name = "libtasn1"
    version = "4.13"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libtasn1 here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://ftp.gnu.org/gnu/libtasn1/libtasn1-{0}.tar.gz'.format(version)
    patches = ['libtasn1/0001-Rename-gnulib-symbols.patch']
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
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/build-aux/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/build-aux/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
            ' --disable-silent-rules --enable-introspection --disable-doc'%(os.getcwd(),os.getcwd()))
        self.run('make -j4')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libtasn1"]


from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class FribidiConan(ConanFile):
    name = "fribidi"
    version = "0.19.7"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Fribidi here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libffi/3.99999@user/channel","glib/2.54.3@user/channel"

    patches = ['fribidi/0001-fribidi.def-Include-all-required-symbols.patch',
               'fribidi/0002-fribidi-disable-docs.patch']
    download_url = 'https://github.com/fribidi/fribidi/releases/download/{0}/fribidi-{0}.tar.bz2'.format(version)
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
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))


    def build(self):
        self.run("autoreconf -f -i")
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
            ' --disable-silent-rules --enable-introspection --enable-shared --enable-static'%(os.getcwd(),os.getcwd()))
        self.run('make -j4')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["fribidi"]


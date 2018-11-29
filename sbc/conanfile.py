from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class SbcConan(ConanFile):
    name = "sbc"
    version = "1.3"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Sbc here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    patches = ['sbc/0001-sbc-Use-stdint.h.patch',
    	       'sbc/0002-Don-t-use-NEON-with-aarch64-on-Clang.patch']
    download_url = 'http://172.16.64.65:8081/artifactory/gstreamer/sbc-1.3.tar.gz'
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
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
        ' --disable-silent-rules --enable-introspection --disable-tester --disable-tools'%(os.getcwd(),os.getcwd()))
        self.run('make -j4')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["sbc"]


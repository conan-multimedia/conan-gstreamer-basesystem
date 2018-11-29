from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class ExpatConan(ConanFile):
    name = "expat"
    version = "2.2.5"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Expat here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'https://github.com/libexpat/libexpat/releases/download/R_2_2_5/expat-2.2.5.tar.bz2'
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -jxvf %s-%s.tar.bz2 --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/conftools/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/conftools/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
                 ' --disable-silent-rules --enable-introspection'%(os.getcwd(),os.getcwd()))
        self.run("make -j2")
        self.run("make install")

    def package(self):
        self.copy("*", src="build")


    def package_info(self):
        self.cpp_info.libs = ["expat"]


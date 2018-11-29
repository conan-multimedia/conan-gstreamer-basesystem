from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibunwindConan(ConanFile):
    name = "libunwind"
    version = "1.1"
    license = "MIT"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libunwind here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://172.16.64.65:8081/artifactory/gstreamer/libunwind-1.1.tar.gz'
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name,self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/aux/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/aux/config.sub"%(os.getcwd()))
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
        ' --disable-silent-rules --enable-introspection'%(os.getcwd(),os.getcwd()))
        self.run("make -j4")
        self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libunwind"]


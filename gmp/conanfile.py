from conans import ConanFile, CMake, tools
import os

class GmpConan(ConanFile):
    name = "gmp"
    version = "6.1.2"
    license = "LGPLv3Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gmp here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://ftp.gnu.org/gnu/gmp/gmp-6.1.2.tar.xz'

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        self.run("./configure --prefix %s/build --libdir %s/build/lib --enable-introspection"%(os.getcwd(),os.getcwd()))
        self.run("make -j4")
        self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gmp"]


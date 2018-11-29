from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class NettleConan(ConanFile):
    name = "nettle"
    version = "3.4"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Nettle here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "gmp/6.1.2@user/channel"

    download_url = 'http://ftp.gnu.org/gnu/{0}/{0}-{1}.tar.gz'.format(name, version)
    patches = ['nettle/0001-ios-fix-build-using-.word-for-assembly-constants.patch']
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
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig"%(self.deps_cpp_info["gmp"].rootpath),
        'LD_LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),
        'LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),
        'C_INCLUDE_PATH' : "%s/include"%(self.deps_cpp_info["gmp"].rootpath)}

        with tools.environment_append(vars):
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
            self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
                ' --disable-silent-rules  --enable-introspection   --enable-shared --enable-public-key'%(os.getcwd(),os.getcwd()))
            self.run("make")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["nettle"]


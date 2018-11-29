from conans import ConanFile, CMake, tools
import os

class LibpngConan(ConanFile):
    name = "libpng"
    version = "1.6.34"
    license = "LibPNG"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libpng here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "zlib/1.2.11@user/channel"

    download_url = 'http://download.sourceforge.net/libpng/libpng-1.6.34.tar.xz'
    patches = ['libpng/0001-neon-fix-function-export-names-for-iOS-armv7.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig"%(self.deps_cpp_info["zlib"].rootpath,)}

        with tools.environment_append(vars):
            self.run("./configure --prefix %s/build --libdir %s/build/lib --enable-introspection"%(os.getcwd(),os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libpng"]


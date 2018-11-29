from conans import ConanFile, CMake, tools
import os

class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    license = "BSD-like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Zlib here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://zlib.net/fossils/zlib-1.2.11.tar.gz'
    patches = ['zlib/0001-win32-fix-dll-name.patch',
               'zlib/0001-Fix-test-builds-to-use-the-built-libz-headers-librar.patch']
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
        self.run("./configure --prefix %s/build --libdir %s/build/lib"%(os.getcwd(),os.getcwd()))
        self.run("make -j2")
        self.run("make install")

    def package(self):
        self.copy("*", src="build")
        ## !FIXME PC PREFIX

    def package_info(self):
        self.cpp_info.libs = ["zlib"]


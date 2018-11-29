from conans import ConanFile, CMake, tools
import os


class Bzip2Conan(ConanFile):
    name = "bzip2"
    version = "1.0.6"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Bzip2 here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'https://gstreamer.freedesktop.org/src/mirror/bzip2-%s.tar.gz'%(version)
    patches = ['bzip2/0001-Fix-Makefiles-and-add-support-for-Windows-and-OS-X.patch']
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
        self.run("make -f Makefile-libbz2_so; make EXT=")
        self.run("make -f Makefile-libbz2_so install PREFIX=%s/build; make install EXT= PREFIX=%s/build"%(os.getcwd(),os.getcwd()))

    def package(self):
        self.copy("*", src="build")
        self.run("ln -s libbz2.so.1.0.6 libbz2.so")
        self.copy("libbz2.so*", dst="lib")

    def package_info(self):
        self.cpp_info.libs = ["bzip2"]


from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class PixmanConan(ConanFile):
    name = "pixman"
    version = "0.34.0"
    license = "MIT"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Pixman here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'https://www.cairographics.org/releases/pixman-%s.tar.gz'%(version)
    patches = ['pixman/0001-Fix-build-on-Android.patch',
               'pixman/0002-Enable-CPU-detection-on-Android.patch',
               'pixman/0003-Fix-build-with-clang-5.patch']
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
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
                 ' --disable-silent-rules  --enable-introspection'%(os.getcwd(),os.getcwd()))
        self.run("make -j2")
        self.run("make install")

    def package(self):
        self.copy("*", src="build")


    def package_info(self):
        self.cpp_info.libs = ["pixman"]


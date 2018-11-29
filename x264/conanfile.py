from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class X264Conan(ConanFile):
    name = "x264"
    version = "20161218-2245"
    license = "GPL"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of X264 here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://download.videolan.org/pub/x264/snapshots/x264-snapshot-20161218-2245-stable.tar.bz2'
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s -O %s-%s.tar.bz2"%(self.download_url, self.name, self.version))
        self.run("tar -jxvf %s-%s.tar.bz2 --strip-components 1"%(self.name, self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        vars = {'AS': 'yasm'}

        with tools.environment_append(vars):
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
            self.run('./configure --prefix=%s/build --libdir=%s/build/lib --enable-introspection'
            ' --enable-shared --enable-static --enable-pic --disable-strip --disable-lavf'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["x264"]


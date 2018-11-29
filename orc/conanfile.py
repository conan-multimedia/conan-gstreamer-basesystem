from conans import ConanFile, CMake, tools
import os

class OrcConan(ConanFile):
    name = "orc"
    version = "0.4.28"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Orc here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    remotes = {'origin': 'https://anongit.freedesktop.org/git/gstreamer/orc'}
    commit = 'orc-0.4.28'

    def source(self):
        self.run("git init")
        for key, val in self.remotes.items():
            self.run("git remote add %s %s"%(key, val))
        self.run("git fetch --all")
        self.run("git reset --hard %s"%(self.commit))
        self.run("git submodule init && git submodule sync && git submodule update")
        self.run("git reset --hard %s"%(self.commit))
        self.run("git branch cerbero_build && git checkout cerbero_build")
        self.run("git reset --hard %s"%(self.commit))
        self.run("git config user.email")
        self.run("git config user.name")

    def build(self):
        self.run("autoreconf -f -i")
        self.run('./configure --prefix %s/build --libdir %s/build/lib'
            ' --enable-introspection --enable-static --disable-gtk-doc'%(os.getcwd(),os.getcwd()))
        self.run("make -j2")
        self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["orc"]


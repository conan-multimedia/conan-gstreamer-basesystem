from conans import ConanFile, CMake, tools
import os

class LibffiConan(ConanFile):
    name = "libffi"
    version = "3.99999"
    license = "BSD-like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libffi here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    remotes = {'origin': 'https://github.com/atgreen/libffi.git'}
    commit = '60e4250a77eb3fde500bfd68ec40519fe34b21bd'
    patches = ['libffi/0001-libffi-Don-t-be-smart-about-toolexeclibdir.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

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
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))

    def build(self):
        self.run("autoreconf -f -i")
        self.run("./configure --prefix %s/build --libdir %s/build/lib --enable-introspection"%(os.getcwd(),os.getcwd()))
        self.run("make -j2")
        self.run("make install")

    def package(self):
        ##!TODO: FIX PC PREFIX
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libffi"]


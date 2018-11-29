from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class FreetypeConan(ConanFile):
    name = "freetype"
    version = "2.9"
    license = "FreeType"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Freetype here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "zlib/1.2.11@user/channel", "bzip2/1.0.6@user/channel", "libpng/1.6.34@user/channel"

    download_url = 'http://172.16.64.65:8081/artifactory/gstreamer/freetype-%s.tar.bz2'%(version)
    patches = ['freetype/0001-pngshim-Workaround-buggy-mingw-compiler.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -jxvf %s-%s.tar.bz2 --strip-components 1"%(self.name, self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"%(self.deps_cpp_info["zlib"].rootpath,
                                                                                         self.deps_cpp_info["bzip2"].rootpath,
                                                                                         self.deps_cpp_info["libpng"].rootpath)}
    
        with tools.environment_append(vars):
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/builds/unix/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/builds/unix/config.sub"%(os.getcwd()))
            self.run("./configure --prefix=%s/build --libdir=%s/build/lib --with-harfbuzz=no --enable-introspection"%(os.getcwd(),os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")
        ## !FIXME PC PREFIX

    def package_info(self):
        self.cpp_info.libs = ["hello"]


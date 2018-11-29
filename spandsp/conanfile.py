from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class SpandspConan(ConanFile):
    name = "spandsp"
    version = "0.0.6"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Spandsp here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "tiff/4.0.9@user/channel"

    download_url = 'http://172.16.64.65:8081/artifactory/gstreamer/spandsp-0.0.6.tar.gz'
    patches = [ 'spandsp/0001-spandsp-do-not-compile-has_X86FEATURE-symbols.patch',
                'spandsp/0002-Define-LIBSPANDSP_EXPORTS-when-building-the-spandsp-.patch',
                'spandsp/0003-Use-BUILT_SOURCES-to-generate-extra-headers.patch',
                'spandsp/0001-Don-t-do-a-whereis-which-dance-to-find-which.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name,self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig"%(self.deps_cpp_info["tiff"].rootpath),
        'LIBRARY_PATH':"%s/lib"%(self.deps_cpp_info["tiff"].rootpath),
        'C_INCLUDE_PATH':"%s/include"%(self.deps_cpp_info["tiff"].rootpath)}

        with tools.environment_append(vars):
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config/config.sub"%(os.getcwd()))
            self.run('sh ./autogen.sh && sh ./configure --prefix %s/build --libdir %s/build/lib'
            ' --disable-maintainer-mode --disable-silent-rules --enable-introspection'%(os.getcwd(),os.getcwd()))
            self.run("make")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["spandsp"]


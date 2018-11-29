from conans import ConanFile, CMake, tools
import os

class GobjectintrospectionConan(ConanFile):
    name = "gobject-introspection"
    version = "1.54.1"
    license = "GPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gobjectintrospection here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libffi/3.99999@user/channel","glib/2.54.3@user/channel"

    download_url = 'http://ftp.gnome.org/pub/GNOME/sources/gobject-introspection/1.54/gobject-introspection-%s.tar.xz'%(version)

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")


    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig"%(self.deps_cpp_info["libffi"].rootpath,
                                                                        self.deps_cpp_info["glib"].rootpath)}
        with tools.environment_append(vars):
            self.run("gtkdocize && autoreconf -vfi")
            self.run("./configure --prefix %s/build --libdir %s/build/lib --enable-introspection"%(os.getcwd(),os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gobject-introspection"]


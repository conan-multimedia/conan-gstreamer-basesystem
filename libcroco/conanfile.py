from conans import ConanFile, CMake, tools
import os

class LibcrocoConan(ConanFile):
    name = "libcroco"
    version = "0.6.12"
    license = "LGPLv2_1"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libcroco here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("libffi/3.99999@user/channel","glib/2.54.3@user/channel",
    "gdk-pixbuf/2.36.2@user/channel","libxml2/2.9.7@user/channel")

    download_url = 'http://ftp.gnome.org/pub/GNOME/sources/libcroco/0.6/libcroco-%s.tar.xz'%(version)

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath,
        self.deps_cpp_info["gdk-pixbuf"].rootpath,self.deps_cpp_info["libxml2"].rootpath)}

        with tools.environment_append(vars):
            self.run("./configure --prefix %s/build --libdir %s/build/lib --enable-introspection"%(os.getcwd(),os.getcwd()))
            self.run("make -j4")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libcroco"]


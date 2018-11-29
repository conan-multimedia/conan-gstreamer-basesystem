from conans import ConanFile, CMake, tools
import os

class CairoConan(ConanFile):
    name = "cairo"
    version = "1.14.12"
    license = "LGPLv2_1"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Cairo here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("libffi/3.99999@user/channel","glib/2.54.3@user/channel",
    "libpng/1.6.34@user/channel","zlib/1.2.11@user/channel",
    "pixman/0.34.0@user/channel","fontconfig/2.12.6@user/channel","bzip2/1.0.6@user/channel",
    "freetype/2.9@user/channel","expat/2.2.5@user/channel",)
    
    download_url = 'https://www.cairographics.org/releases/cairo-%s.tar.xz'%(version)
    patches = ['cairo/0001-Fix-compilation-with-Android-s-bionic-libc.patch',
               'cairo/0001-Disable-building-of-the-tests.patch',
               ]
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))


    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath,self.deps_cpp_info["libpng"].rootpath,self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["pixman"].rootpath,
            self.deps_cpp_info["fontconfig"].rootpath,self.deps_cpp_info["bzip2"].rootpath, self.deps_cpp_info["freetype"].rootpath,self.deps_cpp_info["expat"].rootpath)}
        
        with tools.environment_append(vars):
            self.run("NOCONFIGURE=1 ./autogen.sh")
            self.run("./configure --prefix %s/build --libdir %s/build/lib --enable-introspection"%(os.getcwd(),os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["cairo"]


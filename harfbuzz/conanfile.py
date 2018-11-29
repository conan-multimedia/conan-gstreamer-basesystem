from conans import ConanFile, CMake, tools
from shutil import copyfile
import os


class HarfbuzzConan(ConanFile):
    name = "harfbuzz"
    version = "1.7.5"
    license = "LGPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Harfbuzz here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("expat/2.2.5@user/channel","zlib/1.2.11@user/channel", 
    "bzip2/1.0.6@user/channel","libpng/1.6.34@user/channel","pixman/0.34.0@user/channel",
    "fontconfig/2.12.6@user/channel","glib/2.54.3@user/channel","libffi/3.99999@user/channel",
    "freetype/2.9@user/channel","cairo/1.14.12@user/channel"
    )

    download_url = 'http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-%s.tar.bz2'%(version)
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -jxvf %s-%s.tar.bz2 --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")


    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"%(
            self.deps_cpp_info["expat"].rootpath,self.deps_cpp_info["freetype"].rootpath,self.deps_cpp_info["zlib"].rootpath,
            self.deps_cpp_info["bzip2"].rootpath,self.deps_cpp_info["libpng"].rootpath,self.deps_cpp_info["pixman"].rootpath,
            self.deps_cpp_info["fontconfig"].rootpath,self.deps_cpp_info["glib"].rootpath,self.deps_cpp_info["libffi"].rootpath,
            self.deps_cpp_info["freetype"].rootpath,self.deps_cpp_info["cairo"].rootpath)}
    
        with tools.environment_append(vars):
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
            self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
                     ' --disable-silent-rules --enable-introspection --enable-static --with-icu=no'%(os.getcwd(), os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")
        #self.copy("*.h", dst="include/harfbuzz", src="src")

    def package_info(self):
        self.cpp_info.libs = ["harfbuzz"]

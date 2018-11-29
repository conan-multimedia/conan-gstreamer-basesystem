from conans import ConanFile, CMake, tools
import os

class FlacConan(ConanFile):
    name = "flac"
    version = "1.3.2"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Flac here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libogg/1.3.3@user/channel"

    download_url = 'http://downloads.xiph.org/releases/flac/flac-1.3.2.tar.xz'


    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig"%(self.deps_cpp_info["libogg"].rootpath)}
        
        with tools.environment_append(vars):
            self.run("autoreconf -f -i")
            self.run('./configure --prefix %s/~build --libdir %s/~build/lib --enable-introspection'
                ' --disable-cpplibs --enable-static'%(os.getcwd(),os.getcwd()))
            self.run("make -j4")
            self.run("make install")

    def package(self):
        self.copy("*", src="~build")

    def package_info(self):
        self.cpp_info.libs = ["flac"]


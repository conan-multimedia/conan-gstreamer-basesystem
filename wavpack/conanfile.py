from conans import ConanFile, CMake, tools
import os

class WavpackConan(ConanFile):
    name = "wavpack"
    version = "5.1.0"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Wavpack here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'https://github.com/dbry/WavPack/archive/%s.tar.gz'%(version)

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s.tar.gz --strip-components 1"%(self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        self.run("autoreconf -f -i")
        self.run('./configure --prefix %s/~build --libdir %s/~build/lib --disable-maintainer-mode --disable-silent-rules'
        ' --enable-introspection --disable-apps'%(os.getcwd(),os.getcwd()))
        self.run("make -j4")
        self.run("make install")

    def package(self):
        self.copy("*", src="~build")

    def package_info(self):
        self.cpp_info.libs = ["wavpack"]


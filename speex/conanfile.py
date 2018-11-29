from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class SpeexConan(ConanFile):
    name = "speex"
    version = "1.2rc2"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Speex here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libogg/1.3.3@user/channel"

    download_url = 'http://downloads.xiph.org/releases/speex/speex-1.2rc2.tar.gz'
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib'
            ' --disable-maintainer-mode --disable-silent-rules --enable-introspection'%(os.getcwd(), os.getcwd()))
        self.run('make')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["speex"]


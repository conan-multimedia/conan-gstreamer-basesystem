from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibjpegturboConan(ConanFile):
    name = "libjpeg-turbo"
    version = "1.5.3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libjpegturbo here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://172.16.64.65:8081/artifactory/gstreamer/libjpeg-turbo-%s.tar.gz'%(version)
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
        self.run("autoreconf -f -i")
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
        self.run('./configure --prefix=%s/build --libdir=%s/build/lib'
            ' --disable-maintainer-mode --disable-silent-rules --enable-introspection --with-jpeg8'%(os.getcwd(),os.getcwd()))
        self.run('make -j2')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libjpeg-turbo"]


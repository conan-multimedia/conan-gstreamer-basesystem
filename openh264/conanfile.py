from conans import ConanFile, CMake, tools
import os

class Openh264Conan(ConanFile):
    name = "openh264"
    version = "1.7.0"
    license = "BSD"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Openh264 here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    #download_url = 'https://github.com/cisco/%s/archive/v%s.tar.gz'%(name,version)
    download_url = 'http://172.16.64.65:8081/artifactory/gstreamer/openh264-1.7.0.tar.gz'

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name,self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        self.replace('%s/Makefile'%(os.getcwd()),# Fix hard-coded prefix
        {'PREFIX=/usr/local': "PREFIX=%s/build"%(os.getcwd())})
        self.replace('%s/build/x86-common.mk'%(os.getcwd()),# Use yasm instead of nasm, since that's what Cerbero ships with
        {'ASM = nasm': "ASM = yasm"})
        self.run('make -j4 libraries')
        self.run('make -j4 install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["openh264"]
        
    def replace(self, filepath, replacements):
        ''' Replaces keys in the 'replacements' dict with their values in file '''
        with open(filepath, 'r') as f:
            content = f.read()
        for k, v in replacements.iteritems():
            content = content.replace(k, v)
        with open(filepath, 'w+') as f:
            f.write(content)


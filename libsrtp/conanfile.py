from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibsrtpConan(ConanFile):
    name = "libsrtp"
    version = "1.6.0"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libsrtp here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    
    #download_url = 'https://github.com/cisco/%s/archive/v%s.tar.gz'%(name,version)
    download_url = "http://172.16.64.65:8081/artifactory/gstreamer/libsrtp-1.6.0.tar.gz"
    patches = ['libsrtp/0001-Don-t-create-a-symlink-if-there-is-no-SHAREDLIBVERSI.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s -O %s-%s.tar.gz"%(self.download_url,self.name,self.version))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name,self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
        copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
        self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
        ' --disable-silent-rules  --enable-introspection'%(os.getcwd(),os.getcwd()))
        self.run('make -j4 all shared_library')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libsrtp"]


from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibkateConan(ConanFile):
    name = "libkate"
    version = "0.4.1"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libkate here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libogg/1.3.3@user/channel", "libpng/1.6.34@user/channel"

    patches = ['libkate/0001-be-more-permissive-with-automake-errors-now-that-we-.patch']
    download_url = 'http://downloads.xiph.org/releases/kate/libkate-0.4.1.tar.gz'
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["libogg"].rootpath,self.deps_cpp_info["libpng"].rootpath)}
        
        with tools.environment_append(vars):
            self.run("autoreconf -f -i")
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/misc/autotools/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/misc/autotools/config.sub"%(os.getcwd()))
            self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
            ' --disable-silent-rules  --enable-introspection'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libkate"]


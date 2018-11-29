from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibassConan(ConanFile):
    name = "libass"
    version = "0.13.7"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libass here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("freetype/2.9@user/channel", "fontconfig/2.12.6@user/channel", 
        "libpng/1.6.34@user/channel","fribidi/0.19.7@user/channel")

    download_url = 'https://github.com/libass/libass/releases/download/{0}/libass-{0}.tar.gz'.format(version)
    patches = ['libass/0001-define-IID_Unknown.patch']
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
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
            %(self.deps_cpp_info["freetype"].rootpath,self.deps_cpp_info["fontconfig"].rootpath,
            self.deps_cpp_info["libpng"].rootpath,self.deps_cpp_info["fribidi"].rootpath)}
        
        with tools.environment_append(vars):
            self.run("autoreconf -f -i")
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
            self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
                ' --disable-silent-rules --enable-introspection'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libass"]


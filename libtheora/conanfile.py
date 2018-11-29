from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibtheoraConan(ConanFile):
    name = "libtheora"
    version = "1.1.1"
    license = "BSD"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libtheora here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libogg/1.3.3@user/channel", "libvorbis/1.3.5@user/channel"

    download_url = 'http://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.bz2'
    patches = ['libtheora/0001-Add-option-to-disable-doc.patch',
               'libtheora/0002-Update-makefiles.patch',
               'libtheora/0003-Fix-linking-of-theora-encoder-library.patch',
               'libtheora/0004-Use-our-automake-version-and-not-an-older-one.patch',
               'libtheora/0005-Update-Makefile.in-too-to-avoid-needing-to-call-auto.patch',
               'libtheora/0006-examples-Don-t-use-png_sizeof.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -jxvf %s-%s.tar.bz2 --strip-components 1"%(self.name, self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig"%(
            self.deps_cpp_info["libogg"].rootpath,self.deps_cpp_info["libvorbis"].rootpath)}
    
        with tools.environment_append(vars):
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))

            self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
                ' --disable-silent-rules --enable-introspection --disable-spec --disable-doc'%(os.getcwd(), os.getcwd()))
            self.run('make')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libtheora"]


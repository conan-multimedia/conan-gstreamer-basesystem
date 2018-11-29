from conans import ConanFile, CMake, tools
import os
import stat
import fnmatch

class CdparanoiaConan(ConanFile):
    name = "cdparanoia"
    version = "10.2"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Cdparanoia here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://downloads.xiph.org/releases/cdparanoia/cdparanoia-III-10.2.src.tgz'
    patches = ['cdparanoia/0001-configure.in-Always-use-AC_PROG_CC.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf cdparanoia-III-10.2.src.tgz --strip-components 1")

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        self.run("autoreconf -f -i")
        self.run('CFLAGS=\"$CFLAGS -fPIC\" ./configure --prefix %s/build --libdir %s/build/lib'
            ' --disable-maintainer-mode --disable-silent-rules --enable-introspection'%(os.getcwd(),os.getcwd()))
        self.run('make')
        self.run('make install')

    def package(self):
        for f in os.listdir('build/lib'):
            if fnmatch.fnmatch(f, '*.so*'):
                os.chmod("./build/lib/%s"%(f), stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["cdparanoia"]


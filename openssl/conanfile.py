from conans import ConanFile, CMake, tools
import os

class OpensslConan(ConanFile):
    name = "openssl"
    version = "1.1.0h"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Openssl here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "zlib/1.2.11@user/channel"

    download_url = 'https://ftp.openssl.org/source/{0}-{1}.tar.gz'.format(name, version)
    patches = ['openssl/0001-build-disable-poly1305-custom-assembly-on-armv4-as-i.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name,self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig"%(self.deps_cpp_info["zlib"].rootpath),
        'LDFLAGS' : "-L%s/lib"%(self.deps_cpp_info["zlib"].rootpath),
        'CFLAGS': "-I%s/include"%(self.deps_cpp_info["zlib"].rootpath),
        'CC' : "gcc"}

        with tools.environment_append(vars):
            self.run('perl ./Configure --prefix=%s/build --libdir=%s/build/lib shared enable-ssl3'
            ' enable-ssl3-method enable-md2 linux-x86_64'%(os.getcwd(),os.getcwd()))
            self.run('make CC=\"$CC $CFLAGS\" LDFLAG=\"$LDFLAGS -fPIC\" CFLAG=\"$CFLAGS -fPIC -DOPENSSL_PIC\"')
            self.run('make install_sw')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["openssl"]


from conans import ConanFile, CMake, tools
import os

class LibrtmpConan(ConanFile):
    name = "librtmp"
    version = "2.4_p20151223"
    license = "LGPLv2_1"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Librtmp here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "nettle/3.4@user/channel","gnutls/3.5.18@user/channel","gmp/6.1.2@user/channel"

    patches = ['librtmp/0001-Fix-support-for-cross-compilation.patch']
    download_url = 'https://gstreamer.freedesktop.org/data/src/mirror/rtmpdump-2.4_p20151223.tar.gz'
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s -O %s-%s.tar.gz"%(self.download_url, self.name, self.version))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name, self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["nettle"].rootpath,self.deps_cpp_info["gnutls"].rootpath,self.deps_cpp_info["gmp"].rootpath),
        'LDFLAGS' : "-L%s/lib -L%s/lib -L%s/lib"
        %(self.deps_cpp_info["nettle"].rootpath,self.deps_cpp_info["gnutls"].rootpath,self.deps_cpp_info["gmp"].rootpath),
        'CFLAGS': "-I%s/include -I%s/include -I%s/include"
        %(self.deps_cpp_info["nettle"].rootpath,self.deps_cpp_info["gnutls"].rootpath,self.deps_cpp_info["gmp"].rootpath),
        'CC' : "gcc",
        'LD' : "ld"}
        
        with tools.environment_append(vars):
            self.run('make SYS=posix prefix=%s/build CRYPTO=GNUTLS'
            ' XLDFLAGS=\"$LDFLAGS\" XCFLAGS=\"$CFLAGS\" CC=\"$CC\" LD=\"$LD\"'%(os.getcwd()))
            self.run('make install SYS=posix prefix=%s/build CRYPTO=GNUTLS'
            ' XLDFLAGS=\"$LDFLAGS\" XCFLAGS=\"$CFLAGS\" CC=\"$CC\" LD=\"$LD\"'%(os.getcwd()))

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["librtmp"]


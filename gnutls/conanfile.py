from conans import ConanFile, CMake, tools
import os


class GnutlsConan(ConanFile):
    name = "gnutls"
    version = "3.5.18"
    license = "LGPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gnutls here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "zlib/1.2.11@user/channel", "nettle/3.4@user/channel", "libtasn1/4.13@user/channel","gmp/6.1.2@user/channel"

    maj_ver = '.'.join(version.split('.')[0:2])
    download_url = 'https://www.gnupg.org/ftp/gcrypt/{0}/v{1}/{0}-{2}.tar.xz'.format(name, maj_ver, version)
    patches = [name + "/0003-Disable-ncrypt-support.patch",
               name + "/0001-Undefine-__USE_MINGW_ANSI_STDIO-as-otherwise-stdio.h.patch",
               name + "/0001-pgusage-remove-system-call.patch",
               name + "/0001-asm-rename-some-assembly-functions-to-not-conflict-w.patch",]
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["nettle"].rootpath,self.deps_cpp_info["libtasn1"].rootpath),
        'LD_LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),
        'LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),
        'C_INCLUDE_PATH' : "%s/include:%s/include"%(self.deps_cpp_info["gmp"].rootpath,self.deps_cpp_info["libtasn1"].rootpath)}

        with tools.environment_append(vars):
            self.run("autoreconf -f -i")
            self.run('./configure --prefix %s/build --libdir %s/build/lib --enable-introspection'
                ' --enable-local-libopts --disable-guile --disable-openssl-compatibility'
                ' --without-p11-kit --enable-static --enable-zlib --enable-shared'
                ' --disable-doc --disable-tests --with-included-unistring'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gnutls"]


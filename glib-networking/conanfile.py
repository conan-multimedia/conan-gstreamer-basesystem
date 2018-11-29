from conans import ConanFile, CMake, tools
import os


class GlibnetworkingConan(ConanFile):
    name = "glib-networking"
    version = "2.54.1"
    license = "LGPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Glibnetworking here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("libffi/3.99999@user/channel","glib/2.54.3@user/channel","gnutls/3.5.18@user/channel",
    "nettle/3.4@user/channel","libtasn1/4.13@user/channel")
    
    download_url = 'http://ftp.gnome.org/pub/gnome/sources/glib-networking/2.54/glib-networking-%s.tar.xz'%(version)
    patches = ['glib-networking/0001-Add-support-for-static-modules.patch',
               'glib-networking/0002-Get-the-CA-certificate-path-from-the-environment-var.patch',
               'glib-networking/0003-gnutls-Use-db-relative-to-libglib-2.0-if-needed.patch',
               'glib-networking/0004-gtlsbackend-gnutls-Get-anchor-file-relative-to-libgi.patch']
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
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath,
        self.deps_cpp_info["gnutls"].rootpath,self.deps_cpp_info["nettle"].rootpath,
        self.deps_cpp_info["libtasn1"].rootpath),
        'LD_LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["glib"].rootpath)}
        
        with tools.environment_append(vars):
            self.run("autoreconf -f -i")
            self.run('GIO_QUERYMODULES=%s/bin/gio-querymodules ./configure --prefix %s/build --libdir %s/build/lib'
                ' --enable-introspection --without-ca-certificates --enable-more-warnings'
                %(self.deps_cpp_info["glib"].rootpath, os.getcwd(), os.getcwd()))
            self.run("make -j4")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["glib-networking"]


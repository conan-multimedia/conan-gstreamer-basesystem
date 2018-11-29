from conans import ConanFile, CMake, tools
import os

class LibsoupConan(ConanFile):
    name = "libsoup"
    version = "2.60.3"
    license = "LGPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libsoup here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("libxml2/2.9.7@user/channel","libffi/3.99999@user/channel","glib/2.54.3@user/channel",
    "glib-networking/2.54.1@user/channel","gobject-introspection/1.54.1@user/channel")

    download_url = 'http://ftp.gnome.org/pub/gnome/sources/libsoup/2.60/libsoup-%s.tar.xz'%(version)
    patches = ['libsoup/0001-Rip-out-sqlite-based-cookie-storage.patch',
               'libsoup/0001-build-Fix-enumtypes-on-MinGW-inside-MSYS-Windows.patch']
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
        %(self.deps_cpp_info["libxml2"].rootpath,self.deps_cpp_info["libffi"].rootpath,
        self.deps_cpp_info["glib"].rootpath,self.deps_cpp_info["glib-networking"].rootpath,
        self.deps_cpp_info["gobject-introspection"].rootpath)}

        with tools.environment_append(vars):
            self.run("gtkdocize && intltoolize --automake --copy && autoreconf --force --install --verbose")
            self.run('./configure --prefix %s/build --libdir %s/build/lib --enable-introspection --without-gnome'
            ' --disable-more-warnings --disable-vala --with-gssapi=no --disable-always-build-tests --disable-glibtest --disable-installed-tests'
            %(os.getcwd(),os.getcwd()))
            self.run("make -j4")
            self.run("make install")


    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libsoup"]


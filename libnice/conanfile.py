from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class LibniceConan(ConanFile):
    name = "libnice"
    version = "0.1.14"
    license = "LGPLv2_1Plus,MPLv1_1"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libnice here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("libffi/3.99999@user/channel", "glib/2.54.3@user/channel",
    "gtk-doc-lite/1.27@user/channel","gstreamer/1.14.3@user/channel",
    "gnutls/3.5.18@user/channel","nettle/3.4@user/channel","libtasn1/4.13@user/channel",
    "gobject-introspection/1.54.1@user/channel")

    download_url = 'http://nice.freedesktop.org/releases/%s-%s.tar.gz'%(name,version)
    patches = [
        "libnice/0001-Fix-build-with-android-NDK-r16.patch",
        "libnice/0001-nicesrc-spin-the-agent-mainloop-in-a-separate-thread.patch",
        "libnice/0001-agent-Redefine-socket-error-messages-for-windows.patch",
        "libnice/0001-stun-Also-rename-windows-specific-function.patch"
    ]
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
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath,
        self.deps_cpp_info["gtk-doc-lite"].rootpath,self.deps_cpp_info["gstreamer"].rootpath,
        self.deps_cpp_info["gnutls"].rootpath,self.deps_cpp_info["nettle"].rootpath,
        self.deps_cpp_info["libtasn1"].rootpath,self.deps_cpp_info["gobject-introspection"].rootpath)}

        with tools.environment_append(vars):
            self.run('autoreconf -f -i')
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
            self.run('./configure --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
            ' --disable-silent-rules --enable-introspection --enable-static --enable-static-plugins'
            ' --enable-shared --with-gstreamer --without-gstreamer-0.10 --enable-compile-warnings=maximum --disable-gtk-doc'
            %(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libnice"]


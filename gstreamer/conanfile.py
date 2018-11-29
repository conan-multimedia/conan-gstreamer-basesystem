from conans import ConanFile, CMake, tools
import os

class GstreamerConan(ConanFile):
    name = "gstreamer"
    version = "1.14.3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gstreamer here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    remotes = {'origin': 'https://anongit.freedesktop.org/git/gstreamer/gstreamer'}
    requires = "libffi/3.99999@user/channel", "glib/2.54.3@user/channel", "gtk-doc-lite/1.27@user/channel", "gobject-introspection/1.54.1@user/channel"

    def source(self):
        self.run("git init")
        for key, val in self.remotes.items():
            self.run("git remote add %s %s"%(key, val))
        self.run("git fetch --all")
        self.run("git reset --hard %s"%(self.version))
        self.run("git submodule init && git submodule sync && git submodule update")
        self.run("git reset --hard %s"%(self.version))
        self.run("git branch cerbero_build && git checkout cerbero_build")
        self.run("git reset --hard %s"%(self.version))
        self.run("git config user.email")
        self.run("git config user.name")

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
            %(self.deps_cpp_info["gobject-introspection"].rootpath,
              self.deps_cpp_info["glib"].rootpath, self.deps_cpp_info["gtk-doc-lite"].rootpath,
              self.deps_cpp_info["libffi"].rootpath)}

        with tools.environment_append(vars):
            self.run('sh ./autogen.sh --noconfigure')
            self.run('./configure --prefix %s/build --libdir %s/build/lib --enable-introspection '
                     '--enable-static --program-prefix= --disable-examples'%(os.getcwd(),os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gstreamer"]


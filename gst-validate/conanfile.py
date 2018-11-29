from conans import ConanFile, CMake, tools
import os

class GstvalidateConan(ConanFile):
    name = "gst-validate"
    version = "1.14.3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gstvalidate here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("gstreamer/1.14.3@user/channel", "gst-plugins-base/1.14.3@user/channel",
    "json-glib/1.2.8@user/channel","libffi/3.99999@user/channel","glib/2.54.3@user/channel",
    "gobject-introspection/1.54.1@user/channel","orc/0.4.28@user/channel")

    remotes = {'origin': 'https://anongit.freedesktop.org/git/gstreamer/gst-devtools'}

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
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["gstreamer"].rootpath,self.deps_cpp_info["gst-plugins-base"].rootpath,
        self.deps_cpp_info["json-glib"].rootpath,self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath,
        self.deps_cpp_info["gobject-introspection"].rootpath,self.deps_cpp_info["orc"].rootpath,)}

        with tools.environment_append(vars):
            self.run('cd validate && sh ./autogen.sh --noconfigure && ./configure --enable-static --program-transform-name='
            ' --prefix %s/validate/build --libdir %s/validate/build/lib --enable-introspection'%(os.getcwd(),os.getcwd()))
            self.run('cd validate && make -j4')
            self.run('cd validate && make install')


    def package(self):
        self.copy("*", src="validate/build")

    def package_info(self):
        self.cpp_info.libs = ["gst-validate"]


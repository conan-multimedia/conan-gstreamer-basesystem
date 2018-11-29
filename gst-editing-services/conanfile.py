from conans import ConanFile, CMake, tools
import os

class GsteditingservicesConan(ConanFile):
    name = "gst-editing-services"
    version = "1.14.3"
    license = "LGPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gsteditingservices here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("gstreamer/1.14.3@user/channel", "gst-plugins-base/1.14.3@user/channel",
    "gst-plugins-good/1.14.3@user/channel", "gst-validate/1.14.3@user/channel", "libffi/3.99999@user/channel",
    "gobject-introspection/1.54.1@user/channel","orc/0.4.28@user/channel","libxml2/2.9.7@user/channel")

    remotes = {'origin': 'https://anongit.freedesktop.org/git/gstreamer/gst-editing-services'}

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
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["gstreamer"].rootpath,self.deps_cpp_info["gst-plugins-base"].rootpath,
        self.deps_cpp_info["gst-plugins-good"].rootpath,self.deps_cpp_info["gst-validate"].rootpath,
        self.deps_cpp_info["libffi"].rootpath, self.deps_cpp_info["gobject-introspection"].rootpath,
        self.deps_cpp_info["orc"].rootpath,self.deps_cpp_info["libxml2"].rootpath),
        'BASH_COMPLETION_DIR':"%s/build/share/bash-completion/completions"%(os.getcwd())}

        with tools.environment_append(vars):
            self.run('sh ./autogen.sh --noconfigure && ./configure --prefix %s/build --libdir %s/build/lib'
            ' --enable-introspection --program-prefix= --disable-examples'
            ' --enable-static --with-bash-completion-dir=%s/build/share/bash-completion/completions'%(os.getcwd(),os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gst-editing-services"]


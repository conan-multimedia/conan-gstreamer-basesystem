from conans import ConanFile, CMake, tools
import os

class GstpluginsuglyConan(ConanFile):
    name = "gst-plugins-ugly"
    version = "1.14.3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gstpluginsugly here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("gstreamer/1.14.3@user/channel","gst-plugins-base/1.14.3@user/channel",
    "a52dec/0.7.4@user/channel","opencore-amr/0.1.5@user/channel","libdvdread/5.0.0@user/channel",
    "libmpeg2/0.5.1@user/channel","x264/20161218-2245@user/channel")

    remotes = {'origin': 'https://anongit.freedesktop.org/git/gstreamer/gst-plugins-ugly'}

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
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["gstreamer"].rootpath,self.deps_cpp_info["gst-plugins-base"].rootpath, 
        self.deps_cpp_info["a52dec"].rootpath,self.deps_cpp_info["opencore-amr"].rootpath,
        self.deps_cpp_info["libdvdread"].rootpath,self.deps_cpp_info["libmpeg2"].rootpath,
        self.deps_cpp_info["x264"].rootpath),
        'C_INCLUDE_PATH':"%s/include"%(self.deps_cpp_info["opencore-amr"].rootpath)}

        with tools.environment_append(vars):
            self.run('sh ./autogen.sh --noconfigure && ./configure --prefix %s/build --libdir %s/build/lib'
            ' --enable-introspection --enable-static --disable-examples --disable-iec958'
            ' --disable-mpegstream --disable-cdio --disable-sidplay'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gst-plugins-ugly"]


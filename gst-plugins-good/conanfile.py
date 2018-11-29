from conans import ConanFile, CMake, tools
import os

class GstpluginsgoodConan(ConanFile):
    name = "gst-plugins-good"
    version = "1.14.3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gstpluginsgood here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("gstreamer/1.14.3@user/channel","gst-plugins-base/1.14.3@user/channel","libjpeg-turbo/1.5.3@user/channel",
    "libpng/1.6.34@user/channel","speex/1.2rc2@user/channel","gdk-pixbuf/2.36.2@user/channel","libsoup/2.60.3@user/channel",
    "mpg123/1.25.10@user/channel","lame/3.100@user/channel","orc/0.4.28@user/channel","wavpack/5.1.0@user/channel",
    "flac/1.3.2@user/channel","taglib/1.11.1@user/channel","bzip2/1.0.6@user/channel","zlib/1.2.11@user/channel",
    "libvpx/v1.6.0@user/channel","libdv/1.0.0@user/channel","cairo/1.14.12@user/channel"
    )

    remotes = {'origin': 'https://anongit.freedesktop.org/git/gstreamer/gst-plugins-good'}

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
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        ":%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["gstreamer"].rootpath,self.deps_cpp_info["gst-plugins-base"].rootpath, 
        self.deps_cpp_info["libjpeg-turbo"].rootpath,self.deps_cpp_info["libpng"].rootpath,
        self.deps_cpp_info["speex"].rootpath,self.deps_cpp_info["gdk-pixbuf"].rootpath,
        self.deps_cpp_info["libsoup"].rootpath,self.deps_cpp_info["mpg123"].rootpath,
        self.deps_cpp_info["lame"].rootpath,self.deps_cpp_info["orc"].rootpath,
        self.deps_cpp_info["wavpack"].rootpath,self.deps_cpp_info["flac"].rootpath,
        self.deps_cpp_info["taglib"].rootpath,self.deps_cpp_info["bzip2"].rootpath,
        self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["libvpx"].rootpath,
        self.deps_cpp_info["libdv"].rootpath,self.deps_cpp_info["cairo"].rootpath)}

        with tools.environment_append(vars):
            self.run('sh ./autogen.sh --noconfigure && ./configure --prefix %s/build --libdir %s/build/lib'
                ' --enable-introspection --enable-static --disable-examples --disable-oss4 --disable-oss'
                ' --disable-dv1394 --disable-aalib --disable-libcaca --disable-jack --disable-shout2'
                ' --disable-twolame --disable-qt --disable-gtk3'%(os.getcwd(),os.getcwd()))
        self.run("make -j4")
        self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gst-plugins-good"]


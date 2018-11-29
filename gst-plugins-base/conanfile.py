from conans import ConanFile, CMake, tools
import os


class GstpluginsbaseConan(ConanFile):
    name = "gst-plugins-base"
    version = "1.14.3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gstpluginsbase here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    remotes = {'origin': 'https://anongit.freedesktop.org/git/gstreamer/gst-plugins-base'}
    requires = ("libffi/3.99999@user/channel", "glib/2.54.3@user/channel", 
    "gstreamer/1.14.3@user/channel", "gtk-doc-lite/1.27@user/channel", "gobject-introspection/1.54.1@user/channel",
    "libxml2/2.9.7@user/channel", "zlib/1.2.11@user/channel", 
    "libogg/1.3.3@user/channel","libtheora/1.1.1@user/channel",
    "libvisual/0.4.0@user/channel","libvorbis/1.3.5@user/channel",
    "orc/0.4.28@user/channel", "opus/1.2.1@user/channel", "graphene/1.4.0@user/channel",
    "libjpeg-turbo/1.5.3@user/channel", "libpng/1.6.34@user/channel",
    "pango/1.40.14@user/channel","gobject-introspection/1.54.1@user/channel")

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
                %(
                    self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath,
                    self.deps_cpp_info["gstreamer"].rootpath, self.deps_cpp_info["gtk-doc-lite"].rootpath,
                    self.deps_cpp_info["gobject-introspection"].rootpath,self.deps_cpp_info["libxml2"].rootpath,
                    self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["libogg"].rootpath,
                    self.deps_cpp_info["libtheora"].rootpath,self.deps_cpp_info["libvisual"].rootpath,
                    self.deps_cpp_info["libvorbis"].rootpath,self.deps_cpp_info["orc"].rootpath,
                    self.deps_cpp_info["opus"].rootpath,self.deps_cpp_info["graphene"].rootpath,
                    self.deps_cpp_info["libjpeg-turbo"].rootpath,self.deps_cpp_info["libpng"].rootpath,
                    self.deps_cpp_info["pango"].rootpath,self.deps_cpp_info["gobject-introspection"].rootpath)}

        with tools.environment_append(vars):
            self.run('sh ./autogen.sh --noconfigure && ./configure --prefix %s/build --libdir %s/build/lib'
                ' --enable-introspection --enable-static --program-prefix= --disable-examples'%(os.getcwd(),os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gst-plugins-base"]


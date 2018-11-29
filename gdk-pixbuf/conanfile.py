from conans import ConanFile, CMake, tools
import os

class GdkpixbufConan(ConanFile):
    name = "gdk-pixbuf"
    version = "2.36.2"
    license = "LGPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gdkpixbuf here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("libjpeg-turbo/1.5.3@user/channel","glib/2.54.3@user/channel",
        "libpng/1.6.34@user/channel","tiff/4.0.9@user/channel", "zlib/1.2.11@user/channel",
        "libffi/3.99999@user/channel","gobject-introspection/1.54.1@user/channel")

    download_url = 'http://ftp.gnome.org/pub/gnome/sources/gdk-pixbuf/2.36/gdk-pixbuf-2.36.2.tar.xz'
    patches = ['gdk-pixbuf/0001-thumbnailer-Add-EXEEXT-to-the-the-gdk-pixbuf-print-m.patch']
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
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"%(
        self.deps_cpp_info["libjpeg-turbo"].rootpath, self.deps_cpp_info["glib"].rootpath,
        self.deps_cpp_info["libpng"].rootpath, self.deps_cpp_info["tiff"].rootpath,
        self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["libffi"].rootpath,
        self.deps_cpp_info["gobject-introspection"].rootpath),
        'LD_LIBRARY_PATH' : "%s/lib:%s/lib"%(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath),
        'LIBRARY_PATH' : "%s/lib:%s/lib"%(self.deps_cpp_info["tiff"].rootpath,self.deps_cpp_info["libjpeg-turbo"].rootpath),
        'C_INCLUDE_PATH' : "%s/include:%s/include"%(self.deps_cpp_info["tiff"].rootpath,self.deps_cpp_info["libjpeg-turbo"].rootpath)}

        with tools.environment_append(vars):
            self.run("autoreconf -f -i")
            self.run('./configure --prefix %s/build --libdir %s/build/lib --enable-introspection'
                ' --with-included-loaders --enable-static --enable-gio-sniffing=no'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gdk-pixbuf"]


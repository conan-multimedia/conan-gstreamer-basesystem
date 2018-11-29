from conans import ConanFile, CMake, tools
import os

class LibrsvgConan(ConanFile):
    name = "librsvg"
    version = "2.40.20"
    license = "LGPLv2"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Librsvg here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("libcroco/0.6.12@user/channel","libpng/1.6.34@user/channel","libxml2/2.9.7@user/channel",
    "gdk-pixbuf/2.36.2@user/channel","vala-m4/0.35.2@user/channel","pixman/0.34.0@user/channel",
    "glib/2.54.3@user/channel","libffi/3.99999@user/channel","gobject-introspection/1.54.1@user/channel",
    "gobject-introspection-m4/1.54.1@user/channel","pango/1.40.14@user/channel",
    "cairo/1.14.12@user/channel","fontconfig/2.12.6@user/channel",
    "freetype/2.9@user/channel","harfbuzz/1.7.5@user/channel")

    download_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/librsvg/2.40/librsvg-%s.tar.xz'%(version)
    patches = ['librsvg/option-enable-disable-gtk.patch',
               'librsvg/0001-Use-ACLOCAL_FLAGS.patch',
               'librsvg/0001-build-Fix-enumtypes-on-MinGW-inside-MSYS-Windows.patch']
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
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["libcroco"].rootpath,self.deps_cpp_info["libpng"].rootpath,
        self.deps_cpp_info["libxml2"].rootpath,self.deps_cpp_info["gdk-pixbuf"].rootpath,
        self.deps_cpp_info["vala-m4"].rootpath,self.deps_cpp_info["pixman"].rootpath,
        self.deps_cpp_info["glib"].rootpath,self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["gobject-introspection"].rootpath,
        self.deps_cpp_info["gobject-introspection-m4"].rootpath,self.deps_cpp_info["pango"].rootpath,self.deps_cpp_info["cairo"].rootpath,
        self.deps_cpp_info["fontconfig"].rootpath,self.deps_cpp_info["freetype"].rootpath,self.deps_cpp_info["harfbuzz"].rootpath),
        'XDG_DATA_DIRS':":%s/share/:$XDG_DATA_DIRS"
        %(self.deps_cpp_info["gdk-pixbuf"].rootpath)}


        with tools.environment_append(vars):
            self.run('mkdir -p m4 && autoreconf -fiv')
            self.run('./configure --prefix %s/build --libdir %s/build/lib --enable-introspection'
            ' --disable-pixbuf-loader --without-gtk3'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["librsvg"]


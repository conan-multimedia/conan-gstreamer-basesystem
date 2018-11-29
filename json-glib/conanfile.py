from conans import ConanFile, CMake, tools
import os

class JsonglibConan(ConanFile):
    name = "json-glib"
    version = "1.2.8"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Jsonglib here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libffi/3.99999@user/channel","glib/2.54.3@user/channel","gobject-introspection/1.54.1@user/channel"

    download_url = 'http://172.16.64.65:8081/artifactory/gstreamer/json-glib-%s.tar.xz'%(version)
    patches = ['json-glib/0001-Don-t-override-our-own-ACLOCAL_FLAGS-but-append-them.patch']
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
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath,
        self.deps_cpp_info["gobject-introspection"].rootpath),
        'LD_LIBRARY_PATH' : "%s/lib:%s/lib"
        %(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath),}

        with tools.environment_append(vars):
            self.run("autoreconf -f -i")
            self.run('./configure --prefix %s/build --libdir %s/build/lib --enable-introspection --enable-static'%(os.getcwd(),os.getcwd()))
            self.run("make -j4")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["json-glib"]


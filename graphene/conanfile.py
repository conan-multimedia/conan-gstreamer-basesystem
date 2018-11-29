from conans import ConanFile, CMake, tools
import os

class GrapheneConan(ConanFile):
    name = "graphene"
    version = "1.4.0"
    license = "MIT"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Graphene here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libffi/3.99999@user/channel","glib/2.54.3@user/channel","gobject-introspection/1.54.1@user/channel"

    download_url = 'https://github.com/ebassi/graphene/archive/{0}.tar.gz'.format(version)
    patches = ['graphene/0001-simd4f-Fix-a-compilation-error.patch']
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s.tar.gz --strip-components 1"%(self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
        %(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath,
        self.deps_cpp_info["gobject-introspection"].rootpath,)}
        with tools.environment_append(vars):
            self.run('sh ./autogen.sh --prefix %s/build --libdir %s/build/lib --disable-maintainer-mode'
                ' --disable-silent-rules --enable-introspection --enable-static --enable-shared --disable-arm-neon'%(os.getcwd(),os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["graphene"]


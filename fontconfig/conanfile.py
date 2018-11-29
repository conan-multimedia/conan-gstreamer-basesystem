from conans import ConanFile, CMake, tools
from shutil import copyfile
import os


class FontconfigConan(ConanFile):
    name = "fontconfig"
    version = "2.12.6"
    license = "MIT"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Fontconfig here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "expat/2.2.5@user/channel","freetype/2.9@user/channel","zlib/1.2.11@user/channel", "bzip2/1.0.6@user/channel","libpng/1.6.34@user/channel"

    download_url = 'http://www.freedesktop.org/software/fontconfig/release/fontconfig-%s.tar.gz'%(version)
    patches = ['fontconfig/0003-configure-Allow-static-build.patch',
               'fontconfig/0001-Do-not-build-tests-on-windows.patch',
               'fontconfig/0001-Don-t-use-_mktemp_s-which-is-not-available-in-XP.patch',
               'fontconfig/0004-Fix-cross-compilation-by-passing-CPPFLAGS-to-CPP.patch'
               ]
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name, self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root, patch))

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"%(self.deps_cpp_info["expat"].rootpath,
            self.deps_cpp_info["freetype"].rootpath,self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["bzip2"].rootpath,
            self.deps_cpp_info["libpng"].rootpath)}
        with tools.environment_append(vars):
            self.run('autoreconf -f -i')
            copyfile("%s/data/autotools/config.guess"%(self.cerbero_root), "%s/config.guess"%(os.getcwd()))
            copyfile("%s/data/autotools/config.sub"%(self.cerbero_root), "%s/config.sub"%(os.getcwd()))
            self.run('./configure --prefix %s/build --libdir %s/build/lib'
                     ' --disable-maintainer-mode --disable-silent-rules --enable-introspection --disable-docs'%(os.getcwd(),os.getcwd()))

            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["fontconfig"]


from conans import ConanFile, CMake, tools
import os

class LibvorbisConan(ConanFile):
    name = "libvorbis"
    version = "1.3.5"
    license = "BSD_like"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libvorbis here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libogg/1.3.3@user/channel"

    download_url = 'http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.5.tar.xz'
    patches = ['libvorbis/0001-Fix-linking-on-Android.patch',
               'libvorbis/0003-Link-the-other-libs-with-lm-too.patch',
               'libvorbis/0004-configure-check-for-endianness.patch',
               'libvorbis/0005-darwin-do-not-build-for-a-generic-arm-architecture.patch',
               'libvorbis/0006-Use-our-version-of-automake-instead-of-some-random-o.patch',
               'libvorbis/0007-autogen.sh-Make-sure-libtoolize-runs-fully.patch'
              ]
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
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig"%(self.deps_cpp_info["libogg"].rootpath)}
        
        with tools.environment_append(vars):
            self.run('rm ltmain.sh && sh autogen.sh --prefix %s/build --libdir %s/build/lib --enable-introspection'%(os.getcwd(),os.getcwd()))
            self.run('make -j2')
            self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["libvorbis"]


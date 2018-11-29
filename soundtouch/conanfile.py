from conans import ConanFile, CMake, tools
import os


class SoundtouchConan(ConanFile):
    name = "soundtouch"
    version = "1.9.2"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Soundtouch here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    patches = ['soundtouch/0001-Add-dummy-file-to-make-sure-config-m4-exists.patch',
               'soundtouch/0002-Use-STLPORT-on-Android.patch',
               'soundtouch/0003-Don-t-build-soundstretch.patch',
               'soundtouch/0004-Use-gnustl.patch',
               'soundtouch/0005-Fix-soundstretch-linking.patch',
               'soundtouch/0006-Fix-pkg-config-file.patch',
               'soundtouch/0007-Make-it-compile-on-IOS.patch',
               'soundtouch/0008-Fix-compilation-with-clang.patch',
               'soundtouch/0010-Try-harder-to-generate-Win32-DLLs.patch']
    download_url = 'http://www.surina.net/soundtouch/soundtouch-1.9.2.tar.gz'
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name,self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))

    def build(self):
        self.run("./bootstrap")
        self.run('./configure --prefix %s/build --libdir %s/build/lib'
        ' --disable-maintainer-mode --disable-silent-rules --enable-introspection --enable-static'
        %(os.getcwd(),os.getcwd()))
        self.run('make -j4')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["soundtouch"]


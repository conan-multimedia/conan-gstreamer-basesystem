from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class GtkdocliteConan(ConanFile):
    name = "gtk-doc-lite"
    version = "1.27"
    license = "GPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gtkdoclite here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"

    download_url = 'https://gstreamer.freedesktop.org/src/mirror/gtk-doc-1.27.tar.xz'

    def source(self):
        self.run("wget %s -O %s-%s.tar.xz"%(self.download_url, self.name, self.version))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self.name, self.version))

    def package(self):
        self.copy("gtk-doc.m4", dst="share/aclocal")
        self.copy("gtk-doc.make", dst="share/gtk-doc/data")
        copyfile("gtkdocize.in", "gtkdocize")
        ##!FIXME prefix
        replacements = {'@PACKAGE@': 'gtk-doc', '@VERSION@': self.version,
                        '@prefix@': self.copy._base_dst,
                        '@datarootdir@': '${prefix}/share',
                        '@datadir@': '${datarootdir}'}
        self.replace("gtkdocize", replacements)
        self.copy("gtkdocize", dst="bin")


    def replace(self, filepath, replacements):
        ''' Replaces keys in the 'replacements' dict with their values in file '''
        with open(filepath, 'r') as f:
            content = f.read()
        for k, v in replacements.iteritems():
            content = content.replace(k, v)
        with open(filepath, 'w+') as f:
            f.write(content)

    def package_info(self):
        self.cpp_info.libs = ["gtk-doc-lite"]


from conans import ConanFile, CMake, tools


class Gobjectintrospectionm4Conan(ConanFile):
    name = "gobject-introspection-m4"
    version = "1.54.1"
    license = "GPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gobjectintrospectionm4 here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    _name = 'gobject-introspection'
    maj_ver = '.'.join(version.split('.')[0:2])
    download_url = 'http://ftp.gnome.org/pub/GNOME/sources/{0}/{2}/{0}-{1}.tar.xz'.format(_name, version, maj_ver)

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -xvf %s-%s.tar.xz --strip-components 1"%(self._name, self.version))
        
        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        pass

    def package(self):
        self.copy("introspection.m4", dst="share/aclocal", src="m4")

    def package_info(self):
        self.cpp_info.libs = ["gobject-introspection-m4"]


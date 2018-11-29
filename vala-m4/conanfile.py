from conans import ConanFile, CMake, tools


class Valam4Conan(ConanFile):
    name = "vala-m4"
    version = "0.35.2"
    license = "LGPLv2_1Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Valam4 here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    _name = 'vala'
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
        self.copy("vapigen.m4", src="vapigen", dst="share/aclocal")
        self.copy("vala.m4", dst="share/aclocal")
        self.copy("Makefile.vapigen", src="vapigen", dst="share/vala")

    def package_info(self):
        self.cpp_info.libs = ["vala-m4"]


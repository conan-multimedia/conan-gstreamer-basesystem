from conans import ConanFile, CMake, tools


class LadspaConan(ConanFile):
    name = "ladspa"
    version = "1.13"
    license = "LGPLv2_1"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Ladspa here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"

    download_url = 'http://www.ladspa.org/download/ladspa_sdk_1.13.tgz'

    def source(self):
        self.run("wget %s"%(self.download_url))
        self.run("tar -zxvf ladspa_sdk_1.13.tgz --strip-components 1")

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")

    def build(self):
        pass

    def package(self):
        self.copy("ladspa.h", dst="include", src="src")

    def package_info(self):
        self.cpp_info.libs = ["ladspa"]


from conans import ConanFile, CMake, tools
import os

class OpenjpegConan(ConanFile):
    name = "openjpeg"
    version = "2.3.0"
    license = "BSD"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Openjpeg here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    
    patches = ['openjpeg/0002-Set-INSTALL_NAME_DIR.patch']
    download_url = 'https://github.com/uclouvain/openjpeg/archive/v%s.tar.gz'%(version)
    cerbero_root = '/home/ubuntu/workspace/cerbero'##!TODO: REPLACE WITH ENV VARIABLE

    def source(self):
        self.run("wget %s -O %s-%s.tar.gz"%(self.download_url,self.name,self.version))
        self.run("tar -zxvf %s-%s.tar.gz --strip-components 1"%(self.name,self.version))

        self.run("git init")
        self.run("git config user.email")
        self.run("git config user.name")
        self.run("git add --force -A .")
        self.run("git commit -m \"Initial commit\" > /dev/null 2>&1")
        for patch in self.patches:
            self.run("git am --ignore-whitespace %s/recipes/%s"%(self.cerbero_root,patch))

    def build(self):
        self.run('cmake -DCMAKE_INSTALL_PREFIX=%s/build -DCMAKE_LIBRARY_OUTPUT_PATH=%s/build/lib'
        ' -DBUILD_CODEC:bool=off -DBUILD_PKGCONFIG_FILES:bool=on -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++'
        ' -DCMAKE_C_FLAGS=\" -Wall -g -O2 -m64  -Wall -g -O2 -m64  -Wall -g -O2 -m64 \"'
        ' -DCMAKE_CXX_FLAGS=\" -Wall -g -O2 -m64  -Wall -g -O2 -m64  -Wall -g -O2 -m64 \"'
        ' -DLIB_SUFFIX=  -DCMAKE_BUILD_TYPE=Release -DCMAKE_FIND_ROOT_PATH=%s'%(os.getcwd(),os.getcwd(),self.cerbero_root))
        self.run('make -j4')
        self.run('make install')

    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["openjpeg"]


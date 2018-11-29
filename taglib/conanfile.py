from conans import ConanFile, CMake, tools
import os
import stat
import fnmatch

class TaglibConan(ConanFile):
    name = "taglib"
    version = "1.11.1"
    license = "LGPLv2_1"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Taglib here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "zlib/1.2.11@user/channel"

    download_url = 'http://{0}.org/releases/{0}-{1}.tar.gz'.format(name, version)
    patches = ['taglib/0001-Link-with-correct-STL-on-Android.patch',
               'taglib/0002-Build-a-static-and-non-static-version.patch',
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
        self.run('cmake -DCMAKE_INSTALL_PREFIX=%s/build -DCMAKE_LIBRARY_OUTPUT_PATH=%s/build/lib'
        ' -DWITH_MP4=ON -DWITH_ASF=ON -DBUILD_SHARED_LIBS=1 -DBUILD_STATIC_LIBS=1 -DCMAKE_DISABLE_FIND_PACKAGE_Boost=TRUE -DZLIB_ROOT=%s'
        ' -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DCMAKE_C_FLAGS=\" -Wall -g -O2 -m64  -Wall -g -O2 -m64  -Wall -g -O2 -m64 \"'
        ' -DCMAKE_CXX_FLAGS=\" -Wall -g -O2 -m64  -Wall -g -O2 -m64  -Wall -g -O2 -m64 \"'
        ' -DLIB_SUFFIX=  -DCMAKE_BUILD_TYPE=Release -DCMAKE_FIND_ROOT_PATH=%s'
        %(os.getcwd(),os.getcwd(),self.deps_cpp_info["zlib"].rootpath,self.cerbero_root))
        self.run('make -j4')
        self.run('make install')

    def package(self):
        for f in os.listdir('build/lib'):
            if fnmatch.fnmatch(f, '*.so*'):
                os.chmod("./build/lib/%s"%(f), stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["taglib"]


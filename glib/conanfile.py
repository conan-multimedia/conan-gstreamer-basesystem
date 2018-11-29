from conans import ConanFile, CMake, tools
import os

class GlibConan(ConanFile):
    name = "glib"
    version = "2.54.3"
    license = "LGPLv2Plus"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Glib here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = "libffi/3.99999@user/channel","zlib/1.2.11@user/channel"

    download_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.54/glib-2.54.3.tar.xz'
    patches = ["glib/0001-Let-user-disable-Cocoa-and-Carbon-support-on-demand.patch",
           "glib/0002-Optionally-revert-to-the-old-pre-2.28-URI-handler-co.patch",
           "glib/0003-Add-support-for-loading-GIO-modules-from-the-distro-.patch",
           "glib/0004-Allow-for-a-second-distro-GIO-module-path-as-used-on.patch",
           "glib/0005-Blacklist-the-bamf-GIO-module.patch",
           "glib/0006-giomodule-do-not-try-to-load-modules-from-gio-module.patch",
           "glib/0008-Unhide-_g_io_modules_ensure_extension_points_registe.patch",
           'glib/0009-Implementation-of-Cocoa-event-loop-integration-in-GM.patch',
           'glib/0010-GSocket-Fix-race-conditions-on-Win32-if-multiple-thr.patch',
           'glib/0013-gmain-Fix-erroneous-if-condition-when-dtrace-is-disa.patch',
           'glib/0001-gmodule-Use-RTLD_DEFAULT-if-defined-__BIONIC__.patch'
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
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig"%(self.deps_cpp_info["libffi"].rootpath,
                                                                        self.deps_cpp_info["zlib"].rootpath)}

        with tools.environment_append(vars):
            self.run('sh autogen.sh --prefix %s/build --libdir %s/build/lib --enable-introspection'
                     ' --with-pcre=internal --disable-libmount --enable-dtrace=no'
                     ' --enable-static --disable-selinux'%(os.getcwd(),os.getcwd()))
            self.run("make -j2")
            self.run("make install")

    def package(self):
        self.copy("*", src="build")
        ## !FIXME PC PREFIX

    def package_info(self):
        self.cpp_info.libs = ["glib"]


from conans import ConanFile, CMake, tools
import os

class GstpluginsbadConan(ConanFile):
    name = "gst-plugins-bad"
    version = "1.14.3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gstpluginsbad here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "pkg_config"
    requires = ("gstreamer/1.14.3@user/channel","gst-plugins-base/1.14.3@user/channel","bzip2/1.0.6@user/channel",
    "libass/0.13.7@user/channel","faad2/2.7@user/channel","libkate/0.4.1@user/channel","zlib/1.2.11@user/channel",
    "openh264/1.7.0@user/channel","opus/1.2.1@user/channel","nettle/3.4@user/channel","librtmp/2.4_p20151223@user/channel",
    "libsrtp/1.6.0@user/channel","libdca/0.0.5@user/channel","libmms/0.6.4@user/channel","libdvdnav/5.0.1@user/channel",
    "libnice/0.1.14@user/channel","soundtouch/1.9.2@user/channel","vo-aacenc/0.1.3@user/channel",
    "librsvg/2.40.20@user/channel","openjpeg/2.3.0@user/channel","openssl/1.1.0h@user/channel",
    "spandsp/0.0.6@user/channel","webrtc-audio-processing/0.2@user/channel","sbc/1.3@user/channel",
    "ladspa/1.13@user/channel")

    remotes = {'origin': 'https://anongit.freedesktop.org/git/gstreamer/gst-plugins-bad'}
    
    def source(self):
        self.run("git init")
        for key, val in self.remotes.items():
            self.run("git remote add %s %s"%(key, val))
        self.run("git fetch --all")
        self.run("git reset --hard %s"%(self.version))
        self.run("git submodule init && git submodule sync && git submodule update")
        self.run("git reset --hard %s"%(self.version))
        self.run("git branch cerbero_build && git checkout cerbero_build")
        self.run("git reset --hard %s"%(self.version))
        self.run("git config user.email")
        self.run("git config user.name")

    def build(self):
        vars = {'PKG_CONFIG_PATH': "%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
                ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
                ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
                ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
                ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
                ":%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig:%s/lib/pkgconfig"
                ":%s/lib/pkgconfig"
                %(
                    self.deps_cpp_info["gstreamer"].rootpath,self.deps_cpp_info["gst-plugins-base"].rootpath,
                    self.deps_cpp_info["bzip2"].rootpath, self.deps_cpp_info["libass"].rootpath,
                    self.deps_cpp_info["faad2"].rootpath,self.deps_cpp_info["libkate"].rootpath,
                    self.deps_cpp_info["zlib"].rootpath,self.deps_cpp_info["openh264"].rootpath,
                    self.deps_cpp_info["opus"].rootpath,self.deps_cpp_info["nettle"].rootpath,
                    self.deps_cpp_info["librtmp"].rootpath,self.deps_cpp_info["libsrtp"].rootpath,
                    self.deps_cpp_info["libdca"].rootpath,self.deps_cpp_info["libmms"].rootpath,
                    self.deps_cpp_info["libdvdnav"].rootpath,self.deps_cpp_info["libnice"].rootpath,
                    self.deps_cpp_info["soundtouch"].rootpath,self.deps_cpp_info["vo-aacenc"].rootpath,
                    self.deps_cpp_info["librsvg"].rootpath,self.deps_cpp_info["openjpeg"].rootpath,
                    self.deps_cpp_info["openssl"].rootpath,self.deps_cpp_info["spandsp"].rootpath,
                    self.deps_cpp_info["webrtc-audio-processing"].rootpath,self.deps_cpp_info["sbc"].rootpath,
                    self.deps_cpp_info["ladspa"].rootpath
                ),
                'LIBRARY_PATH':"%s/lib:$LIBRARY_PATH"%(self.deps_cpp_info["openjpeg"].rootpath),
                'C_INCLUDE_PATH':"%s/include:%s/include"%(self.deps_cpp_info["tiff"].rootpath,self.deps_cpp_info["soundtouch"].rootpath),
                'CPLUS_INCLUDE_PATH':"%s/include:%s/include"%(self.deps_cpp_info["tiff"].rootpath,self.deps_cpp_info["soundtouch"].rootpath)}

        with tools.environment_append(vars):
            self.run('sh ./autogen.sh --noconfigure && ./configure --prefix %s/build --libdir %s/build/lib'
            ' --enable-introspection --enable-static --disable-introspection --disable-gsm --disable-examples --disable-festival         --disable-videomaxrate --disable-bz2 --disable-libde265         --disable-linsys --disable-fbdev --disable-apexsink         --disable-celt --disable-curl --disable-dc1394 --disable-directfb         --disable-dirac --disable-faac --disable-flite --disable-gme         --disable-lv2 --disable-mimic --disable-modplug         --disable-mpeg2enc --disable-mplex --disable-musepack --disable-mythtv         --disable-neon --disable-ofa --disable-openal --disable-opencv         --disable-pvr --disable-sdl --disable-sndfile         --disable-teletextdec --disable-timidity         --disable-vdpau --disable-voamrwbenc --disable-wildmidi         --disable-xvid --disable-zbar --disable-sdi --disable-srt --enable-bz2 --enable-assrender         --enable-faad --enable-kate --enable-openh264 --enable-opus         --enable-hls --enable-rtmp --enable-srtp --enable-dts         --enable-libmms --enable-resindvd --enable-soundtouch         --enable-voaacenc'
            ' --enable-rsvg --enable-openjpeg --enable-spandsp --enable-decklink --enable-webrtc --enable-dtls'%(os.getcwd(),os.getcwd()))
            self.run('make -j4')
            self.run('make install')


    def package(self):
        self.copy("*", src="build")

    def package_info(self):
        self.cpp_info.libs = ["gst-plugins-bad"]


FAQ
===

INSTALLATION
------------

###1. Error on compiling filter in c++ with opencv.
Example, with the filter ScipyExample.py.
Do you install opencv-dev? Is this repertory exist: /usr/local/include/opencv
If not, maybe you need this: sudo ln -s /usr/include/opencv /usr/local/include/opencv

###2. Error when recording video.
Maybe you need to compile opencv with ffmpeg. Be sure you install ffmpeg dependance.
About fedora package, follow this: https://bugzilla.redhat.com/show_bug.cgi?id=812628

###3. How compile OpenCV.
Sometime, you need specific function in Opencv, this is the procedure to install it.
####a. Install required OpenCV dependencies
	sudo apt-get install cmake cmake-gui gcc pkg-config libavformat-dev libswscale-dev

####b. Download the archive manually
	From here: http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.5/opencv-2.4.5.tar.gz
	Go to directory containing downloaded file with a command line.

####c. Extract the archive
	tar -xvf OpenCV-2.4.5.tar.gz && cd OpenCV-2.4.5

####d. Configure
	mkdir release
	cd release
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON ..

####e. Compile (replace # by the number of processor core)
	make -j#

####f. Install
	sudo make install

####g. Do crazy stuff!
More information is available here: http://opencv.willowgarage.com/wiki/InstallGuide



DEVELOP FILTERS
---------------

1. How adding filters. Template of code is in the directory: filters/template/
Add your code in filters/private or filters/public
Read filters/README for more information.

2. How running filters. You need to open a client and create filterchain.
The configuration is in this directory: configurations/private or configurations/public
Read configurations/README for more information.

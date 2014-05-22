SeaGoatVision
=============
SeaGoatVision is a vision server to develop and execute filter on different media.
This Vision Server is tested on OpenCV 2.4.5 with Python 2.7 on Fedora 18, Ubuntu 12.04, Arch Linux and OSX 10.9.

Requirements
------------

 - Python 2.7
 - PyQt4
 - Glade 3
 - OpenCV 2.4 w/ Python/Numpy bindings
 - Numpy
 - Scipy
 - JSON-RPC
 - ZeroMQ

Until OpenCV 2.4 is fully supported, the preferred way is to compile OpenCV manually:
http://opencv.willowgarage.com/wiki/InstallGuide

Installation
------------
### A. Download the project
	git clone git://github.com/Octets/SeaGoatVision.git

###B. Install dependencies
#### Ubuntu :
	sudo apt-get install python python-numpy python-scipy python-opencv python-pyside python-qt4 python-imaging libopencv-dev python-pip ffmpeg
	sudo pip install jsonrpclib-pelix pyzmq

#### Fedora :
	sudo yum install python numpy scipy opencv-python python-pyside PyQt4 python-pillow-qt opencv-devel python-pip ffmpeg
	sudo pip install jsonrpclib-pelix pyzmq

#### Arch Linux :
Don't forget to active the "community" repositorie. See https://wiki.archlinux.org/index.php/Pacman

	yaourt -S python2 python2-numpy python2-scipy opencv python2-pyside python2-pyqt python2-imaging python2-pip ffmpeg
	sudo pip2 install jsonrpclib-pelix pyzmq

#### Windows :
Install the following dependencies:

 - Python:	http://python.org/ftp/python/2.7.3/python-2.7.3.msi
 - Numpy:	http://sourceforge.net/projects/numpy/files/NumPy/	# Choose the installer
 - Scipy:	http://sourceforge.net/projects/scipy/files/scipy/	# Choose the installer
 - PyQt4:	http://www.riverbankcomputing.co.uk/software/pyqt/download
 - PySide:	http://qt-project.org/wiki/PySide_Binaries_Windows
 - PIL:		http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
 - OpenCV:	http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv	# OpenCV installer for Windows.
 - pip:		https://github.com/simpleservices/app_report-python/wiki/How-to-install-pip-on-Windows
 - ffmpeg:	http://ffmpeg.zeranoe.com/builds/	# Install the static version

	pip install jsonrpclib-pelix pyzmq

#### Mac OSX :
Start by installing Xcode command-line tools. On 10.9 Mavericks, this is as straightforward as entering this line in a terminal:

	xcode-select --install

On previous versions, you'll have to download the package from Apple Dev website at http://developers.apple.com/downloads .

You will also need the QT4 library. Grab it from the official QT Project site (http://qtproject.org/downloads). You'll also need to fetch the PySide Mac binary from the side. Install both.

For recording video, we use ffmpeg : http://ffmpegmac.net/

Then, from the terminal:

	sudo easy_install pip pil
	sudo pip install numpy scipy pyqt libopencv jsonrpclib-pelix pyzmq

Finally, you will need to compile OpenCV with python bindings from source. Please refer to the FAQ for this.

### C. Third-party Libs

#### PyDC1394

Note: pydc1394 is dependant on cython 0.19. Make sure it is installed, using easy_install:

	easy_install cython

Go to the root of the SeaGoatVision project and setup git submodule for pydc1394:

	git submodule init
	git submodule update

In the case submodule update doesn't work, you can always clone the repo manually. From the root of the project:

	cd thirdparty/public
	rm -rf pydc1394
	git clone https://github.com/mathben/PyDC1394.git pydc1394

### D. Compile
To compile the filters in Cpp and the third-party, do on the root of the project:

	make


This Vision Serveur is tested on OpenCV 2.4.2 and Python 2.7 on Fedora 17 and Ubuntu 12.04.

Requirements:
 - Python 2.7
 - PyQt4
 - Glade 3
 - OpenCV 2.4 w/ Python/Numpy bindings
 - Numpy
 - Scipy

Until OpenCV 2.4 is fully supported, the preferred way is to compile OpenCV manually: 
 - http://opencv.willowgarage.com/wiki/InstallGuide

==== INSTALLATION ====

A. Install dependencies

Ubuntu :
	sudo apt-get install python python-numpy python-scipy python-opencv python-protobuf protobuf-compiler python-pyside python-qt4 python-imaging

Fedora :
	sudo yum install python numpy scipy opencv-python protobuf-python protobuf protobuf-compiler python-pyside PyQT4 python-imaging

Arch Linux package :
	python2 python2-numpy python2-scipy opencv protobuf protobuf-python python2-pyside python2-pyqt python2-imaging
Some package is on aur, you can use yaourt or pacman.

Windows :
Install the following dependencies :
 - Python: 	http://python.org/ftp/python/2.7.3/python-2.7.3.msi
 - Numpy: 	http://sourceforge.net/projects/numpy/files/NumPy/	# Choose the installer
 - Scipy:	http://sourceforge.net/projects/scipy/files/scipy/	# Choose the installer
 - PyQt4:	http://www.riverbankcomputing.co.uk/software/pyqt/download
 - PySide: 	http://qt-project.org/wiki/PySide_Binaries_Windows
 - PIL:		http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
 - OpenCV: 	http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv	# OpenCV installer for Windows.

B. Install OpenCV 2.4

1. Install required OpenCV dependencies
	sudo apt-get install cmake cmake-gui gcc pkg-config libavformat-dev libswscale-dev

2. Download the archive manually 
	From here: http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.2/OpenCV-2.4.2.tar.bz2/
	Go to directory containing downloaded file with a command line.
 
3. Extract the archive
	tar -jxvf OpenCV-2.4.2.tar.bz2 && cd OpenCV-2.4.2

4. Configure
	mkdir release
	cd release
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON ..

5. Compile
	make -j

6. Do crazy stuff!

More information is available here: http://opencv.willowgarage.com/wiki/InstallGuide


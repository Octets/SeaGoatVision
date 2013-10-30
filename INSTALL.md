SeaGoatVision
=============
SeaGoatVision is a vision server to develop and execute filter on different media.
This Vision Serveur is tested on OpenCV 2.4.5 with Python 2.7 on Fedora 18, Ubuntu 12.04 and Arch Linux.

Requirements
------------

 - Python 2.7
 - PyQt4
 - Glade 3
 - OpenCV 2.4 w/ Python/Numpy bindings
 - Numpy
 - Scipy
 - JSON-RPC

Until OpenCV 2.4 is fully supported, the preferred way is to compile OpenCV manually:
http://opencv.willowgarage.com/wiki/InstallGuide

Installation
------------
### A. Download the project
    git clone git://github.com/Octets/SeaGoatVision.git

###B. Install dependencies
#### Ubuntu :
    sudo apt-get install python python-numpy python-scipy python-opencv python-pyside python-qt4 python-imaging libopencv-dev python-pip
    sudo pip install jsonrpclib-pelix

#### Fedora :
	sudo yum install python numpy scipy opencv-python python-pyside PyQT4 python-imaging opencv-devel python-pip
	sudo pip install jsonrpclib-pelix

#### Arch Linux :
Don't forget to active the "community" repositorie. See https://wiki.archlinux.org/index.php/Pacman

	pacman -S python2 python2-numpy python2-scipy opencv python2-pyside python2-pyqt python2-imaging python2-pip
	sudo pip2 install jsonrpclib-pelix

#### Windows :
Install the following dependencies:

 - Python:	http://python.org/ftp/python/2.7.3/python-2.7.3.msi
 - Numpy:	http://sourceforge.net/projects/numpy/files/NumPy/	# Choose the installer
 - Scipy:		http://sourceforge.net/projects/scipy/files/scipy/	# Choose the installer
 - PyQt4:	http://www.riverbankcomputing.co.uk/software/pyqt/download
 - PySide:	http://qt-project.org/wiki/PySide_Binaries_Windows
 - PIL:		http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
 - OpenCV:	http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv	# OpenCV installer for Windows.
 - pip:		https://github.com/simpleservices/app_report-python/wiki/How-to-install-pip-on-Windows

### C. Third-party
Note: The third-party pydc1394 is dependant of cython 0.19. Be sure you have it, else install it with easy_install from his website. You don't need Pydc1394 if you haven't Firewire camera.

On the root of the project:

    git submodule init
    git submodule update

### D. Compile
To compile the filters in Cpp and the third-party, do on the root of the project:

    make


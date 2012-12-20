This Vision Serveur is tested on OpenCV 2.4.2 and Python 2.7 on Fedora 17 and Ubuntu 12.04.

Requirements:
 - Python 2.7
 - PyGObjet/GTK+3
 - Glade 3
 - OpenCV 2.4 w/ Python/Numpy bindings
 - Numpy

Until OpenCV 2.4 is fully supported, the preferred way is to compile OpenCV manually: 
 - http://opencv.willowgarage.com/wiki/InstallGuide

==== INSTALLATION ====

A. Install dependencies
     Execution only :
 sudo apt-get install glade python python-numpy python-scipy python-opencv protobuf-python protobuf

    Compilation proto : 
 sudo apt-get install protobuf-compiler

    Client qt :
 sudo apt-get install python-pyside python-qt4

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



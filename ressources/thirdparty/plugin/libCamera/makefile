all:
	g++ -Wall -fexceptions -I/usr/include/python2.7 -I/usr/lib/python2.7/dist-packages/numpy/core/include/numpy  -g     -c /home/yohan/git/SeaGoatVision/ressources/thirdparty/plugin/libCamera/camera.cpp -o obj/Debug/camera.o
	g++ -Wall -fexceptions -I/usr/include/python2.7 -I/usr/lib/python2.7/dist-packages/numpy/core/include/numpy  -g     -c /home/yohan/git/SeaGoatVision/ressources/thirdparty/plugin/libCamera/main.cpp -o obj/Debug/main.o
	g++ -shared  obj/Debug/camera.o obj/Debug/main.o   -o bin/Debug/camera.so x86/4.5/libPvAPI.a x86/4.5/libImagelib.a  -glibc -lrt -lopencv_core -lopencv_highgui -lpthread -lpython2.7 -lboost_python-mt-py27


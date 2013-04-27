CC = g++
CFLAGS = -Wall -fexceptions -I/usr/include/python2.7 -I/usr/lib/python2.7/dist-packages/numpy/core/include/numpy -g -c 
LDFLAGS = -lrt -lopencv_core -lopencv_highgui -lpython2.7 -lboost_python

all : camera.so

camera.o: camera.cpp
			$(CC) $(CFLAGS) camera.cpp 
main.o: main.cpp
		$(CC) $(CFLAGS) main.cpp 

camera.so: main.o camera.o
			$(CC) -shared main.o camera.o -o camera.so x86/4.5/libPvAPI.a x86/4.5/libImagelib.a $(LDFLAGS)

install:
	sudo mv camera.so /usr/lib/python2.7/
	
clean: 
	rm -rf *.o camera.so


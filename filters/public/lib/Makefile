CFLAGS= -c -fPIC
LDFLAGS= -shared -lm `pkg-config --cflags --libs opencv`

ALL:
	gcc $(CFLAGS) lib.cpp -o lib.o
	gcc lib.o $(LDFLAGS) -o liblib.so

clean:
	-rm lib.o
	-rm liblib.so

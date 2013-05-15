CPPFLAGS=-I../deps/eigen -I../deps/qd/include -I../include
LDFLAGS=../deps/qd/src/libqd.a

all: libdrunkardswalk.so libdrunkardswalk.a

drunkardswalk.o: ../include/drunkardswalk/solve.h

libdrunkardswalk.so: drunkardswalk.o ../deps/qd/src/libqd.a
	$(CXX) -shared -o $@ drunkardswalk.o $(CXXFLAGS) $(LDFLAGS) $(CPPFLAGS)

libdrunkardswalk.a: drunkardswalk.o ../deps/qd/src/libqd.a
	ar rcs $@ drunkardswalk.o 

.PHONY: clean

clean:
	-rm -f libdrunkardswalk.so libdrunkardswalk.a drunkardswalk.o

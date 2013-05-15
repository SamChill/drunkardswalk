CPPFLAGS=-I../deps/eigen -I../deps/qd/include -I../include
LDFLAGS=../deps/qd/src/libqd.a

all: libdrunkardswalk.so libdrunkardswalk.a

libdrunkardswalk.so: drunkardswalk.o ../deps/qd/src/libqd.a
	$(CXX) -shared -o $@ libdrunkardswalk.o $(CXXFLAGS) $(LDFLAGS) $(CPPFLAGS)

libdrunkardswalk.a: drunkardswalk.o ../deps/qd/src/libqd.a
	ar rcs $@ libdrunkardswalk.o 

.PHONY: clean

clean:
	-rm -f libdrunkardswalk.so libdrunkardswalk.a drunkardswalk.o

CXX=g++
#CXXFLAGS=-O3 -fPIC 
#can be compiled with threading
CXXFLAGS=-O3 -fPIC -fopenmp

#intel c++ compiler
#CXX=icpc
#must use -fp-model precise with intel compiler or extended precision 
#CXXFLAGS=-O2 -fPIC -openmp -fp-model precise -vec-report1
#AR=xiar

PREFIX?=/usr/local

export CXX CXXFLAGS AR

.PHONY: clean deps/qd/src src

all: deps/qd/src src

test: all
	$(MAKE) -C test

install: all
	test -d $(PREFIX) || mkdir $(PREFIX)

	test -d $(PREFIX)/lib || mkdir $(PREFIX)/lib
	install -c src/libdrunkardswalk.a $(PREFIX)/lib
	install -c src/libdrunkardswalk.so $(PREFIX)/lib
	test -d $(PREFIX)/include || mkdir $(PREFIX)/include

	test -d $(PREFIX)/include/drunkardswalk || \
		mkdir $(PREFIX)/include/drunkardswalk
	install -c include/drunkardswalk/solve.h $(PREFIX)/include/drunkardswalk

deps/qd/src src:
	$(MAKE) -C $@

clean:
	$(MAKE) -C src clean
	$(MAKE) -C deps/qd/src clean

src: deps/qd/src

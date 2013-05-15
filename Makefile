CXX=g++
CXXFLAGS=-O3 -fPIC 
#can be compiled with threading
#CXXFLAGS=-O3 -fPIC -fopenmp

export CXX CXXFLAGS

.PHONY: clean deps/qd/src src

all: deps/qd/src src

deps/qd/src src:
	$(MAKE) -C $@

clean:
	$(MAKE) -C src clean
	$(MAKE) -C deps/qd/src clean

src: deps/qd/src

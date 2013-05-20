.PHONY:clean

CPPFLAGS+=-I../../deps/eigen -I../../include

example: example.o
	$(CXX) -o $@ example.o

clean:
	-rm -f example.o example

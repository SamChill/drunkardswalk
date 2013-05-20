.PHONY:simple all performance random 

CPPFLAGS+=-I../deps/eigen -I../include

simple:
	python simple.py

all: simple random performance

performance:
	python performance.py

random:
	python random_chain.py

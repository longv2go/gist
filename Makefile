CCFLAGS = -fPIC -g -O2 -m64
CFLAGS = $(CCFLAGS)
LDFLAGS = -lOpenCL

INC_DIRS = /usr/local/cuda/include
LIB_DIRS = /usr/local/cuda/lib64

SRCS = src/test_aaa.cpp\
    src/test_kernel.cu\
    src/test_processor.cpp

OBJS = $(SRCS:.cpp=.o) $(SRCS:.cu=.o)

%.o: %.cpp
    g++ -c $(CCFLAGS) -I$(INC_DIRS) $< -o $@

%.o: %.cu
    nvcc --compiler-options $(CCFLAGS) -I$(INC_DIRS) -c $< -o $@

libtest.a: $(OBJS)
    @$(AR) -rvcs $@ $^

sample: src/test_sample.o
    g++ $(LDFLAGS) -o test_sample

.PHONY: clean
clean:
    @rm src/*o libtest.a

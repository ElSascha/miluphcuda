# This is the miluphcuda Makefile.

CC = /usr/bin/g++
CFLAGS   = -c -std=c99 -O3 -DVERSION=\"$(GIT_VERSION)\" -fPIC
LDFLAGS  = -lm

GIT_VERSION := $(shell git describe --abbrev=4 --dirty --always --tags)

CUDA_DIR    = $(HOME)/.conda/envs/miluphcuda
NVCC   = $(CUDA_DIR)/bin/nvcc

NVFLAGS  = -ccbin ${CC} -x cu -c -dc -O3 -Xcompiler "-O3 -pthread -fPIE" -Wno-deprecated-gpu-targets -DVERSION=\"$(GIT_VERSION)\" --ptxas-options=-v
GPU_ARCH = -arch=sm_80

CUDA_LIB      = $(CUDA_DIR)
INCLUDE_DIRS += -I$(CUDA_DIR)/include -I/usr/lib/openmpi/include -I/usr/include/hdf5/serial
LDFLAGS      += -L$(CUDA_LIB)/lib -L$(CUDA_LIB)/lib64 -L/usr/lib/x86_64-linux-gnu/hdf5/serial \
				-Xlinker -rpath -Xlinker $(CUDA_LIB)/lib -Xlinker -rpath -Xlinker $(CUDA_LIB)/lib64 -lcudart -lpthread -lconfig -lhdf5



# --- Project structure ---
# include both top-level source directories: src and lib (some sources live in lib/)
SRC_DIRS   = src lib
INC_DIR    = include
LIB_DIR    = lib
OBJ_DIR    = build/obj
BIN_DIR    = build/bin


# Create dirs if not existing
$(shell mkdir -p $(OBJ_DIR) $(BIN_DIR))

# --- Source discovery ---
## Find source files recursively under each source dir (handles nested folders like src/integration)
SRC_C   = $(shell find $(SRC_DIRS) -type f -name '*.c')
SRC_CU  = $(shell find $(SRC_DIRS) -type f -name '*.cu')

# --- Object files ---
# Map any source file under the listed source dirs to build/obj/<dir>/file.o
OBJ_C   = $(patsubst %.c,$(OBJ_DIR)/%.o,$(SRC_C))
OBJ_CU  = $(patsubst %.cu,$(OBJ_DIR)/%.o,$(SRC_CU))
OBJECTS = $(OBJ_C) $(OBJ_CU)

# --- Output binary ---
TARGET = $(BIN_DIR)/miluphcuda

# --- Include directories ---
INCLUDE_DIRS += $(addprefix -I, $(INC_DIR) $(SRC_DIRS))
INCLUDE_DIRS += -Iinclude -Iinclude -Iinclude/hydro -Iinclude/lib -Iinclude/integration
LIBRARY_DIRS = -L$(LIB_DIR) -L$(HOME)/.conda/envs/miluphcuda/lib -L/usr/lib/x86_64-linux-gnu/hdf5/serial
# --- Build rules ---
all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(NVCC) $(GPU_ARCH) $(OBJECTS) $(LDFLAGS) -o $@


# Compile .c files into build/obj (works for src/ and lib/ subdirs)
$(OBJ_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCLUDE_DIRS) -o $@ $<


# Compile .cu files into build/obj (works for src/ and lib/ subdirs)
$(OBJ_DIR)/%.o: %.cu
	@mkdir -p $(dir $@)
	$(NVCC) $(GPU_ARCH) $(NVFLAGS) $(INCLUDE_DIRS) -o $@ $<

# --- Cleanup ---
.PHONY: clean
clean:
	@rm -rf $(OBJ_DIR) $(BIN_DIR)
	@echo "make clean: done"

# --- Dependencies ---
$(OBJ_C):  $(HEADERS) Makefile
$(OBJ_CU): $(HEADERS) $(CUDA_HEADERS) Makefile
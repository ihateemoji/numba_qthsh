# Variables
CC = gcc
CFLAGS = -Wall -O3 -march=native -shared -fPIC
LDFLAGS = -lm
SRC = src/qthsh.c
OBJ = numba_qthsh/qthsh.so

# Target to build the shared library
$(OBJ): $(SRC)
	$(CC) $(CFLAGS) $(SRC) $(LDFLAGS) -o $(OBJ)

# Phony target for clean
.PHONY: clean
clean:
	rm -rf $(OBJ)

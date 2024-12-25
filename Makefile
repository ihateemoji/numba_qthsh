qthsh.o: src/qthsh.c
	gcc -Wall src/qthsh.c -lm -O3 -march=native -shared -fPIC -o numba_qthsh/qthsh.so

clean:
	rm -rf numba_qthsh/qthsh.so

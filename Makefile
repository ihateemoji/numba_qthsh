qthsh.o: src/qthsh.c
	gcc -Wall src/qthsh.c -lm -O3 -march=native -shared -fPIC -o qthsh.so

clean:
	rm -rf qthsh.so

void negativo_im_c(unsigned char *array_in,int T, unsigned char *array_out)
{
    for (int i=0;i<T;i++)
    {
        array_out[i] = 255-array_in[i];
    }

}
/*

gcc suma.c -o suma
 

para generar el object file
gcc -c -Wall -Werror  -fpic  c_fib.c

para crear la shared library
gcc -shared  c_fib.o -o _c_fib.so
*/
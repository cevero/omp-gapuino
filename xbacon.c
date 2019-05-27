#include <stdio.h>
#include <omp.h>
#include "omp_gap8.h"
void function(){
int soma;
soma = 10;
#pragma omp parallel
printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}

int main()
{
    int soma=400,a=10,w=5,b=10,c=2,r = 30;
    int nada = 2000;
    function();
#pragma omp parallel for default(none) private(b,r,soma) shared(a,c) reduction(+:soma)
for (int i = 0 ; i < nada; i++  )
{
    a+=b+i;
#pragma omp single
    {   
        printf("%d\n",a);
        c+=a;
    }
    printf("o valor de a no core %d e: %d\n",omp_get_thread_num(),a);
    soma+=b+c;
}

function();
    //teste na main
    //outro teste
printf("o resultado da soma e %d\n",soma);
exit (0);

}

//teste dps da main

#include "cmsis.h"
#include "gap_common.h"
#include "mbed_wait_api.h"
// FEATURE_CLUSTER
#include "gap_cluster.h"
#include "gap_dmamchan.h"
#include <time.h>
#define CORE_NUMBER   (8)
#include <stdio.h>
#include "omp_gap8.h"
void generic_function0(void* gen_var0){

printf("sera que vai dar certo no core: %d\n",omp_get_thread_num());
}
void generic_function1(void* gen_var1){

printf("Hello fom core %d\n",omp_get_thread_num());
}
void generic_function2(void* gen_var2){
{
    printf("esse teste veio do core ");
    printf("%d\n",omp_get_thread_num());
}

}
void caller(void* arg){
int x = (int)arg;
if(x ==0)return generic_function0(0);
if(x ==1)return generic_function1(0);
if(x ==2)return generic_function2(0);
}


void Master_Entry(void *arg) {
    CLUSTER_CoresFork(caller, arg);
}
void function(){
int soma;
soma = 10;
CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)0, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
}

int main()
{
CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)1, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
CLUSTER_Start(0, CORE_NUMBER);
CLUSTER_SendTask(0, Master_Entry, (void *)2, 0);
CLUSTER_Wait(0);
CLUSTER_Stop(0);
function();
    //teste na main
    //outro teste

exit (0);

}

//teste dps da main

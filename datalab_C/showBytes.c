#include <stdio.h> 
#include <string.h>

typedef unsigned char *byte_pointer;

void show_bytes(byte_pointer start, int len){
    int i;
    for (i = 0; i < len; i++)
        printf("%.2x", start[i]);
    //printf("\n");
}

void show_int(int x){
    show_bytes((byte_pointer) &x, sizeof(float));
}

void show_float(float x){
    show_bytes((byte_pointer) &x, sizeof(float));
}

void show_pointer(void *x){
    show_bytes((byte_pointer) &x, sizeof(void *));
}

void show_string(char xs[]){
    for (int i = 0; i < strlen(xs); i++){
        show_bytes((byte_pointer) &xs[i], sizeof(char));
    }
}

void show_twos_complement(int x){
    int y = (~x)+1;
    show_bytes((byte_pointer) &x, sizeof(float));
    show_bytes((byte_pointer) &y, sizeof(float));
}

void main(){
    //show_int(12);
    //show_float(2.4);

    char apple[] = "apple";
    show_string(apple);
    printf("\n");
    char orange[] = "orange";
    show_string(orange);
    printf("\n");
    char pear[] = "pear";
    show_string(pear);
    printf("\n");
    
    show_twos_complement(12);
    printf("\n");
    show_twos_complement(64);
    printf("\n");
    show_twos_complement(37);
}
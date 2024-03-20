#include <stdio.h>

//Any bit of x equals 1.
//if x == 0000 0000 0000 0000 then return false, otherwise return true
int any1(int x){
    return x;
}

//if x == 1111 1111 1111 1111 then return false, otherwise return true
int any0(int x){
    return ~x;
}

//if x == ____ ____ ____ 0000 return false, otherwise return true.
int any1_in_byte(int x){
    x << sizeof(int) - 4;
    return x;
}

//if x == ____ ____ ____ 1111 return false, otherwise return true.
int any0_in_byte(int x){
    x = ~x;
    x << sizeof(int) - 4;
    return x;
}
void main(){
    
}
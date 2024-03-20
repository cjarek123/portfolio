// K = 10
// K = -9
// K = 120
// K = -224

// In order to multiply a number by 2^n, shift the bits n times to the left. To divide by 2^n, shift the bits n times right

#include <stdio.h>

int russian_peasant_algorithm(int x, int y){
    int result = 0;

    while(y > 0){
        if (y & 1)
            result = result + x;
        
        x = x << 1;
        y = y >> 1;
    }
    return result;
}

int times_10(int x){
    return russian_peasant_algorithm(x, 10);
}

int times_negative9(int x){
    int result = russian_peasant_algorithm(x, 9);
    result = (~result)+1;
    return result;
}

int times_120(int x){
    return russian_peasant_algorithm(x, 120);
}

int times_negative224(int x){
    int result = russian_peasant_algorithm(x, 10);
    result = (~result)+1;
    return result;
}

int russian_peasant_altered(int x, int y){
    int neg = 0;
    if((x < 0) ^ (y < 0)){
        neg = 1;
    }
    x = abs(x);
    y = abs(y);
    
    int result = 0;
    while(y > 0){
        if (y & 1)
            result = result + x;
        
        x = x << 1;
        y = y >> 1;
    }

    if (neg){
        return (~result)+1;
    }else{
        return result;
    }
}

void main(){

    printf("%d\n", russian_peasant_algorithm(67, 3));

    printf("%d\n", times_negative9(7));

    printf("%d\n", russian_peasant_altered(-3, -7));
}
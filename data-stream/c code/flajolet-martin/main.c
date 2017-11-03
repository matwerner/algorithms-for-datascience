//
//  main.c
//  flajolet-martin
//
//  Created by Varela on 11/3/17.
//  Copyright © 2017 Varela. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <time.h> 
#include <math.h>

const double MAX_X = 10000000000.0;
double random_generator() {
    double z = (double)rand()/RAND_MAX;
    printf("z:%f\n", z);
    double x = fmin(1/(z*z), MAX_X);
    printf("x:%f\n", x);
    return x;
}

int main(int argc, const char *argv[]) {
    srand((unsigned int)time(NULL));

    unsigned long batch_size = 0, stream_size = 0 ;

    for (int i = 0; i < argc; ++i)
    {
        switch (i) {
            case 1:
                batch_size = (unsigned long)argv[i];
                printf("argv[%d]: batch_size=%s\n", i, argv[i]);
                break;
            case 2:
                stream_size = (unsigned long)argv[i];
                printf("argv[%d]: stream_size=%s\n", i, argv[i]);
                break;
        }

    }
//    unsigned long x = 0;
//    for (int i =0; i < 100; i++) {
//        x = (unsigned long)random_generator();
//        printf("unsigned long(x):%lu\n", x);
//    }

    return 0;
}

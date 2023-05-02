#include<stdlib.h>

#include "rng.h"

uint32_t rng_random() {
    uint32_t r = 0;
    r = arc4random();
    return r;
}

uint64_t rng_random64() {
    uint64_t r = rng_random();
    r <<= 32;
    r |= rng_random();

    return r;
}

uint32_t rng_bounded_random(uint32_t bound) {
    return arc4random_uniform(bound);
}

#ifndef RNG_H
#define RNG_H

#include<inttypes.h>

uint32_t rng_random();
uint64_t rng_random64();
uint32_t rng_bounded_random(uint32_t bound);

#endif

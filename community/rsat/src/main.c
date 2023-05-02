#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<time.h>
#include<inttypes.h>
#include<errno.h>
#include<assert.h>
#include<math.h>
#include<omp.h>
#include<stdbool.h>

#include<z3.h>

#include "pcg_basic.h"
#include "rng.h"


typedef struct {
    char* prefix;
    uint64_t nb_vl;
    uint64_t nb_vh;
    uint64_t nb_cl;
    uint64_t nb_ch;
    uint64_t nb_f;
    uint64_t k;

    bool check_sat;
} Options;

Options options_default() {
    Options r = {
        .prefix = NULL,
        .nb_vl = 50,
        .nb_vh = 0,
        .nb_cl = 100,
        .nb_ch = 0,
        .nb_f = 10,
        .k = 3,
        .check_sat = false,
    };
    return r;
}

void print_help_screen() {
    printf("rsat options:\n"
    "--nvl uint\n"
        "\tset the minimum number of variables (default: 50)\n"
    "--ncl uint\n"
        "\tset the minimum number of clauses (default: 100)\n"
    "--nvh uint\n"
        "\tset the maximum number of variables (default: 0 -> nvh = nvl)\n"
    "--nch uint\n"
        "\tset the maximum number of clauses (default: 0 -> nch = ncl)\n"
    "--k  uint\n"
        "\tset the size of each clause (default: 3)\n"
    "--nf uint\n"
        "\tset the number of formulas to generate (default: 10)\n"
    "--prefix str\n"
        "\tset a prefix to the formula file names\n"
    "--sat\n"
        "\tonly generate sat formulas (default: false)\n"
    "--help\n"
    "-h\n"
        "\tdisplay this help screen\n"
    "\ntotal number of formulas generated: $nf * ($nvh - $nvl + 1) * ($nch - $ncl + 1)\n"
    );
}

uint64_t parse_int(char const * restrict str) {
    errno = 0;
    int64_t n = strtol(str, NULL, 10);
    if(errno != 0 || n < 0) {
        fprintf(stderr, "error while parsing number \"%s\"\nexiting\n", str);
        exit(EXIT_FAILURE);
    }
    return n;
}

double parse_double(char const * restrict str) {
    double res;

    if(1 != sscanf(str, "%lf", &res) || res < 0) {
        fprintf(stderr, "error while parsing float number \"%s\"\nexiting\n", str);
        exit(EXIT_FAILURE);
    }
    return res;
}

Options options_parse(int argc, char** argv) {
    Options r = options_default();

    for(int i = 1; i < argc; i++) {
        if(!strcmp(argv[i], "--nvl")) {
            i++;
            r.nb_vl = parse_int(argv[i]);
        }
        else if(!strcmp(argv[i], "--ncl")) {
            i++;
            r.nb_cl = parse_int(argv[i]);
        }
        else if(!strcmp(argv[i], "--nvh")) {
            i++;
            r.nb_vh = parse_int(argv[i]);
        }
        else if(!strcmp(argv[i], "--nch")) {
            i++;
            r.nb_ch = parse_int(argv[i]);
        }
        else if(!strcmp(argv[i], "--nf")) {
            i++;
            r.nb_f = parse_int(argv[i]);
        }
        else if(!strcmp(argv[i], "--k")) {
            i++;
            r.k = parse_int(argv[i]);
        }
        else if(!strcmp(argv[i], "--prefix")) {
            i++;
            r.prefix = argv[i];
        }
        else if(!strcmp(argv[i], "--sat")) {
            r.check_sat = true;
        }
        else if(!strcmp(argv[i], "--help") || !strcmp(argv[i], "-h")) {
            print_help_screen();
            exit(EXIT_SUCCESS);
        }
        else {
            print_help_screen();
            fprintf(stderr, "unrecognized option:\n\"%s\"\n", argv[i]);
            perror("exiting due to errors\n");
            exit(EXIT_FAILURE);
        }
    }

    if(r.nb_ch == 0 || r.nb_ch <= r.nb_cl) {
        r.nb_ch = r.nb_cl;
    }
    if(r.nb_vh == 0 || r.nb_vh <= r.nb_vl) {
        r.nb_vh = r.nb_vl;
    }

    return r;
}

bool contains(int64_t const * st, int64_t const * const ed, int64_t const v) {
    for(;st != ed; ++st) {
        if(*st == v) {
            return true;
        }
    }
    return false;
}

/**
 * k: size of each clause
 * nb: total number of clauses
 * c: pos of new clause
 */
bool already_generated(int64_t const * cls, uint64_t k, uint64_t nb, uint64_t c) {
    for(uint64_t i = 0; i < nb; i++) {
        if(i != c && !memcmp(&cls[i * k], &cls[c * k], k * sizeof(int64_t))) {
            return true;
        }
    }
    return false;
}

void genFormula(pcg32_random_t* rng, uint64_t nv, uint64_t nc, uint64_t k, char const * path) {
    FILE* file = fopen(path, "w");

    fprintf(file, "p cnf %" PRIu64 " %" PRIu64 "\n", nv, nc);

    int64_t * cls = malloc(sizeof(int64_t) * k * nc);
    for(uint64_t c = 0; c < nc; c++) {
         do {
             for(uint64_t i = c * k; i < (c + 1) * k; i++) {
                 do {
                     cls[i] = pcg32_boundedrand_r(rng, nv) + 1;
                 } while(contains(cls + c * k, cls + i, cls[i]));
             }

             for(uint64_t i = c * k; i < (c + 1) * k; i++) {
                 cls[i] *= pcg32_boundedrand_r(rng, 2) ? -1 : 1;
             }
         } while(already_generated(cls, k, c, c));

        for(uint64_t ki = 0; ki < k; ki++) {
            fprintf(file, "%" PRIi64 " ", cls[c * k + ki]);
        }
        fprintf(file, "0\n");
    }

    free(cls);
    fclose(file);
    /*printf("done %" PRIu64 "\n", nc);*/
}

bool is_sat(char const* path) {
    Z3_config conf = Z3_mk_config();
    Z3_context context = Z3_mk_context(conf);
    Z3_solver solver = Z3_mk_solver(context);

    Z3_solver_from_file(context, solver, path);

    bool res = Z3_solver_check(context, solver) == Z3_L_TRUE;

    Z3_del_context(context);
    Z3_del_config(conf);

    return res;
}

/**
 * usage:
 * rsat #v #c k
 */
int main(int argc, char** argv) {
    Options options = options_parse(argc, argv);
    //pcg32_srandom(time(NULL) ^ (intptr_t)&printf, (intptr_t)&options);
    uint64_t const num_threads = omp_get_max_threads();
    pcg32_random_t* rng_state = malloc(sizeof(pcg32_random_t) * num_threads);

    for(uint64_t i = 0; i < num_threads; i++) {
        // pcg32_srandom(time(NULL) ^ rng_random64(), rng_random64());
        pcg32_srandom_r(rng_state + i, time(NULL) ^ rng_random64(), rng_random64());
    }


    uint64_t path_len = ceil(log(options.nb_f))
        + ceil(log(options.nb_vh))
        + ceil(log(options.nb_ch))
        + 2
        + 4
        + 1
        ;
    if(options.prefix != NULL) {
        path_len += strlen(options.prefix);
    }

#pragma omp parallel for collapse(3)
    for(uint64_t c = options.nb_cl; c <= options.nb_ch; c++) {
        for(uint64_t v = options.nb_vl; v <= options.nb_vh; v++) {
            for(uint64_t i = 0; i < options.nb_f; i++) {
                bool unsat = true;
                char* path = malloc(path_len * sizeof(char));

                pcg32_random_t* rng = rng_state + omp_get_thread_num();

                if(options.prefix == NULL) {
                    sprintf(path, "%" PRIu64 ".%" PRIu64 ".%" PRIu64 ".cnf", v, c, i);
                }
                else {
                    sprintf(path, "%s%" PRIu64 ".%" PRIu64 ".%" PRIu64 ".cnf", options.prefix, v, c, i);
                }

                do {
                    genFormula(rng, v, c, options.k, path);
                    unsat = options.check_sat && !is_sat(path);
                } while(unsat);

                printf("%s\n", path);
                free(path);
            }
        }
    }
    free(rng_state);

    return EXIT_SUCCESS;
}

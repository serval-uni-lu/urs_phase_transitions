#include<iostream>
#include<string>

#include "CNF.hpp"

void print_stats(std::string const& path, CNF & cnf) {
    cnf.simplify();
    cnf.compute_free_vars();
    
    std::cout << "\nc file, #v, #vu, #vf, #c-u, #c2, #v2, #c3, #v3, #c4, #v4, #c5, #v5\nc ";

    std::cout << path << ", ";

    std::cout << cnf.nb_vars() << ", ";
    std::cout << cnf.nb_units() << ", ";
    std::cout << cnf.nb_free_vars() << ", ";
    std::cout << cnf.nb_active_clauses() << ", ";

    auto nb_by_k = cnf.get_nb_by_clause_len();
    auto var_by_k = cnf.get_vars_by_clause_len();

    for(std::size_t i = 2; i <= 5; i++) {
        if(i < nb_by_k.size()) {
            std::cout << nb_by_k[i] << ", " << var_by_k[i].size();
        }
        else {
            std::cout << "0, 0";
        }
        if(i < 5) {
            std::cout << ", ";
        }
    }
    std::cout << "\n";
}

int main(int argc, char const** argv) {
    if(argc < 2) {
        std::cerr << "too few arguments\nexiting\n";
        exit(1);
    }

    std::string const path(argv[1]);
    CNF cnf(path.c_str());
    cnf.simplify();
    cnf.subsumption();


#ifdef RENAME
    //cnf.compute_free_vars();
    std::cout << cnf.rename_vars();
#else
    std::cout << cnf;
#endif

#ifdef STATS
    print_stats(path, cnf);
#endif

    return 0;
}

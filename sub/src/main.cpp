#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<algorithm>
#include<random>

#include "CNF.hpp"

int main(int argc, char const** argv) {
    if(argc < 2) {
        std::cerr << "sub <nb subs> <cnf>\n";
        std::cerr << "too few arguments\nexiting\n";
        exit(1);
    }

    int const nb_subs = std::stoi(argv[1]);
    std::string const path(argv[2]);

    CNF cnf(path.c_str());

    std::random_device dev;
    std::mt19937 g(dev());

    std::vector<std::size_t> ids;
    for(std::size_t i = 0; i < cnf.nb_clauses(); i++) {
        ids.push_back(i);
    }

    std::size_t const split_size = cnf.nb_clauses() / (nb_subs + 1);
    for(int i = 1; i <= nb_subs; i++) {
        std::shuffle(ids.begin(), ids.end(), g);

        std::size_t const lsplit = i * split_size;

        for(std::size_t j = 0; j < lsplit; j++) {
            cnf.set_active(j, false);
        }

        std::ofstream out(path + ".s" + std::to_string(i) + ".cnf");
        out << cnf;
        out.close();


        for(std::size_t j = 0; j < lsplit; j++) {
            cnf.set_active(j, true);
        }
    }

    return 0;
}

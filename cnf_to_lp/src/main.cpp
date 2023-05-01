#include<iostream>
#include<cstdlib>

#include "cnf.hpp"

int main(int argc, char** argv) {
    CNF cnf(argv[1]);

    std::size_t const k = strtoll(argv[2], 0, 10);
    double const r = strtold(argv[3], 0);
    //cnf.simplify();

    //std::cout << "min: Z;\n";
    std::cout << "min: Z;\n";
    //std::cout << "T <= X;\n-T <= X;\n\n";
    //std::cout << "T > 1;\n";
    std::cout << "Y - " << (r) << " * X <= Z;\n";
    std::cout << "-Y + " << (r) << " * X <= Z;\n";
    std::cout << "Y > 1;\nX > 1;\n";
    std::set<int> vars;

    std::cout << "Y =";
    for(std::size_t ci = 0; ci < cnf.get_nb_clauses(); ci++) {
        std::cout << " c" << ci;
        if(ci + 1 < cnf.get_nb_clauses()) {
            std::cout << " +";
        }
        for(int v : cnf[ci]) {
            vars.insert(std::abs(v));
        }
    }
    std::cout << ";\nX = ";
    for(auto const v : vars) {
        std::cout << "v" << v << " + ";
    }
    std::cout << "0;\n\n";

    for(std::size_t ci = 0; ci < cnf.get_nb_clauses(); ci++) {
        for(int v : cnf[ci]) {
            v = std::abs(v);
            std::cout << "c" << ci << " <= v" << v << ";\n";
            //std::cout << "v" << v << " = c" << ci << ";\n";
        }
    }
    std::cout << "\n";

    for(auto const v : vars) {
        std::cout << "v" << v << " <= ";

        for(std::size_t ci = 0; ci < cnf.get_nb_clauses(); ci++) {
            if(cnf[ci].find(v) != cnf[ci].end() || cnf[ci].find(-v) != cnf[ci].end()) {
                std::cout << "c" << ci << " + ";
            }
        }
        std::cout << "0;\n";
    }
    std::cout << "\n";

    for(std::size_t ci = 0; ci < cnf.get_nb_clauses(); ci++) {
        if(cnf[ci].size() >= k)
            std::cout << "c" << ci << " <= 1;\n";
        else
            std::cout << "c" << ci << " = 0;\n";
    }
    std::cout << "\n";

    for(int v : vars) {
        std::cout << "v" << v << " <= 1;\n";
    }
    std::cout << "\n";

    for(std::size_t ci = 0; ci < cnf.get_nb_clauses(); ci++) {
        std::cout << "int c" << ci << ";\n";
    }
    std::cout << "\n";

    for(int v : vars) {
        std::cout << "int v" << v << ";\n";
    }
    std::cout << "\n";
    return 0;
}

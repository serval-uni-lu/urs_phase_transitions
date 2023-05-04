//
// Created by oz on 1/12/22.
//

#include "CNF.hpp"

#include<fstream>
#include<iostream>
#include<sstream>
#include<algorithm>

Literal::Literal (Variable v) : l((v.get() << 1)) {
}

Literal::Literal (Variable v, int sign) : l((v.get() << 1) | (sign < 0 ? -1 : 1)) {
}

Literal::Literal (int i) : l(((std::abs(i) - 1) << 1) ^ (i < 0 ? 1 : 0)) {
}

bool Literal::operator == (Literal p) const {
    return l == p.get();
}

bool Literal::operator != (Literal p) const {
    return l != p.get();
}

// '<' makes p, ~p adjacent in the ordering.
bool Literal::operator <  (Literal p) const {
    return l < p.get();
}  

Variable::Variable(int i) : v(std::abs(i) - 1) {
}

Variable::Variable(Literal l) : v(l.get() >> 1) {
}

bool Variable::operator == (Variable p) const {
    return v == p.v;
}

bool Variable::operator != (Variable p) const {
    return v != p.v;
}

bool Variable::operator <  (Variable p) const {
    return v < p.v;
}

Clause::Clause() {
}

void Clause::push(Literal const& l) {
    for(auto const& i : c) {
        if(i == l)
            return;
    }
    c.push_back(l);
}

void Clause::remove(Literal const& l) {
    auto it = std::remove(c.begin(), c.end(), l);
    c.erase(it, c.end());
}

void Clause::remove(Variable const& v) {
    auto it = std::remove_if(c.begin(), c.end()
            , [v] (Literal const& li) {
                return Variable(li) == v;
            });
    c.erase(it, c.end());
}

bool Clause::contains(Literal const& l) const {
    return std::find(c.begin(), c.end(), l) != c.end();
}

bool Clause::contains(Clause const& cls) const {
    return std::all_of(cls.c.begin(), cls.c.end(), [this](auto const& l) {
        return contains(l);
    });
}

CNF::CNF(char const* path) {
    std::ifstream f(path);

    if(!f) {
        std::cerr << "error opening file " << path << "\n";
        return;
    }

    int nb_vars;
    std::string line;
    while(getline(f, line)) {
        if(line.rfind("p cnf ", 0) == 0) {
            std::stringstream iss(line);
            std::string tmp;
            iss >> tmp >> tmp;
            iss >> nb_vars;

            idx.reserve(2 * nb_vars);

            for(int i = 1; i <= nb_vars; i++) {
                auto tmp = Variable(i);
                vars.insert(tmp);

                idx.push_back({});
                idx.push_back({});
            }
        }
        else if(line.rfind("c ind ", 0) == 0) {
            std::stringstream iss(line);
            std::string tmp;

            iss >> tmp >> tmp;
            while(iss) {
                int v;
                iss >> v;
                if(v != 0) {
                    ind.insert(Variable(v));
                }
            }
        }
        else if(line[0] != 'c' && line[0] != 'p') {
            Clause clause;
            std::stringstream iss(line);

            while(iss) {
                int v;
                iss >> v;
                if(v != 0) {
                    auto tmp = Literal(v);
                    clause.push(tmp);

                    idx[tmp.get()].insert(clauses.size());
                }
            }

            clauses.push_back(clause);
            active.push_back(true);
        }
    }

    nb_active = active.size();
    //simplify();
    //compute_free_vars();
}

std::ostream & operator<<(std::ostream & out, CNF const& cnf) {
    out << "p cnf " << cnf.vars.size() << " " << (cnf.nb_active + cnf.units.size());
    for(std::size_t i = 0; i < cnf.clauses.size(); i++) {
        if(cnf.active[i]) {
            out << "\n" << cnf.clauses[i];
        }
    }

    for(Literal const& l : cnf.units) {
        out << "\n" << l << " 0";
    }

    for(Variable const& v : cnf.free) {
        out << "\nc " << v;
    }

    return out;
}

void CNF::simplify() {
    bool change = true;
    while(change) {
        change = false;
        std::set<Literal> u;

        for(std::size_t i = 0; i < clauses.size(); i++) {
            if(active[i] && clauses[i].size() == 1) {
                u.insert(clauses[i][0]);
                units.insert(clauses[i][0]);
                active[i] = false;
                nb_active -= 1;
            }
        }

        change = u.size() != 0;

        for(Literal const& l : u) {
            Literal nl = ~l;

            for(std::size_t i : idx[l.get()]) {
                if(active[i]) {
                    nb_active -= 1;
                }
                active[i] = false;

                for(Literal const& li : clauses[i]) {
                    if(li != l) {
                        idx[li.get()].erase(i);
                    }
                }
            }
            idx[l.get()].clear();

            for(std::size_t id : idx[(nl).get()]) {
                clauses[id].remove(nl);
            }
            idx[(nl).get()].clear();
        }
    }
}

void CNF::subsumption() {
    for(std::size_t i = 0; i < clauses.size(); i++) {
        if(active[i]) {
            for(auto const& j : clauses[i]) {
                auto ids = idx[j.get()];

                for(auto const& id : ids) {
                    if( active[id] && id != i && clauses[id].contains(clauses[i])) {
                        active[id] = false;
                        nb_active--;
                        for(auto const& l : clauses[id]) {
                            idx[l.get()].erase(id);
                        }
                    }
                }
            }
        }
    }
}

void CNF::compute_free_vars() {
    free = vars;

    for(std::size_t i = 0; i < clauses.size(); i++) {
        if(active[i]) {
            for(Literal const& l : clauses[i]) {
                free.erase(Variable(l));
            }
        }
    }

    for(Literal const& l : units) {
        free.erase(Variable(l));
    }
}

std::map<Variable, std::size_t> CNF::get_reduced_mapping() const {
    std::set<Variable> vars;
    for(std::size_t i = 0; i < clauses.size(); i++) {
        if(active[i]) {
            for(auto const& l : clauses[i]) {
                vars.insert(Variable(l));
            }
        }
    }

    std::map<Variable, std::size_t> res;

    std::size_t i = 0;
    for(auto const& v : vars) {
        res.emplace(v, i);
        i++;
    }

    return res;
}

std::vector<std::size_t> CNF::get_nb_by_clause_len() const {
    std::vector<std::size_t> res;
    res.push_back(0);
    res.push_back(units.size());

    for(std::size_t i = 0; i < clauses.size(); i++) {
        if(active[i]) {
            Clause const& c = clauses[i];

            while(c.size() >= res.size()) {
                res.push_back(0);
            }
            res[c.size()]++;
        }
    }

    return res;
}

std::vector<std::set<Variable> > CNF::get_vars_by_clause_len() const {
    std::vector<std::set<Variable> > res;
    res.reserve(vars.size());
    res.push_back({});
    res.push_back({});

    for(Literal const& l : units) {
        res[1].insert(Variable(l));
    }

    for(std::size_t i = 0; i < clauses.size(); i++) {
        if(active[i]) {
            Clause const& c = clauses[i];

            while(c.size() >= res.size()) {
                res.push_back({});
            }
            for(auto const& l : c) {
                res[c.size()].insert(Variable(l));
                res[0].insert(Variable(l));
            }
        }
    }

    return res;
}

/**
 * returns the clauses that have all their variables in the set v
 * clause length has to be >= m_len to be included
 */
std::vector<Clause> CNF::get_clauses_by_vars(std::set<Variable> const& v, std::size_t m_len) const {
    std::vector<Clause> res;

    for(std::size_t i = 0; i < clauses.size(); i++) {
        if(active[i] && clauses[i].size() >= m_len) {
            bool include = true;
            for(auto const& l : clauses[i]) {
                auto it = v.find(Variable(l));
                if(it == v.end()) {
                    include = false;
                    break;
                }
            }

            if(include) {
                res.push_back(clauses[i]);
            }
        }
    }

    return res;
}

/**
 * returns the clauses that have any of their variables in the set v
 * clause length has to be >= m_len to be included
 */
std::vector<Clause> CNF::get_clauses_by_vars_wide(std::set<Variable> const& v, std::size_t m_len) const {
    std::vector<Clause> res;

    for(std::size_t i = 0; i < clauses.size(); i++) {
        if(active[i] && clauses[i].size() >= m_len) {
            bool include = false;
            for(auto const& l : clauses[i]) {
                auto it = v.find(Variable(l));
                if(it != v.end()) {
                    include = true;
                    break;
                }
            }

            if(include) {
                res.push_back(clauses[i]);
            }
        }
    }

    return res;
}

//
// Created by oz on 1/12/22.
//

#ifndef BN_CNF_HPP
#define BN_CNF_HPP

#include<set>
#include<vector>
#include<map>
#include<ostream>

//using Literal = int;
struct Literal;
struct Variable;

struct Literal {
    private:
    int l;

    public:
    Literal (Variable v);
    Literal (Variable v, int sign);
    Literal (int i);

    Literal(Literal const& v) = default;
    Literal(Literal && v) = default;

    Literal& operator= (Literal const& p) = default;
    Literal& operator= (Literal && p) = default;

    inline int sign() const { return l & 1 ? -1 : 1; }
    inline int to_int() const { return sign() * ((l >> 1) + 1); }
    inline int get() const { return l; }

    bool operator == (Literal p) const;
    bool operator != (Literal p) const;
    bool operator <  (Literal p) const; // '<' makes p, ~p adjacent in the ordering.  

    friend inline Literal operator ~ (Literal p);
};

inline Literal operator ~ (Literal p) {
    p.l ^= 1;
    return p;
}

inline std::ostream & operator<<(std::ostream & out, Literal const& l) {
    out << l.to_int();
    //out << l.get();
    return out;
}

struct Variable {
    private:
    int v;

    public:
    Variable(int i);
    Variable(Literal l);

    Variable(Variable const& v) = default;
    Variable(Variable && v) = default;

    Variable& operator= (Variable const& p) = default;
    Variable& operator= (Variable && p) = default;

    inline int to_int() const { return v + 1; }
    inline int get() const { return v; }

    bool operator == (Variable p) const;
    bool operator != (Variable p) const;
    bool operator <  (Variable p) const;
};

inline std::ostream & operator<<(std::ostream & out, Variable const& v) {
    out << v.to_int();
    return out;
}

struct Clause {
    private:
    std::vector<Literal> c;

    public:
    Clause();
    Clause(Clause const& c) = default;
    Clause(Clause && c) = default;

    Clause& operator=(Clause const& c) = default;
    Clause& operator=(Clause && c) = default;

    void push(Literal const& l);
    void remove(Literal const& l);
    void remove(Variable const& v);
    bool contains(Literal const& l) const;
    bool contains(Clause const& cls) const;

    inline auto begin() const {
        return c.begin();
    }

    inline auto end() const {
        return c.end();
    }

    inline std::size_t size() const {
        return c.size();
    }

    inline auto operator[](std::size_t const& i) {
        return c[i];
    }

    inline auto const& operator[](std::size_t const& i) const {
        return c[i];
    }
};

inline std::ostream & operator<<(std::ostream & out, Clause const& c) {
    for(auto const& l : c) {
        out << l << " ";
    }
    out << "0";
    return out;
}

class CNF {
    private:
        std::vector<Clause> clauses;
        std::vector<bool> active;
        std::vector<std::set<std::size_t> > idx;
        std::set<Literal> units;
        std::set<Variable> free;
        std::set<Variable> vars;
        std::set<Variable> ind;

        std::size_t nb_active = 0;

    public:
        CNF() = default;
        CNF(char const* path);
        CNF(CNF const& c) = default;
        CNF(CNF && c) = default;

        CNF& operator=(CNF const& c) = default;
        CNF& operator=(CNF && c) = default;

        void compute_free_vars();
        void simplify();
        void subsumption();

        std::map<Variable, std::size_t> get_reduced_mapping() const;

        std::vector<std::size_t> get_nb_by_clause_len() const;
        std::vector<std::set<Variable> > get_vars_by_clause_len() const;

        inline bool is_active(std::size_t i) const { return active[i]; }
        inline Clause const& clause(std::size_t i) const { return clauses[i]; }

        inline std::size_t nb_vars() const { return vars.size(); }
        inline std::size_t nb_free_vars() const { return free.size(); }
        inline std::size_t nb_units() const { return units.size(); }
        inline std::size_t nb_c_vars() const { return nb_vars() - nb_free_vars(); }
        inline std::size_t nb_clauses() const { return clauses.size(); }
        inline std::size_t nb_active_clauses() const { return nb_active; }

        std::vector<Clause> get_clauses_by_vars(std::set<Variable> const& v, std::size_t m_len) const;
        std::vector<Clause> get_clauses_by_vars_wide(std::set<Variable> const& v, std::size_t m_len) const;

    friend std::ostream & operator<<(std::ostream & out, CNF const& cnf);
};

std::ostream & operator<<(std::ostream & out, CNF const& cnf);

#endif //BN_CNF_HPP

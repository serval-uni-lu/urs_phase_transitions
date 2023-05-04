#ifndef GRAPH_H
#define GRAPH_H

#include<vector>
#include<map>

struct Graph {
    std::vector<std::map<int, double> > g;

    Graph(std::size_t nb_nodes);

    int size() const;

    void add_edge(int i1, int i2, double w);
    void remove_edge(int i1, int i2);

    double get_edge(int i1, int i2) const;
    bool has_edge(int i1, int i2) const;

    double deg(int i) const;
    double deg_sum() const;
    int arity(int i) const;

    std::vector<int> neighbors(int i) const;
};

#endif

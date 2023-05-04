#include "graph.hpp"
#include<iostream>

Graph::Graph(std::size_t nb_nodes) : g(nb_nodes) {
}

int Graph::size() const {
    return g.size();
}

void Graph::add_edge(int i1, int i2, double w) {
    g[i1][i2] = w;
    g[i2][i1] = w;
}

void Graph::remove_edge(int i1, int i2) {
    g[i1].erase(i2);
    g[i2].erase(i1);
}

double Graph::get_edge(int i1, int i2) const {
    auto it = g[i1].find(i2);

    if(it != g[i1].end()) {
        return it->second;
    }
    return 0;
}

bool Graph::has_edge(int i1, int i2) const {
    auto it = g[i1].find(i2);

    if(it != g[i1].end() && it->second != 0) {
        return true;
    }
    return false;
}

double Graph::deg(int i) const {
    double r = 0;
    for(auto const& t : g[i]) {
        r += t.second;
    }
    return r;
}

int Graph::arity(int i) const {
    return g[i].size();
}

std::vector<int> Graph::neighbors(int i) const {
    std::vector<int> r;
    r.reserve(g[i].size());

    for(auto const& j : g[i]) {
        r.push_back(j.first);
    }

    return r;
}

double Graph::deg_sum() const {
    double r = 0;

    for(int i = 0; i < size(); i++) {
        r += deg(i);
    }

    return r;
}

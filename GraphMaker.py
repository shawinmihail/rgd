# -*- coding: utf-8 -*-
import math
import networkx as nx


def create_simple_graph():

    g = nx.DiGraph()
    for i in range(11):
        g.add_node(i+1)

    loads_list = list()
    loads1 = [[1, 11, 0.45]]
    loads2 = [[3, 11, 0.45]]
    loads3 = [[7, 11, 0.25]]
    loads4 = [[2, 12, 0.33]]
    loads_list.append(loads1)
    loads_list.append(loads2)
    loads_list.append(loads3)
    loads_list.append(loads4)

    g.node[1]["loads"] = loads1
    g.node[3]["loads"] = loads2
    g.node[7]["loads"] = loads3
    g.node[2]["loads"] = loads4

    g.add_edge(1, 4, d=1, cap=1, cur=0)
    g.add_edge(4, 8, d=1, cap=1, cur=0)
    g.add_edge(8, 11, d=1,cap=1, cur=0)
    g.add_edge(4, 1, d=1, cap=1, cur=0)
    g.add_edge(8, 4, d=1, cap=1, cur=0)
    g.add_edge(11, 8, d=1,cap=1, cur=0)
    g.add_edge(2, 5, d=1, cap=1, cur=0)
    g.add_edge(5, 9, d=1, cap=1, cur=0)
    g.add_edge(9, 12, d=1,cap=1, cur=0)
    g.add_edge(5, 2, d=1, cap=1, cur=0)
    g.add_edge(9, 5, d=1, cap=1, cur=0)
    g.add_edge(12, 9, d=1,cap=1, cur=0)
    g.add_edge(3, 4, d=1, cap=1, cur=0)
    g.add_edge(4, 5, d=1, cap=1, cur=0)
    g.add_edge(5, 6, d=1, cap=1, cur=0)
    g.add_edge(4, 3, d=1, cap=1, cur=0)
    g.add_edge(5, 4, d=1, cap=1, cur=0)
    g.add_edge(6, 5, d=1, cap=1, cur=0)
    g.add_edge(7, 8, d=1, cap=1, cur=0)
    g.add_edge(8, 9, d=1, cap=1, cur=0)
    g.add_edge(9, 10, d=1,cap=1, cur=0)
    g.add_edge(8, 7, d=1, cap=1, cur=0)
    g.add_edge(9, 8, d=1, cap=1, cur=0)
    g.add_edge(10, 9, d=1,cap=1, cur=0)

    g.add_edge(12, 11, d=1,cap=1, cur=0)

    holls = [3, 11]
    pos = dict()
    x = 0
    for n in g.nodes():
        if n in holls:
            x += 1
        pos[n] = ((n + x) % 4, int ((n + x) / 4))

    return g, loads_list, pos


def create_grid():

    n = 6
    g = nx.DiGraph()
    for i in range(n*n):
        g.add_node(i)

    for i in g.nodes():
        edges = list()
        top = i + n
        bot = i - n
        right = i + 1
        left = i - 1
        if(top < n*n - 1):
            edges.append(top)
        if(bot > 0):
            edges.append(bot)
        if(left > 0 and int(i / n) == int(left / n)):
            edges.append(left)
        if(right < n*n - 1 and int(i / n) == int(right / n)):
            edges.append(right)

        cap = 1
        for e in edges:
            g.add_edge(i, e, d=1, cap=cap, cur=0)

    g.remove_edge(12, 18)
    g.remove_edge(18, 12)
    g.remove_edge(13, 19)
    g.remove_edge(19, 13)
    g.remove_edge(25, 26)
    g.remove_edge(26, 25)
    g.remove_edge(27, 28)
    g.remove_edge(28, 27)
    g.remove_edge(28, 22)
    g.remove_edge(22, 28)
    g.remove_edge(14, 15)
    g.remove_edge(15, 14)



    pos = dict()
    for i in g.nodes():
        pos[i] = (i % n, int(i / n))

    loads_list = list()
    loads1 = [[1, 11, 0.45]]
    loads2 = [[3, 11, 0.45]]
    loads3 = [[7, 23, 0.25]]
    loads4 = [[2, 14, 0.33]]
    loads5 = [[22, 25, 0.41]]
    loads6 = [[21, 28, 0.33]]
    loads7 = [[6, 9, 0.51]]
    loads8 = [[14, 25, 0.33]]
    loads9 = [[13, 19, 0.33]]
    loads10 = [[20, 31, 0.33]]

    loads_list.append(loads1)
    loads_list.append(loads2)
    loads_list.append(loads3)
    loads_list.append(loads4)
    loads_list.append(loads5)
    loads_list.append(loads6)
    loads_list.append(loads7)
    loads_list.append(loads8)
    loads_list.append(loads9)
    loads_list.append(loads10)

    for loads in loads_list:
        g.node[loads[0][0]]["loads"] = loads

    return g, loads_list, pos
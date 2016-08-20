# -*- coding: utf-8 -*-
import networkx as nx
import GraphMaker
import matplotlib.pyplot as plt

graph, loads_list = GraphMaker.create_simple_graph()
loads_and_paths = list()

for loads in loads_list:
    for load in loads:
        path = nx.shortest_path(graph, load[0], load[1],  "d")
        way_path = list()
        for way in zip(path, path[1:]):
            graph.edge[way[0]][way[1]]["cur"] += load[2]
            way_path.append(way)
        loads_and_paths.append([load, way_path])

bad_ways = list()
for way in graph.edges():
    cur = graph.edge[way[0]][way[1]]["cur"]
    cap = graph.edge[way[0]][way[1]]["cap"]
    if cur >= cap:
        bad_ways.append(way)

for loads_and_path in loads_and_paths:
    load = loads_and_path[0]
    path = loads_and_path[1]
    is_bad = False
    for way in bad_ways:
        if way in path:
            is_bad = True

    if is_bad:
        pass
    else:
        print(load)
        cur = load[2]
        for way in path:
            graph.edge[way[0]][way[1]]["cur"] -= cur
            graph.edge[way[0]][way[1]]["cap"] -= cur

for way in bad_ways:
    graph.remove_edge(way[0], way[1])



nx.draw(graph)
plt.show()


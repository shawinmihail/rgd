# -*- coding: utf-8 -*-
import networkx as nx
import GraphMaker
import matplotlib.pyplot as plt

def iterate(graph):
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

    good_loads_and_paths = list()
    stop_ways_dict = dict()
    for load_and_path in loads_and_paths:
        load = load_and_path[0]
        path = load_and_path[1]
        stop_way = None

        for way in bad_ways:
            if way in path:
                stop_way = way
                break

        if stop_way is not None:
            if stop_way in stop_ways_dict.keys():
                stop_ways_dict[stop_way].append(load_and_path)
            else:
                stop_ways_dict[stop_way] = [load_and_path]
        else:
            cur = load[2]
            for way in path:
                graph.edge[way[0]][way[1]]["cur"] -= cur
                graph.edge[way[0]][way[1]]["cap"] -= cur
            graph.node[load[0]]["loads"].remove(load)
            good_loads_and_paths.append(load_and_path)

        for way, loads_and_paths in stop_ways_dict.items():
            loads_and_paths_sorted = sorted(loads_and_paths, key=lambda x: x[0][3])
            cap = graph.edge[way[0]][way[1]]["cap"]
            good_loads_and_paths.append(load_and_path)
            for load_and_path in loads_and_paths_sorted:




graph, loads_list = GraphMaker.create_simple_graph()
iterate(graph)

# nx.draw(graph)
# plt.show()


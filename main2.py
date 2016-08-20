# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import networkx as nx
import GraphMaker
import matplotlib.pyplot as plt

BAD = "bad"
GOOD = "good"
NEXT = "next"

def iterate(graph, result):
    loads_and_paths = list()
    for loads in loads_list:
        for load in loads:
            try:
                path = nx.shortest_path(graph, load[0], load[1],  "d")
            except:
                return BAD
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

    ways_and_bad_loads_and_paths = list()
    good_loads_and_paths = list()
    for load_and_path in loads_and_paths:
        load = load_and_path[0]
        path = load_and_path[1]
        is_good = True
        for way in path:
            cur = graph.edge[way[0]][way[1]]["cur"]
            cap = graph.edge[way[0]][way[1]]["cap"]
            if cur > cap:
                ways_and_bad_loads_and_paths.append([way, load_and_path])
                for way in path:
                    graph.edge[way[0]][way[1]]["cur"] -= cur
                is_good = False
                break

        if is_good:
            good_loads_and_paths.append(load_and_path)

    for load_and_path in good_loads_and_paths:
        path = load_and_path[1]
        load = load_and_path[0]
        cur = load[2]
        for way in path:
            graph.edge[way[0]][way[1]]["cur"] -= cur
            graph.edge[way[0]][way[1]]["cap"] -= cur
        graph.node[load[0]]["loads"].remove(load)

    for way_and_bad_load_and_path in ways_and_bad_loads_and_paths:
        way = way_and_bad_load_and_path[0]
        graph.remove_edge(way[0], way[1])

    result.append(good_loads_and_paths)
    if len(ways_and_bad_loads_and_paths) == 0:
        return GOOD
    else:
        return NEXT

graph, loads_list = GraphMaker.create_simple_graph()
result = list()
while True:
    res = iterate(graph, result)
    if res == GOOD:
        print(result)
        break
    if res == BAD:
        print("cant resolve")
        break

# nx.draw(graph)
# plt.show()


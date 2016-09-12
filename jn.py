# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt

BAD = "bad"
GOOD = "good"
NEXT = "next"

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

    return g, loads_list

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

graph, loads_list = create_simple_graph()
result = list()
while True:
    res = iterate(graph, result)
    if res == GOOD:
        print(result)
        break
    if res == BAD:
        print("cant resolve")
        break

nx.draw_networkx_labels(graph)
plt.show()


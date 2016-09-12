# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import networkx as nx
import GraphMaker
import matplotlib.pyplot as plt
from copy import copy

BAD = "bad"
GOOD = "good"
NEXT = "next"

graph, loads_list, pos = GraphMaker.create_simple_graph()

def find_problems():
    loads_and_paths = list()
    for loads in loads_list:
        for load in loads:
            try:
                path = nx.shortest_path(graph, load[0], load[1],  "d")
            except:
                return BAD, dict(), list()
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

    bad_ways_and_paths = dict()
    for bad_way in bad_ways:
        bad_ways_and_paths[bad_way] = list()
        for load_and_path in loads_and_paths:
            load = load_and_path[0]
            path = load_and_path[1]
            for way in path:
                if way == bad_way:
                    bad_ways_and_paths[bad_way] += path
                    is_good = False

    good_ways = list()

    for load_and_path in loads_and_paths:
        is_good = True
        load = load_and_path[0]
        path = load_and_path[1]
        for way in path:
            if way in bad_ways:
                is_good = False
        if is_good:
            good_ways += path

    return GOOD, bad_ways_and_paths, good_ways


def show_problems(bad_ways_and_paths, good_ways, shown):

    union_paths = list()
    for paths in bad_ways_and_paths.values():
        union_paths += paths
    union_paths = union_paths + good_ways + shown

    colors = list()
    labels_dict = dict()

    for way in graph.edges():
        if way in bad_ways_and_paths.keys():
            colors.append("red")
        elif way in union_paths:
            colors.append("green")
        else:
            colors.append("blue")

        if way in union_paths:
            cur = graph.edge[way[0]][way[1]]["cur"]
            cap = graph.edge[way[0]][way[1]]["cap"]
            labels_dict[way] = "%.2f / %.2f" % (cur, cap)

    nx.draw_networkx_nodes(graph, pos, node_size=225, node_color="blue", with_labels=True)
    nx.draw_networkx_labels(graph, pos, font_color="white")
    nx.draw_networkx_edges(graph, pos, width=2, alpha=0.5, edge_color=colors)
    nx.draw_networkx_edge_labels(graph, pos, labels_dict)
    plt.show()

    return union_paths


def try_solve_problems(result):
    loads_and_paths = list()
    for loads in loads_list:
        for load in loads:
            try:
                path = nx.shortest_path(load[0], load[1],  "d")
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
                is_good = False
                break
        if is_good:
            good_loads_and_paths.append(load_and_path)

    new_graph = copy(graph)
    for way_and_bad_load_and_path in ways_and_bad_loads_and_paths:
        way = way_and_bad_load_and_path[0]
        new_graph.remove_edge(way[0], way[1])
        new_path = nx.shortest_path(load[0], load[1], "d")



    result.append(good_loads_and_paths)
    if len(ways_and_bad_loads_and_paths) == 0:
        return GOOD
    else:
        return NEXT


def iterate(result):
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

result = list()

res, bws_ps, good_ways = find_problems()
shown = show_problems(bws_ps, good_ways, list())
iterate(result)

res, bws_ps, good_ways = find_problems()
shown = show_problems(bws_ps, good_ways, shown)
iterate(result)


# try_solve_problems(result)
# res, bws_ps = find_problems()
# show_problems(bws_ps)


# k = 0
# while True:
#     print(k)
#     k += 1
#
#     r1, ws_ps = find_problems(graph)
#     print(ws_ps)
#     show_problems(graph, ws_ps)
#     res = try_solve_problems(graph, result)
#     if res == GOOD:
#         print("solved")
#         break
#     if res == BAD:
#         print("can't resolve")
#         break

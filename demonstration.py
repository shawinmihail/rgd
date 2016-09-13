# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import networkx as nx
import GraphMaker
import matplotlib.pyplot as plt
from copy import copy

BAD = "bad"
GOOD = "good"
NEXT = "next"
COUNTER = 0

# graph, loads_list, pos = GraphMaker.create_simple_graph()
graph, loads_list, pos = GraphMaker.create_grid()

def generate_path_msg(paths):
    text = ""
    for path in paths:
        if len(path) == 0:
            continue
        for way in path:
            text += "%s;" % way[0]
        text += "%s\n" % (path[-1][1])
    return text

def show_problems(paths, bad_ways):
    global COUNTER
    colors = list()
    labels_dict = dict()

    all_path_ways = list()
    for p in paths:
        all_path_ways += p

    for way in graph.edges():
        cur = graph.edge[way[0]][way[1]]["cur"]
        cap = graph.edge[way[0]][way[1]]["cap"]
        if cur < 0.01:
            colors.append("blue")
        elif way in bad_ways:
            colors.append("red")
        elif way in all_path_ways:
            colors.append("green")
        else:
            colors.append("blue")

        if way in all_path_ways:
            cur = graph.edge[way[0]][way[1]]["cur"]
            cap = graph.edge[way[0]][way[1]]["cap"]
            labels_dict[way] = "%.2f / %.2f" % (cur, cap)

    nx.draw_networkx_nodes(graph, pos, node_size=225, node_color="blue", with_labels=True)
    nx.draw_networkx_labels(graph, pos, font_color="white")
    nx.draw_networkx_edges(graph, pos, width=2, alpha=0.5, edge_color=colors)
    nx.draw_networkx_edge_labels(graph, pos, labels_dict)
    plt.annotate(generate_path_msg(paths), xy=(5.1, 4))
    plt.show()
    # plt.savefig("%s.png" % COUNTER)
    # COUNTER += 1

def calculate_init():
    loads_and_paths = list()
    for loads in loads_list:
        for load in loads:
            try:
                path = nx.shortest_path(graph, load[0], load[1],  "d")
            except:
                return BAD, list(), list()

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

    paths = [x[1] for x in loads_and_paths]
    return loads_and_paths, paths, bad_ways

def iterate(result, loads_and_paths, bad_ways):
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
                for way in path:
                    graph.edge[way[0]][way[1]]["cur"] -= load[2]
                ways_and_bad_loads_and_paths.append([way, load_and_path])
                is_good = False
                break
        if is_good:
            good_loads_and_paths.append(load_and_path)

    for load_and_path in good_loads_and_paths:
        path = load_and_path[1]
        load = load_and_path[0]
        cur = load[2]
        # print(load_and_path)
        # print(graph.node[load[0]]["loads"])
        for way in path:
            graph.edge[way[0]][way[1]]["cur"] -= cur
            graph.edge[way[0]][way[1]]["cap"] -= cur
        index = graph.node[load[0]]["loads"].index(load)
        graph.node[load[0]]["loads"][index][2] = 0

    for way_and_bad_load_and_path in ways_and_bad_loads_and_paths:
        way = way_and_bad_load_and_path[0]
        try:
            graph.remove_edge(way[0], way[1])
        except:
            pass


    result.append(good_loads_and_paths)
    if len(ways_and_bad_loads_and_paths) == 0:
        return GOOD, bad_ways
    else:
        return NEXT, bad_ways

def csv_text(paths):
    text = ""
    for path in paths:
        if len(path) == 0:
            continue
        for way in path:
            text += "%s;" % way[0]
        text += "%s\n" % (path[-1][1])
    return text

def save_paths_csv(paths_list):
    c = 1
    text = ""
    for paths in paths_list:
        text += "it%s\n%s\n" % (c, csv_text(paths))
        c += 1
    file = open("res.csv", "w")
    file.write(text)
    file.close()


result = list()

path_list = list()
loads_and_paths, paths, bad_ways = calculate_init()
show_problems(paths, bad_ways)
path_list.append(paths)

while True:
    res, bad_ways = iterate(result, loads_and_paths, bad_ways)
    loads_and_paths, paths, bad_ways = calculate_init()
    show_problems(paths, bad_ways)
    path_list.append(paths)
    if res == GOOD:
        print("solved")
        break
    if res == BAD:
        print("can't resolve")
        break

save_paths_csv(path_list)

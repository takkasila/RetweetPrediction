import json
import datetime, time
from datetime import timedelta as dt
import collections
import networkx as nx
import matplotlib.pyplot as plt

def jsonToGraph(jsonFileName):
    data = json.load(open(jsonFileName))
    G = nx.DiGraph()
    for node_id in data:
        for target_node_id in data[node_id]['edge']:
            G.add_edge(int(node_id), int(target_node_id), {'count': data[node_id]['edge'][target_node_id]['count'], 'time_stamp': data[node_id]['edge'][target_node_id]['time_stamp']})
    return G

def cleanGraph(graph):
    for node in graph:
        for edge in graph[node].keys():
            if graph[node][edge]['count'] == 0:
                graph.remove_edge(node, edge)
    for node in graph.nodes():
        if graph.degree(node) == 0:
            graph.remove_node(node)
    for node in graph.nodes():
        for edge in graph[node]:
            counter = 0
            for time_stamp_key in graph[node][edge]['time_stamp'].keys():
                graph[node][edge]['time_stamp'][counter] = graph[node][edge]['time_stamp'].pop(time_stamp_key)
                counter += 1
    return graph

def splitTrainGraph(graph, epoch_split):
    trainGraph = graph.copy()
    for node in trainGraph:
        for edge in trainGraph[node].keys():
            for time_stamp_key in trainGraph[node][edge]['time_stamp'].keys():
                if trainGraph[node][edge]['time_stamp'][time_stamp_key] > epoch_split:
                    trainGraph[node][edge]['time_stamp'].pop(time_stamp_key)
                    trainGraph[node][edge]['count'] -= 1
    trainGraph = cleanGraph(trainGraph)
    return trainGraph

def graphToDict(graph):
    gDict = {}
    for node in graph:
        gDict[node] = {}
        gDict[node]['uid'] = node
        gDict[node]['edge'] = {}
        for edge in graph[node]:
            gDict[node]['edge'][edge] = {}
            gDict[node]['edge'][edge]['uid'] = edge
            gDict[node]['edge'][edge]['count'] = graph[node][edge]['count']
            gDict[node]['edge'][edge]['time_stamp'] = {}
            for time_stamp_key in graph[node][edge]['time_stamp']:
                gDict[node]['edge'][edge]['time_stamp'][time_stamp_key] = graph[node][edge]['time_stamp'][time_stamp_key]
    return gDict

visited_node = []
if __name__ == '__main__':
    graph =  jsonToGraph('test_data.json')
    epoch_split = int((datetime.datetime(2017,4,22) -  datetime.datetime(1970,1,1)).total_seconds())
    trainGraph = splitTrainGraph(graph, epoch_split)
    print "Test data nodes: ", graph.number_of_nodes()
    print "Test data edges: ", graph.number_of_edges()
    print "Train data nodes: ", trainGraph.number_of_edges()
    print "Train data edges: ", trainGraph.number_of_edges()
    with open("train_data.json", "w") as fp:
		json.dump(graphToDict(trainGraph), fp)

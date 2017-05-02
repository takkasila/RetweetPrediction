import json
import datetime, time
from datetime import timedelta as dt
import collections
import networkx as nx
import matplotlib.pyplot as plt
import sys

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
    leftGraph = graph.copy()
    for node in leftGraph:
        for edge in leftGraph[node].keys():
            for time_stamp_key in leftGraph[node][edge]['time_stamp'].keys():
                if leftGraph[node][edge]['time_stamp'][time_stamp_key] > epoch_split:
                    leftGraph[node][edge]['time_stamp'].pop(time_stamp_key)
                    leftGraph[node][edge]['count'] -= 1
    leftGraph = cleanGraph(leftGraph)

    rightGraph = graph.copy()
    for node in rightGraph:
        for edge in rightGraph[node].keys():
            for time_stamp_key in rightGraph[node][edge]['time_stamp'].keys():
                if rightGraph[node][edge]['time_stamp'][time_stamp_key] <= epoch_split:
                    rightGraph[node][edge]['time_stamp'].pop(time_stamp_key)
                    rightGraph[node][edge]['count'] -= 1
    rightGraph = cleanGraph(rightGraph)
    return leftGraph, rightGraph

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
    sys.stdout.write("Input filename: ")
    inputFileName = raw_input()
    sys.stdout.write("Day: ")
    day = int(raw_input())
    sys.stdout.write("Month: ")
    month = int(raw_input())
    sys.stdout.write("Year: ")
    year = int(raw_input())
    sys.stdout.write("Left output filename: ")
    outputLeftGraphFilename = raw_input()
    sys.stdout.write("Right output filename: ")
    outputRightGraphFilename = raw_input()

    graph =  jsonToGraph(inputFileName)
    epoch_split = int((datetime.datetime(year,month,day) -  datetime.datetime(1970,1,1)).total_seconds())
    leftGraph, rightGraph = splitTrainGraph(graph, epoch_split)
    print "Test data nodes: ", graph.number_of_nodes()
    print "Test data edges: ", graph.number_of_edges()
    print "Left data nodes: ", leftGraph.number_of_nodes()
    print "Left data edges: ", leftGraph.number_of_edges()
    print "Right data nodes: ", rightGraph.number_of_nodes()
    print "Right data edges: ", rightGraph.number_of_edges()

    with open(outputLeftGraphFilename, "w") as fp:
		json.dump(graphToDict(leftGraph), fp)
    with open(outputRightGraphFilename, "w") as fp:
		json.dump(graphToDict(rightGraph), fp)

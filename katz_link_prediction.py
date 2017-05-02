import json
import datetime, time
from datetime import timedelta as dt
import collections
import networkx as nx
from create_train_data import *

beta = 0.8

def weightedKatzScore(graph):
    maxScore = 0
    scoreGraph = graph.copy()
    nodeCount = 0
    for sourceNode in graph.nodes():
        print '-------------------------'
        print ("{}/5524".format(nodeCount))
        print "Node: ", sourceNode
        for targetNode in graph.nodes():
            if sourceNode == targetNode:
                continue
            # print nodeCount, "/5524 ", "Souce: ", sourceNode, " Target: ", targetNode
            # Count number of simple path length-l from source to target
            # Also creating all possible edges
            if targetNode not in scoreGraph[sourceNode]:
                scoreGraph[sourceNode][targetNode] = {}
                scoreGraph[sourceNode][targetNode]['count'] = 0
                scoreGraph[sourceNode][targetNode]['time_stamp'] = {}
            scoreGraph[sourceNode][targetNode]['length'] = {}
            possiblePath = 0
            for path in nx.all_simple_paths(graph, sourceNode, targetNode):
                if (len(path)-1) not in scoreGraph[sourceNode][targetNode]['length']:
                    scoreGraph[sourceNode][targetNode]['length'][(len(path)-1)] = 1
                else:
                    scoreGraph[sourceNode][targetNode]['length'][(len(path)-1)] += 1
                possiblePath += 1
                print "Path count: ", possiblePath
            # Calculate score
            scoreGraph[sourceNode][targetNode]['score'] = 0.0
            for length in scoreGraph[sourceNode][targetNode]['length']:
                scoreGraph[sourceNode][targetNode]['score'] += pow(beta, length) * scoreGraph[sourceNode][targetNode]['length'][length]
                if maxScore < scoreGraph[sourceNode][targetNode]['score']:
                    maxScore = scoreGraph[sourceNode][targetNode]['score']
        nodeCount += 1
    # Normalize score
    for sourceNode in scoreGraph.nodes():
        for targetNode in scoreGraph.nodes():
            if sourceNode == targetNode:
                continue
            scoreGraph[sourceNode][targetNode]['score'] /= maxScore
    return scoreGraph
                
def scoreGraphToDict(graph):
    gDict = {}
    nodeCount = 0
    for node in graph:
        nodeCount += 1
        gDict[node] = {}
        gDict[node]['uid'] = node
        gDict[node]['edge'] = {}
        edgeCount = 0
        for edge in graph[node]:
            edgeCount += 1
            gDict[node]['edge'][edge] = {}
            gDict[node]['edge'][edge]['uid'] = edge
            gDict[node]['edge'][edge]['count'] = graph[node][edge]['count']
            gDict[node]['edge'][edge]['time_stamp'] = {}
            for time_stamp_key in graph[node][edge]['time_stamp']:
                gDict[node]['edge'][edge]['time_stamp'][time_stamp_key] = graph[node][edge]['time_stamp'][time_stamp_key]
            gDict[node]['edge'][edge]['score'] = graph[node][edge]['score']
    return gDict

if __name__ == '__main__':
    graph = jsonToGraph('train_data.json')
    scoreGraph = weightedKatzScore(graph)
    with open("predicted_data.json", "w") as fp:
		json.dump(scoreGraphToDict(scoreGraph), fp)
    

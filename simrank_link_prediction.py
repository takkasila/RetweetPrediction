import json
import datetime, time
from datetime import timedelta as dt
import collections
import networkx as nx
from split_data import *
import numpy
import itertools
from katz_link_prediction import scoreGraphToDict
def simrank(G, r=0.8, max_iter=100, eps=1e-4):

    nodes = G.nodes()
    # print len(nodes)
    nodes_i = {k: v for(k, v) in [(nodes[i], i) for i in range(0, len(nodes))]}

    sim_prev = numpy.zeros(len(nodes))
    sim = numpy.identity(len(nodes))

    for i in range(max_iter):
        # print i
        if numpy.allclose(sim, sim_prev, atol=eps):
            break
        sim_prev = numpy.copy(sim)
        tmp = itertools.product(nodes, nodes)
        for u, v in tmp:
            # print (u, v)
            if u is v:
                continue
            u_ns, v_ns = G.predecessors(u), G.predecessors(v)

            # evaluating the similarity of current iteration nodes pair
            if len(u_ns) == 0 or len(v_ns) == 0: 
                # if a node has no predecessors then setting similarity to zero
                sim[nodes_i[u]][nodes_i[v]] = 0
            else:                    
                s_uv = sum([sim_prev[nodes_i[u_n]][nodes_i[v_n]] for u_n, v_n in itertools.product(u_ns, v_ns)])
                sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / (len(u_ns) * len(v_ns))


    return sim

def addScoreMatToGraph(graph, scoreMat):
    nodeList = graph.nodes()
    scoreGraph = graph.copy()
    for sourceNode in graph.nodes():
        for targetNode in graph.nodes():
            if sourceNode == targetNode:
                continue
            score = scoreMat[ nodeList.index(sourceNode) ][ nodeList.index(targetNode) ]
            # Newly inserted
            if targetNode not in scoreGraph[sourceNode]:
                scoreGraph[sourceNode][targetNode] = {}
                scoreGraph[sourceNode][targetNode]['count'] = 0
                scoreGraph[sourceNode][targetNode]['time_stamp'] = {}

            scoreGraph[sourceNode][targetNode]['score'] = score
    return scoreGraph

if __name__ == '__main__':
    graph = jsonToGraph('./Dataset2/from-2017-4-8-to-2017-4-16.json')
    scoreMat = simrank(graph)
    graph = addScoreMatToGraph(graph, scoreMat)
    with open("from-2017-4-8-to-2017-4-16_sim.json", "w") as fp:
        json.dump(scoreGraphToDict(graph), fp)
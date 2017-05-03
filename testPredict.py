import json
import operator
import networkx as nx
import sys

def returnNotInObj(g1,g2):
	notInList = []
	for node in g1["edge"]:
		if(not node in g2["edge"]):
			notInList.append(node)
	return notInList

def checkSimilarity(g1,g2):
	sameEdge = 0
	totalG1Edge = 0
	totalG2Edge = 0
	for node in g1:
		sameEdge += len(g1[node]["edge"])-len(returnNotInObj(g1[node],g2[node]))
		totalG1Edge += len(g1[node]["edge"])
		totalG2Edge += len(g2[node]["edge"])
	precision = 0
	recall = 0
	if(totalG2Edge != 0):
		precision = 1.0*(sameEdge)/totalG1Edge
		recall = 1.0*(sameEdge)/totalG2Edge
	return {"precision":precision,"recall":recall}

def checkPerformance(old,predict,new,coreList):
	newAdd = {}
	totalEdge = 0
	for oldNode in coreList:
		for newEdge in new[oldNode]['edge']:
			if(not(newEdge in old[oldNode]['edge'])):
				if(not(oldNode in newAdd)):
					newAdd[oldNode] = {}
				newAdd[oldNode][newEdge] = new[oldNode]['edge'][newEdge]
				totalEdge += 1
#			elif(new[oldNode]['edge'][newEdge]['count'] > old[oldNode]['edge'][newEdge]['count']):
#				if(not(oldNode in newAdd)):
#					newAdd[oldNode] = {}
#				newAdd[oldNode][newEdge] = new[oldNode]['edge'][newEdge]
#				totalEdge += new[oldNode]['edge'][newEdge]['count']-old[oldNode]['edge'][newEdge]['count']
	correctPredict = 0
	totalPredict = 0
#	print "totalEdge:",totalEdge
	for score in reversed(predict["sortKey"]):
		print score
		for predictEdge in predict["sortPredict"][score]:
#			print predictNode
			totalPredict += 1
#			print newAdd[predictNode["from"]]
			if(predictEdge["from"] in newAdd):
#				print predictEdge
#				print newAdd[predictEdge["from"]]
				if(str(predictEdge["edge"]["uid"]) in newAdd[predictEdge["from"]]):
					correctPredict += 1
#				sys.exit()
			if(True and totalPredict == totalEdge):
				break
		if(True and totalPredict == totalEdge):
			break
	print "correctPredict:",correctPredict
	print "totalPredict:",totalPredict
	print "totalEdge:",totalEdge
	return 1.0*correctPredict/totalPredict
#	return checkSimilarity(predictOnly, newOnly)

def jsonLoader(fileName):
	nodeObjs = {}
	dataFile = open(fileName)
	data = json.load(dataFile)
	nodeWithEdge = 0
	totalEdge = 0
	for node_id in data:
		totalEdge += len(data[node_id]['edge'])
		nodeWithEdge += 1
#		nodeObjs[node_id] = {"uid":node_id,"edge":[]}
		nodeObjs[node_id] = data[node_id]
#		for target_node in data[node_id]['edge']:
#			nodeObjs[node_id]["edge"].append(data[node_id]['edge'][target_node])
	print fileName,"Edge:",totalEdge,"nodeWithEdge:",nodeWithEdge
	return {"graph":nodeObjs,"totalEdge":totalEdge}

def jsonToGraph(jsonFileName):
	data = json.load(open(jsonFileName))
	G = nx.DiGraph()
	for node_id in data:
		for target_node_id in data[node_id]['edge']:
			G.add_edge(int(node_id), int(target_node_id), {'count': data[node_id]['edge'][target_node_id]['count'], 'time_stamp': data[node_id]['edge'][target_node_id]['time_stamp']})
	return G

def findCore(old,new,oldTotalEdge):
	oldCore = {}
	newCore = {}
	coreList = []
	totalEdgeInOldCore = 0
	totalEdgeInNewCore = 0
	for node in new:
		if(node in old):
			if(len(new[node]['edge']) > 0 and len(old[node]['edge']) > 0):
				totalEdgeInOldCore += len(old[node]['edge'])
				totalEdgeInNewCore += len(new[node]['edge'])
				coreList.append(node)
	for node in coreList:
		if(len(new[node]['edge']) > 0):
			newCore[node] = new[node]
			edgeDict = {}
			for edge in new[node]['edge']:
				if(edge in coreList):
					edgeDict[edge] = new[node]['edge'][edge]
			if(edgeDict):
				newCore[node] = new[node]
				newCore[node]['edge'] = edgeDict
				totalEdgeInNewCore += len(newCore[node]['edge'])
			else:
				newCore[node]['edge'] = {}
		if(len(old[node]['edge']) > 0):
			oldCore[node] = old[node]
			edgeDict = {}
			for edge in old[node]['edge']:
				if(edge in coreList):
					edgeDict[edge] = old[node]['edge'][edge]
			if(edgeDict):
				oldCore[node] = old[node]
				oldCore[node]['edge'] = edgeDict
				totalEdgeInOldCore += len(oldCore[node]['edge'])
			else:
				oldCore[node]['edge'] = {}
	print "coreLen:",len(coreList)
	print "totalEdgeInOldCore:",totalEdgeInOldCore
	print "totalEdgeInNewCore:",totalEdgeInNewCore
	print "newCore:",len(newCore)
	print "oldCore:",len(oldCore)
	temp = 0
	for i in newCore:
		temp += len(newCore[i]['edge'])
	print "myNewCoreTotalEdge:",temp
	temp = 0
	for i in oldCore:
		temp += len(oldCore[i]['edge'])
	print "myOldCoreTotalEdge:",temp
	print "random predictor:",totalEdgeInNewCore/(len(newCore)*(len(newCore)-1.0)-oldTotalEdge)
	return {"newCore":newCore,"oldCore":oldCore,"coreList":coreList}

def printOne(g):
	for n in g:
		print g[n]
		if(g[n]['edge']):
			break
	return

def sortPredict(predictGraph,coreList):
	predictCount = 0
	temp = 0
	lastPredict = 0
	sortPredict = {}
	sortKey = []
	for node in coreList:
		for edge in predictGraph[node]['edge']:
			if(predictGraph[node]['edge'][edge]['count'] == 0 and edge in coreList):
				predictCount += 1
				if(not (predictGraph[node]['edge'][edge]['score'] in sortPredict)):
					sortPredict[predictGraph[node]['edge'][edge]['score']] = []
					sortKey.append(predictGraph[node]['edge'][edge]['score'])
				sortPredict[predictGraph[node]['edge'][edge]['score']].append({"from":node,"edge":predictGraph[node]['edge'][edge]})
			else:
				temp+=1
		lastPredict = predictCount
	sortKey = sorted(sortKey)
	print "predictCount: ",predictCount,temp
	return {"sortPredict":sortPredict,"sortKey":sortKey}
#	print predictCount				

#oldGraphFile = "Dataset2/from-2017-4-8-to-2017-4-16.json"
#predictGraphFile = "Dataset2/from-2017-4-8-to-2017-4-18-predicted-simrank.json"#from-2017-4-8-to-2017-4-18-predicted-katz.json"
#newGraphFile = "Dataset2/from-2017-4-8-to-2017-4-18.json"
oldGraphFile = "Dataset1/from-2017-2-11-to-2017-3-20.json"
predictGraphFile = "Dataset1/from-2017-2-11-to-2017-3-31-predicted-simrank.json"#from-2017-2-11-to-2017-3-31-predicted-katz.json"
newGraphFile = "Dataset1/from-2017-2-11-to-2017-3-31.json"
tempOldGraph = jsonLoader(oldGraphFile)
oldGraph = tempOldGraph["graph"]
oldTotalEdge = tempOldGraph["totalEdge"]
predictGraph = jsonLoader(predictGraphFile)["graph"]
newGraph = jsonLoader(newGraphFile)["graph"]
#printOne(predictGraph)
#printOne(newGraph)
core = findCore(oldGraph,newGraph,oldTotalEdge)
sortPredict = sortPredict(predictGraph,core["coreList"])
print "algoProb: "+str(checkPerformance(core["oldCore"],sortPredict,core["newCore"],core["coreList"]))

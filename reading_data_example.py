import json
import pprint

dataFile = open('jsonFormatExample.json')

data = json.load(dataFile)

for node_id in data:
	print "At node: ", data[node_id]['uid']
	for target_node in data[node_id]['edge']:
		print("Visit: {} for: {} times".format(data[node_id]['edge'][target_node]['uid']
												, data[node_id]['edge'][target_node]['count']))
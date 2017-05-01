import json
import datetime, time
from datetime import timedelta as dt
import collections
import matplotlib.pyplot as plt

if __name__ == '__main__':
    dataFile = open('test_data.json')
    data = json.load(dataFile)

    epochTimeCount = collections.OrderedDict()
    
    for node_id in data:
        for target_node_id in data[node_id]['edge']:
            time_stamp = datetime.datetime.utcfromtimestamp(data[node_id]['edge'][target_node_id]['time_stamp']['0'])
            time_stamp = time_stamp.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
            epochTime = int((time_stamp -  datetime.datetime(1970,1,1)).total_seconds())
            if epochTime not in epochTimeCount:
                epochTimeCount[epochTime] = 1
            else:
                epochTimeCount[epochTime] += 1
    
    epochTimeCount = collections.OrderedDict(sorted(epochTimeCount.items()))
    minTimeEpoch = epochTimeCount.keys()[0]
    minTimeDateTime = datetime.datetime.utcfromtimestamp(minTimeEpoch)
    maxTimeEpoch = epochTimeCount.keys()[len(epochTimeCount)-1]
    maxTimeDateTime = datetime.datetime.utcfromtimestamp(maxTimeEpoch)
    deltaTime = maxTimeDateTime - minTimeDateTime

    newTimeDict = collections.OrderedDict()
    for i in range(deltaTime.days):
        timeKeyEpoch = minTimeEpoch + i * 86400
        timeKeyDateTime = datetime.datetime.utcfromtimestamp(timeKeyEpoch)
        if timeKeyEpoch in epochTimeCount:
            # Rename existing key
            newTimeDict[timeKeyDateTime] = epochTimeCount[timeKeyEpoch]
        else:
            # Add new key
            newTimeDict[timeKeyDateTime] = 0

    plt.plot(newTimeDict.values(), 'b-', newTimeDict.values(), 'ro')
    plt.xticks(range(len(newTimeDict.values())), newTimeDict.keys(), rotation = 'vertical')
    plt.xlabel('Date')
    plt.ylabel('Number of retweet')
    plt.title('Frequency of overall retweet data')
    plt.show()
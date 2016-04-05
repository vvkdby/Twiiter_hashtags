import json
import networkx as nx
from dateutil import parser
import datetime




"""
Following functions work with comparisons of the timestamp of the current tweet with the
previous tweets
"""


# this function checks if the current tweet lies in our 60 second window
def within_last_minute(time):
    if not ht_dict.keys():
        return True
    latest_Time = max(ht_dict.keys())
    if time <= latest_Time and time >= latest_Time - datetime.timedelta(minutes=1):
        return True

    return False

# this function checks if the current tweet's timestamp is more than a minute ago
def more_than_minute(time):
    if not ht_dict.keys():
        return False
    latest_Time = max(ht_dict.keys())
    if time < latest_Time - datetime.timedelta(minutes=1):
        return True

    return False


# this function checks if the current tweet's timestamp is newer than the latest tweet
def latest_timestamp(time):
    if not ht_dict:
        return False
    latest_Time = max(ht_dict.keys())
    if time > latest_Time:
        return True

    return False



"""
This function creates the graph, finds the average degree and writes the result on to the output.
This graph is created at any given point, with the given set of to-be-processed tweets.
"""

def graph_degree():
    G = nx.Graph()
    avg_degree = 0
    # create the graph from the dictionary of hashtags(fpr faster lookup)
    # the following loop
    for tags in ht_dict.values():
        for tag in tags:
            if len(tag) > 1:
                for element in tag:
                    G.add_node(element)
                for element1 in tag:
                    for element2 in tag:
                        if element1 != element2 and not G.has_edge(element1, element2):
                            G.add_edge(element1, element2)

    # create a list of degrees of all the nodes in the graph
    degrees = nx.degree(G).values()
    #calculate the average
    if degrees:
        avg_degree = float(sum(degrees)) / len(degrees)
    outputStr = "%.2f" % (avg_degree)
    out_file.write(outputStr + "\n")
    G.clear()




"""
This is the main routine that processes the tweet one at a time (as they are being read
off an input file)
"""

print "Enter the input file name:"
inputFile = raw_input()
print "Enter the output file name:"
outputFile = raw_input()
out_file = open(outputFile, "w+")

# initialize the dictionary that is organized with timestamps as keys and hashtags as values
# this allows for faster lookup
ht_dict = {}
tweets_file = open(inputFile, 'r')
for line in tweets_file:
    tweet = json.loads(line)
    hashTags = []
    if 'created_at' not in tweet:
        continue
    time = tweet['created_at']
    time = parser.parse(time)
    for hashtag in tweet['entities']['hashtags']:
        hashTags.append(hashtag['text'])
    if within_last_minute(time):
        # add the hashtags to the dictionary
        if time in ht_dict:
            ht_dict.get(time).append(hashTags)
        else:
            ht_dict[time] = [hashTags]
        graph_degree()
    elif more_than_minute(time):
        # calculate and write the degree
        graph_degree()
    elif latest_timestamp(time):
        # our latest timestamp is now different
        # remove the tweets that apeared more than a minute ago from the latest
        for key in ht_dict.keys():
            if key < time - datetime.timedelta(minutes=1):
                ht_dict.pop(key)
        # add the new hashtag that arrived
        if time in ht_dict:
            ht_dict.get(time).append(hashTags)
        else:
            ht_dict[time] = [hashTags]
        # calculate and write the degree
        graph_degree()








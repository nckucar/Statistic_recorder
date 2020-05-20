#!/usr/bin/env python
import rospy
#from std_msgs.msg import String
from rosgraph_msgs.msg import TopicStatistics
import sys
import atexit

edges = dict([])
minmax_freq = dict([])

def exit_handler():
    print_all_data(minmax_freq)

def listener():
    
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('/statistics', TopicStatistics, statistics_callback)
    rospy.spin()
   

def statistics_callback(msg):

    # add connections (if new)
    if msg.node_sub not in edges:
        edges[msg.node_sub] = dict([])
        minmax_freq[msg.node_sub] = dict([])

    if msg.topic not in edges[msg.node_sub]:
        edges[msg.node_sub][msg.topic] = dict([])
        minmax_freq[msg.node_sub][msg.topic] = dict([])

    edges[msg.node_sub][msg.topic][msg.node_pub] = msg
    
    if msg.node_pub not in minmax_freq[msg.node_sub][msg.topic]:
        minmax_freq[msg.node_sub][msg.topic][msg.node_pub] = dict([])


    if 'count' not in minmax_freq[msg.node_sub][msg.topic][msg.node_pub]:
        minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['min_freq'] = sys.maxint
        minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['max_freq'] = 0
        minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['avg_freq'] = 0
        minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['count'] = 0

    #store max freq
    period = edges[msg.node_sub][msg.topic][msg.node_pub].period_mean.to_sec()
    if period > 0.0:
        freq = round(1.0 / period, 1)
    else:
        freq = 0.0
        print('detect no period in: ' + str(msg.node_pub) +'/'+ str(msg.topic) +'/' + str(msg.node_sub))
    
    if minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['max_freq'] <  freq:
        minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['max_freq'] = freq

    if minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['min_freq'] >  freq:
        minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['min_freq'] = freq

    count = minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['count']
    minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['avg_freq'] = (minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['avg_freq'] * count + freq) / (count + 1)
    minmax_freq[msg.node_sub][msg.topic][msg.node_pub]['count'] += 1
    

def print_all_data(minmax_freq):
    for sub in minmax_freq.keys():
        for topic in minmax_freq[sub].keys():
            for pub in minmax_freq[sub][topic].keys():
                    print(str(pub)  + ' ---> ' + str(topic) + '-->' + str(sub) +': ' 
                    + str(minmax_freq[sub][topic][pub]['max_freq']) + '/' 
                    + str(minmax_freq[sub][topic][pub]['avg_freq']) + '/'
                    + str(minmax_freq[sub][topic][pub]['min_freq'])
                    )                    
    

if __name__ == '__main__':
    listener()
    atexit.register(exit_handler)

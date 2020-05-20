# Statistic_recorder
## Requirement
* ROS indigo/kinetic
* Python 2.7

## Usage
```
# Execute ROS system first (i.e. roscore)
rosparam set enable_statistics true
python statistic_recorder
# Ctrl-c to terminate recording
```


## Data format
* (publisher) —> (topic) --> (subscriber): (Max)/(avg)/(min) publish frequency

```
/lane_select ---> /closest_waypoint-->/waypoint_marker_publisher: 10.3/7.73333333333/5.5
/velocity_set ---> /final_waypoints-->/waypoint_marker_publisher: 10.1/10.0041666667/10.0
/pure_pursuit ---> /twist_raw-->/twist_filter: 10.0/7.58333333333/5.4
/websocket_bridge ---> /points_raw-->/lidar_euclidean_cluster_detect: 11.0/9.958/9.3
/base_link_to_localizer ---> /tf-->/lidar_euclidean_cluster_detect: 97.8/97.8/97.8
...
```


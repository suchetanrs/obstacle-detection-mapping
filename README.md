# obstacle-detection-mapping

# Video Demonstration
![](https://github.com/suchetanrs/obstacle-detection-mapping/blob/master/README-files/animation.gif)<br/>
This is a video demonstration of mapping of the turtlebot's environment.

# Explanation
```map_animation.py``` subsribes to the ```/odom``` topic to localize the robot's position and ```/scan``` topic to map the obstacles. <br/>
This obstacle mapping is then converted to a binary occupancy grid for further use. <br/>

# How to use
__Setting up your environment__
1. Clone this repository into your ```catkin_workspace```
2. Run ```cd catkin_ws && catkin_make```
3. Roscore ```roscore```
4. Export your turtlebot model. ```EXPORT TURTLEBOT3_MODEL=waffle```
5. Loading up your gazebo ```roslaunch obstacle_detection_mapping automation_task.launch```
6. Run ```rosrun teleop_twist_keyboard teleop_twist_keyboard.py```

__Running the scripts__
1. ```roscd obstacle_detection_mapping/scripts```
2. Making the files executable 
  2.1 ```chmod +x map_animation.py```
  2.2 ```chmod +x occupancy_grid.py```
3.  Run the mapping script ```rosrun obstacle_detection_mapping map_animation.py``` <br/>
This will do your job, if in case you want to see the live occupancy grid plot, execute the command ```rosrun <package_name> occupancy_grid.py```<br/>
The occupancy grids co-ordinates can also be obtained with the command ```rosservice call /get_obstacles_grid```

Hope you have fun running this and is useful to you!

#!/usr/bin/env python

import rospy
import matplotlib.pyplot as plt
from obstacle_detection_mapping.srv import GetPathPoints, GetPathPointsResponse
import draw_graph as drawer


def serv():
    rospy.wait_for_service('/get_obstacles_grid')
    try:
        get_path_points=rospy.ServiceProxy('/get_obstacles_grid', GetPathPoints)
        resp=get_path_points()
        return resp.points
    except:
        pass


while not rospy.is_shutdown():
    points=serv()
    for item in points:
        print(item)
        rectangle = plt.Rectangle((item.x,item.y), 1, 1, fc='k')
        plt.gca().add_patch(rectangle)
    # plt.grid()
    plt.pause(0.0001)
    # rospy.sleep(0.5)
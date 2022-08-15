#!/usr/bin/env python

from math import cos,sin,floor
import rospy
from sensor_msgs.msg import LaserScan
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from math import tan,radians,degrees
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from obstacle_detection_mapping.srv import GetPathPoints,GetPathPointsResponse
from obstacle_detection_mapping.msg import GoalPoint
from matplotlib.animation import FuncAnimation

class Plots():
    def __init__(self):
        # self.ani=animation.FuncAnimation(self.fig, animate, interval=1000)
        # plt.ion()
        # plt.show()
        self.fig, self.ax = plt.subplots(1, 1)
        self.curr_x=0
        self.curr_y=0
        self.rot_q=0
        self.roll=0
        self.pitch=0
        self.theta=0
        self.scan_data=[]
        self.active_scan_data=[]
        self.mappingtime_nsecs=0
        self.localizationtime_nsecs=0
        self.mappingtime_secs=0
        self.localizationtime_secs=0
        self.obstacles_blocks=[]
        self.obstacle_points=[]

    def mapping(self,msg):
        self.active_scan_data=msg.ranges
        self.mappingtime_secs=msg.header.stamp.secs
        self.mappingtime_nsecs=msg.header.stamp.nsecs
        # rospy.loginfo("Scan...")
        # rospy.Rate(3).sleep()

    def localization(self,msg):
        self.curr_x=msg.pose.pose.position.x
        self.curr_y=msg.pose.pose.position.y
        self.localizationtime_secs=msg.header.stamp.secs
        self.localizationtime_nsecs=msg.header.stamp.nsecs
        # rospy.loginfo("Odom")

        self.rot_q=msg.pose.pose.orientation
        (self.roll,self.pitch,self.theta)=euler_from_quaternion([self.rot_q.x,self.rot_q.y,self.rot_q.z,self.rot_q.w])
        if(self.theta<0):
            self.theta=360-abs(degrees(self.theta))
            self.theta=radians(self.theta)
        if(abs(self.mappingtime_nsecs-self.localizationtime_nsecs)<=100000000 and self.mappingtime_secs==self.localizationtime_secs):
            # print("Matched") 
            self.scan_data=self.active_scan_data
            for items in self.scan_data:
                if(items<float('inf')):
                    try:
                        # print(self.theta)
                        index=self.scan_data.index(items) 
                        x=items*cos(radians(index)+self.theta)
                        y=items*sin(radians(index)+self.theta)
                        # plt.plot(self.curr_x+x,self.curr_y+y,marker="o")        
                        # plt.plot(self.curr_x,self.curr_y,marker="x")

                        rect_x=floor(self.curr_x+x)
                        rect_y=floor(self.curr_y+y)
                        if([rect_x,rect_y] not in self.obstacles_blocks):
                            self.obstacles_blocks.append([rect_x,rect_y])
                            print(len(self.obstacles_blocks))
                        self.obstacle_points.append([self.curr_x+x,self.curr_y+y])
                        if(len(self.obstacle_points)>360):
                            self.obstacle_points=[]
                        
                    except:
                        print("Exception")
        # self.ax.xlim(-10,10)
        # self.ax.ylim(-10,10)
        # self.fig.canvas.draw()
        # self.fig.canvas.flush_events()
        # plt.grid()
        # plt.pause(1e-10)
        # plt.grid()
        # rospy.sleep(0.01)

    def get_obstacles(self,msg):
        self.obstacles_blocks_copy=self.obstacles_blocks
        result=[]
        for items in self.obstacles_blocks_copy:
            obj=GoalPoint()
            obj.x=items[0]
            obj.y=items[1]
            result.append(obj)
        return GetPathPointsResponse(result)
    
    def animate(self,i):
        rospy.loginfo("animating")
        # self.ax.clear()
        # self.ax.grid()
        obstacle_points_copy=self.obstacle_points
        counter=0
        for items in obstacle_points_copy:
            counter+=1
            self.ax.plot(items[0],items[1],marker="o")
        # self.ax.grid()
            # self.obstacle_points.remove([items[0],items[1]])
        


    def main(self):
        rospy.init_node('map',anonymous=True)
        sub=rospy.Subscriber('/scan',LaserScan,self.mapping,queue_size=1)
        sub2=rospy.Subscriber('/odom',Odometry,self.localization,queue_size=1)

        serv1=rospy.Service('/get_obstacles_grid',GetPathPoints,self.get_obstacles)

        # rospy.spin()
        # plt.show()
        # while not rospy.is_shutdown():
        ani=FuncAnimation(self.fig,self.animate,interval=10,repeat=False)
        plt.grid()
        plt.show()
        rospy.spin()
        # plt.close()
            

if __name__=="__main__":
    Plots().main()
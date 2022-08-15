
from matplotlib import pyplot as plt
import rospy
from obstacle_detection_mapping.srv import GetPathPoints

no_of_rows=12
no_of_cols=35


#every block in a graph has a list assigned to it called grid id.
#list contains left bottom coordinates, [x,y,status]
#status: 
    #-1 if obstacle
    #0 if clear path


obstacle_list=[]
grid_id_list=[]
def make_obstacles1():
    global obstacle_list
    for y in range(no_of_rows):
        obstacle_list.append([0,y])
        obstacle_list.append([no_of_cols-1,y])
    for x in range(no_of_cols):
        obstacle_list.append([x,no_of_rows-1])
        obstacle_list.append([x,0])
    obstacle_list.remove([1,0])
    obstacle_list.remove([2,0])
    obstacle_list.remove([3,0])
    temp_list=[[4,1],[6,1],[6,2],[6,3],[5,3],[4,3],[5,10],[5,9],[10,11],[10,10],[10,9],[10,8],[10,7],[10,6],[10,5],[10,4],[10,3],[9,7],[8,7],[7,7]]
    obstacle_list=obstacle_list+temp_list
    temp_list=[[7,6],[7,5],[6,5],[5,5],[16,1],[16,2],[16,3],[16,4],[16,5],[16,6],[16,7],[13,7],[14,7],[15,7],[13,3],[14,3],[15,3],[13,2],[13,4],[13,6]]
    obstacle_list=obstacle_list+temp_list
    temp_list=[[19,1],[19,2],[19,6],[19,7],[19,8],[19,9],[19,10],[20,6],[21,6],[21,7],[21,8],[22,8],[23,8],[24,8],[25,8],[26,4],[26,3],[26,8],[26,7],[26,6],[26,5]]
    obstacle_list=obstacle_list+temp_list
    temp_list=[[21,3],[21,4],[22,4],[23,4],[23,3],[29,10],[29,9],[30,7],[31,7],[32,7],[33,7],[29,3],[29,4],[30,4],[31,4],[32,4],[33,4],[29,2],[1,0],[2,0],[3,0]]
    obstacle_list=obstacle_list+temp_list

def make_obstacles2():
    global obstacle_list
    obstacle_list=[]

def make_obstacles3():
    global obstacle_list
    # obstacle_list=[[3,0],[3,1],[3,2],[3,3],[3,4],[3,5]]
    obstacle_list=[[3,0]]

def active_make_obstacles():
    global obstacle_list
    rospy.wait_for_service('/get_obstacles_grid')
    # rospy.loginfo("Grid")
    get_obstacles_grid=rospy.ServiceProxy('/get_obstacles_grid',GetPathPoints)
    resp=get_obstacles_grid()
    for item in resp.points:
        obstacle_list.append([item.x,item.y])


def draw_obstacles():
    # make_obstacles1()
    active_make_obstacles()
    for x in range(no_of_cols):
        for y in range(no_of_rows):
            if([x,y] in obstacle_list):
                rectangle = plt.Rectangle((x,y), 1, 1, fc='k')
                plt.gca().add_patch(rectangle)


def draw_grid():
    for x in range(no_of_cols+1):
        x_vals = [x,x]
        y_vals = [0,no_of_rows]
        plt.plot(x_vals,y_vals,color="k")

    for y in range(no_of_rows+1):
        x_vals = [0,no_of_cols]
        y_vals = [y,y]
        plt.plot(x_vals, y_vals,color="k")




def grid_id_generator():
    global grid_id_list
    for x in range(no_of_cols):
        for y in range(no_of_rows):
            if([x,y] in obstacle_list):
                grid_id_list.append([x,y,-1])
            else:
                grid_id_list.append([x,y,0])
    return grid_id_list


def get_grid_id(x,y):
    for coords in grid_id_list:
        if(coords[0]==x and coords[1]==y):
            return coords


def is_obstacle(x,y):
    if([x,y] in obstacle_list):
        return True
    else:
        return False


def is_in_boundary(x,y):
    if(x<no_of_cols and y<no_of_rows):
        return True


def get_neighbor_list(x,y):
    temp_list= [[x+1,y],[x-1,y],[x,y+1],[x,y-1],[x+1,y+1],[x-1,y+1],[x+1,y-1],[x-1,y-1]]
    temp_list2=[]
    for coords in temp_list:
        if(is_obstacle((coords[0]),(coords[1]))==False):
            temp_list2.append(coords)
    return temp_list2



def h_value(point,goal):
    h_val=0
    point_coords=point
    goal_coords=goal
    while(goal_coords!=point_coords):
        if(goal_coords[0]==point_coords[0]):
            h_val+=abs(point_coords[1]-goal_coords[1])
            point_coords[1]-=(point_coords[1]-goal_coords[1])
            break
        if(goal_coords[1]==point_coords[1]):
            h_val+=abs(point_coords[0]-goal_coords[0])
            point_coords[0]-=(point_coords[1]-goal_coords[1])
            break
        if(goal_coords[1]>point_coords[1]):
            if(goal_coords[0]>point_coords[0]):
                point_coords[0]+=1
                point_coords[1]+=1
                h_val+=1.4
            if(goal_coords[0]<point_coords[0]):
                point_coords[0]-=1
                point_coords[1]+=1
                h_val+=1.4
        if(goal_coords[1]<point_coords[1]):
            if(goal_coords[0]>point_coords[0]):
                point_coords[0]+=1
                point_coords[1]-=1
                h_val+=1.4
            if(goal_coords[0]<point_coords[0]):
                point_coords[0]-=1
                point_coords[1]-=1
                h_val+=1.4

    return h_val

def show_plot():
    plt.show()

def animate_plot():
    plt.pause(1e-10)

def draw_node(x,y,color):
    rectangle = plt.Rectangle((x,y), 1, 1, fc=color)
    plt.gca().add_patch(rectangle)



# rospy.init_node('draw_graph',anonymous=True)
draw_grid()
draw_obstacles()
grid_id_generator()
# print(obstacle_list)
# print(is_obstacle(13,7))
# print(get_neighbor_list(27,3))
# print(h_value([28,3],[27,5]))
# show_plot()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import smach
import smach_ros
import actionlib
import math
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from turtlebot3_msgs.msg import Sound


def movebase_client():
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    point = 5
    count = 0
    for i in range(5):         
        if(i == 1):
            goal.target_pose.pose.position.x = -1.0
            goal.target_pose.pose.position.y = 0.0199
            goal.target_pose.pose.orientation.w = 0.9124
            client.send_goal(goal)
            wait = client.wait_for_result()
            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server not available!")
            else:
                rospy.loginfo("Point2 get!")
        elif (i == 2):
            goal.target_pose.pose.position.x = 3.0
            goal.target_pose.pose.position.y = 0.26
            goal.target_pose.pose.orientation.w = -1.0
            client.send_goal(goal)
            wait = client.wait_for_result()
            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server not available!")
            else:
                rospy.loginfo("Point3 get!")
        elif (i == 3):
            goal.target_pose.pose.position.x = 2.85
            goal.target_pose.pose.position.y = 4.26
            goal.target_pose.pose.orientation.w = 0.6
            client.send_goal(goal)
            wait = client.wait_for_result()
            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server not available!")
            else:
                rospy.loginfo("Point4 get!")
        elif (i == 4):
            goal.target_pose.pose.position.x = -0.89
            goal.target_pose.pose.position.y = 3.5
            goal.target_pose.pose.orientation.z = -0.707
            goal.target_pose.pose.orientation.w = 0.707
            client.send_goal(goal)
            wait = client.wait_for_result()
            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server not available!")
            else:
                rospy.loginfo("Point5 get!")
    return client.get_result()

# def movebase_client():
#     client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
#     client.wait_for_server()

#     goal = MoveBaseGoal()
#     goal.target_pose.header.frame_id = "map"
#     goal.target_pose.header.stamp = rospy.Time.now()
#     point = 5
#     count = 0
#     for i in range(1):
#         if (i == 0):
#             goal.target_pose.pose.position.x = -0.80
#             goal.target_pose.pose.position.y = 3.5
#             goal.target_pose.pose.orientation.z = -0.707
#             goal.target_pose.pose.orientation.w = 0.707
#             client.send_goal(goal)
#             wait = client.wait_for_result()
#             if not wait:
#                 rospy.logerr("Action server not available!")
#                 rospy.signal_shutdown("Action server not available!")
#             else:
#                 rospy.loginfo("Point5 get!")
#     return client.get_result()




class Foo(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        try:
            result = movebase_client()
            if result:
                return 'outcome1'
        except rospy.ROSInterruptException:
            return 'outcome2'


class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome_id2','outcome_id3','outcome_id4','outcome_Aruco_wrong'])

    def execute(self, userdata):
        rospy.loginfo('Executing state BAR')
        try:
            id = aruco_sub()
            buzzer(id)
            if (id == 2):
                return 'outcome_id2'
            elif (id == 3):
                return 'outcome_id3'
            elif (id == 4):
                return 'outcome_id4'
        except rospy.ROSInterruptException:
            pass
            rospy.loginfo('Aruco:wrong!')
            return 'outcome_Aruco_wrong'

def buzzer(id):
    pub = rospy.Publisher('/sound', Sound, queue_size=10)
    msg = Sound()
    if (id == 2):
        msg.value = 0
    elif (id == 3):
        msg.value = 1
    elif (id == 4):
        msg.value = 2
    count = 0
    while(count < 2):
        pub.publish(msg)
        rospy.loginfo("beep")
        rospy.sleep(1.0)
        count = count+1

def aruco_sub():
    stop = -1
    id = -1
    while(stop == -1):
        rospy.logerr("hhhhhello_122433443")
        msg_id2 = None
        msg_id3 = None
        msg_id4 = None
        try:
            msg_id4 = rospy.wait_for_message("/aruco_single_id4/pose",PoseStamped,timeout= 0.1)
        except:
            pass
        try:
            msg_id3 = rospy.wait_for_message("/aruco_single_id3/pose",PoseStamped,timeout= 0.1)
        except: 
            pass
        try:
            msg_id2 = rospy.wait_for_message("/aruco_single_id2/pose",PoseStamped,timeout= 0.1)
        except:
            pass       
        
        rospy.logerr("hhhhhello")
        if(msg_id2 != None):
            stop,id = callback_id2(msg_id2)
        if(msg_id3 != None):
            stop,id = callback_id3(msg_id3)
        if(msg_id4 != None):
            rospy.loginfo("id444444444444444444444444444444444444444444444")
            stop,id = callback_id4(msg_id4)
        rospy.loginfo("id= "+str(id))

    pub = rospy.Publisher('/cmd_vel', Twist,queue_size=10)
    msg = Twist()
    msg.linear.x=0.1
    msg.angular.z=0
    pub.publish(msg)
    rospy.sleep(2)
    msg.linear.x=0
    msg.angular.z=0
    pub.publish(msg)
    return id
    

        
def callback_id2(data):
    id = -1
    stop = -1
    if(data != None):
        id = 2
        x = data.pose.position.x
        y = data.pose.position.y
        z = data.pose.position.z
        distance = math.sqrt(pow(x,2)+pow(y,2)+pow(z,2))
        rospy.loginfo("distance"+str(distance))
    else:
        distance = 100
    pub = rospy.Publisher('/cmd_vel', Twist,queue_size=10)
    msg = Twist()
    if(distance<0.3):
        msg.linear.x=0
        msg.angular.z=0
        pub.publish(msg)
        stop = 0
        rospy.loginfo("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"+str(distance))
    else:
        msg.linear.x=0.1
        msg.angular.z=0
        pub.publish(msg)
        rospy.loginfo("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"+str(distance))
    return [stop,id]

def callback_id3(data):
    id = -1
    stop = -1
    if(data != None):
        id = 3
        x = data.pose.position.x
        y = data.pose.position.y
        z = data.pose.position.z
        distance = math.sqrt(pow(x,2)+pow(y,2))
        rospy.loginfo("distance"+str(distance))
    else:
        distance = 100
    pub = rospy.Publisher('/cmd_vel', Twist,queue_size=10)
    msg = Twist()
    if(distance<0.03):
        msg.linear.x=0
        msg.angular.z=0
        pub.publish(msg)
        stop = 0
        rospy.loginfo("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"+str(distance))
    else:
        msg.linear.x=0.1
        msg.angular.z=0
        pub.publish(msg)
        rospy.loginfo("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"+str(distance))
    return [stop,id]

def callback_id4(data):
    id = -1
    stop = -1
    if(data != None):
        id = 4
        stop = 0 
    # if(data != None):
    #     id = 4
    #     x = data.pose.position.x
    #     y = data.pose.position.y
    #     z = data.pose.position.z
    #     distance = math.sqrt(pow(x,2)+pow(y,2))
    #     rospy.loginfo("distance"+str(distance))
    # else:
    #     distance = 100
    # pub = rospy.Publisher('/cmd_vel', Twist,queue_size=10)
    # msg = Twist()
    # if(distance<0.075):
    #     msg.linear.x=0
    #     msg.angular.z=0
    #     pub.publish(msg)
    #     stop = 0
    #     rospy.loginfo("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"+str(distance))
    # else:
    #     msg.linear.x=0.05
    #     msg.angular.z=0
    #     pub.publish(msg)
    #     rospy.loginfo("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"+str(distance))
    return [stop,id]

def movebase_client_id(x,y,z,w):
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    for i in range(1):
        if (i == 0):
            goal.target_pose.pose.position.x = x
            goal.target_pose.pose.position.y = y
            goal.target_pose.pose.orientation.z = z
            goal.target_pose.pose.orientation.w = w
            client.send_goal(goal)
            wait = client.wait_for_result()
            if not wait:
                rospy.logerr("Action server not available!")
                rospy.signal_shutdown("Action server not available!")
            else:
                rospy.loginfo("Point get!")
    return client.get_result()



class ID2(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome_id2_right','outcome_id2_wrong'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ID2')
        try:
            result = movebase_client_id( -1.0, 0.0199,0,0.9124)
            if result:
                return 'outcome_id2_right'
        except rospy.ROSInterruptException:
            pass
            rospy.loginfo('ID2:wrong!')
            return 'utcome_id2_wrong'


class ID3(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome_id3_right','outcome_id3_wrong'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ID3')
        try:
            result = movebase_client_id( 3, 0.36,0,-1)
            if result:
                return 'outcome_id3_right'
        except rospy.ROSInterruptException:
            pass
            rospy.loginfo('ID3:wrong!')
            return 'utcome_id3_wrong'


class ID4(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome_id4_right','outcome_id4_wrong'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ID4')
        try:
            # result0 = movebase_client_id(-0.3,3.3,-0.707,0.707)
            result = movebase_client_id( 2.85,4.26,0,0.6)
            if result:
                return 'outcome_id4_right'
        except rospy.ROSInterruptException:
            pass
            rospy.loginfo('ID4:wrong!')
            return 'utcome_id4_wrong'





def main():
    rospy.init_node('movebase_client_py')

    # 创建一个状态机
    sm = smach.StateMachine(outcomes=['outcome4'])

    # 打开状态机容器
    with sm:
        # 使用add方法添加状态到状态机容器当中
        smach.StateMachine.add('FOO', Foo(), 
                               transitions={'outcome1':'BAR', 
                                            'outcome2':'FOO'})
        smach.StateMachine.add('BAR', Bar(), 
                               transitions={'outcome_id2':'ID2',
                                            'outcome_id3':'ID3',
                                            'outcome_id4':'ID4',
                                            'outcome_Aruco_wrong':'outcome4' })
        smach.StateMachine.add('ID2', ID2(), 
                               transitions={'outcome_id2_right':'outcome4' ,
                                            'outcome_id2_wrong':'outcome4' })
        smach.StateMachine.add('ID3', ID3(), 
                               transitions={'outcome_id3_right':'outcome4' ,
                                            'outcome_id3_wrong':'outcome4' })
        smach.StateMachine.add('ID4', ID4(), 
                               transitions={'outcome_id4_right':'outcome4' ,
                                            'outcome_id4_wrong':'outcome4' })
    # 创建并启动内部监测服务器
    sis = smach_ros.IntrospectionServer('my_smach_introspection_server', sm, '/SM_ROOT')
    sis.start()
    
    # 开始执行状态机
    outcome = sm.execute()
    
    # 等待退出
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()






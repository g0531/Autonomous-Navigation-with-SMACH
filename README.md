# Autonomous-Navigation-with-SMACH
THis lab uses a state machine SMACH to sequence the tasks: 

First, the robot shoud successively move to P2,P3,p4 and back to P1 in that order. 

Then, upon returning to P1, the robot should move toward the ArUco marker to recognize the ID of the marker n=2, 3 or 4. 

Third, after recognizing the ID, the robot sould beep with the buzzer on TurtleBOt3 n times and then move to Pn before coming to a stop.
## Step 1: install SMACH
sudo apt-get install ros-melodic-smach-ros
## Step 2: robot set up
roslaunch turtlebot3_bringup turtlebot3_robot.launch

roslaunch hls_lfcd_lds_driver hlds_laser.launch

roslaunch raspicam_node camerav2_410x308_30fps.launch 

## Step 3: roslaunch to recognize ArUco marker ID on PC
roslaunch aruco_marker_finder_2.launch markerID:=2 markerSize:=0.05

roslaunch aruco_marker_finder_3.launch markerID:=3 markerSize:=0.05

roslaunch aruco_marker_finder_4.launch markerID:=4 markerSize:=0.05

## Step 3: roslaunch navigation based on the map.yaml on PC
roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml

# Step 4: start the SMACH GUI on PC to visually observe the current running process
rosrun smach_viewer smach_viewer.py

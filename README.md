# Autonomous-Navigation-with-SMACH
THis lab uses a state machine SMACH to sequence the tasks: first the robot shoud successively move to P2,P3,p4 and back to P1 in that order. 
Then upon returning to P1, the robot should move toward the ArUco marker to recognize the ID of the marker n=2, 3 or 4. 
Third, after recognizing the ID, the robot sould beep with the buzzer on TurtleBOt3 n times and then move to Pn before coming to a stop.
## Step1: install SMACH
sudo apt-get install ros-melodic-smach-ros
## Step2: robot set up

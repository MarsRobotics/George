# George
Code on George
George is the codename for the RPi that is central to the functioning of the robot.
George is the "brain" of the robot and essentially performs all the executive control functions of the other parts of the robot and can interface with a human driver.
The code on George is organized by which function it holds. The Arduino folder contains the files pertaining to communication with the Arduino which is done through the Robot Operating System (ROS)
command2ros is what allows for translating a command from the state machine running on George to a ros command that will be interpreted and completed on the Arduino.
manual contains the files used for manual control of the robot which is performed through keyboard presses.

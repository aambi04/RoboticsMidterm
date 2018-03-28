Robotics Term Project

In this application you will be able to run a simulated autonomous robot on various paths. 

To start the program, you will see 6 different options on which path the autonomous car can travel on. 

    For each path you must fill on the necessary fields related to the path. When clicking the submit button 
    underneath the fields it was capture the values inputed and run the simulated path as expected. Each path 
    has its own submit button. Once the robot has completed one cycle of the path there is the opportunity to 
    try another path of the same one at the current position of the robot. To the right of the input fields is
    the display with the realtime placement (based on reference point) and various velocities of the vehicle. 
    When the vehicle is running these values are updated every 100 milliseconds. Underneath the display is a 
    reset button which will bring the vehicle back to the center of the grid layout as well as reinitialize its 
    current state such as velocities and placement. 
    
    A run throught of the behavior of each path:
        1. Circle: the circle path has two inputs, radi and inclincation angle. The inclincation angle is 
            not required to run this path. After filling out the fields you may click the submit button below
            to run it. 
        2. Rectangle: The rectangular path will take in the length, width, and inclincation of the path. Once 
            again the inclincation path is not required to run this simulation. Once clicked on "submit" the
            robot will move to the left then downward, right, and back up to its starting point. If the vehicle 
            falls within three feet away from the borders it will be recentered and continue its path. 
        3. Figure 8: The rigure 8 path is a fun one. Once a radi for the top and bottom circles are inputted the 
            robot will start its journey around the figure 8. 
        4. Point Execution: This field has a couple of options on the path it will take. The user may decide to 
            only put in the values for one destination end point in Xf and Yf fields. This will be a single jouney 
            to the expected point. If the user would like to add in some waypoints they must add upto 3 points to 
            see a different path. The robot will go to each point in the order the waypoints are given, meaning it 
            will go through waypoint1, then waypoint2, the waypoint3, and maybe even waypoint 4, ending at x_f and y_f.
        5. Wheels Rotation: This path is quite different then the last 4 described. In this section you will find that
            once inputting in values for each mecanum wheels the robot will starts its journey until told to stop. The way
            to get the robot to stop is to press down on the mouse anywhere on the application. The vehicle will freeze at 
            its current position. The user can choose to continue the path or reset and start a different path. 
        6. The last section is similar to number 5 but instead the user can input in values for the desired direction 
            and velocity the vehicle will go. Then the user can also input in a rotational rate which will add some fun 
            twirling to the path. What you will see here is that the robot will not stay as clear on the path when that 
            field is added into the mix. Also note that the velocity of the vehicle must stay below 15ft/sec. No warning
            or error will show. The user will need to try another value less than or equal to the max. 
        7. Lastly is the time taken from start to end points on any of the paths (except for the last 2). If the value 
            inputed can not be completed in the time and error message will show. 
   
   
   
That should be it for now! Enjoy :)
from Tkinter import *
# from robots import *
import numpy as np
import math
from copy import *

# constants
PI = math.pi
L = 4
H = 2
R = 1.0   # wheel radius
ri = 0.25   # roller radius

NORM = 12
WIDTH = 360 + NORM
HEIGHT = 720 + NORM
THREEFEET = 72  + NORM  # 3ft to pixels conversion
X_CENTER = WIDTH/2      # starting point for robot
Y_CENTER = HEIGHT/2     # starting point for robot
VERTICES = [[WIDTH/2 - 26, HEIGHT/2 - 52],
            [WIDTH/2 + 26, HEIGHT/2 - 52],
            [WIDTH/2 + 26, HEIGHT/2 + 52],
            [WIDTH/2 - 26, HEIGHT/2 + 52]
            ]
x1 = NORM
x2 = WIDTH
omega = 0
position = [3,3]
wheelRotation = [0,1,2,3]
velocity=[-1,-3]

#helper functions
def feettoPixels(feet):
    return 24 * int(feet)


class Vehicle:
    def __init__(self, active):
        self.shape = canvas.create_polygon(VERTICES, fill=color)       # robot is 4.33 ft long, 2.17 ft wide
        self.speedx = 1
        self.speedy = 1
        self.inclineAngle = 0  # heading angle
        self.ref_point = [X_CENTER, Y_CENTER]
        self.active = active
        self.dist = [0, 0]
        self.relative = [X_CENTER, Y_CENTER]
        self.vd = 1
        self.rect = [0,0,0, 0, 0]         # length, width, inclincation theta
        self.circle = [0,0]
        self.figure = [0,0,0,0]
        self.resetdist = [0, 0]
        self.cicumference = 0
        self.figIndex = 0
        self.degRotation = 10.0 * PI/180.0
        self.headingAngle = PI/2
        self.wheelRotation = [0,0,0,0]
        self.mode = None
        self.totalDist = 0
        self.waypoints = []


##################### HELPER FUNCTIONS #####################################

    def setActive(self, active):
        self.active = active

    def setVD(self, vd):
        self.vd = vd

    def getVelocity(self):
        return [self.speedx, self.speedy]

    def getRefPoint(self):
        return self.ref_point

    def setMode(self, mode):
        self.mode = mode

    def getMode(self):
        return self.mode

    def getWheelRotation(self):
        return self.wheelRotation

    def setRelative(self):
        self.active = False
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.relative = [(pos[0] + pos[4])/2, (pos[1] + pos[5])/2]
        self.speedx = 1
        self.speedy = 1
        self.inclineAngle = 0
        self.dist = [0, 0]
        self.vd = 2
        self.rect = [0,0,0,0,0]         # length, width, inclincation theta
        self.circle = [0,0]
        self.figure = [0,0,0,0]
        self.resetdist = [0, 0]
        self.cicumference = 0
        self.figIndex = 0
        self.degRotation = 10.0 * PI/180.0
        self.headingAngle = PI/2
        self.wheelRotation = [0,0,0,0]
        self.totalDist = 0
        self.waypoints = []

    def processing(self, v_d, theta_d):         #20 ms readings

        v_cx = v_d * np.cos(theta_d)

        v_cy = v_d * np.sin(theta_d + np.pi)

        self.wheelRotation = self.wheelRotationalVelocity(v_cx, v_cy, self.inclineAngle)

        return v_cx, v_cy

    def wheelRotationalVelocity(self, vcx, vcy, omega):

        state_matrix = np.transpose([[vcx, vcy, omega]])                # take the transpose of the state vector. Dimnesions are 3x1

        inverse_kinematic = np.array([[1, 1, -(L+H)], [-1, 1, (L+H)], [-1, 1, -(L+H)], [1, 1, (L+H)]])     # kinematic equations

        psi = (1/R) * np.dot(inverse_kinematic, state_matrix)       # find the velocities of each of the wheels

        return psi

    def kinematic(self, wheel1, wheel2, wheel3, wheel4):

        wheels = np.transpose([[wheel1, wheel2, wheel3, wheel4]])

        jacobian = np.array([[1., -1., -1., 1.], [1., 1., 1., 1.], [(-1./(L+H)), (1./(L+H)), (-1./(L+H)), (1./(L+H))]])

        velocity = (R/4.0) * np.dot(jacobian, wheels)

        return velocity


    def reset(self):
        canvas.delete(self.shape)
        self.active = False
        self.shape = canvas.create_polygon(VERTICES, fill=color)       # robot is 4.33 ft long, 2.17 ft wide
        self.speedx = 1
        self.speedy = 1
        self.inclineAngle = 0  # heading angle
        self.ref_point = [X_CENTER, Y_CENTER]
        self.dist = [0, 0]
        self.relative = [X_CENTER, Y_CENTER]
        self.vd = 1
        self.rect = [0,0,0,0,0]         # length, width, inclincation theta
        self.circle = [0,0]
        self.figure = [0,0,0,0]
        self.resetdist = [0, 0]
        self.cicumference = 0
        self.figIndex = 0
        self.degRotation = 10.0 * PI/180.0
        self.headingAngle = PI/2
        self.wheelRotation = [0,0,0,0]
        self.totalDist = 0
        self.waypoints = []

############################# RECTANGLE ########################################


    def move_activeRect(self):
        if self.active:
            self.vehicle_updateRectangle()
            canvas.after(10, self.move_activeRect) # time in terms of miliseconds

    def vehicle_updateRectangle(self):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        canvas.move(self.shape, delta_x , delta_y)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[4])/2, (pos[1] + pos[5])/2]


        self.dist[0] = self.resetdist[0] + math.fabs(self.ref_point[0] - self.relative[0])
        self.dist[1] = self.resetdist[1] + math.fabs(self.ref_point[1] - self.relative[1])

        if np.linalg.norm(self.dist) >= self.rect[self.totalDist]:
            thetaD = self.inclineAngle - (PI / 2.0)          # move along the x axis
            self.speedx, self.speedy = self.processing(self.vd, thetaD)
            self.relative = [self.ref_point[0], self.ref_point[1]]

            self.totalDist += 1
            if self.totalDist == 4:
                self.active = False
            self.dist = [0,0]
            self.resetdist = [0,0]
            self.inclineAngle = deepcopy(thetaD)

        elif self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_polygon(VERTICES, fill=color)
            self.resetdist = deepcopy(self.dist)
            self.relative = [X_CENTER, Y_CENTER]


    def moveRectangle(self, length, width, incline = 0):
        thetaD = incline
        self.rect = [feettoPixels(width), feettoPixels(length), feettoPixels(width), feettoPixels(length), incline]
        self.speedx, self.speedy = self.processing(self.vd, thetaD)
        self.inclineAngle = thetaD
        self.move_activeRect()

####################### CIRCLE ###############################################

    def move_activeCircle(self):
        if self.active:
            self.vehicle_updateCircle()
            canvas.after(100, self.move_activeCircle) # time in terms of miliseconds

    def activateCircle(self):
        self.move_activeCircle()

    def vehicle_updateCircle(self):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        canvas.move(self.shape, delta_x , delta_y)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[4])/2, (pos[1] + pos[5])/2]

        self.cicumference += np.linalg.norm(np.array(self.ref_point) - np.array(self.relative))
        cicum = 2 * PI * self.circle[0]


        if self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_polygon(VERTICES, fill=color)
        elif self.cicumference >= cicum:
            self.active = False
        else:
            thetaD = self.inclineAngle - (10.0 * PI / 180.0)
            self.speedx, self.speedy = self.processing(self.vd, thetaD)
            self.inclineAngle = deepcopy(thetaD)
            self.relative = [self.ref_point[0], self.ref_point[1]]


    def moveCircle(self, radi, incline = 0):
        thetaD = (85.0 * PI)/180.0 + incline
        self.circle = [radi, incline]
        self.speedx, self.speedy = self.processing(self.vd, thetaD)
        self.inclineAngle = thetaD
        self.move_activeCircle()

######################### FIGURE 8 ##########################################


    def move_activeFigure(self):
        if self.active:
            self.vehicle_updateFigure()
            canvas.after(100, self.move_activeFigure) # time in terms of miliseconds

    def vehicle_updateFigure(self):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        canvas.move(self.shape, delta_x , delta_y)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[4])/2, (pos[1] + pos[5])/2]

        self.cicumference += np.linalg.norm(np.array(self.ref_point) - np.array(self.relative))
        cicum = 2 * PI * self.figure[self.figIndex]

        if self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_polygon(VERTICES, fill=color)
        elif self.cicumference >= cicum - 5:
            #swap between top of bottom
            self.figIndex = 1 if self.figIndex == 0 else 0
            self.totalDist += 1
            self.vd = self.figure[self.figIndex] * (PI * 10.0 / 180.0)
            self.cicumference = 0
            self.speedx, self.speedy = self.processing(self.vd, self.inclineAngle)
            self.relative = [self.ref_point[0], self.ref_point[1]]
            self.degRotation *= -1
            if self.totalDist == 2:
                self.active = False
            return



        thetaD = self.inclineAngle - self.degRotation
        self.speedx, self.speedy = self.processing(self.vd, thetaD)
        self.relative = [self.ref_point[0], self.ref_point[1]]
        self.inclineAngle = deepcopy(thetaD)



    def moveFigure(self, topradi, bottomradi, topIncline = 0):
        thetaD = (85.0 * PI)/180.0 + topIncline
        self.figure = [topradi, bottomradi, topIncline]
        self.dist[0] = topradi
        self.dist[1] = bottomradi
        self.speedx, self.speedy = self.processing(self.vd, thetaD)
        self.inclineAngle = thetaD
        self.move_activeFigure()

############ POINT EXECUTION ##########################################
    def move_activePoint(self):
        if self.active:
            self.vehicle_updatePoints()
            canvas.after(10, self.move_activePoint)

    def vehicle_updatePoints(self):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        canvas.move(self.shape, delta_x , delta_y)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[4])/2, (pos[1] + pos[5])/2]

        # how much the vehicle has traveled in the x and y direction
        normx = self.resetdist[0] + math.fabs(self.ref_point[0] - self.relative[0])
        normy = self.resetdist[1] + math.fabs(self.ref_point[1] - self.relative[1])


        if self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            self.relative = [X_CENTER, Y_CENTER]
            canvas.delete(self.shape)
            self.shape = canvas.create_polygon(VERTICES, fill=color)
            self.resetdist = deepcopy([normx, normy])


        if normx >= self.dist[0] and normy >= self.dist[1]:

            self.totalDist += 1
            if self.totalDist == len(self.waypoints):
                self.active = False
                return
            self.relative = deepcopy(self.ref_point)
            self.helpStart(self.waypoints[self.totalDist][0], self.waypoints[self.totalDist][1])



    def helpStart(self, x, y):
        self.resetdist = [0, 0]
        rel_x = (feettoPixels(float(x)) + X_CENTER) - self.relative[0]
        rel_y = (-feettoPixels(float(y)) + Y_CENTER) - self.relative[1]

        self.dist[0] = math.fabs(rel_x)
        self.dist[1] = math.fabs(rel_y)

        if rel_x == 0 and rel_y <= 0:
            thetaD = 3*PI/2.
        elif rel_x == 0 and rel_y > 0:
            thetaD = PI/ 2.
        elif rel_y == 0 and rel_x < 0:
            thetaD = PI
        elif rel_y == 0 and rel_x > 0:
            thetaD = 0
        else:
            thetaD = np.arctan(rel_y / rel_x)
            if (rel_x < 0 and rel_y < 0) or (rel_x < 0 and rel_y > 0):
                thetaD += np.pi

        self.speedx = self.vd * np.cos(thetaD)
        self.speedy = self.vd * np.sin(thetaD)

    def movePoints(self, points):
        x = points[0][0]
        y = points[0][1]
        self.totalDist = 0
        self.waypoints = deepcopy(points)
        self.helpStart(x, y)
        self.move_activePoint()

################## WayPoints ############################

    def moveWayPoint(self,iter, index = 0):

        if not self.active and index < len(iter):
            point = iter[index]
            self.active = True
            self.movePoints(point[0],point[1])

            index += 1
        canvas.after(50, self.moveWayPoint, iter, index)



################### Infinite Rotate #####################

    def rotate(self, points, angle, center):
        # angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = center
        new_points = []

        for index in range(0, len(points), 2):
            points[index] -= cx
            points[index + 1] -= cy
            x_new = points[index] * cos_val - points[index + 1] * sin_val
            y_new = points[index] * sin_val + points[index + 1] * cos_val
            new_points.append(x_new + cx)
            new_points.append(y_new + cy)
        return new_points

    def adjustHeadingAngle(self, theta):

        self.headingAngle = theta
        self.wheelRotation = self.wheelRotationalVelocity(self.speedx, self.speedy, self.headingAngle)
        pos = canvas.coords(self.shape)
        self.ref_point = [(pos[0] + pos[4])/2, (pos[1] + pos[5])/2]
        new_points = self.rotate(pos, self.headingAngle, self.ref_point)
        canvas.coords(self.shape, *new_points)

    def move_active(self, theta, omega):
        if self.active:
            self.vehicle_update(theta, omega)
            canvas.after(100, self.move_active, theta, omega) # time in terms of miliseconds

    def vehicle_update(self, theta, omega):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        canvas.move(self.shape, delta_x , delta_y)
        self.adjustHeadingAngle(omega/10)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[4])/2, (pos[1] + pos[5])/2]

        if self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_polygon(VERTICES, fill=color)
        else:
            thetaD = theta - (self.headingAngle + omega/10)
            self.speedx, self.speedy = self.processing(self.vd, thetaD)
            self.headingAngle +=  omega/10


    def moveInfinite(self, theta, omega, speed):
        thetanew = theta - (self.headingAngle + omega)
        self.vd = speed
        self.speedx, self.speedy = self.processing(self.vd, thetanew)
        self.headingAngle += omega/10
        self.move_active(theta, omega)

####### GIVEN WHEEL ROTATIONS ###############

    def move_wheels(self):
        if self.active:
            self.rotateWheels()
            canvas.after(100, self.move_wheels)

    def rotateWheels(self):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        canvas.move(self.shape, delta_x , delta_y)
        self.adjustHeadingAngle(self.headingAngle)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[4])/2, (pos[1] + pos[5])/2]
        if self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_polygon(VERTICES, fill=color)

    def setWheels(self, wheel1, wheel2, wheel3, wheel4):
        velocity = self.kinematic(wheel1, wheel2, wheel3, wheel4)
        self.wheelRotation = [wheel1, wheel2, wheel3, wheel4]

        self.speedx = -velocity[0]
        self.speedy = -velocity[1]
        self.headingAngle = velocity[2]
        self.move_wheels()


def stopCallback(event):
    if robot.getMode() == 'infinite':
        robot.setActive(False)

root = Tk()             # blank window
root.config(background = "White")

rightFrame = Frame(root, width=2000, height=1000, pady=100)
rightFrame.grid(row=0, column=1, columnspan=2)

root.bind('<Button>', stopCallback)
root.bind('<Return>', stopCallback)

leftFrame = Frame(root, width=300, height=800)
leftFrame.grid(row=0, column=0)


#Right Frame with animation of car moving

canvas = Canvas(rightFrame, width=380, height=740)
canvas.config(background="grey")
canvas.grid(row=0, column=0, padx=100)
color = 'blue'

canvas.create_line(x1, HEIGHT, x2, HEIGHT, arrow=LAST)

# draw horizontal lines

for k in range(NORM, HEIGHT, 12):
    y1 = k
    y2 = k
    canvas.create_line(x1, y1, x2, y2)

# draw vertical lines
y1 = NORM
y2 = HEIGHT
canvas.create_line(NORM, y1, NORM, y2, arrow=FIRST)
for k in range(NORM + 12, WIDTH + NORM, 12):
    x1 = k
    x2 = k
    canvas.create_line(x1, y1, x2, y2)

# Left frame with controls and inputs

robot = Vehicle(False)

#CATEGORIES
#Circle

circle = Text(leftFrame, width=50, height=1, takefocus=0)
circle.grid(row=0, column=0)
circle.insert(5.5, "CIRCLE")

radi = Text(leftFrame, width=50, height=1, takefocus=0)
radi.grid(row=1, column=0)
radi.insert(5.5, "Radi (ft): ")
radiInp = Entry(leftFrame, width=10)
radiInp.grid(row=1, column=1)

inclin = Text(leftFrame, width=50, height=1, takefocus=0)
inclin.grid(row=2, column=0)
inclin.insert(5.5, "inclination, thetap (radians): ")
inclinInp = Entry(leftFrame, width=10)
inclinInp.grid(row=2, column=1)

def circleCallback():
    radiAns = float(radiInp.get()) if radiInp.get() != '' else 0.0
    inclinAns = inclinInp.get() if inclinInp.get() != '' else 0.0

    radi = feettoPixels(radiAns)

    incline = np.radians(float(inclinAns))         # TODO: remove this before submitting

    robot.setRelative()
    robot.setVD(radi * (PI * 10.0 / 180.0))
    robot.setMode('circle')

    robot.setActive(True)
    robot.moveCircle(radi, incline)

circleSubmit = Button(leftFrame, text="submit", width=10, command=circleCallback)
circleSubmit.grid(row=3, column = 1)

#Rectangle

rectangle = Text(leftFrame, width=50, height=1, takefocus=0)
rectangle.grid(row=5, column=0)
rectangle.insert(5.5, "RECTANGLE")

length = Text(leftFrame, width=50, height=1, takefocus=0)
length.grid(row=6, column=0)
length.insert(5.5, "Length of rectangle (ft): ")
lengthInp = Entry(leftFrame, width=10)
lengthInp.grid(row=6, column=1)

width = Text(leftFrame, width=50, height=1, takefocus=0)
width.grid(row=7, column=0)
width.insert(5.5, "Width of rectangle (ft): ")
widthInp = Entry(leftFrame, width=10)
widthInp.grid(row=7, column=1)

inclinRec = Text(leftFrame, width=50, height=1, takefocus=0)
inclinRec.grid(row=8, column=0)
inclinRec.insert(5.5, "inclination, thetap (radians):")
inclinInpRec = Entry(leftFrame, width=10)
inclinInpRec.grid(row=8, column=1)

def rectangleCallback():
    lengthAns = lengthInp.get()
    widthAns = widthInp.get()
    thetaAns = inclinInpRec.get() if inclinInpRec.get() != '' else 0

    theta = np.radians(float(thetaAns))         # TODO: remove this before submitting

    robot.setRelative()
    robot.setMode('rectangle')
    robot.setActive(True)
    robot.moveRectangle(lengthAns, widthAns, theta)


rectangleSubmit = Button(leftFrame, text="submit", width=10, command=rectangleCallback)
rectangleSubmit.grid(row=9, column = 1)

#Figure 8
fig = Text(leftFrame, width=50, height=1, takefocus=0)
fig.grid(row=10, column=0)
fig.insert(5.5, "FIGURE 8")

radiTop = Text(leftFrame, width=50, height=1, takefocus=0)
radiTop.grid(row=11, column=0)
radiTop.insert(5.5, "Top Radi of Figure 8 (ft): ")
radiTopInp = Entry(leftFrame, width=10)
radiTopInp.grid(row=11, column=1)

radiBot = Text(leftFrame, width=50, height=1, takefocus=0)
radiBot.grid(row=12, column=0)
radiBot.insert(5.5, "Bottom Radi of Figure 8 (ft): ")
radiBotInp = Entry(leftFrame, width=10)
radiBotInp.grid(row=12, column=1)

inclinTop = Text(leftFrame, width=50, height=1, takefocus=0)
inclinTop.grid(row=13, column=0)
inclinTop.insert(5.5, "Top inclination, thetap (radians):")
inclinTopInp = Entry(leftFrame, width=10)
inclinTopInp.grid(row=13, column=1)


def figureCallback():
    radiTopAns = radiTopInp.get()
    radiBotAns = radiBotInp.get()
    inclinTopAns = inclinTopInp.get() if inclinTopInp.get() != '' else 0

    topRadi = feettoPixels(radiTopAns)
    bottomRadi = feettoPixels(radiBotAns)

    inclineTop= np.radians(float(inclinTopAns))         # TODO: remove this before submitting

    robot.setRelative()
    robot.setMode('figure 8')
    robot.setVD(topRadi * (PI * 10.0 / 180.0))

    robot.setActive(True)
    robot.moveFigure(topRadi, bottomRadi, inclineTop)


figSubmit = Button(leftFrame, text="submit", width=10, command=figureCallback)
figSubmit.grid(row=15, column = 1, sticky = W)


#Execution Paths

endPoints = Text(leftFrame, width=20, height=1, takefocus=0)
endPoints.grid(row=16, column=0, sticky=W)
endPoints.insert(5.5, "Point Execution:")

x_f = Text(leftFrame, width=50, height=1, takefocus=0)
x_f.grid(row=17, column=0, sticky=W)
x_f.insert(5.5, "Xf: ")
x_fInp = Entry(leftFrame, width=10)
x_fInp.grid(row=17, column=1)

y_f = Text(leftFrame, width=50, height=1, takefocus=0)
y_f.grid(row=18, column=0)
y_f.insert(5.5, "Yf: ")
y_fInp = Entry(leftFrame, width=10)
y_fInp.grid(row=18, column=1)

way1 = Text(leftFrame, width=50, height=1, takefocus=0)
way1.grid(row=19, column=0)
way1.insert(5.5, "WayPoint1 X & Y: ")
way1Inpx = Entry(leftFrame, width=10)
way1Inpx.grid(row=19, column=1)
way1Inpy = Entry(leftFrame, width=10)
way1Inpy.grid(row=19, column=2)

way2 = Text(leftFrame, width=50, height=1, takefocus=0)
way2.grid(row=20, column=0)
way2.insert(5.5, "WayPoint2 X & Y: ")
way2Inpx = Entry(leftFrame, width=10)
way2Inpx.grid(row=20, column=1)
way2Inpy = Entry(leftFrame, width=10)
way2Inpy.grid(row=20, column=2)

way3 = Text(leftFrame, width=50, height=1, takefocus=0)
way3.grid(row=21, column=0)
way3.insert(5.5, "WayPoint3 X & Y: ")
way3Inpx = Entry(leftFrame, width=10)
way3Inpx.grid(row=21, column=1)
way3Inpy = Entry(leftFrame, width=10)
way3Inpy.grid(row=21, column=2)

way4 = Text(leftFrame, width=50, height=1, takefocus=0)
way4.grid(row=22, column=0)
way4.insert(5.5, "WayPoint4 X & Y: ")
way4Inpx = Entry(leftFrame, width=10)
way4Inpx.grid(row=22, column=1)
way4Inpy = Entry(leftFrame, width=10)
way4Inpy.grid(row=22, column=2)


def pointCallback():
    x_fAns = float(x_fInp.get()) if x_fInp.get() != '' else 0
    y_fAns = float(y_fInp.get()) if y_fInp.get() != '' else 0

    result = []
    if way1Inpx.get() != '' and way1Inpy.get() != ''\
            and way2Inpy.get() != '' and way2Inpx.get() != ''\
            and way3Inpx.get() != '' and way3Inpy.get() != '':
        way1_x = float(way1Inpx.get())
        way1_y = float(way1Inpy.get())
        way2_x = float(way2Inpx.get())
        way2_y = float(way2Inpy.get())
        way3_x = float(way3Inpx.get())
        way3_y = float(way3Inpy.get())
        if  way4Inpx.get() == '' or way4Inpy.get() == '':
            result = [[way1_x, way1_y], [way2_x, way2_y], [way3_x, way3_y], [x_fAns, y_fAns]]
        else:
            way4_x = float(way4Inpx.get())
            way4_y = float(way4Inpy.get())
            result = [[way1_x, way1_y], [way2_x, way2_y], [way3_x, way3_y], [way4_x, way4_y], [x_fAns, y_fAns]]

    else:
        result.append([x_fAns, y_fAns])

    robot.setRelative()
    robot.setMode('Point')
    robot.setActive(True)
    robot.movePoints(result)



pointSubmit = Button(leftFrame, text="submit", width=10, command=pointCallback)
pointSubmit.grid(row=23, column = 1, sticky = W)


#Manual Inputs
wheelRotation = Text(leftFrame, width=50, height=1, takefocus=0)
wheelRotation.grid(row=24, column=0)
wheelRotation.insert(5.5, "Wheels Rotation")

wheel1 = Text(leftFrame, width=50, height=1, takefocus=0)
wheel1.grid(row=25, column=0)
wheel1.insert(5.5, "Top Left Wheel Rotational Rate (ft/sec): ")
wheel1Inp = Entry(leftFrame, width=10)
wheel1Inp.grid(row=25, column=1)

wheel2 = Text(leftFrame, width=50, height=1, takefocus=0)
wheel2.grid(row=26, column=0)
wheel2.insert(5.5, "Top Right Wheel Rotational Rate (ft/sec): ")
wheel2Inp = Entry(leftFrame, width=10)
wheel2Inp.grid(row=26, column=1)

wheel3 = Text(leftFrame, width=50, height=1, takefocus=0)
wheel3.grid(row=27, column=0)
wheel3.insert(5.5, "Bottom Left Wheel Rotational Rate (ft/sec): ")
wheel3Inp = Entry(leftFrame, width=10)
wheel3Inp.grid(row=27, column=1)

wheel4 = Text(leftFrame, width=50, height=1, takefocus=0)
wheel4.grid(row=28, column=0)
wheel4.insert(5.5, "Bottom Right Wheel Rotational Rate (ft/sec): ")
wheel4Inp = Entry(leftFrame, width=10)
wheel4Inp.grid(row=28, column=1)

thetaP = Text(leftFrame, width=50, height=1, takefocus=0)
thetaP.grid(row=29, column=0)
thetaP.insert(5.5, "Direction (thetaP in radians): ")
thetaPInp = Entry(leftFrame, width=10)
thetaPInp.grid(row=29, column=1)

speed = Text(leftFrame, width=50, height=1, takefocus=0)
speed.grid(row=30, column=0)
speed.insert(5.5, "Velocity of vehicle (ft/sec & max:15ft/sec): ")
speedInp = Entry(leftFrame, width=10)
speedInp.grid(row=30, column=1)

rotationalrate = Text(leftFrame, width=50, height=1, takefocus=0)
rotationalrate.grid(row=31, column=0)
rotationalrate.insert(5.5, "Rotational Rate of vehicle (rad/sec): ")
rotationalrateInp = Entry(leftFrame, width=10)
rotationalrateInp.grid(row=31, column=1)



def wheelCallback():
    wheel1Ans = int(wheel1Inp.get()) if wheel1Inp.get() != '' else 0.0
    wheel2Ans = int(wheel2Inp.get()) if wheel2Inp.get() != '' else 0.0
    wheel3Ans = int(wheel3Inp.get()) if wheel3Inp.get() != '' else 0.0
    wheel4Ans = int(wheel4Inp.get()) if wheel4Inp.get() != '' else 0.0
    thetaPAns = thetaPInp.get() if thetaPInp.get() != '' else 0.0
    speedAns =  int(speedInp.get())  if speedInp.get() != '' else 0.0
    rotationalAns = rotationalrateInp.get() if rotationalrateInp != '' else 0.0

    # thetaPRads= np.radians(float(thetaPAns))         # TODO: remove this before submitting
    # rotateRads = np.radians(float(rotationalAns))

    # velocity = robot.kinematic()


    robot.setActive(True)
    robot.setWheels(wheel1Ans, wheel2Ans, wheel3Ans, wheel4Ans)
    robot.setMode('infinite')
    # robot.moveInfinite(thetaPRads, rotateRads, speedAns)


wheelSubmit = Button(leftFrame, text="submit", width=10, command=wheelCallback)
wheelSubmit.grid(row=32, column = 1, sticky = W)


time = Text(leftFrame, width=50, height=1, takefocus=0)
time.grid(row=33, column=0)
time.insert(5.5, "Time taken from Start to End Points ")
timeEnt = Entry(leftFrame, width=10)
timeEnt.grid(row=33, column=1)

def timeCallback():
    timeAns = timeEnt.get()

    # if

reset = Button(leftFrame, text="submit", width=10, command=timeCallback)
reset.grid(row=34, column = 1)

def resetCallback():
    robot.reset()

reset = Button(leftFrame, text="RESET", width=10, command=resetCallback)
reset.grid(row=35, column = 2)

#Output Values


positionx = Text(leftFrame, width=30, height=1, takefocus=0, bg="black", fg="white")
positionx.grid(row=10, column=3)
positionx.insert(5.5, "Vehicle Position X")
positionLabelx = Label(leftFrame)
positionLabelx.grid(row=10, column=4, columnspan=2, padx=10)
ref_point = robot.getRefPoint()
def getLabelX():
    value = round((robot.getRefPoint()[0] - X_CENTER) / 24., 2)
    positionLabelx.config(text=value)
    positionLabelx.after(100, getLabelX)
getLabelX()

positiony = Text(leftFrame, width=30, height=1, takefocus=0, bg="black", fg="white")
positiony.grid(row=11, column=3)
positiony.insert(5.5, "Vehicle Position Y")
positionLabely = Label(leftFrame)
positionLabely.grid(row=11, column=4, padx=10)
def getLabelY():
    value = round((Y_CENTER - robot.getRefPoint()[1])/ 24., 2)
    positionLabely.config(text=value)
    positionLabely.after(100, getLabelY)
getLabelY()
# #
wheel1 = Text(leftFrame, width=30, height=1, takefocus=0, bg="black", fg="white")
wheel1.grid(row=12, column=3)
wheel1.insert(5.5, "Top left Wheel Rotation Rate")
wheel1Label = Label(leftFrame)
wheel1Label.grid(row=12, column=4)
def getWheel1():
    value = round(robot.getWheelRotation()[0],2)
    wheel1Label.config(text=value)
    wheel1Label.after(100, getWheel1)
getWheel1()


wheel2 = Text(leftFrame, width=30, height=1, takefocus=0, bg="black", fg="white")
wheel2.grid(row=13, column=3)
wheel2.insert(5.5, "Top Right Wheel Rotation Rate")
wheel2Label = Label(leftFrame)
wheel2Label.grid(row=13, column=4)
def getWheel2():
    value = round(robot.getWheelRotation()[1],2)
    wheel2Label.config(text=value)
    wheel2Label.after(100, getWheel2)
getWheel2()

wheel3 = Text(leftFrame, width=30, height=1, takefocus=0, bg="black", fg="white")
wheel3.grid(row=14, column=3)
wheel3.insert(5.5, "Bottom Left Wheel Rotation Rate")
wheel3Label = Label(leftFrame)
wheel3Label.grid(row=14, column=4)
def getWheel3():
    value = round(robot.getWheelRotation()[2],2)
    wheel3Label.config(text=value)
    wheel3Label.after(100, getWheel3)
getWheel3()

wheel4 = Text(leftFrame, width=30, height=1, takefocus=0, bg="black", fg="white")
wheel4.grid(row=15, column=3)
wheel4.insert(5.5, "Bottom Right Wheel Rotation Rate")
wheel4Label = Label(leftFrame)
wheel4Label.grid(row=15, column=4)
def getWheel4():
    value = round(robot.getWheelRotation()[3],2)
    wheel4Label.config(text=value)
    wheel4Label.after(100, getWheel4)
getWheel4()

velocity_x = Text(leftFrame, width=30, height=1, takefocus=0, bg="black", fg="white")
velocity_x.grid(row=16, column=3)
velocity_x.insert(5.5, "Vehicle Velocity X")
velocity_xLabel = Label(leftFrame, text=velocity[0])
velocity_xLabel.grid(row=16, column=4)
def getSpeedX():
    value = round((robot.getVelocity()[0]), 2)
    velocity_xLabel.config(text=value)
    velocity_xLabel.after(100, getSpeedX)
getSpeedX()

velocity_y = Text(leftFrame, width=30, height=1, takefocus=0, bg="black", fg="white")
velocity_y.grid(row=17, column=3)
velocity_y.insert(5.5, "Vehicle Velocity Y")
velocity_yLabel = Label(leftFrame, text=velocity[1])
velocity_yLabel.grid(row=17, column=4)
def getSpeedY():
    value = round((robot.getVelocity()[1]), 2)
    velocity_yLabel.config(text=value)
    velocity_yLabel.after(100, getSpeedY)
getSpeedY()


root.mainloop()
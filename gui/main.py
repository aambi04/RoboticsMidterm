from Tkinter import *
from robots import *
import math
from copy import *
import tkMessageBox

# constants
PI = math.pi

#helper functions

def feettoPixels(feet):
    return 24 * int(feet)


position = [3,3]
wheelRotation = [0,1,2,3]
velocity=[-1,-3]

root = Tk()             # blank window
root.config(background = "White")

rightFrame = Frame(root, width=1000, height=1000, bg="black")
rightFrame.grid(row=0, column=1)
leftFrame = Frame(root, width=300, height=800)
leftFrame.grid(row=0, column=0)


#Right Frame with animation of car moving

canvas = Canvas(rightFrame, width=380, height=740)
canvas.config(background="grey")
canvas.pack()
color = 'blue'

# draw horizontal lines

NORM = 12
WIDTH = 360 + NORM
HEIGHT = 720 + NORM
THREEFEET = 72  + NORM  # 3ft to pixels conversion
X_CENTER = WIDTH/2      # starting point for robot
Y_CENTER = HEIGHT/2     # starting point for robot
x1 = NORM
x2 = WIDTH
omega = 0
for k in range(NORM, HEIGHT + NORM, 12):
    y1 = k
    y2 = k
    canvas.create_line(x1, y1, x2, y2)

# draw vertical lines
y1 = NORM
y2 = HEIGHT
for k in range(NORM, WIDTH + NORM, 12):
    x1 = k
    x2 = k
    canvas.create_line(x1, y1, x2, y2)


class Vehicle:
    def __init__(self, active):
        self.shape = canvas.create_rectangle(WIDTH/2 - 26, HEIGHT/2 + 52, WIDTH/2 + 26, HEIGHT/2 - 52, fill=color)       # robot is 4.33 ft long, 2.17 ft wide
        self.speedx = 1
        self.speedy = 1
        self.headingAngle = 0  # heading angle
        self.ref_point = [WIDTH + 26, HEIGHT + 52]
        self.active = active
        self.dist = [0, 0]
        self.relative = [X_CENTER, Y_CENTER]
        self.vd = 2
        self.rect = [0,0,0]         # length, width, inclincation theta
        self.circle = [0,0]
        self.figure = [0,0,0,0]
        self.resetdist = [0, 0]
        self.cicumference = 0
        self.figIndex = 0
        self.degRotation = 10.0 * PI/180.0


##################### HELPER FUNCTIONS #####################################

    def setActive(self, active):
        self.active = active

    def setVD(self, vd):
        self.vd = vd

    def getRefPoint(self):
        return self.ref_point

    def reset(self):
        canvas.delete(self.shape)
        self.active = False
        self.shape = canvas.create_rectangle(WIDTH/2 - 26, HEIGHT/2 + 52, WIDTH/2 + 26, HEIGHT/2 - 52, fill=color)       # robot is 4.33 ft long, 2.17 ft wide
        self.speedx = 1
        self.speedy = 1
        self.headingAngle = 0  # heading angle
        self.ref_point = [WIDTH + 26, HEIGHT + 52]
        self.dist = [0, 0]
        self.relative = [X_CENTER, Y_CENTER]
        self.vd = 2
        self.rect = [0,0,0]         # length, width, inclination theta
        self.circle = [0,0]
        self.figure = [0,0,0,0]
        self.resetdist = [0, 0]
        self.cicumference = 0
        self.figIndex = 0

############################# RECTANGLE ########################################


    def activateRect(self, active):
        self.active = active
        self.move_activeRect()

    def move_activeRect(self):
        if self.active:
            self.vehicle_updateRectangle()
            canvas.after(10, self.move_activeRect) # time in terms of miliseconds

    def vehicle_updateRectangle(self):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        # print "speedx", delta_x, delta_y
        canvas.move(self.shape, delta_x , delta_y)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[2])/2, (pos[1] + pos[3])/2]

        # print "ref point", self.ref_point[0], self.ref_point[1]
        # print "relative", self.relative[0], self.relative[1]
        # print "self.resetdist", self.resetdist[0], self.resetdist[1]

        # how much the vehicle has traveled in the x and y direction
        self.dist[0] = self.resetdist[0] + math.fabs(self.ref_point[0] - self.relative[0])
        self.dist[1] = self.resetdist[1] + math.fabs(self.ref_point[1] - self.relative[1])
        length = self.rect[1]
        width = self.rect[0]
        #
        print width, length
        # print "dist", self.dist[0], self.dist[1]
        # print "rect, ", self.rect
        sin_angle = math.fabs(round(np.sin(math.fabs(self.headingAngle - self.rect[2])), 2))
        # print "angle", sin_angle
        if (self.dist[1] >= length and sin_angle == 1) or (self.dist[0] >= width and sin_angle == 0):
            thetaD = self.headingAngle - (PI/2.0)          # move along the x axis
            self.speedx, self.speedy = processing(self.vd, thetaD)
            self.relative = [self.ref_point[0], self.ref_point[1]]
            self.dist = [0,0]
            self.resetdist = [0,0]
            self.headingAngle = deepcopy(thetaD)
            # print "CHANGE"
            # print self.speedx, self.speedy
            # print self.relative[0], self.relative[1]
        elif self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_rectangle(WIDTH/2 - 26, HEIGHT/2 + 52, WIDTH/2 + 26, HEIGHT/2 - 52, fill=color)
            self.resetdist = deepcopy(self.dist)
            self.relative = [X_CENTER, Y_CENTER]
            # print "RESTART"

    def moveRectangle(self, length, width, incline = 0):
        thetaD = (PI/2.0) + incline
        self.rect = [feettoPixels(width), feettoPixels(length), incline]
        self.speedx, self.speedy = processing(self.vd, thetaD)
        self.headingAngle = thetaD
        self.activateRect(self.active)

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
        print "speedx", delta_x, delta_y
        canvas.move(self.shape, delta_x , delta_y)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[2])/2, (pos[1] + pos[3])/2]

        print "ref point", self.ref_point[0], self.ref_point[1]
        if self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_rectangle(WIDTH/2 - 26, HEIGHT/2 + 52, WIDTH/2 + 26, HEIGHT/2 - 52, fill=color)
            print "RESTART"
        else:
            thetaD = self.headingAngle - (10.0 * PI/180.0)
            print "thetaD", thetaD
            self.speedx, self.speedy = processing(self.vd, thetaD)
            self.headingAngle = deepcopy(thetaD)
            print "CHANGE CIRCLE"


    def moveCircle(self, radi, incline = 0):
        thetaD = (85.0 * PI)/180.0 + incline
        self.circle = [radi, incline]
        self.speedx, self.speedy = processing(self.vd, thetaD)
        self.headingAngle = thetaD
        self.activateCircle()

######################### FIGURE 8 ##########################################


    def move_activeFigure(self):
        if self.active:
            self.vehicle_updateFigure()
            canvas.after(100, self.move_activeFigure) # time in terms of miliseconds

    def vehicle_updateFigure(self):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        print "speedx", delta_x, delta_y
        canvas.move(self.shape, delta_x , delta_y)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[2])/2, (pos[1] + pos[3])/2]

        self.cicumference += np.linalg.norm(np.array(self.ref_point) - np.array(self.relative))
        cicum = 2 * PI * self.figure[self.figIndex]

        if self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_rectangle(WIDTH/2 - 26, HEIGHT/2 + 52, WIDTH/2 + 26, HEIGHT/2 - 52, fill=color)
            print "RESTART figure"
        elif self.cicumference >= cicum - 5:
            #swap between top of bottom
            self.figIndex = 1 if self.figIndex == 0 else 0

            self.vd = self.figure[self.figIndex] * (PI * 10.0 / 180.0)
            print"self.vd", self.vd
            self.cicumference = 0
            thetaD = (self.headingAngle + self.figure[self.figIndex + 2])    #+ self.figure[self.figIndex + 2]
            print thetaD
            self.speedx, self.speedy = processing(self.vd, thetaD)
            self.relative = [self.ref_point[0], self.ref_point[1]]
            self.headingAngle = deepcopy(thetaD)
            self.degRotation *= -1
            print "changing", self.speedx, self.speedy
            return


        thetaD = self.headingAngle - self.degRotation
        print "thetaD", thetaD
        self.speedx, self.speedy = processing(self.vd, thetaD)
        self.relative = [self.ref_point[0], self.ref_point[1]]
        self.headingAngle = deepcopy(thetaD)



    def moveFigure(self, topradi, bottomradi, topIncline = 0, bottomIncline = 0):
        thetaD = (85.0 * PI)/180.0 + topIncline
        self.figure = [topradi, bottomradi, topIncline, bottomIncline]
        self.dist[0] = topradi
        self.dist[1] = bottomradi
        self.speedx, self.speedy = processing(self.vd, thetaD)
        self.headingAngle = thetaD
        self.move_activeFigure()

############ POINT EXECUTION ##########################################
    def move_activePoint(self):
        if self.active:
            self.vehicle_updatePoints()
            canvas.after(10, self.move_activePoint)

    def vehicle_updatePoints(self):
        delta_x = int(round(self.speedx))
        delta_y = int(round(self.speedy))
        # print "speedx", delta_x, delta_y
        canvas.move(self.shape, delta_x , delta_y)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[2])/2, (pos[1] + pos[3])/2]

        # how much the vehicle has traveled in the x and y direction
        normx = self.resetdist[0] + math.fabs(self.ref_point[0] - self.relative[0])
        normy = self.resetdist[1] + math.fabs(self.ref_point[1] - self.relative[1])


        if normx >= self.dist[0] and normy >= self.dist[1]:
            self.active = False
        elif self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_rectangle(WIDTH/2 - 26, HEIGHT/2 + 52, WIDTH/2 + 26, HEIGHT/2 - 52, fill=color)
            self.resetdist = deepcopy([normx, normy])

    def movePoints(self, x, y):
        end_x = feettoPixels(float(math.fabs(x)))
        end_y = feettoPixels(float(math.fabs(y)))
        self.resetdist = [0,0]
        self.dist[0] = end_x
        self.dist[1] = end_y
        thetaD = np.arctan(float(y) / float(x))
        print "x and y ", x, y

        if (x < 0 and y < 0) or (x < 0 and y > 0):
            print "x and y ", x, y
            thetaD += np.pi
        self.speedx, self.speedy = processing(self.vd, thetaD)
        self.move_activePoint()


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
    radiAns = radiInp.get()
    inclinAns = inclinInp.get() if inclinInp.get() != '' else 0

    radi = feettoPixels(radiAns)

    incline = np.radians(float(inclinAns))         # TODO: remove this before submitting

    robot.setActive(True)
    robot.setVD(radi * (PI * 10.0 / 180.0))
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

inclinBot = Text(leftFrame, width=50, height=1, takefocus=0)
inclinBot.grid(row=14, column=0)
inclinBot.insert(5.5, "Bottom inclination, thetap (radians):")
inclinBotInp = Entry(leftFrame, width=10)
inclinBotInp.grid(row=14, column=1)

def figureCallback():
    radiTopAns = radiTopInp.get()
    radiBotAns = radiBotInp.get()
    inclinTopAns = inclinTopInp.get() if inclinTopInp.get() != '' else 0
    inclinBotAns = inclinBotInp.get() if inclinBotInp.get() != '' else 0

    topRadi = feettoPixels(radiTopAns)
    bottomRadi = feettoPixels(radiBotAns)

    inclineTop= np.radians(float(inclinTopAns))         # TODO: remove this before submitting
    inclineBottom = np.radians(float(inclinBotAns))

    robot.setActive(True)
    robot.setVD(topRadi * (PI * 10.0 / 180.0))
    robot.moveFigure(topRadi, bottomRadi, inclineTop, inclineBottom)


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


def pointCallback():
    x_fAns = float(x_fInp.get()) if x_fInp.get() != '' else 0
    y_fAns = float(y_fInp.get()) if y_fInp.get() != '' else 0


    robot.setActive(True)
    robot.movePoints(x_fAns, y_fAns)

pointSubmit = Button(leftFrame, text="submit", width=10, command=pointCallback)
pointSubmit.grid(row=19, column = 1, sticky = W)


#Manual Inputs
wheelRotation = Text(leftFrame, width=50, height=1, takefocus=0)
wheelRotation.grid(row=20, column=0)
wheelRotation.insert(5.5, "Wheels Rotation")

wheel1 = Text(leftFrame, width=50, height=1, takefocus=0)
wheel1.grid(row=21, column=0)
wheel1.insert(5.5, "Top Left Wheel Rotational Rate (ft/sec): ")
wheel1Inp = Entry(leftFrame, width=10)
wheel1Inp.grid(row=21, column=1)

wheel2 = Text(leftFrame, width=50, height=1, takefocus=0)
wheel2.grid(row=22, column=0)
wheel2.insert(5.5, "Top Right Wheel Rotational Rate (ft/sec): ")
wheel2Inp = Entry(leftFrame, width=10)
wheel2Inp.grid(row=22, column=1)

wheel3 = Text(leftFrame, width=50, height=1, takefocus=0)
wheel3.grid(row=23, column=0)
wheel3.insert(5.5, "Bottom Left Wheel Rotational Rate (ft/sec): ")
wheel3Inp = Entry(leftFrame, width=10)
wheel3Inp.grid(row=23, column=1)

wheel4 = Text(leftFrame, width=50, height=1, takefocus=0)
wheel4.grid(row=24, column=0)
wheel4.insert(5.5, "Bottom Right Wheel Rotational Rate (ft/sec): ")
wheel4Inp = Entry(leftFrame, width=10)
wheel4Inp.grid(row=24, column=1)

thetaP = Text(leftFrame, width=50, height=1, takefocus=0)
thetaP.grid(row=25, column=0)
thetaP.insert(5.5, "Direction (thetaP in radians): ")
thetaPInp = Entry(leftFrame, width=10)
thetaPInp.grid(row=25, column=1)

speed = Text(leftFrame, width=50, height=1, takefocus=0)
speed.grid(row=26, column=0)
speed.insert(5.5, "Velocity of vehicle (ft/sec & max:15ft/sec): ")
speedInp = Entry(leftFrame, width=10)
speedInp.grid(row=26, column=1)





def wheelCallback():
    wheel1Ans = wheel1Inp.get() if wheel1Inp.get() != '' else 0
    wheel2Ans = wheel2Inp.get() if wheel2Inp.get() != '' else 0
    wheel3Ans = wheel3Inp.get() if wheel3Inp.get() != '' else 0
    wheel4Ans = wheel4Inp.get() if wheel4Inp.get() != '' else 0
    thetaPAns = thetaPInp.get() if thetaPInp.get() != '' else 0
    speedAns  = speedInp.get()  if speedInp.get() != ''  else 0


    thetaPRads= np.radians(float(thetaPAns))         # TODO: remove this before submitting

    robot.setActive(True)
    robot.setVD(speedAns)


wheelSubmit = Button(leftFrame, text="submit", width=10, command=wheelCallback)
wheelSubmit.grid(row=27, column = 1, sticky = W)





def resetCallback():
    robot.reset()

reset = Button(leftFrame, text="RESET", width=10, command=resetCallback)
reset.grid(row=28, column = 2)
#
# #Output Values
#
#
# positionx = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
# positionx.grid(row=16, column=0)
# positionx.insert(5.5, "Vehicle Position X")
# positionLabelx = Label(leftFrame)
# positionLabelx.grid(row=16, column=1)
# ref_point = robot.getRefPoint()
# def getLabelX():
#     positionLabelx.config(text=robot.getRefPoint()[0])
#     positionLabelx.after(10, getLabelX)
# getLabelX()
#
# positiony = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
# positiony.grid(row=17, column=0)
# positiony.insert(5.5, "Vehicle Position Y")
# positionLabely = Label(leftFrame)
# positionLabely.grid(row=17, column=1)
# def getLabelY():
#     positionLabely.config(text=robot.getRefPoint()[1])
#     positionLabely.after(10, getLabelY)
# getLabelY()
#
# wheel1 = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
# wheel1.grid(row=19, column=0)
# wheel1.insert(5.5, "Top left Wheel Rotation Rate")
# wheel1Label = Label(leftFrame, text=wheelRotation[0])
# wheel1Label.grid(row=19, column=1)
#
# wheel2 = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
# wheel2.grid(row=20, column=0)
# wheel2.insert(5.5, "Top Right Wheel Rotation Rate")
# wheel2Label = Label(leftFrame, text=wheelRotation[1])
# wheel2Label.grid(row=20, column=1)
#
# wheel3 = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
# wheel3.grid(row=21, column=0)
# wheel3.insert(5.5, "Bottom Left Wheel Rotation Rate")
# wheel3Label = Label(leftFrame, text=wheelRotation[2])
# wheel3Label.grid(row=21, column=1)
#
# wheel4 = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
# wheel4.grid(row=22, column=0)
# wheel4.insert(5.5, "Bottom Right Wheel Rotation Rate")
# wheel4Label = Label(leftFrame, text=wheelRotation[3])
# wheel4Label.grid(row=22, column=1)
#
# velocity_x = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
# velocity_x.grid(row=24, column=0)
# velocity_x.insert(5.5, "Vehicle Velocity X")
# velocity_xLabel = Label(leftFrame, text=velocity[0])
# velocity_xLabel.grid(row=24, column=1)
#
# velocity_y = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
# velocity_y.grid(row=25, column=0)
# velocity_y.insert(5.5, "Vehicle Velocity Y")
# velocity_yLabel = Label(leftFrame, text=velocity[1])
# velocity_yLabel.grid(row=25, column=1)
#

root.mainloop()
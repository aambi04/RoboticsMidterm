from Tkinter import *
from robots import *
import math

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
count = 0
for k in range(NORM, HEIGHT + NORM, 12):
    y1 = k
    y2 = k
    canvas.create_line(x1, y1, x2, y2)
    count += 1
print "COUNT", count
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
        self.speedx = 1 # changed from 3 to 9
        self.speedy = 1 # changed from 3 to 9
        self.headingAngle = 0  # heading angle
        self.ref_point = [WIDTH + 26, HEIGHT + 52]
        self.active = active
        self.dist = [0, 0]
        self.relative = [X_CENTER, Y_CENTER]
        self.vd = 2
        self.rect = [0,0,0]         # length, width, height
        self.resetdist = [0, 0]

    def getRefPoint(self):
        return self.ref_point

    def activateRect(self, active):
        self.active = active
        self.move_activeRect()

    def reset(self):
        canvas.delete(self.shape)
        self.active = False
        self.shape = canvas.create_rectangle(WIDTH/2 - 26, HEIGHT/2 + 52, WIDTH/2 + 26, HEIGHT/2 - 52, fill=color)       # robot is 4.33 ft long, 2.17 ft wide
        self.speedx = 1 # changed from 3 to 9
        self.speedy = 1 # changed from 3 to 9
        self.headingAngle = 0  # heading angle
        self.ref_point = [WIDTH + 26, HEIGHT + 52]
        self.dist = [0, 0]
        self.relative = [X_CENTER, Y_CENTER]
        self.vd = 2
        self.rect = [0,0,0]         # length, width, height
        self.resetdist = [0, 0]

    def move_activeRect(self):
        if self.active:
            self.vehicle_updateRectangle()
            rightFrame.after(10, self.move_activeRect) # time in terms of miliseconds

    def vehicle_updateRectangle(self):
        print "speedx", self.speedx, self.speedy
        canvas.move(self.shape, self.speedx, self.speedy)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[2])/2, (pos[1] + pos[3])/2]

        print "ref point", self.ref_point[0], self.ref_point[1]
        print "relative", self.relative[0], self.relative[1]

        # how much the vehicle has traveled in the x and y direction
        self.dist[0] = self.resetdist[0] + math.fabs(self.ref_point[0] - self.relative[0])
        self.dist[1] = self.resetdist[1] + math.fabs(self.ref_point[1] - self.relative[1])
        length = self.rect[1]
        width = self.rect[0]
        #
        print width, length
        print "dist"
        print self.dist[0], self.dist[1]
        #top left conrner
        if (self.dist[1] >= length and self.dist[0] == 0) or (self.dist[1] == 0 and self.dist[0] >= width):
            thetaD = self.headingAngle - 90          # move along the x axis
            self.speedx, self.speedy = processing(self.vd, thetaD, 0)
            self.relative = [self.ref_point[0], self.ref_point[1]]
            self.dist = [0,0]
            self.resetdist = [0,0]
            self.headingAngle = thetaD
            print "CHANGE"
            print self.speedx, self.speedy
            print self.relative[0], self.relative[1]
        elif self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_rectangle(WIDTH/2 - 26, HEIGHT/2 + 52, WIDTH/2 + 26, HEIGHT/2 - 52, fill=color)
            self.resetdist = self.dist
            self.relative = [X_CENTER, Y_CENTER]


    #start forward so initial thetaD will equal 90 degrees

    def moveRectangle(self, length, width, inclin = 0):
        thetaD = 90
        theta_new = self.headingAngle
        self.rect = (feettoPixels(width), feettoPixels(length), inclin)
        self.speedx, self.speedy = processing(self.vd, thetaD, theta_new)
        self.headingAngle = thetaD
        print self.speedx, self.speedy
        self.activateRect(True)



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

#draw path of the circle and start the vehicle

def circleCallback():
    radiAns = radiInp.get()
    inclinAns = inclinInp.get()

    radi = feettoPixels(radiAns)

    print "radi,", radi

    x_0 = robot.getRefPoint()[0]
    y_0 = int(robot.getRefPoint()[1]) + radi

    x_1 = int(robot.getRefPoint()[0]) + (radi * 2)
    y_1 = int(robot.getRefPoint()[1]) - radi

    print x_0, y_0, x_1, y_1

    robot.activate(True)
    robot.circlePath(x_0, y_0, x_1, y_1)

    # rightFrame.update()


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
    thetaAns = inclinInp.get()

    robot.moveRectangle(lengthAns, widthAns, thetaAns)



rectangleSubmit = Button(leftFrame, text="submit", width=10, command=rectangleCallback)
rectangleSubmit.grid(row=9, column = 1)

#Figure 8
fig = Text(leftFrame, width=50, height=1, takefocus=0)
fig.grid(row=10, column=0)
fig.insert(5.5, "FIGURE 8")

radiTop = Text(leftFrame, width=50, height=1, takefocus=0)
radiTop.grid(row=11, column=0)
radiTop.insert(5.5, "Top Radi of Figure 8 ")
radiTopInp = Entry(leftFrame, width=10)
radiTopInp.grid(row=11, column=1)

radiBot = Text(leftFrame, width=50, height=1, takefocus=0)
radiBot.grid(row=12, column=0)
radiBot.insert(5.5, "Bottom Radi of Figure 8 (ft): ")
radiBotInp = Entry(leftFrame, width=10)
radiBotInp.grid(row=12, column=1)

inclinTop = Text(leftFrame, width=50, height=1, takefocus=0)
inclinTop.grid(row=13, column=0)
inclinTop.insert(5.5, "Top inclination, thetap (ft):")
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
    inclinTopAns = inclinTopInp.get()
    inclinBotAns = inclinBotInp.get()

rectangleSubmit = Button(leftFrame, text="submit", width=10, command=figureCallback)
rectangleSubmit.grid(row=15, column = 1, sticky = W)


def resetCallback():
    robot.reset()

reset = Button(leftFrame, text="RESET", width=10, command=resetCallback)
reset.grid(row=15, column = 2)

#Output Values


positionx = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
positionx.grid(row=16, column=0)
positionx.insert(5.5, "Vehicle Position X")
positionLabelx = Label(leftFrame)
positionLabelx.grid(row=16, column=1)
ref_point = robot.getRefPoint()
def getLabelX():
    positionLabelx.config(text=robot.getRefPoint()[0])
    positionLabelx.after(10, getLabelX)
getLabelX()

positiony = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
positiony.grid(row=17, column=0)
positiony.insert(5.5, "Vehicle Position Y")
positionLabely = Label(leftFrame)
positionLabely.grid(row=17, column=1)
def getLabelY():
    positionLabely.config(text=robot.getRefPoint()[1])
    positionLabely.after(10, getLabelY)
getLabelY()

wheel1 = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
wheel1.grid(row=19, column=0)
wheel1.insert(5.5, "Top left Wheel Rotation Rate")
wheel1Label = Label(leftFrame, text=wheelRotation[0])
wheel1Label.grid(row=19, column=1)

wheel2 = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
wheel2.grid(row=20, column=0)
wheel2.insert(5.5, "Top Right Wheel Rotation Rate")
wheel2Label = Label(leftFrame, text=wheelRotation[1])
wheel2Label.grid(row=20, column=1)

wheel3 = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
wheel3.grid(row=21, column=0)
wheel3.insert(5.5, "Bottom Left Wheel Rotation Rate")
wheel3Label = Label(leftFrame, text=wheelRotation[2])
wheel3Label.grid(row=21, column=1)

wheel4 = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
wheel4.grid(row=22, column=0)
wheel4.insert(5.5, "Bottom Right Wheel Rotation Rate")
wheel4Label = Label(leftFrame, text=wheelRotation[3])
wheel4Label.grid(row=22, column=1)

velocity_x = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
velocity_x.grid(row=24, column=0)
velocity_x.insert(5.5, "Vehicle Velocity X")
velocity_xLabel = Label(leftFrame, text=velocity[0])
velocity_xLabel.grid(row=24, column=1)

velocity_y = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
velocity_y.grid(row=25, column=0)
velocity_y.insert(5.5, "Vehicle Velocity Y")
velocity_yLabel = Label(leftFrame, text=velocity[1])
velocity_yLabel.grid(row=25, column=1)


root.mainloop()
from Tkinter import *
from robots import *

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
x1 = NORM
x2 = WIDTH
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
    def __init__(self):
        self.shape = canvas.create_rectangle(WIDTH/2, HEIGHT/2, WIDTH/2 + 52, HEIGHT/2 + 104, fill=color)       # robot is 4.33 ft long, 2.17 ft wide
        self.speedx = 1 # changed from 3 to 9
        self.speedy = 1 # changed from 3 to 9
        self.headingAngle = 0  # heading angle
        self.ref_point = [WIDTH + 26, HEIGHT + 52]
        self.active = True
        self.move_active()

    def getRefPoint(self):
        return self.ref_point


    def vehicle_update(self):
        canvas.move(self.shape, self.speedx, self.speedy)
        pos = canvas.coords(self.shape)                     #get the coordinates of the vehicle
        self.ref_point = [(pos[0] + pos[2])/2, (pos[1] + pos[3])/2]
        if self.ref_point[0] >= WIDTH - THREEFEET or self.ref_point[0] <= THREEFEET or self.ref_point[1] >= HEIGHT - THREEFEET or self.ref_point[1] <= THREEFEET:        # reset and put image in the center of the screen
            canvas.delete(self.shape)
            self.shape = canvas.create_rectangle(WIDTH/2, HEIGHT/2, WIDTH/2 + 52, HEIGHT/2 + 104, fill=color)

    def move_active(self):
        if self.active:
            self.vehicle_update()
            rightFrame.after(10, self.move_active) # time in terms of miliseconds
# Left frame with controls and inputs


ball = Vehicle()

#CATEGORIES
#Circle

circle = Text(leftFrame, width=50, height=1, takefocus=0)
circle.grid(row=0, column=0)
circle.insert(5.5, "CIRCLE")

radi = Text(leftFrame, width=50, height=1, takefocus=0)
radi.grid(row=1, column=0)
radi.insert(5.5, "Radi: ")
radiInp = Entry(leftFrame, width=10)
radiInp.grid(row=1, column=1)

inclin = Text(leftFrame, width=50, height=1, takefocus=0)
inclin.grid(row=2, column=0)
inclin.insert(5.5, "inclination, thetap")
inclinInp = Entry(leftFrame, width=10)
inclinInp.grid(row=2, column=1)

def circleCallback():
    radiAns = radiInp.get()
    inclinAns = inclinInp.get()

circleSubmit = Button(leftFrame, text="submit", width=10, command=circleCallback)
circleSubmit.grid(row=3, column = 1)

#Rectangle

rectangle = Text(leftFrame, width=50, height=1, takefocus=0)
rectangle.grid(row=5, column=0)
rectangle.insert(5.5, "RECTANGLE")

length = Text(leftFrame, width=50, height=1, takefocus=0)
length.grid(row=6, column=0)
length.insert(5.5, "Length of rectangle: ")
lengthInp = Entry(leftFrame, width=10)
lengthInp.grid(row=6, column=1)

width = Text(leftFrame, width=50, height=1, takefocus=0)
width.grid(row=7, column=0)
width.insert(5.5, "Width of rectangle: ")
widthInp = Entry(leftFrame, width=10)
widthInp.grid(row=7, column=1)

inclinRec = Text(leftFrame, width=50, height=1, takefocus=0)
inclinRec.grid(row=8, column=0)
inclinRec.insert(5.5, "inclination, thetap")
inclinInpRec = Entry(leftFrame, width=10)
inclinInpRec.grid(row=8, column=1)

def rectangleCallback():
    lengthAns = lengthInp.get()
    widthAns = widthInp.get()
    # processRectangle(lengthInp.get(), widthInp.get())

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
radiBot.insert(5.5, "Bottom Radi of Figure 8 ")
radiBotInp = Entry(leftFrame, width=10)
radiBotInp.grid(row=12, column=1)

inclinTop = Text(leftFrame, width=50, height=1, takefocus=0)
inclinTop.grid(row=13, column=0)
inclinTop.insert(5.5, "Top inclination, thetap")
inclinTopInp = Entry(leftFrame, width=10)
inclinTopInp.grid(row=13, column=1)

inclinBot = Text(leftFrame, width=50, height=1, takefocus=0)
inclinBot.grid(row=14, column=0)
inclinBot.insert(5.5, "Bottom inclination, thetap")
inclinBotInp = Entry(leftFrame, width=10)
inclinBotInp.grid(row=14, column=1)

def figureCallback():
    radiTopAns = radiTopInp.get()
    radiBotAns = radiBotInp.get()
    inclinTopAns = inclinTopInp.get()
    inclinBotAns = inclinBotInp.get()

rectangleSubmit = Button(leftFrame, text="submit", width=10, command=figureCallback)
rectangleSubmit.grid(row=15, column = 1)

#Output Values


positionx = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
positionx.grid(row=16, column=0)
positionx.insert(5.5, "Vehicle Position X")
positionLabelx = Label(leftFrame)
positionLabelx.grid(row=16, column=1)
ref_point = ball.getRefPoint()
def getLabelX():
    positionLabelx.config(text=ball.getRefPoint()[0])
    positionLabelx.after(1000, getLabelX)
getLabelX()

positiony = Text(leftFrame, width=50, height=1, takefocus=0, bg="black", fg="white")
positiony.grid(row=17, column=0)
positiony.insert(5.5, "Vehicle Position Y")
positionLabely = Label(leftFrame)
positionLabely.grid(row=17, column=1)
def getLabelY():
    positionLabely.config(text=ball.getRefPoint()[1])
    positionLabely.after(1000, getLabelY)
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
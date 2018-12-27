import sys
import pygame
import math

#Global variables
datafile = sys.argv[1]
steps = 0 #placeholder, it will be set up in checkUsage()
animated = True 

x_screen = 1500
y_screen = 1000

#Colors
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
gray = (120, 120, 120)
light_gray = (220, 220, 220)

#Function to test if you have valid arguments. It exits the program if not valid.
#(Doesn't check if file exists)
def checkUsage():
    usage_str = "\nUsage: python process.py [data_file] [num_steps]\n \
                \nNumber of steps has to be greater than 0 and MUST be less or equal to the number of steps recorded in the data_file. \
                \nMake sure the data file exists.\n"

    if len(sys.argv) != 3:
        print(usage_str)
        sys.exit()
    
    global steps
    steps = int(sys.argv[2])

    if steps < 0:
        print(usage_str)
        sys.exit()

#Function to get the bare data from the specified file.
#It returns it as an integer vector with as many positions as 
#specified steps in the program argument.
def readData():
    file_content = []
    points = []

    #Get all the lines as an array
    with open(datafile, "r") as f:
        file_content = f.read().splitlines()

    #Get all the valuable data and save it as integers
    for i in range (0, len(file_content), 2):
        points.append(int(file_content[i]))

    points = points[0:steps]

    return points

#Function to convert a list of polar coordinates (angles are calculated from the number of steps) to cartesian ones.
#It returns a list of pairs of points (integer), with length = steps.
#NOTE: the data is scaled to 1/2 and adapted to be centered, so it can be represented in the window
def polarToCartesian(points):
    global steps
    cPoints = []
    totalAngle = 0.0
    angleInc = 360.0 / float(steps)

    print(len(points))
    print(angleInc*steps)

    for point in points:
        x = math.cos(math.radians(totalAngle)) * float(point) / 2  + x_screen // 2 
        y = math.sin(math.radians(totalAngle)) * float(point) / 2  + y_screen // 2
        cPoints.append((x,y))
        totalAngle += angleInc
    
    return cPoints

#Function to draw "steps" cartesian points, with lines. It can operate in two ways (animated vs still image),
#depending on the program arguments. The input is the screen that is going to be drawn on and a list with the points.
def drawData(cPoints, screen):
    #Inner function for drawing coordinate axis and grid
    def drawAxisGrid():
        #Draw a grid, each line representing 500mm
        for i in range (-10, 10):
            pygame.draw.line(screen, light_gray, (x_screen//2 + i*250, -5000), (x_screen//2 + i*250, 5000), 1)
            pygame.draw.line(screen, light_gray, (-5000, y_screen//2 + i*250), (5000, y_screen//2 + i*250), 1)
        #Draw main axis
        pygame.draw.line(screen, gray, (x_screen//2, -5000), (x_screen//2, 5000), 1)
        pygame.draw.line(screen, gray, (-5000, y_screen//2), (5000, y_screen//2), 1)

    #TODO: this garbage ass loop eats resources like crazy, tune it down later
    clock = pygame.time.Clock()
    if not animated:
        while True:
            clock.tick(10)
            drawAxisGrid()
            pygame.draw.lines(screen, black, True, cPoints, 5)
            pygame.display.update()
    else:
        while True:
            for i in range(1, len(cPoints)-1):
                clock.tick(60)
                drawAxisGrid()
                pygame.draw.line(screen, black, cPoints[i-1], cPoints[i], 5)
                pygame.draw.line(screen, red, (x_screen//2, y_screen//2), cPoints[i], 1)
                pygame.display.update()
            
def main():
    #Check argument correctness and retrieve data
    checkUsage()
    data = readData()
    cPoints = polarToCartesian(data)

    #Print list of retrieved data. Debugging purposes.
    #print("Retrieved data")
    #print(data)
    #print(len(data))
    #print("Cartesian coordinates:")
    #print(cPoints)

    #Start white canvas
    pygame.init()
    screen = pygame.display.set_mode((x_screen, y_screen))
    screen.fill(white)
    pygame.display.update()

    #Drawing loop
    drawData(cPoints, screen)


if __name__ == "__main__":
    main()
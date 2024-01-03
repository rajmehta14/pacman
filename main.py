#Import the necessary modules
from random import choice       #Random for random movements of ghosts
from turtle import *            #Turtle for drawing map
from freegames import floor, vector     #Freegames for vectoring the movements

state = {'score': 0}        #State Dict to store Score
path = Turtle(visible=False)    #Path object to draw the map
writer = Turtle(visible=False)  #Writer object to display score
aim = vector(5, 0)              #Vector for direction
pacman = vector(-40, -80)       #Vector for Position
ghosts = [                      #List of Ghosts
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

"""
2D representation of map
    0-> For Wall
    1-> For Path
"""
 # ... 0s and 1s representing the game map ...
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

"""Function to draw individual squares"""

def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


"""Function to return the index number for respective coordinates """

def offset(point):
    """Return offset of point in tiles."""
    # ... calculates the index in the tiles list for a given point ...
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

"""
Function to check if a point is valid
i.e. Is it a Path or is it a Wall
"""

def valid(point):
    """Return True if point is valid in tiles."""
    # ... checks if a point is valid within the game map ...
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)#to check if there is path or wall

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


"""Draw world using path."""

def world():
    bgcolor('black') #set bg color to black
    path.color('blue')#set path color to blue
    # ... draws the game world ...

    for index in range(len(tiles)):
        tile = tiles[index]#returns the value of given tile

        if tile > 0:
            x = (index % 20) * 20 - 200  #find x co-ordinate
            y = 180 - (index // 20) * 20 #find y co-ordinate
            square(x, y)#creates the square

            if tile == 1:#if value of tile is 1
                path.up()
                path.goto(x + 10, y + 10)#it will move to center
                path.dot(2, 'white')#it will create the size and color of dot


"""Move pacman and all ghosts."""

def move():
    # ... moves Pac-Man and the ghosts, handles collisions, and updates the game..
    writer.undo()#it will undo the previous score
    writer.write(state['score'])#it will update the current score

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman) #gives the position of packman

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:        #Make random movements of Ghosts
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:        #Collision detection of ghosts and pacman
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)      #Run move function every 100ms/*


"""Change pacman aim if valid."""


def change(x, y):
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

#Setup Canvas
#This part of the code sets up the game window with a size of 420x420, hides the default turtle cursor,
#turns off screen updates, positions the 'writer' turtle, sets its color to white,
#and initially displays the player's score (which is initially 0).

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])

#Controls
#These lines set up event listeners for keyboard input.
#They allow the player to control Pac-Man's movement using the arrow keys.
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

world()   #to draw the game world
move()    #to start the game loop
done()    #to finish setting up the game window

from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import numpy as np

HEIGHT, WIDTH = 600, 800
SCALE = 100

WHITE = (1.0, 1.0, 1.0)

rot_x = 0
rot_y = 0
rot_z = 0

coor_arr = [[0.0, -0.618034005, -1.618033946], [-0.618034005, -1.618033946, 0.0], [-1.618033946, 0.0, -0.618034005], [-1.0, -1.0, -1.0], [-1.0, -1.0, 1.0], [0.0, -0.618034005, 1.618033946], [-0.618034005, 1.618033946, 0.0], [-1.618033946, 0.0, 0.618034005], [-1.0, 1.0, -1.0], [-1.0, 1.0, 1.0], [0.0, 0.618034005, -1.618033946], [0.618034005, -1.618033946, 0.0], [1.618033946, 0.0, -0.618034005], [1.0, -1.0, -1.0], [1.0, -1.0, 1.0], [0.0, 0.618034005, 1.618033946], [0.618034005, 1.618033946, 0.0], [1.618033946, 0.0, 0.618034005], [1.0, 1.0, -1.0], [1.0, 1.0, 1.0]]
connnection = {0: [3, 10, 13], 1: [3, 4, 11], 2: [3, 7, 8], 4: [5, 7], 5: [14, 15], 6: [8, 9, 16], 7: [9], 8: [10], 9: [15], 10: [18], 11: [13, 14], 12: [13, 17, 18], 14: [17], 15: [19], 16: [18, 19], 17: [19]}


class Shape:

    def __init__(self, c, *ver):

        self.vertex = ver
        self.c = c

        self.x = np.array([])
        self.y = np.array([])
        self.z = np.array([])

        for v in self.vertex:
            self.x = np.concatenate((self.x, np.array([v[0] * SCALE])))
            self.y = np.concatenate((self.y, np.array([v[1] * SCALE])))
            self.z = np.concatenate((self.z, np.array([v[2] * SCALE])))

    def colour(self, c):
        self.c = c

    def draw(self, outline = 0):

        lst = []

        for i in range(len(self.vertex)):
            lst.append((self.x[i] + WIDTH // 2, -self.y[i] + HEIGHT // 2))

        for i in range(len(lst) - 1):
            x0, y0 = lst[i]
            x1, y1 = lst[i + 1]

            x0 = round(x0)
            y0 = round(y0)
            x1 = round(x1)
            y1 = round(y1)

            drawLine(x0, y0, x1, y1)

        x0, y0 = lst[-1]
        x1, y1 = lst[0]

        drawLine(x0, y0, x1, y1)


    def rotate(self, theta, axis = "z"):

        theta = theta * (math.pi / 180)

        if axis.lower() == "x":
            self.matrix(1, 0, 0, 0, math.cos(theta), -math.sin(theta), 0, math.sin(theta), math.cos(theta))

        elif axis.lower() == "y":
            self.matrix(math.cos(theta), 0, math.sin(theta), 0, 1, 0, -math.sin(theta), 0, math.cos(theta))

        elif axis.lower() == "z":
            self.matrix(math.cos(theta), -math.sin(theta), 0, math.sin(theta), math.cos(theta), 0, 0, 0, 1)

    def translate(self, dx, dy, dz):
        self.x += dx * SCALE
        self.y += dy * SCALE
        self.z += dz * SCALE

    def enlarge(self, s):
        self.x *= s
        self.y *= s
        self.z *= s

    def matrix(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
        new_x = (x1 * self.x) + (y1 * self.y) + (z1 * self.z)
        new_y = (x2 * self.x) + (y2 * self.y) + (z2 * self.z)
        new_z = (x3 * self.x) + (y3 * self.y) + (z3 * self.z)

        self.x = new_x
        self.y = new_y
        self.z = new_z

def draw_points(x, y):
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_rgb_points(x, y, c):
    glColor3f(c[0], c[1], c[2])
    glPointSize(1)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def drawLine(x0, y0, x1, y1):

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    if dy >= 0:
        sign = 1
    else:
        sign = -1

    if abs(dx) >= abs(dy):
        d = 2 * dy - dx
        x, y = x0, y0
        draw_points(x, y)

        while x < x1:
            if d * sign > 0:
                d -= 2 * abs(dx) * sign
                y += 1 * sign

            x += 1
            d += 2 * abs(dy) * sign

            draw_points(x, y)

    else:
        d = 2 * dx - dy

        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        x, y = x0, y0
        draw_points(x, y)

        while y < y1:
            if d * sign > 0:
                d -= 2 * abs(dy) * sign
                x += 1 * sign

            y += 1
            d += 2 * abs(dx) * sign

            draw_points(x, y)

def drawText(text,x,y):
    glColor3fv((0,0,0))
    glWindowPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(fonts.GLUT_BITMAP_HELVETICA_18, ord(ch))



def iterate():
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    try:
       glPushMatrix()
    except:
        glPopMatrix()
        glPopMatrix()
    glLoadIdentity()
    glOrtho(0.0, WIDTH, 0.0, HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def mainLoop():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 1.0)

    if False:
        cubeFront = Shape(WHITE, (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1))
        cubeRear = Shape(WHITE, (1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, 1, -1))
        cubeRight = Shape(WHITE, (1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1))
        cubeLeft = Shape(WHITE, (-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (-1, -1, 1))
        cubeTop = Shape(WHITE, (1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1))
        cubeBottom = Shape(WHITE, (1, -1, 1), (1, -1, -1), (-1, -1, -1), (-1, -1, 1))

        env = [cubeFront, cubeRear, cubeRight, cubeLeft, cubeTop, cubeBottom]

    env = []

    for key in connnection.keys():
        for val in connnection[key]:
            s = Shape(WHITE, coor_arr[key], coor_arr[val])
            env.append(s)

    global rot_x, rot_y, rot_z

    for c in env:

        c.rotate(rot_x, "x")
        c.rotate(rot_y, "y")
        c.rotate(rot_z, "z")

        c.draw()

    #rot_x += 1.3
    #rot_y += 0.7
    #rot_z += 1.2

    rot_x += 1.3 * 3
    rot_y += 0.7 * 3
    rot_z += 1.2 * 3
    
    
    glutPostRedisplay()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"3D Box")
#glutKeyboardFunc(mainLoop)
glutDisplayFunc(mainLoop)
glutMainLoop()
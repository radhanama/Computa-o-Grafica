import sys
import sdl2
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
import sys

N = 50
df = 3/N

#https://www.opengl.org/wiki/Calculating_a_Surface_Normal
#Begin Function CalculateSurfaceNormal (Input Triangle) Returns Vector
#  Set Vector U to (Triangle.p2 minus Triangle.p1)
#  Set Vector V to (Triangle.p3 minus Triangle.p1)
#  Set Normal.x to (multiply U.y by V.z) minus (multiply U.z by V.y)
#  Set Normal.y to (multiply U.z by V.x) minus (multiply U.x by V.z)
#  Set Normal.z to (multiply U.x by V.y) minus (multiply U.y by V.x)
#  Returning Normal
#End Function

def calculaNormalFace(v0,v1,v2):
    x = 0
    y = 1
    z = 2
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)

def cor(i,j):
    r = 0.5+0.5*j
    g = 0.5+0.5*i
    b = r
    return r, g, b

def sla1(x,y):
    return x**2+y**2

def sla2(x,y):
    return x**2-y**2

a=0
r=1
def malha1():
    global a
    y=-1.5
    for _ in range(0,N):
        glBegin(GL_TRIANGLE_STRIP)
        x=-1.5
        for _ in range(0,N):
            z = sla1(x,y)
            z_2 = sla1(x,y+df)
            z_3 = sla1(x+df,y)
            glNormal3fv(calculaNormalFace([x,y,z],[x,y+df,z_2],[x+df,y,z_3]))
            glVertex3f(x,y,z)
            glVertex3f(x,y+df,z_2)
            x+=df
        glEnd()
        y+=df
    a+=1

a=0
r=1
def malha2():
    global a
    y=-1.5
    for _ in range(0,N):
        glBegin(GL_TRIANGLE_STRIP)
        x=-1.5
        for _ in range(0,N):
            z = sla2(x,y)
            z_2 = sla2(x,y+df)
            z_3 = sla2(x+df,y)
            glNormal3fv(calculaNormalFace([x,y,z],[x,y+df,z_2],[x+df,y,z_3]))
            glVertex3f(x,y,z)
            glVertex3f(x,y+df,z_2)
            x+=df
        glEnd()
        y+=df
    a+=1


def display():
    # Cubo da Esquerda
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(-4.0,-5.0,-20.0)
    glRotatef(a,1.0,1.0,0.0)
    malha1()
    glPopMatrix()
    # Cubo da Direita
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(4.0,5.0,-20.0)
    glRotatef(a,-1.0,1.0,0.0)
    malha2()
    glPopMatrix()
    


def InitGL(width, height):
    mat_ambient = (0.0, 0.7, 0.0, 1.0)
    mat_diffuse = (0.0, 1.0, 0.0, 1.0)
    mat_specular = (0.5, 1.0, 0.5, 1.0)
    mat_shininess = (50,)
    light_position = (10, 0, 0)
    glClearColor(0.0,0.0,0.0,0.0)
    glShadeModel(GL_SMOOTH)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)               
    glEnable(GL_DEPTH_TEST)            
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,10,0,0,0,0,1,0)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
sdl2.SDL_GL_SetSwapInterval(1)
window = sdl2.SDL_CreateWindow(b"Cubo Iluminado", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)
if not window:
    sys.stderr.write("Error: Could not create window\n")
    exit(1)
glcontext = sdl2.SDL_GL_CreateContext(window)
InitGL(WINDOW_WIDTH, WINDOW_HEIGHT)
running = True
event = sdl2.SDL_Event()
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            running = False
        if event.type == sdl2.events.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
    display()
    sdl2.SDL_GL_SwapWindow(window)
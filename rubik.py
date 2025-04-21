from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

angleX, angleY = 30, 30
zoom = -20
mouseDown = False
mouseX, mouseY = 0, 0

def draw_cube(x, y, z, size):
    colors = [
        (1, 0, 0),   # Merah
        (0, 1, 0),   # Hijau
        (0, 0, 1),   # Biru
        (1, 1, 0),   # Kuning
        (1, 0.5, 0), # Oranye
        (1, 1, 1)    # Putih
    ]

    vertices = [
        [x-size, y-size, z-size],
        [x+size, y-size, z-size],
        [x+size, y+size, z-size],
        [x-size, y+size, z-size],
        [x-size, y-size, z+size],
        [x+size, y-size, z+size],
        [x+size, y+size, z+size],
        [x-size, y+size, z+size]
    ]

    faces = [
        (0, 1, 2, 3),  # Belakang
        (4, 5, 6, 7),  # Depan
        (0, 4, 7, 3),  # Kiri
        (1, 5, 6, 2),  # Kanan
        (3, 2, 6, 7),  # Atas
        (0, 1, 5, 4)   # Bawah
    ]

    # Gambar permukaan berwarna
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Gambar outline hitam tipis
    glLineWidth(1.5)
    glColor3f(0, 0, 0)  # Hitam
    for face in faces:
        glBegin(GL_LINE_LOOP)
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()

    colors = [
        (1, 0, 0),   # Merah
        (0, 1, 0),   # Hijau
        (0, 0, 1),   # Biru
        (1, 1, 0),   # Kuning
        (1, 0.5, 0), # Oranye
        (1, 1, 1)    # Putih
    ]

    vertices = [
        [x-size, y-size, z-size],
        [x+size, y-size, z-size],
        [x+size, y+size, z-size],
        [x-size, y+size, z-size],
        [x-size, y-size, z+size],
        [x+size, y-size, z+size],
        [x+size, y+size, z+size],
        [x-size, y+size, z+size]
    ]

    faces = [
        (0, 1, 2, 3),  # Belakang
        (4, 5, 6, 7),  # Depan
        (0, 4, 7, 3),  # Kiri
        (1, 5, 6, 2),  # Kanan
        (3, 2, 6, 7),  # Atas
        (0, 1, 5, 4)   # Bawah
    ]

    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_rubik():
    size = 0.9
    spacing = size  # Tidak ada gap
    half_size = size / 2

    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                draw_cube(x * spacing, y * spacing, z * spacing, half_size)

def draw_floor():
    glDisable(GL_LIGHTING)
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-10, -3, -10)
    glVertex3f(10, -3, -10)
    glVertex3f(10, -3, 10)
    glVertex3f(-10, -3, 10)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_light_indicator():
    glPushMatrix()
    glTranslatef(10.0, 10.0, 10.0)
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 0.0)  # Kuning terang sebagai sumber cahaya
    glutSolidSphere(0.2, 20, 20)
    glEnable(GL_LIGHTING)
    glPopMatrix()

def init_lighting():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    light_pos = [10.0, 10.0, 10.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

def display():
    global angleX, angleY, zoom
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, zoom)
    glRotatef(angleX, 1, 0, 0)
    glRotatef(angleY, 0, 1, 0)

    draw_floor()
    draw_rubik()
    draw_light_indicator()

    glutSwapBuffers()

def reshape(w, h):
    if h == 0:
        h = 1
    aspect = w / h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, aspect, 1, 100)
    glMatrixMode(GL_MODELVIEW)

def mouse(button, state, x, y):
    global mouseDown, mouseX, mouseY
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mouseDown = True
            mouseX = x
            mouseY = y
        elif state == GLUT_UP:
            mouseDown = False

def mouse_motion(x, y):
    global angleX, angleY, mouseX, mouseY
    if mouseDown:
        dx = x - mouseX
        dy = y - mouseY
        angleX += dy * 0.5
        angleY += dx * 0.5
        mouseX = x
        mouseY = y
        glutPostRedisplay()

def mouse_wheel(button, direction, x, y):
    global zoom
    if direction > 0:
        zoom += 1
    else:
        zoom -= 1
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Rubik's Cube 3D - No Gap + Lighting Indicator + Floor")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)
    glutMouseWheelFunc(mouse_wheel)

    glClearColor(0.1, 0.1, 0.1, 1.0)
    init_lighting()
    glutMainLoop()

if __name__ == "__main__":
    main()

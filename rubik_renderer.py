# rubik_renderer.py

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import rubik_globals as g

def check_gl_error():
    err = glGetError()
    if err != GL_NO_ERROR:
        print(f"OpenGL Error: {err}")
        return False
    return True

def draw_cube(x, y, z, size, face_colors, is_selected=False, is_hovered=False):
    colors = [
        (1, 0.5, 0),  # Oranye (Depan, face 4)
        (1, 0, 0),    # Merah (Kanan, face 1)
        (0, 0, 1),    # Biru (Atas, face 2)
        (1, 1, 0),    # Kuning (Bawah, face 3)
        (0, 1, 0),    # Hijau (Kiri, face 0)
        (1, 1, 1)     # Putih (Belakang, face 5)
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
        glColor3fv(colors[face_colors[i]])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    glLineWidth(4.0 if is_selected else (2.5 if is_hovered else 1.5))
    glColor3f(0, 0, 0)
    for face in faces:
        glBegin(GL_LINE_LOOP)
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()

def draw_rubik():
    size = 0.9
    spacing = size
    half_size = size / 2
    glPushMatrix()
    holder_to_use = g.temp_rubik_holder if g.temp_rubik_holder is not None else g.rubik_holder
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                is_selected = (g.selected_face is not None and
                              ((g.selected_face == 0 and x == -1) or
                               (g.selected_face == 1 and x == 1) or
                               (g.selected_face == 2 and y == 1) or
                               (g.selected_face == 3 and y == -1) or
                               (g.selected_face == 4 and z == 1) or
                               (g.selected_face == 5 and z == -1)))
                is_hovered = (g.hovered_face is not None and
                             ((g.hovered_face == 0 and x == -1) or
                              (g.hovered_face == 1 and x == 1) or
                              (g.hovered_face == 2 and y == 1) or
                              (g.hovered_face == 3 and y == -1) or
                              (g.hovered_face == 4 and z == 1) or
                              (g.hovered_face == 5 and z == -1)))
                face_colors = [5, 4, 0, 1, 2, 3]
                if x == -1:
                    face_colors[2] = holder_to_use.get_color(0, 1-y, z+1)
                if x == 1:
                    face_colors[3] = holder_to_use.get_color(1, 1-y, 1-z)
                if y == 1:
                    face_colors[4] = holder_to_use.get_color(2, z+1, x+1)
                if y == -1:
                    face_colors[5] = holder_to_use.get_color(3, 1-z, x+1)
                if z == 1:
                    face_colors[1] = holder_to_use.get_color(4, 1-y, x+1)
                if z == -1:
                    face_colors[0] = holder_to_use.get_color(5, 1-y, x+1)
                glPushMatrix()
                if g.is_animating and g.current_face_to_rotate is not None:
                    if ((g.current_face_to_rotate == 0 and x == -1) or
                        (g.current_face_to_rotate == 1 and x == 1) or
                        (g.current_face_to_rotate == 2 and y == 1) or
                        (g.current_face_to_rotate == 3 and y == -1) or
                        (g.current_face_to_rotate == 4 and z == 1) or
                        (g.current_face_to_rotate == 5 and z == -1)):
                        effective_angle = g.current_rotation_angle * g.rotation_sign[g.current_face_to_rotate]
                        if g.rotation_axis == 'x':
                            glRotatef(effective_angle, 1, 0, 0)
                        elif g.rotation_axis == 'y':
                            glRotatef(effective_angle, 0, 1, 0)
                        elif g.rotation_axis == 'z':
                            glRotatef(effective_angle, 0, 0, 1)
                draw_cube(x * spacing, y * spacing, z * spacing, half_size, face_colors, is_selected, is_hovered)
                glPopMatrix()
    glPopMatrix()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, g.zoom)
    glRotatef(g.angleX, 1, 0, 0)
    glRotatef(g.angleY, 0, 1, 0)
    draw_rubik()
    glutSwapBuffers()
    check_gl_error()

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

def reshape(w, h):
    if h == 0:
        h = 1
    aspect = w / h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, aspect, 1, 100)
    glMatrixMode(GL_MODELVIEW)

def get_face_from_position(x, y):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, g.zoom)
    glRotatef(g.angleX, 1, 0, 0)
    glRotatef(g.angleY, 0, 1, 0)
    size = 0.9
    spacing = size
    half_size = size / 2
    min_depth = 1.0
    closest_face = None
    for face in range(6):
        glPushMatrix()
        if face == 0:
            glTranslatef(-spacing, 0, 0)
            glRotatef(90, 0, 1, 0)
        elif face == 1:
            glTranslatef(spacing, 0, 0)
            glRotatef(-90, 0, 1, 0)
        elif face == 2:
            glTranslatef(0, spacing, 0)
            glRotatef(-90, 1, 0, 0)
        elif face == 3:
            glTranslatef(0, -spacing, 0)
            glRotatef(90, 1, 0, 0)
        elif face == 4:
            glTranslatef(0, 0, spacing)
        elif face == 5:
            glTranslatef(0, 0, -spacing)
            glRotatef(180, 0, 1, 0)
        glBegin(GL_QUADS)
        glVertex3f(-half_size, -half_size, 0)
        glVertex3f(half_size, -half_size, 0)
        glVertex3f(half_size, half_size, 0)
        glVertex3f(-half_size, half_size, 0)
        glEnd()
        glPopMatrix()
        buffer = glReadPixels(x, glutGet(GLUT_WINDOW_HEIGHT) - y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        depth = buffer[0][0]
        if depth < min_depth:
            min_depth = depth
            closest_face = face
    return closest_face if min_depth < 1.0 else None
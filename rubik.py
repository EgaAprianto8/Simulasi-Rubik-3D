import time
import sys
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Variabel global
angleX, angleY = 45, 45  # Sudut awal untuk tampilan lebih jelas
zoom = -20
mouseDown = False
mouseX, mouseY = 0, 0
scramble_moves = []
current_move_index = 0
is_animating = False
current_rotation_angle = 0
current_face_to_rotate = None
rotation_direction = 1
temp_rubik_holder = None
selected_face = None
hovered_face = None
is_solving = False
rotation_axis = None
rotation_speed = 5  # Kecepatan animasi rotasi
rotation_sign = [1, -1, -1, 1, -1, 1]  # Tanda rotasi untuk sisi 0-5: kiri, kanan, atas, bawah, depan, belakang

# Kelas untuk mengelola warna Rubik's Cube
class RubikColorHolder:
    def __init__(self):
        # Warna: 0=Oranye, 1=Merah, 2=Biru, 3=Kuning, 4=Hijau, 5=Putih
        self.sides = [
            [4] * 9,  # Kiri (Hijau, face 0)
            [1] * 9,  # Kanan (Merah, face 1)
            [2] * 9,  # Atas (Biru, face 2)
            [3] * 9,  # Bawah (Kuning, face 3)
            [0] * 9,  # Depan (Oranye, face 4)
            [5] * 9   # Belakang (Putih, face 5)
        ]

    def copy(self):
        new_holder = RubikColorHolder()
        new_holder.sides = [side.copy() for side in self.sides]
        return new_holder

    def get_color(self, side, row, col):
        return self.sides[side][row * 3 + col]

    def validate_cube(self):
        color_count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for face in self.sides:
            for color in face:
                color_count[color] += 1
        for color, count in color_count.items():
            if count != 9:
                raise ValueError(f"Invalid cube state: Color {color} appears {count} times, expected 9.")

    def rotate_face(self, face, direction):
        # Rotasi sisi itu sendiri
        new_face = [0] * 9
        for i in range(3):
            for j in range(3):
                if direction == 1:  # Searah jarum jam
                    new_face[j * 3 + (2-i)] = self.sides[face][i * 3 + j]
                else:  # Berlawanan jarum jam
                    new_face[(2-j) * 3 + i] = self.sides[face][i * 3 + j]
        self.sides[face] = new_face

        # Rotasi sisi-sisi yang berdekatan
        if face == 0:  # Kiri (L, Hijau)
            old_F_l = [self.sides[4][0], self.sides[4][3], self.sides[4][6]]  # Kolom kiri Depan
            old_U_l = [self.sides[2][0], self.sides[2][3], self.sides[2][6]]  # Kolom kiri Atas
            old_B_l = [self.sides[5][0], self.sides[5][3], self.sides[5][6]]  # Kolom kiri Belakang
            old_D_l = [self.sides[3][0], self.sides[3][3], self.sides[3][6]]  # Kolom kiri Bawah
            if direction == 1:  # L (searah jarum jam)
                self.sides[4][0:7:3] = old_U_l  # F_l = old_U_l
                self.sides[2][0:7:3] = old_B_l  # U_l = old_B_l
                self.sides[5][0:7:3] = old_D_l  # B_l = old_D_l
                self.sides[3][0:7:3] = old_F_l  # D_l = old_F_l
            else:  # L' (berlawanan jarum jam)
                self.sides[4][0:7:3] = old_D_l  # F_l = old_D_l
                self.sides[3][0:7:3] = old_B_l  # D_l = old_B_l
                self.sides[5][0:7:3] = old_U_l  # B_l = old_U_l
                self.sides[2][0:7:3] = old_F_l  # U_l = old_F_l

        elif face == 1:  # Kanan (R, Merah)
            old_F_r = [self.sides[4][2], self.sides[4][5], self.sides[4][8]]  # Kolom kanan Depan
            old_U_r = [self.sides[2][2], self.sides[2][5], self.sides[2][8]]  # Kolom kanan Atas
            old_B_r = [self.sides[5][2], self.sides[5][5], self.sides[5][8]]  # Kolom kanan Belakang
            old_D_r = [self.sides[3][2], self.sides[3][5], self.sides[3][8]]  # Kolom kanan Bawah
            if direction == 1:  # R (searah jarum jam)
                self.sides[4][2:9:3] = old_U_r  # F_r = old_U_r
                self.sides[2][2:9:3] = old_B_r  # U_r = old_B_r
                self.sides[5][2:9:3] = old_D_r  # B_r = old_D_r
                self.sides[3][2:9:3] = old_F_r  # D_r = old_F_r
            else:  # R' (berlawanan jarum jam)
                self.sides[4][2:9:3] = old_D_r  # F_r = old_D_r
                self.sides[3][2:9:3] = old_B_r  # D_r = old_B_r
                self.sides[5][2:9:3] = old_U_r  # B_r = old_U_r
                self.sides[2][2:9:3] = old_F_r  # U_r = old_F_r

        elif face == 2:  # Atas (U, Biru)
            old_F_t = [self.sides[4][0], self.sides[4][1], self.sides[4][2]]  # Baris atas Depan
            old_R_t = [self.sides[1][0], self.sides[1][1], self.sides[1][2]]  # Baris atas Kanan
            old_B_t = [self.sides[5][0], self.sides[5][1], self.sides[5][2]]  # Baris atas Belakang
            old_L_t = [self.sides[0][0], self.sides[0][1], self.sides[0][2]]  # Baris atas Kiri
            if direction == 1:  # U (searah jarum jam)
                self.sides[4][0:3] = old_R_t  # F_t = old_R_t
                self.sides[1][0:3] = old_B_t  # R_t = old_B_t
                self.sides[5][0:3] = old_L_t  # B_t = old_L_t
                self.sides[0][0:3] = old_F_t  # L_t = old_F_t
            else:  # U' (berlawanan jarum jam)
                self.sides[4][0:3] = old_L_t  # F_t = old_L_t
                self.sides[0][0:3] = old_B_t  # L_t = old_B_t
                self.sides[5][0:3] = old_R_t  # B_t = old_R_t
                self.sides[1][0:3] = old_F_t  # R_t = old_F_t

        elif face == 3:  # Bawah (D, Kuning)
            old_F_b = [self.sides[4][6], self.sides[4][7], self.sides[4][8]]  # Baris bawah Depan
            old_L_b = [self.sides[0][6], self.sides[0][7], self.sides[0][8]]  # Baris bawah Kiri
            old_B_b = [self.sides[5][6], self.sides[5][7], self.sides[5][8]]  # Baris bawah Belakang
            old_R_b = [self.sides[1][6], self.sides[1][7], self.sides[1][8]]  # Baris bawah Kanan
            if direction == 1:  # D (searah jarum jam)
                self.sides[4][6:9] = old_L_b  # F_b = old_L_b
                self.sides[0][6:9] = old_B_b  # L_b = old_B_b
                self.sides[5][6:9] = old_R_b  # B_b = old_R_b
                self.sides[1][6:9] = old_F_b  # R_b = old_F_b
            else:  # D' (berlawanan jarum jam)
                self.sides[4][6:9] = old_R_b  # F_b = old_R_b
                self.sides[1][6:9] = old_B_b  # R_b = old_B_b
                self.sides[5][6:9] = old_L_b  # B_b = old_L_b
                self.sides[0][6:9] = old_F_b  # L_b = old_F_b

        elif face == 4:  # Depan (F, Oranye)
            old_U_b = [self.sides[2][6], self.sides[2][7], self.sides[2][8]]  # Baris bawah Atas
            old_L_r = [self.sides[0][2], self.sides[0][5], self.sides[0][8]]  # Kolom kanan Kiri
            old_D_t = [self.sides[3][0], self.sides[3][1], self.sides[3][2]]  # Baris atas Bawah
            old_R_l = [self.sides[1][0], self.sides[1][3], self.sides[1][6]]  # Kolom kiri Kanan
            if direction == 1:  # F (searah jarum jam)
                self.sides[2][6:9] = old_L_r  # U_b = old_L_r
                self.sides[0][2:9:3] = old_D_t  # L_r = old_D_t
                self.sides[3][0:3] = old_R_l  # D_t = old_R_l
                self.sides[1][0:7:3] = old_U_b  # R_l = old_U_b
            else:  # F' (berlawanan jarum jam)
                self.sides[2][6:9] = old_R_l  # U_b = old_R_l
                self.sides[1][0:7:3] = old_D_t  # R_l = old_D_t
                self.sides[3][0:3] = old_L_r  # D_t = old_L_r
                self.sides[0][2:9:3] = old_U_b  # L_r = old_U_b

        elif face == 5:  # Belakang (B, Putih)
            old_U_t = [self.sides[2][0], self.sides[2][1], self.sides[2][2]]  # Baris atas Atas
            old_R_r = [self.sides[1][2], self.sides[1][5], self.sides[1][8]]  # Kolom kanan Kanan
            old_D_b = [self.sides[3][6], self.sides[3][7], self.sides[3][8]]  # Baris bawah Bawah
            old_L_l = [self.sides[0][0], self.sides[0][3], self.sides[0][6]]  # Kolom kiri Kiri
            if direction == 1:  # B (searah jarum jam)
                self.sides[2][0:3] = old_R_r  # U_t = old_R_r
                self.sides[1][2:9:3] = old_D_b  # R_r = old_D_b
                self.sides[3][6:9] = old_L_l  # D_b = old_L_l
                self.sides[0][0:7:3] = old_U_t  # L_l = old_U_t
            else:  # B' (berlawanan jarum jam)
                self.sides[2][0:3] = old_L_l  # U_t = old_L_l
                self.sides[0][0:7:3] = old_D_b  # L_l = old_D_b
                self.sides[3][6:9] = old_R_r  # D_b = old_R_r
                self.sides[1][2:9:3] = old_U_t  # R_r = old_U_t

        self.validate_cube()  # Validasi setelah rotasi

rubik_holder = RubikColorHolder()

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
        [x-size, y-size, z-size],  # 0: Belakang bawah kiri
        [x+size, y-size, z-size],  # 1: Belakang bawah kanan
        [x+size, y+size, z-size],  # 2: Belakang atas kanan
        [x-size, y+size, z-size],  # 3: Belakang atas kiri
        [x-size, y-size, z+size],  # 4: Depan bawah kiri
        [x+size, y-size, z+size],  # 5: Depan bawah kanan
        [x+size, y+size, z+size],  # 6: Depan atas kanan
        [x-size, y+size, z+size]   # 7: Depan atas kiri
    ]

    faces = [
        (0, 1, 2, 3),  # Belakang (z = -size, face 5)
        (4, 5, 6, 7),  # Depan (z = +size, face 4)
        (0, 4, 7, 3),  # Kiri (x = -size, face 0)
        (1, 5, 6, 2),  # Kanan (x = +size, face 1)
        (3, 2, 6, 7),  # Atas (y = +size, face 2)
        (0, 1, 5, 4)   # Bawah (y = -size, face 3)
    ]

    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3fv(colors[face_colors[i]])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Garis tepi untuk hover dan seleksi
    glLineWidth(4.0 if is_selected else (2.5 if is_hovered else 1.5))
    glColor3f(0, 0, 0)
    for face in faces:
        glBegin(GL_LINE_LOOP)
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()

def draw_rubik():
    global temp_rubik_holder, current_rotation_angle, current_face_to_rotate, rotation_axis
    size = 0.9
    spacing = size
    half_size = size / 2

    glPushMatrix()
    holder_to_use = temp_rubik_holder if temp_rubik_holder is not None else rubik_holder

    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                is_selected = (selected_face is not None and
                             ((selected_face == 0 and x == -1) or  # Kiri
                              (selected_face == 1 and x == 1) or   # Kanan
                              (selected_face == 2 and y == 1) or   # Atas
                              (selected_face == 3 and y == -1) or  # Bawah
                              (selected_face == 4 and z == 1) or   # Depan
                              (selected_face == 5 and z == -1)))   # Belakang
                is_hovered = (hovered_face is not None and
                             ((hovered_face == 0 and x == -1) or
                              (hovered_face == 1 and x == 1) or
                              (hovered_face == 2 and y == 1) or
                              (hovered_face == 3 and y == -1) or
                              (hovered_face == 4 and z == 1) or
                              (hovered_face == 5 and z == -1)))

                # Inisialisasi warna default: Belakang, Depan, Kiri, Kanan, Atas, Bawah
                face_colors = [5, 4, 0, 1, 2, 3]
                if x == -1:  # Kiri (face 0, hijau)
                    face_colors[2] = holder_to_use.get_color(0, 1-y, z+1)
                if x == 1:   # Kanan (face 1, merah)
                    face_colors[3] = holder_to_use.get_color(1, 1-y, 1-z)
                if y == 1:   # Atas (face 2, biru)
                    face_colors[4] = holder_to_use.get_color(2, z+1, x+1)
                if y == -1:  # Bawah (face 3, kuning)
                    face_colors[5] = holder_to_use.get_color(3, 1-z, x+1)
                if z == 1:   # Depan (face 4, oranye)
                    face_colors[1] = holder_to_use.get_color(4, 1-y, x+1)
                if z == -1:  # Belakang (face 5, putih)
                    face_colors[0] = holder_to_use.get_color(5, 1-y, x+1)

                glPushMatrix()
                if is_animating and current_face_to_rotate is not None:
                    if ((current_face_to_rotate == 0 and x == -1) or
                        (current_face_to_rotate == 1 and x == 1) or
                        (current_face_to_rotate == 2 and y == 1) or
                        (current_face_to_rotate == 3 and y == -1) or
                        (current_face_to_rotate == 4 and z == 1) or
                        (current_face_to_rotate == 5 and z == -1)):
                        effective_angle = current_rotation_angle * rotation_sign[current_face_to_rotate]
                        if rotation_axis == 'x':
                            glRotatef(effective_angle, 1, 0, 0)
                        elif rotation_axis == 'y':
                            glRotatef(effective_angle, 0, 1, 0)
                        elif rotation_axis == 'z':
                            glRotatef(effective_angle, 0, 0, 1)
                draw_cube(x * spacing, y * spacing, z * spacing, half_size, face_colors, is_selected, is_hovered)
                glPopMatrix()

    glPopMatrix()

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

def check_gl_error():
    err = glGetError()
    if err != GL_NO_ERROR:
        print(f"OpenGL Error: {err}")
        return False
    return True

def display():
    global angleX, angleY, zoom
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, zoom)
    glRotatef(angleX, 1, 0, 0)
    glRotatef(angleY, 0, 1, 0)
    draw_rubik()
    glutSwapBuffers()
    check_gl_error()

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
    global angleX, angleY, zoom
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, zoom)
    glRotatef(angleX, 1, 0, 0)
    glRotatef(angleY, 0, 1, 0)

    size = 0.9
    spacing = size
    half_size = size / 2

    min_depth = 1.0
    closest_face = None

    for face in range(6):
        glPushMatrix()
        if face == 0:  # Kiri
            glTranslatef(-spacing, 0, 0)
            glRotatef(90, 0, 1, 0)
        elif face == 1:  # Kanan
            glTranslatef(spacing, 0, 0)
            glRotatef(-90, 0, 1, 0)
        elif face == 2:  # Atas
            glTranslatef(0, spacing, 0)
            glRotatef(-90, 1, 0, 0)
        elif face == 3:  # Bawah
            glTranslatef(0, -spacing, 0)
            glRotatef(90, 1, 0, 0)
        elif face == 4:  # Depan
            glTranslatef(0, 0, spacing)
        elif face == 5:  # Belakang
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

def mouse(button, state, x, y):
    global mouseDown, mouseX, mouseY, selected_face
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if not is_animating:
                selected_face = get_face_from_position(x, y)
                mouseDown = True
                mouseX = x
                mouseY = y
            glutPostRedisplay()
        elif state == GLUT_UP:
            mouseDown = False

def passive_motion(x, y):
    global hovered_face
    if not is_animating:
        hovered_face = get_face_from_position(x, y)
        glutPostRedisplay()

def mouse_motion(x, y):
    global angleX, angleY, mouseX, mouseY
    if mouseDown and not is_animating:
        dx = x - mouseX
        dy = y - mouseY
        angleX += dy * 0.5
        angleY += dx * 0.5
        mouseX = x
        mouseY = y
        glutPostRedisplay()

def mouse_wheel(button, dir, x, y):
    global zoom
    if dir > 0:
        zoom += 1
    else:
        zoom -= 1
    zoom = max(-50, min(-5, zoom))
    glutPostRedisplay()

def animate():
    global is_animating, current_rotation_angle, current_face_to_rotate, temp_rubik_holder, rotation_direction
    if is_animating:
        current_rotation_angle += rotation_speed * rotation_direction
        if abs(current_rotation_angle) >= 90:
            is_animating = False
            current_rotation_angle = 0
            rubik_holder.rotate_face(current_face_to_rotate, rotation_direction)
            temp_rubik_holder = None
            if is_solving and scramble_moves:
                perform_solve_step()
        glutPostRedisplay()

def keyboard(key, x, y):
    global is_animating, current_face_to_rotate, rotation_direction, temp_rubik_holder, rotation_axis, is_solving
    if key == b'\x1b':
        sys.exit(0)
    elif selected_face is not None and not is_animating:
        if key.lower() in [b'a', b'd']:
            is_animating = True
            current_face_to_rotate = selected_face
            temp_rubik_holder = rubik_holder.copy()
            
            # Tentukan arah rotasi
            rotation_direction = 1 if key.lower() == b'd' else -1

            # Tentukan sumbu rotasi
            if current_face_to_rotate == 0:  # Kiri
                rotation_axis = 'x'
            elif current_face_to_rotate == 1:  # Kanan
                rotation_axis = 'x'
            elif current_face_to_rotate == 2:  # Atas
                rotation_axis = 'y'
            elif current_face_to_rotate == 3:  # Bawah
                rotation_axis = 'y'
            elif current_face_to_rotate == 4:  # Depan
                rotation_axis = 'z'
            elif current_face_to_rotate == 5:  # Belakang
                rotation_axis = 'z'

            scramble_moves.append((current_face_to_rotate, rotation_direction))
            glutPostRedisplay()
        elif key.lower() == b'r':  # Reset/Solve
            is_solving = True
            perform_solve_step()

def perform_solve_step():
    global is_animating, current_face_to_rotate, rotation_direction, temp_rubik_holder, scramble_moves, is_solving, rotation_axis
    if scramble_moves:
        move = scramble_moves.pop()
        is_animating = True
        current_face_to_rotate = move[0]
        rotation_direction = -move[1]  # Kebalikan dari gerakan asli
        temp_rubik_holder = rubik_holder.copy()
        
        # Tentukan sumbu rotasi
        if current_face_to_rotate == 0:
            rotation_axis = 'x'
        elif current_face_to_rotate == 1:
            rotation_axis = 'x'
        elif current_face_to_rotate == 2:
            rotation_axis = 'y'
        elif current_face_to_rotate == 3:
            rotation_axis = 'y'
        elif current_face_to_rotate == 4:
            rotation_axis = 'z'
        elif current_face_to_rotate == 5:
            rotation_axis = 'z'
    else:
        is_solving = False

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Rubik's Cube 3D - Interactive")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)
    glutPassiveMotionFunc(passive_motion)
    glutMouseWheelFunc(mouse_wheel)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(animate)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
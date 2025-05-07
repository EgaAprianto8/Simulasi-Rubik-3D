# rubik_utils.py

from OpenGL.GLUT import glutPostRedisplay
import rubik_globals as g

def animate():
    if g.is_animating:
        g.current_rotation_angle += g.rotation_speed * g.rotation_direction
        if abs(g.current_rotation_angle) >= 90:
            g.is_animating = False
            g.current_rotation_angle = 0
            g.rubik_holder.rotate_face(g.current_face_to_rotate, g.rotation_direction)
            g.temp_rubik_holder = None
            if g.is_solving and g.scramble_moves:
                perform_solve_step()
        glutPostRedisplay()

def perform_solve_step():
    if g.scramble_moves:
        move = g.scramble_moves.pop()
        g.is_animating = True
        g.current_face_to_rotate = move[0]
        g.rotation_direction = -move[1]
        g.temp_rubik_holder = g.rubik_holder.copy()
        if g.current_face_to_rotate == 0:
            g.rotation_axis = 'x'
        elif g.current_face_to_rotate == 1:
            g.rotation_axis = 'x'
        elif g.current_face_to_rotate == 2:
            g.rotation_axis = 'y'
        elif g.current_face_to_rotate == 3:
            g.rotation_axis = 'y'
        elif g.current_face_to_rotate == 4:
            g.rotation_axis = 'z'
        elif g.current_face_to_rotate == 5:
            g.rotation_axis = 'z'
    else:
        g.is_solving = False
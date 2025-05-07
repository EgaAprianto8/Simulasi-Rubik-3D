# rubik_input_handler.py

from OpenGL.GLUT import *
import rubik_globals as g
from rubik_renderer import get_face_from_position

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if not g.is_animating:
                g.selected_face = get_face_from_position(x, y)
                g.mouseDown = True
                g.mouseX = x
                g.mouseY = y
            glutPostRedisplay()
        elif state == GLUT_UP:
            g.mouseDown = False

def passive_motion(x, y):
    if not g.is_animating:
        g.hovered_face = get_face_from_position(x, y)
        glutPostRedisplay()

def mouse_motion(x, y):
    if g.mouseDown and not g.is_animating:
        dx = x - g.mouseX
        dy = y - g.mouseY
        g.angleX += dy * 0.5
        g.angleY += dx * 0.5
        g.mouseX = x
        g.mouseY = y
        glutPostRedisplay()

def mouse_wheel(button, dir, x, y):
    g.zoom += 1 if dir > 0 else -1
    g.zoom = max(-50, min(-5, g.zoom))
    glutPostRedisplay()

def keyboard(key, x, y):
    if key == b'\x1b':
        import sys
        sys.exit(0)
    elif g.selected_face is not None and not g.is_animating:
        if key.lower() in [b'a', b'd']:
            g.is_animating = True
            g.current_face_to_rotate = g.selected_face
            g.temp_rubik_holder = g.rubik_holder.copy()
            g.rotation_direction = 1 if key.lower() == b'd' else -1
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
            g.scramble_moves.append((g.current_face_to_rotate, g.rotation_direction))
            glutPostRedisplay()
        elif key.lower() == b'r':
            g.is_solving = True
            from rubik_utils import perform_solve_step
            perform_solve_step()
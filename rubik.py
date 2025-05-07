# rubik.py

import sys
from OpenGL.GLUT import *
from rubik_renderer import display, reshape, init
from rubik_input_handler import mouse, passive_motion, mouse_motion, mouse_wheel, keyboard
from rubik_utils import animate

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
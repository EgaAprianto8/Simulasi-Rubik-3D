# rubik_globals.py

angleX = 45
angleY = 45
zoom = -20

mouseDown = False
mouseX = 0
mouseY = 0

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
rotation_speed = 5
rotation_sign = [1, -1, -1, 1, -1, 1]

from rubik_color_holder import RubikColorHolder
rubik_holder = RubikColorHolder()
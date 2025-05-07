# rubik_color_holder.py

import rubik_globals as g

class RubikColorHolder:
    def __init__(self):
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
        new_face = [0] * 9
        for i in range(3):
            for j in range(3):
                if direction == 1:
                    new_face[j * 3 + (2-i)] = self.sides[face][i * 3 + j]
                else:
                    new_face[(2-j) * 3 + i] = self.sides[face][i * 3 + j]
        self.sides[face] = new_face

        if face == 0:
            old_F_l = [self.sides[4][0], self.sides[4][3], self.sides[4][6]]
            old_U_l = [self.sides[2][0], self.sides[2][3], self.sides[2][6]]
            old_B_l = [self.sides[5][0], self.sides[5][3], self.sides[5][6]]
            old_D_l = [self.sides[3][0], self.sides[3][3], self.sides[3][6]]
            if direction == 1:
                self.sides[4][0:7:3] = old_U_l
                self.sides[2][0:7:3] = old_B_l
                self.sides[5][0:7:3] = old_D_l
                self.sides[3][0:7:3] = old_F_l
            else:
                self.sides[4][0:7:3] = old_D_l
                self.sides[3][0:7:3] = old_B_l
                self.sides[5][0:7:3] = old_U_l
                self.sides[2][0:7:3] = old_F_l
        elif face == 1:
            old_F_r = [self.sides[4][2], self.sides[4][5], self.sides[4][8]]
            old_U_r = [self.sides[2][2], self.sides[2][5], self.sides[2][8]]
            old_B_r = [self.sides[5][2], self.sides[5][5], self.sides[5][8]]
            old_D_r = [self.sides[3][2], self.sides[3][5], self.sides[3][8]]
            if direction == 1:
                self.sides[4][2:9:3] = old_U_r
                self.sides[2][2:9:3] = old_B_r
                self.sides[5][2:9:3] = old_D_r
                self.sides[3][2:9:3] = old_F_r
            else:
                self.sides[4][2:9:3] = old_D_r
                self.sides[3][2:9:3] = old_B_r
                self.sides[5][2:9:3] = old_U_r
                self.sides[2][2:9:3] = old_F_r
        elif face == 2:
            old_F_t = [self.sides[4][0], self.sides[4][1], self.sides[4][2]]
            old_R_t = [self.sides[1][0], self.sides[1][1], self.sides[1][2]]
            old_B_t = [self.sides[5][0], self.sides[5][1], self.sides[5][2]]
            old_L_t = [self.sides[0][0], self.sides[0][1], self.sides[0][2]]
            if direction == 1:
                self.sides[4][0:3] = old_R_t
                self.sides[1][0:3] = old_B_t
                self.sides[5][0:3] = old_L_t
                self.sides[0][0:3] = old_F_t
            else:
                self.sides[4][0:3] = old_L_t
                self.sides[0][0:3] = old_B_t
                self.sides[5][0:3] = old_R_t
                self.sides[1][0:3] = old_F_t
        elif face == 3:
            old_F_b = [self.sides[4][6], self.sides[4][7], self.sides[4][8]]  # Baris bawah Depan
            old_L_b = [self.sides[0][6], self.sides[0][7], self.sides[0][8]]  # Baris bawah Kiri
            old_B_b = [self.sides[5][6], self.sides[5][7], self.sides[5][8]]  # Baris bawah Belakang
            old_R_b = [self.sides[1][6], self.sides[1][7], self.sides[1][8]]  # Baris bawah Kanan
            if direction == 1:
                self.sides[4][6:9] = old_L_b
                self.sides[0][6:9] = old_B_b
                self.sides[5][6:9] = old_R_b
                self.sides[1][6:9] = old_F_b
            else:
                self.sides[4][6:9] = old_R_b
                self.sides[1][6:9] = old_B_b
                self.sides[5][6:9] = old_L_b
                self.sides[0][6:9] = old_F_b
        elif face == 4:
            old_U_b = [self.sides[2][6], self.sides[2][7], self.sides[2][8]]
            old_L_r = [self.sides[0][2], self.sides[0][5], self.sides[0][8]]
            old_D_t = [self.sides[3][0], self.sides[3][1], self.sides[3][2]]
            old_R_l = [self.sides[1][0], self.sides[1][3], self.sides[1][6]]
            if direction == 1:
                self.sides[2][6:9] = old_L_r
                self.sides[0][2:9:3] = old_D_t
                self.sides[3][0:3] = old_R_l
                self.sides[1][0:7:3] = old_U_b
            else:
                self.sides[2][6:9] = old_R_l
                self.sides[1][0:7:3] = old_D_t
                self.sides[3][0:3] = old_L_r
                self.sides[0][2:9:3] = old_U_b
        elif face == 5:
            old_U_t = [self.sides[2][0], self.sides[2][1], self.sides[2][2]]
            old_R_r = [self.sides[1][2], self.sides[1][5], self.sides[1][8]]
            old_D_b = [self.sides[3][6], self.sides[3][7], self.sides[3][8]]
            old_L_l = [self.sides[0][0], self.sides[0][3], self.sides[0][6]]
            if direction == 1:
                self.sides[2][0:3] = old_R_r
                self.sides[1][2:9:3] = old_D_b
                self.sides[3][6:9] = old_L_l
                self.sides[0][0:7:3] = old_U_t
            else:
                self.sides[2][0:3] = old_L_l
                self.sides[0][0:7:3] = old_D_b
                self.sides[3][6:9] = old_R_r
                self.sides[1][2:9:3] = old_U_t
        self.validate_cube()
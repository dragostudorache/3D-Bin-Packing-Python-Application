import pygame
import copy
from math import ceil
class Container(object):
    def __init__(self, surface, width, height, depth, window_dimensions):
        self.surface = surface

        self.window_size = window_dimensions
        self.center_coords = (self.window_size[0] // 2, self.window_size[1] // 2)

        # dimensions
        self.width = width
        self.height = height
        self.depth = depth

        # conditions
        if self.width <= 0 or self.height <= 0 or self.depth <= 0:
            print("Wrong bin dimensions")
            exit(10)

        # bin's items
        self.items = []

        self.remaining_space = self.width * self.height * self.depth

        # 3D representation for the bin
        self.vector_3D = []
        self.build_vector()

        # some values
        self.pixel_height = self.center_coords[1]
        self.pixel_width = self.width * self.pixel_height // self.height
        self.pixel_depth = self.depth * self.pixel_height // self.height

        # if you're confused and wanna know what corner is each letter check 'scheme.png' from project files
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.B_1 = 0
        self.C_1 = 0
        self.calculate_values()

    def get_points(self):
        # Get self.A
        self.A = (self.center_coords[0], self.center_coords[1] - self.pixel_height)

        # Get self.B
        a1 = self.pixel_depth * 0.5  # sin30 = 0.5
        b1 = self.pixel_depth * 0.86  # cos30 = 0.86
        bx = self.center_coords[0] - b1
        by = self.center_coords[1] + a1
        self.B = (bx, by)
        self.B_1 = (bx, by - self.pixel_height)

        # Get self.C
        a2 = self.pixel_width * 0.5
        b2 = self.pixel_width * 0.86
        cx = self.center_coords[0] + b2
        cy = self.center_coords[1] + a2
        self.C = (cx, cy)
        self.C_1 = (cx, cy - self.pixel_height)

        # Get self.D
        dx = bx + b2
        dy = by + a2
        self.D = (dx, dy)

    def check_current_points(self):
        if self.B[0] < 0 or self.B[1] > self.window_size[1]:
            return False

        if self.C[0] > self.window_size[0] or self.C[1] > self.window_size[1]:
            return False

        if self.D[0] < 0 or self.D[0] > self.window_size[0] or self.D[1] > self.window_size[1]:
            return False

        return True

    def calculate_values(self):
        # calculate points coords, see scheme.png to understand the calculs
        self.get_points()

        # check if they are in drawing_are
        while not self.check_current_points():
            # if they are, stop loop
            # else decrease self.pixel_height and calculate the points again
            self.pixel_height -= 1
            self.pixel_width = self.width * self.pixel_height // self.height
            self.pixel_depth = self.depth * self.pixel_height // self.height
            self.get_points()

    def build_vector(self):
        # 3D - Vector
        for i in range(0, self.width):
            new_list1 = []

            for j in range(0, self.height):
                new_list2 = []

                for k in range(0, self.depth):
                    new_list2.append(0)

                new_list1.append(new_list2)

            self.vector_3D.append(new_list1)

    def print_data(self):
        print(self.width, "x", self.height, "x", self.depth, "|", len(self.items), "items |", self.remaining_space, "remaining space")

    def pack(self, item, position, type):
        # add item to packed items
        self.items.append(item)

        # edit 3D vector
        for i in range(position[0], position[0] + item.rotate(type)[0]):
            for j in range(position[1], position[1] + item.rotate(type)[1]):
                for k in range(position[2], position[2] + item.rotate(type)[2]):
                    self.vector_3D[i][j][k] = 1

        # edit remaining space
        volume = item.width * item.height * item.depth
        self.remaining_space -= volume

        # edit item's info
        item.pos = copy.deepcopy(list(position))
        item.RT = type

    def can_be_packed(self, item, position, type):
        for i in range(position[0], position[0] + item.rotate(type)[0]):
            for j in range(position[1], position[1] + item.rotate(type)[1]):
                for k in range(position[2], position[2] + item.rotate(type)[2]):
                    # check for bin's limits
                    if i >= self.width or j >= self.height or k >= self.depth:
                        return False

                    # check if the space is already used
                    if self.vector_3D[i][j][k] == 1:
                        return False

        # check if the item above another item has at least half of its dimension on the underitem
        if position[1] >= 1:
            for i in range(position[0], ceil((position[0] + item.rotate(type)[0]) / 2)):
                for k in range(position[2], ceil((position[2] + item.rotate(type)[2]) / 2)):
                    if self.vector_3D[i][position[1] - 1][k] == 0:
                        return False

        return True

    def draw_container(self):
        # draw outlines
        points = [self.A, self.B_1, self.B, self.center_coords, self.A]
        pygame.draw.lines(self.surface, (0, 0, 0), False, points, 2)

        points = [self.A, self.C_1, self.C, self.center_coords]
        pygame.draw.lines(self.surface, (0, 0, 0), False, points, 2)

        points = [self.C, self.D, self.B]
        pygame.draw.lines(self.surface, (0, 0, 0), False, points, 2)

        # grid lines
        for i in range(1, self.depth):
            # get that "M" point, see scheme2.png if you wanna understand these calculs
            k = (self.depth - i) / i
            mx = (self.B[0] + k * self.center_coords[0]) / (k + 1)
            my = (self.B[1] + k * self.center_coords[1]) / (k + 1)

            # up grid line
            pygame.draw.line(self.surface, (0, 0, 0), (mx, my), (mx, my - self.pixel_height))
            pygame.draw.line(self.surface, (0, 0, 0), (mx, my), (mx + (self.C[0] - self.center_coords[0]), my + (self.C[1] - self.center_coords[1])))

        for i in range(1, self.width):
            # get that "M" point, see scheme2.png if you wanna understand these calculs
            k = (self.width - i) / i
            mx = (self.C[0] + k * self.center_coords[0]) / (k + 1)
            my = (self.C[1] + k * self.center_coords[1]) / (k + 1)

            # up grid line
            pygame.draw.line(self.surface, (0, 0, 0), (mx, my), (mx, my - self.pixel_height))
            pygame.draw.line(self.surface, (0, 0, 0), (mx, my), (mx - (self.center_coords[0] - self.B[0]), my + (self.B[1] - self.center_coords[1])))

        for i in range(1, self.height):
            u_m = self.pixel_height / self.height
            start_pos = (self.B[0], self.B[1] - i * u_m)
            end_pos = (self.center_coords[0], self.center_coords[1] - i * u_m)
            pygame.draw.line(self.surface, (0, 0, 0), start_pos, end_pos)
            start_pos = (self.C[0], self.C[1] - i * u_m)
            pygame.draw.line(self.surface, (0, 0, 0), end_pos, start_pos)
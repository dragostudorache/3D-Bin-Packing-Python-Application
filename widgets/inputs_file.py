import pygame
import copy

class input(object):
    def __init__(self, surface, type, text, free_space, limits, text_color, background_color, font_size):
        self.surface = surface
        self.type = type
        self.text = text
        self.free_space = free_space
        self.limits = limits
        self.values = 0
        if self.type == "normal":
            self.values = "1"
        else:
            self.values = ("1", "1")
        self.input_size = (0, 0)
        self.text_color = text_color
        self.background_color = background_color

        self.font_size = font_size
        self.font = pygame.font.Font('res\\Rubik-Regular.ttf', self.font_size)
        self.status = "not focused"
        self.press_pause = 6

    def display_input(self):
        text = self.font.render(self.text, True, self.text_color, self.background_color)
        text_rect = text.get_rect()
        self.input_size = text.get_size()
        text_rect.center = (self.free_space[0] + self.free_space[2] // 8 + self.input_size[0] // 2, self.free_space[1] + self.input_size[1] // 2)

        self.surface.blit(text, text_rect)

        # fields
        text = self.font.render(self.values, True, self.text_color, self.background_color)
        text_rect = text.get_rect()
        text_rect.center = (self.free_space[0] + 3 * self.free_space[2] // 4, self.free_space[1] + self.input_size[1] // 2)

        self.surface.blit(text, text_rect)

        points = [
            (self.free_space[0] + 5 * self.free_space[2] // 8, self.free_space[1]),
            (self.free_space[0] + 5 * self.free_space[2] // 8, self.free_space[1] + self.input_size[1]),
            (self.free_space[0] + 7 * self.free_space[2] // 8, self.free_space[1] + self.input_size[1]),
            (self.free_space[0] + 7 * self.free_space[2] // 8, self.free_space[1])
        ]
        pygame.draw.lines(self.surface, self.text_color, False, points, 3)

        # highlights for inputs (top line)
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if mouse_pos[0] >= points[0][0] and \
                mouse_pos[0] <= points[2][0] and \
                mouse_pos[1] >= points[0][1] and \
                mouse_pos[1] <= points[1][1]:
                self.status = "focused"
            else:
                self.status = "not focused"
        if self.status == "focused":
            pygame.draw.line(self.surface, self.text_color, points[0], points[3], 3)
            self.values = self.typing(self.values, self.limits)
        if self.status == "not focused":
            if self.values == "":
                self.values = str(self.limits[0])

    def typing(self, text, nr_limits):
        if len(text) >= len(str(self.limits[1])) + 1:
            return text
        elif self.press_pause >= 6:
            auxText = copy.deepcopy(text)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_0] == True and len(text) != 0:
                text += "0"
            if keys[pygame.K_1]:
                text += "1"
            if keys[pygame.K_2]:
                text += "2"
            if keys[pygame.K_3]:
                text += "3"
            if keys[pygame.K_4]:
                text += "4"
            if keys[pygame.K_5]:
                text += "5"
            if keys[pygame.K_6]:
                text += "6"
            if keys[pygame.K_7]:
                text += "7"
            if keys[pygame.K_8]:
                text += "8"
            if keys[pygame.K_9]:
                text += "9"
            if keys[pygame.K_BACKSPACE]:
                text = copy.deepcopy(text[:(len(text) - 1)])
            if text != auxText:
                self.press_pause = 0
        else:
            if pygame.key.get_focused():
                self.press_pause += 1
        if len(text) == 0:
            return ""
        elif int(text) > nr_limits[1]:
            return str(nr_limits[1])
        else:
            return text
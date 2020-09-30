import pygame
import copy
class icon_Button(object):
    def __init__(self, surface, rect, icon_color, background_color, draw_function):
        self.surface = surface
        self.rect = rect

        self.icon_color = icon_color
        self.aux_icon_color = icon_color

        self.background_color = background_color
        self.aux_background_color = background_color
        self.draw_function = draw_function
        self.status = "not pressed"
        self.over_status = "not over"

        self.press_delay = 10

    def display_button(self):
        pygame.draw.rect(self.surface, self.background_color, self.rect)
        self.draw_function(self.surface, self.rect, self.icon_color, self.background_color)

    def check_for_action(self):
        mouse_pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] and self.press_delay >= 10:
            if mouse_pos[0] >= self.rect[0] and \
                mouse_pos[0] <= self.rect[0] + self.rect[2] and \
                mouse_pos[1] >= self.rect[1] and \
                mouse_pos[1] <= self.rect[1] + self.rect[3]:
                self.status = "pressed"
                self.press_delay = 0
        else:
            self.status = "not pressed"
            self.press_delay += 1
        if mouse_pos[0] >= self.rect[0] and \
            mouse_pos[0] <= self.rect[0] + self.rect[2] and \
            mouse_pos[1] >= self.rect[1] and \
            mouse_pos[1] <= self.rect[1] + self.rect[3]:
            self.icon_color = self.aux_background_color
            self.background_color = self.aux_icon_color
            self.over_status = "over"
        else:
            self.icon_color = self.aux_icon_color
            self.background_color = self.aux_background_color
            self.over_status = "not over"

class Button(object):
    def __init__(self, surface, position, text, text_color, background_color, font_size):
        self.surface = surface
        self.position = position

        self.button_text = text

        self.text_color = text_color
        self.aux_text_color = text_color

        self.background_color = background_color
        self.aux_background_color = background_color

        self.boarders_color = text_color

        self.font_size = font_size
        self.font = pygame.font.Font('res\\Rubik-Regular.ttf', self.font_size)

        self.button_size = 0
        self.status = "not pressed"

        self.press_delay = 10

    def display_button(self):
        text = self.font.render(self.button_text, True, self.text_color, self.background_color)
        text_rect = text.get_rect()
        self.button_size = text.get_size()
        text_rect.center = (self.position[0], self.position[1] + self.button_size[1] // 2)

        rect = (self.position[0] - self.button_size[0] // 2 - self.button_size[0] // 10, self.position[1], 12 * self.button_size[0] // 10, self.button_size[1])
        pygame.draw.rect(self.surface, self.background_color, rect)
        self.surface.blit(text, text_rect)

        # borders
        points = [
            (self.position[0] - self.button_size[0] // 2 - self.button_size[0] // 10, self.position[1]),
            (self.position[0] - self.button_size[0] // 2 - self.button_size[0] // 10, self.position[1] + self.button_size[1]),
            (self.position[0] + 6 * self.button_size[0] // 10, self.position[1] + self.button_size[1]),
            (self.position[0] + 6 * self.button_size[0] // 10, self.position[1])
        ]
        pygame.draw.lines(self.surface, self.boarders_color, True, points, 3)

    def check_for_action(self):
        if type(self.button_size) != tuple:
            print("check after displaying it!")
            exit()

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.press_delay >= 10:
            if mouse_pos[0] >= self.position[0] - self.button_size[0] // 2 and \
                mouse_pos[0] <= self.position[0] + self.button_size[0] // 2 and \
                mouse_pos[1] >= self.position[1] and \
                mouse_pos[1] <= self.position[1] + self.button_size[1]:
                self.status = "pressed"
                self.press_delay = 0
        else:
            self.status = "not pressed"
            self.press_delay += 1

        if mouse_pos[0] >= self.position[0] - self.button_size[0] // 2 and \
                mouse_pos[0] <= self.position[0] + self.button_size[0] // 2 and \
                mouse_pos[1] >= self.position[1] and \
                mouse_pos[1] <= self.position[1] + self.button_size[1]:
                self.text_color = self.aux_background_color
                self.background_color = self.aux_text_color
        else:
            self.text_color = self.aux_text_color
            self.background_color = self.aux_background_color
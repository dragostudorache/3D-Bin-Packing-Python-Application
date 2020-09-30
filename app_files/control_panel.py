import pygame
from app_files.container import Container
import copy
from widgets.buttons_file import Button, icon_Button
from app_files.items_panel import items_panel
import app_files._3dbp as _3dbp
from widgets.symbols_file import draw_left_arrow_icon, draw_right_arrow_icon, draw_double_left_arrow_icon, draw_double_right_arrow_icon

class control_panel(object):
    def __init__(self, surface, window_size):
        self.surface = surface
        self.window_size = window_size
        #                        Container(surface, width, height, depth, (dimensions) - (3/4, full)
        self.current_container = Container(self.surface, 1, 1, 1, (3 * self.window_size[0] // 4, self.window_size[1]))

        # the text from container input fields
        self.width_field_text = "1"
        self.height_field_text = "1"
        self.depth_field_text = "1"

        # for mouse click, to not click 100 times at once
        self.press_pause = 6

        # increasing font depends on window size
        # An usual resolution is 1920x1080(16:9), after this resolution I calculate some multipliers for different things
        self.increase_font = self.window_size[0] // 1920

        # that's for smth else but in first place i named it that way and I'm too lazy to edit it for the moment :)
        self.increase_font2 = self.increase_font
        if self.increase_font == 0:
            self.increase_font2 = 1

        # ARGUMENTS:
            # surface
            # self.window_size - to know how big will the widgets and other things be
            # 0, 0 - top and bottom limit for items panel. It's 0, 0 for the moment, The values are going to be calculated later after I place other things.
            # font size - The minimal value is 15, I add to it other 10 * self.increase_font pixels depends on self.increase_font
            # font color
            # background color
        self.items_panel = items_panel(self.surface, self.window_size, 0, 0, 15 + self.increase_font * 10, (50, 55, 64), (255, 255, 255))

        # container buttons
        # ARGUMENTS:
            # surface
            # The position of the button
                # (x, y). x is 7/8 from window width because I want the button to be in the center of the forth 1/4 of the window. Yeah it sounds complicated but it is not
                # y is 0 because I'm gonna calculated it apart for every button later
            # button text
            # font color
            # background color
            # font size - I explained why I calculated it like that above(line 36)
        self.generate = Button(self.surface, (7 * self.window_size[0] // 8, 0), "Generate", (255, 255, 255), (50, 55, 64), 30 + self.increase_font * 30)
        self.restore_items = Button(self.surface, (13 * self.window_size[0] // 16, 0), "Restore items", (255, 255, 255), (50, 55, 64), 15 + self.increase_font * 10)
        self.remove_items = Button(self.surface, (15 * self.window_size[0] // 16, 0), "Remove items", (255, 255, 255), (50, 55, 64), 15 + self.increase_font * 10)

        # ARGUMENTS:
            #......
            # The position of the button
                # x is 13/16 because I want the button to be in the center of the first half of the forth 1/4 of the window
                # and 15/16 is the second half of the forth 1/4 of the window
            #.......
        self.pack_items = Button(self.surface, (13 * self.window_size[0] // 16, 0), "Pack items", (255, 255, 255), (50, 55, 64), 15 + self.increase_font * 10)
        self.close_app = Button(self.surface, (15 * self.window_size[0] // 16, 0), "Close app", (255, 0, 0), (50, 55, 64), 15 + self.increase_font * 10)

        # I want two font sizes
        # Yes, I can have any size but if I wanna change it I need to reload the font, so it's better if I have just two versions but I don't reload the font every time
            # big version
        self.big_font = pygame.font.Font('res\\Rubik-Regular.ttf', 30 + self.increase_font * 30)

            # small version
        self.small_font = pygame.font.Font('res\\Rubik-Regular.ttf', 15 + self.increase_font * 10)

        # for fields complete, I need it to know in what input field I currently typing
        # 0 - none
        # 1 - ..
        self.current_completing_container = 0

        # the positions for the highlight rect for current input field which is used
        self.start_pos_container_highlight = 0
        self.end_pos_container_highlight = 0

        # I calculate these and after that I pass them to items_panel top and bottom limits
        self.top_margin_for_pack_panel = 0
        self.bottom_margin_for_pack_panel = 0

        # info window vars
        # just estetic stuffs
        self.open_flag = False
        self.start_animation_flag = False
        self.current_window_info_rect = (3 * self.window_size[0] // 4, self.window_size[1] // 20, self.window_size[0] // 4, self.window_size[1] // 3)
        open_info_button_rect = (
                self.current_window_info_rect[0] - self.window_size[1] // 20,
                self.current_window_info_rect[1] + self.current_window_info_rect[3] // 2 - self.window_size[1] // 20,
                self.window_size[1] // 20,
                self.window_size[1] // 10
        )
        self.open_info_window_button = icon_Button(self.surface, open_info_button_rect, (0, 0, 0), (37, 43, 54), draw_left_arrow_icon)
        self.animation_velocity = 25

        # what packing stage to display
        self.display_items_stage = 0

        # other buttons
        self.move_to_first_stage = icon_Button(self.surface, (0, 0, 0, 0), (37, 43, 54), (255, 255, 255), draw_double_left_arrow_icon)
        self.move_to_before_stage = icon_Button(self.surface, (0, 0, 0, 0), (37, 43, 54), (255, 255, 255), draw_left_arrow_icon)
        self.move_to_next_stage = icon_Button(self.surface, (0, 0, 0, 0), (37, 43, 54), (255, 255, 255), draw_right_arrow_icon)
        self.move_to_last_stage = icon_Button(self.surface, (0, 0, 0, 0), (37, 43, 54), (255, 255, 255), draw_double_right_arrow_icon)

        self.total_items = 0

        # show items vars
        # for bin items to differentiate the boxes
        self.current_item_color = 240

    def show_content(self):
        self.current_container.draw_container()

        self.draw_container_items()

        self.draw_info_section()

        # control panel background
        coords = (3 * self.window_size[0] // 4, 0, self.window_size[0] // 4, self.window_size[1])
        pygame.draw.rect(self.surface, (50, 55, 64), coords)

        # display container panel
        self.container_panel()

        self.packing_panel()

    # visual prioritization
    def set_priorities(self, items_list):
        for i in range(len(items_list)):
            for j in range((len(items_list))):
                ok = False
                if i < j:
                    if items_list[i].pos[0] + items_list[i].rotate(items_list[i].RT)[0] <= items_list[j].pos[0]:
                        ok = True

                    if items_list[i].pos[1] + items_list[i].rotate(items_list[i].RT)[1] <= items_list[j].pos[1]:
                        ok = True

                    if items_list[i].pos[2] + items_list[i].rotate(items_list[i].RT)[2] <= items_list[j].pos[2]:
                        ok = True

                if ok == False and i < j:
                    items_list[i], items_list[j] = items_list[j], items_list[i]

        return items_list

    def draw_container_items(self):
        items_to_show = []
        if self.display_items_stage != 0:
            for i in range(self.display_items_stage):
                items_to_show.append(self.current_container.items[i])

            items_to_show = self.set_priorities(items_to_show)

            b = (self.current_container.C[0] - self.current_container.center_coords[0]) // self.current_container.width
            a = (self.current_container.C[1] - self.current_container.center_coords[1]) // self.current_container.width

            height = self.current_container.pixel_height // self.current_container.height

            color_i = 0
            for item in items_to_show:
                item_color = (self.current_item_color - (color_i % 12) * 20, self.current_item_color - (color_i % 12) * 20, self.current_item_color - (color_i % 12) * 20)
                color_i += 1
                # left part
                if item.rotate(item.RT)[0] > item.rotate(item.RT)[2]:
                    min_or_max = min(item.rotate(item.RT)[0], item.rotate(item.RT)[2])
                else:
                    min_or_max = max(item.rotate(item.RT)[0], item.rotate(item.RT)[2])
                points = (
                    (self.current_container.center_coords[0] + (item.pos[0] - item.pos[2]) * b - item.rotate(item.RT)[2] * b, self.current_container.center_coords[1] + (item.pos[0] + item.pos[2] + min_or_max) * a - item.pos[1] * height),
                    (self.current_container.center_coords[0] + (item.pos[0] - item.pos[2]) * b - item.rotate(item.RT)[2] * b, self.current_container.center_coords[1] + (item.pos[0] + item.pos[2] + min_or_max) * a - item.pos[1] * height - item.rotate(item.RT)[1] * height),
                    (self.current_container.center_coords[0] + (item.pos[0] - item.pos[2]) * b - item.rotate(item.RT)[2] * b + item.rotate(item.RT)[0] * b, self.current_container.center_coords[1] + (item.pos[0] + item.pos[2] + min_or_max) * a - item.pos[1] * height + item.rotate(item.RT)[0] * a - item.rotate(item.RT)[1] * height),
                    (self.current_container.center_coords[0] + (item.pos[0] - item.pos[2]) * b - item.rotate(item.RT)[2] * b + item.rotate(item.RT)[0] * b, self.current_container.center_coords[1] + (item.pos[0] + item.pos[2] + min_or_max) * a - item.pos[1] * height + item.rotate(item.RT)[0] * a)
                )
                pygame.draw.polygon(self.surface, item_color, points)
                pygame.draw.lines(self.surface, (0, 0, 0), True, points)

                points2 = (
                    points[1],
                    points[2],
                    (points[2][0] + item.rotate(item.RT)[2] * b, points[2][1] - item.rotate(item.RT)[2] * a),
                    (points[1][0] + item.rotate(item.RT)[2] * b, points[1][1] - item.rotate(item.RT)[2] * a)
                )
                pygame.draw.polygon(self.surface, item_color, points2)
                pygame.draw.lines(self.surface, (0, 0, 0), True, points2)

                points3 = (
                    points[3],
                    points[2],
                    points2[2],
                    (points[3][0] + item.rotate(item.RT)[2] * b, points[3][1] - item.rotate(item.RT)[2] * a)
                )
                pygame.draw.polygon(self.surface, item_color, points3)
                pygame.draw.lines(self.surface, (0, 0, 0), True, points3)

    def draw_info_section(self):
        pygame.draw.rect(self.surface, (37, 43, 54), self.current_window_info_rect)
        self.open_info_window_button.display_button()
        self.open_info_window_button.check_for_action()
        if self.open_info_window_button.status == "pressed":
            self.start_animation_flag = True

        if self.start_animation_flag == True:
            if self.open_flag == False:
                if self.current_window_info_rect[0] - self.animation_velocity >= self.window_size[0] // 2:
                    self.current_window_info_rect = (self.current_window_info_rect[0] - self.animation_velocity, self.window_size[1] // 20, self.window_size[0] // 4, self.window_size[1] // 3)
                else:
                    self.current_window_info_rect = (self.window_size[0] // 2, self.window_size[1] // 20, self.window_size[0] // 4, self.window_size[1] // 3)

                if self.current_window_info_rect[0] == self.window_size[0] // 2:
                    self.start_animation_flag = False
                    self.open_flag = True
                self.open_info_window_button.draw_function = draw_right_arrow_icon
            else:
                if self.current_window_info_rect[0] + self.animation_velocity <= 3 * self.window_size[0] // 4:
                    self.current_window_info_rect = (self.current_window_info_rect[0] + self.animation_velocity, self.window_size[1] // 20, self.window_size[0] // 4, self.window_size[1] // 3)
                else:
                    self.current_window_info_rect = (3 * self.window_size[0] // 4, self.window_size[1] // 20, self.window_size[0] // 4, self.window_size[1] // 3)

                if self.current_window_info_rect[0] == 3 * self.window_size[0] // 4:
                    self.start_animation_flag = False
                    self.open_flag = False
                self.open_info_window_button.draw_function = draw_left_arrow_icon

        open_info_button_rect = (
            self.current_window_info_rect[0] - self.window_size[1] // 20,
            self.current_window_info_rect[1] + self.current_window_info_rect[3] // 2 - self.window_size[1] // 20,
            self.window_size[1] // 20,
            self.window_size[1] // 10
        )
        self.open_info_window_button.rect = open_info_button_rect

        # stage text and stage buttons
        text = self.small_font.render(str(self.display_items_stage) + "/" + str(len(self.current_container.items)) , True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + self.current_window_info_rect[2] // 2, self.current_window_info_rect[1] + text.get_size()[1])

        self.surface.blit(text, text_rect)

        self.move_to_first_stage.rect = (
            self.current_window_info_rect[0] + (self.current_window_info_rect[2] - 3 * self.current_window_info_rect[3] // 4) // 2,
            self.current_window_info_rect[1] + 2 * text.get_size()[1],
            3 * self.current_window_info_rect[3] // 16,
            3 * self.current_window_info_rect[3] // 16
        )
        self.move_to_first_stage.display_button()
        self.move_to_first_stage.check_for_action()
        if self.move_to_first_stage.status == "pressed":
            self.display_items_stage = 0

        self.move_to_before_stage.rect = (
            self.current_window_info_rect[0] + (self.current_window_info_rect[2] - 3 * self.current_window_info_rect[3] // 4) // 2 + 3 * self.current_window_info_rect[3] // 16,
            self.current_window_info_rect[1] + 2 * text.get_size()[1],
            3 * self.current_window_info_rect[3] // 16,
            3 * self.current_window_info_rect[3] // 16
        )
        self.move_to_before_stage.display_button()
        self.move_to_before_stage.check_for_action()
        if self.move_to_before_stage.status == "pressed":
            if self.display_items_stage != 0:
                self.display_items_stage -= 1

        self.move_to_next_stage.rect = (
            self.current_window_info_rect[0] + (
            self.current_window_info_rect[2] - 3 * self.current_window_info_rect[3] // 4) // 2 + 2 * (3 * self.current_window_info_rect[3] // 16),
            self.current_window_info_rect[1] + 2 * text.get_size()[1],
            3 * self.current_window_info_rect[3] // 16,
            3 * self.current_window_info_rect[3] // 16
        )
        self.move_to_next_stage.display_button()
        self.move_to_next_stage.check_for_action()
        if self.move_to_next_stage.status == "pressed":
            if self.display_items_stage != len(self.current_container.items):
                self.display_items_stage += 1

        self.move_to_last_stage.rect = (
            self.current_window_info_rect[0] + (
            self.current_window_info_rect[2] - 3 * self.current_window_info_rect[3] // 4) // 2 + 3 * (3 * self.current_window_info_rect[3] // 16),
            self.current_window_info_rect[1] + 2 * text.get_size()[1],
            3 * self.current_window_info_rect[3] // 16,
            3 * self.current_window_info_rect[3] // 16
        )
        self.move_to_last_stage.display_button()
        self.move_to_last_stage.check_for_action()
        if self.move_to_last_stage.status == "pressed":
            self.display_items_stage = len(self.current_container.items)

        # some info
        texts_top_margin = self.current_window_info_rect[1] + 3 * text.get_size()[1] + 3 * self.current_window_info_rect[3] // 16

        # text
        text = self.small_font.render("Bin\'s volume", True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + self.current_window_info_rect[2] // 8 + text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # value
        text = self.small_font.render(str(self.current_container.width * self.current_container.height * self.current_container.depth), True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + 7 * self.current_window_info_rect[2] // 8 - text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # text
        texts_top_margin += text.get_size()[1]
        text = self.small_font.render("Bin\'s items volume", True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + self.current_window_info_rect[2] // 8 + text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # value

        text = self.small_font.render(str(_3dbp.get_items_total_volume(self.current_container.items)), True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + 7 * self.current_window_info_rect[2] // 8 - text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # text
        texts_top_margin += text.get_size()[1]
        text = self.small_font.render("Unpacked items volume", True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + self.current_window_info_rect[2] // 8 + text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # value

        text = self.small_font.render(str(_3dbp.get_items_total_volume(self.items_panel.items_list)), True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + 7 * self.current_window_info_rect[2] // 8 - text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # text
        texts_top_margin += text.get_size()[1]
        text = self.small_font.render("Unused space", True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + self.current_window_info_rect[2] // 8 + text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # value

        value_text = str(self.current_container.remaining_space)
        val = (100 * self.current_container.remaining_space) / (self.current_container.width * self.current_container.height * self.current_container.depth)
        value_text = value_text + "(" + '%.2f'%val
        value_text = value_text + "%)"

        text = self.small_font.render(value_text, True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + 7 * self.current_window_info_rect[2] // 8 - text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # text
        texts_top_margin += text.get_size()[1]
        text = self.small_font.render("Wasted space", True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + self.current_window_info_rect[2] // 8 + text.get_size()[0] // 2, texts_top_margin)

        self.surface.blit(text, text_rect)

        # value
        if self.total_items < self.current_container.width * self.current_container.height * self.current_container.depth:
            bin_items_volume = _3dbp.get_items_total_volume(self.current_container.items)
            wasted = self.total_items - bin_items_volume
            if self.total_items == 0:
                val = 0.00
            else:
                val = (100 * wasted) / self.total_items
            value_text = str(wasted) + "(" + '%.2f'%val + "%)"

        text = self.small_font.render(value_text, True, (255, 255, 255), (37, 43, 54))
        text_rect = text.get_rect()
        text_rect.center = (self.current_window_info_rect[0] + 7 * self.current_window_info_rect[2] // 8 - text.get_size()[0] // 2,
        texts_top_margin)

        self.surface.blit(text, text_rect)

    def packing_panel(self):
        self.items_panel.container_dimensions = (self.current_container.width, self.current_container.height, self.current_container.depth)
        bottom_margin = self.window_size[1] - self.restore_items.button_size[1] // 2 - 30 * self.increase_font2
        # Packing panel buttons

        # Close app
        self.close_app.position = (15 * self.window_size[0] // 16, bottom_margin)
        self.close_app.display_button()
        self.close_app.check_for_action()
        self.bottom_margin_for_pack_panel = bottom_margin - 30 * self.increase_font2
        # action in main file

        self.items_panel.top_limit = self.top_margin_for_pack_panel
        self.items_panel.bottom_limit = self.bottom_margin_for_pack_panel

        self.items_panel.container_volume = self.current_container.width * self.current_container.height * self.current_container.depth
        self.items_panel.show_content()

        # Pack items
        self.pack_items.position = (13 * self.window_size[0] // 16, bottom_margin)
        self.pack_items.display_button()
        self.pack_items.check_for_action()

        if self.pack_items.status == "pressed" and len(self.items_panel.items_list) != 0:
            self.items_panel.items_list = _3dbp.bp3D(self.current_container, self.items_panel.items_list)
            self.display_items_stage = len(self.current_container.items)

            self.total_items = 0
            for i in self.current_container.items:
                self.total_items = self.total_items + i.width * i.height * i.depth

            for i in self.items_panel.items_list:
                self.total_items = self.total_items + i.width * i.height * i.depth

    def container_panel(self):
        # container title
        text = self.big_font.render('Container', True, (255, 255, 255), (50, 55, 64))
        textRect = text.get_rect()

        textRect.center = (7 * self.window_size[0] // 8, 20 + text.get_size()[1] // 2)
        self.surface.blit(text, textRect)

        top_margin = 20 + text.get_size()[1]
        # container fields | texts
        self.add_text_field("Width", top_margin, 1)
        self.add_text_field("Height", top_margin, 2)
        self.add_text_field("Depth", top_margin, 3)

        # container fields | inputs
        top_margin += self.fields_code(top_margin)

        # container buttons
        # Generate
        self.generate.position = (7 * self.window_size[0] // 8, top_margin)
        self.generate.display_button()
        self.generate.check_for_action()
        if self.generate.status == "pressed":
            self.current_container = Container(self.surface, int(self.width_field_text), int(self.height_field_text), int(self.depth_field_text), (3 * self.window_size[0] // 4, self.window_size[1]))
            self.display_items_stage = 0
            self.total_items = 0

        top_margin = top_margin + self.generate.button_size[1] + self.increase_font2 * 30
        # Restore items
        self.restore_items.position = (13 * self.window_size[0] // 16, top_margin)
        self.restore_items.display_button()
        self.restore_items.check_for_action()
        # for pressed
        if self.restore_items.status == "pressed":
            for i in self.current_container.items:
                self.items_panel.items_list.append(i)
            self.current_container = Container(self.surface, int(self.width_field_text), int(self.height_field_text), int(self.depth_field_text), (3 * self.window_size[0] // 4, self.window_size[1]))
            self.total_items = 0
            self.display_items_stage = 0

        # Remove items
        self.remove_items.position = (15 * self.window_size[0] // 16, top_margin)
        self.remove_items.display_button()
        self.remove_items.check_for_action()
        # for pressed
        if self.remove_items.status == "pressed":
            self.current_container = Container(self.surface, int(self.width_field_text), int(self.height_field_text), int(self.depth_field_text), (3 * self.window_size[0] // 4, self.window_size[1]))
            self.total_items = 0
            self.display_items_stage = 0

        # Pack!
        self.top_margin_for_pack_panel = top_margin + self.restore_items.button_size[1] + 30 * self.increase_font2

    def add_text_field(self, text, top_margin, i):
        text = self.small_font.render(text, True, (255, 255, 255), (50, 55, 64))
        textRect = text.get_rect()

        textRect.center = (25 * self.window_size[0] // 32 + text.get_size()[0] // 2, top_margin + i * (self.increase_font2 * 30 + text.get_size()[1] // 2))
        self.surface.blit(text, textRect)

    def fields_code(self, top_margin):
        new_top_margin = 0
        # draw fields shapes
        texts = [self.width_field_text, self.height_field_text, self.depth_field_text]
        text = self.small_font.render(texts[1], True, (255, 255, 255), (50, 55, 64))

        for i in range(1, 4):
            # add current values
            textA = self.small_font.render(texts[i - 1], True, (255, 255, 255), (50, 55, 64))
            textARect = textA.get_rect()
            textARect.center = (59 * self.window_size[0] // 64, top_margin + i * (self.increase_font2 * 30 + text.get_size()[1] // 2))
            self.surface.blit(textA, textARect)

            # build top margin
            new_top_margin = i * (self.increase_font2 * 30 + text.get_size()[1] // 2)

            points = [
                (7 * self.window_size[0] // 8, top_margin + i * self.increase_font2 * 30 + (i - 1) * text.get_size()[1] // 2),
                (7 * self.window_size[0] // 8, top_margin + i * self.increase_font2 * 30 + (i - 1) * text.get_size()[1] // 2 + text.get_size()[1]),
                (31 * self.window_size[0] // 32, top_margin + i * self.increase_font2 * 30 + (i - 1) * text.get_size()[1] // 2 + text.get_size()[1]),
                (31 * self.window_size[0] // 32, top_margin + i * self.increase_font2 * 30 + (i - 1) * text.get_size()[1] // 2)
            ]
            pygame.draw.lines(self.surface, (255, 255, 255), False, points, 3)

        # highlights for inputs (top line)
        mouse_pos = pygame.mouse.get_pos()
        x_lim1 = 7 * self.window_size[0] // 8
        x_lim2 = 31 * self.window_size[0] // 32
        if pygame.mouse.get_pressed()[0]:
            if mouse_pos[0] >=  x_lim1 and \
                mouse_pos[0] <= x_lim2 and \
                mouse_pos[1] >= top_margin + self.increase_font2 * 30 and \
                mouse_pos[1] <= top_margin + self.increase_font2 * 30 + text.get_size()[1]:
                self.current_completing_container = 1
                self.start_pos_container_highlight = (x_lim1, top_margin + self.increase_font2 * 30)
                self.end_pos_container_highlight = (x_lim2, top_margin + self.increase_font2 * 30)
            elif mouse_pos[0] >=  x_lim1 and \
                mouse_pos[0] <= x_lim2 and \
                mouse_pos[1] >= top_margin + 2 * self.increase_font2 * 30 + text.get_size()[1] // 2 and \
                mouse_pos[1] <= top_margin + 2 * self.increase_font2 * 30 + text.get_size()[1] + text.get_size()[1] // 2:
                self.current_completing_container = 2
                self.start_pos_container_highlight = (x_lim1, top_margin + 2 * self.increase_font2 * 30 + text.get_size()[1] // 2)
                self.end_pos_container_highlight = (x_lim2, top_margin + 2 * self.increase_font2 * 30 + text.get_size()[1] // 2)
            elif mouse_pos[0] >=  x_lim1 and \
                mouse_pos[0] <= x_lim2 and \
                mouse_pos[1] >= top_margin + 3 * self.increase_font2 * 30 + 2 * text.get_size()[1] // 2 and \
                mouse_pos[1] <= top_margin + 3 * self.increase_font2 * 30 + text.get_size()[1] + 2 * text.get_size()[1] // 2:
                self.current_completing_container = 3
                self.start_pos_container_highlight = (x_lim1, top_margin + 3 * self.increase_font2 * 30 + 2 * text.get_size()[1] // 2)
                self.end_pos_container_highlight = (x_lim2, top_margin + 3 * self.increase_font2 * 30 + 2 * text.get_size()[1] // 2)
            else:
                self.current_completing_container = 0
                if self.width_field_text == "":
                    self.width_field_text = "1"
                if self.height_field_text == "":
                    self.height_field_text = "1"
                if self.depth_field_text == "":
                    self.depth_field_text = "1"

        if self.current_completing_container != 0:
            # draw top line if exists
            pygame.draw.line(self.surface, (255, 255, 255), self.start_pos_container_highlight, self.end_pos_container_highlight, 3)

            # add current value to inputs
            if self.current_completing_container == 1:
                self.width_field_text = self.typing(self.width_field_text, (1, 300))
                if self.height_field_text == "":
                    self.height_field_text = "1"
                if self.depth_field_text == "":
                    self.depth_field_text = "1"
            elif self.current_completing_container == 2:
                self.height_field_text = self.typing(self.height_field_text, (1, 300))
                if self.width_field_text == "":
                    self.width_field_text = "1"
                if self.depth_field_text == "":
                    self.depth_field_text = "1"
            elif self.current_completing_container == 3:
                self.depth_field_text = self.typing(self.depth_field_text, (1, 300))
                if self.width_field_text == "":
                    self.width_field_text = "1"
                if self.height_field_text == "":
                    self.height_field_text = "1"
        new_top_margin = new_top_margin + self.increase_font2 * 45
        return new_top_margin

    def typing(self, text, nr_limits):
        if len(text) >= 4:
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
            return "300"
        else:
            return text


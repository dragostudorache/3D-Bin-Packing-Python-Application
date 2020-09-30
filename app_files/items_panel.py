import pygame
from widgets.buttons_file import icon_Button, Button
from widgets.symbols_file import draw_items_list_icon, draw_delete_all_items_icon, draw_random_add_icon, draw_add_item_icon, draw_remove_item_icon, draw_left_arrow_icon, draw_right_arrow_icon
from widgets.inputs_file import input

# Item object, it's for algorithm, see the text based script project if you wanna learn more about it
class Item(object):
    def __init__(self, name, width, height, depth):
        self.name = name

        # dimensions w x h x d
        self.width = width
        self.height = height
        self.depth = depth

        if self.width <= 0 or self.height <= 0 or self.depth <= 0:
            print("Wrong item dimensions")
            exit(20)

        # position in the bin, if it'll be packed
        self.pos = [-1, -1, -1]

        # rotation type - [0; 5], see Item.rotate to know how the item is rotated
        self.RT = 0

    def print_data(self):
        print(self.name, "|", self.width, "x", self.height, "x", self.depth, "|", self.pos, "| self.RT =", self.RT)

    # rotations
    def rotate(self, type):
        if type == 0: # normal position
            return (self.width, self.height, self.depth)
        elif type == 1: # rotate Z
            return (self.height, self.width, self.depth)
        elif type == 2: # rotate Y
            return (self.width, self.depth, self.height)
        elif type == 3: # rotate X, rotate Y
            return (self.depth, self.width, self.height)
        elif type == 4: # rotate X
            return (self.depth, self.height, self.width)
        else: # rotate X, rotate Z
            return (self.height, self.depth, self.width)

class items_panel(object):
    def __init__(self, surface, window_size, top_limit, bottom_limit, font_size, text_color, background_color):
        self.surface = surface
        self.window_size = window_size
        self.top_limit = top_limit
        self.bottom_limit = bottom_limit

        self.current_title = "Items panel"
        self.current_section = "Items list"

        self.font_size = font_size
        self.font = pygame.font.Font('res\\Rubik-Regular.ttf', self.font_size)

        self.text_color = text_color

        self.background_color = background_color

        # THAT MUST BE HERE BECAUSE IF NOT THE MOUSE OVER ANIMATION WILL NOT WORK
        self.items_list_button = icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_items_list_icon)
        self.delete_all_items_button = icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_delete_all_items_icon)
        self.random_add_button = icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_random_add_icon)
        self.add_item_button = icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_add_item_icon)



        self.add_item_width_input = input(self.surface, "normal", "Width", (0, 0, 0, 0), 1, self.background_color, self.text_color, self.font_size)
        self.add_item_height_input = input(self.surface, "normal", "Height", (0, 0, 0, 0), 1, self.background_color, self.text_color, self.font_size)
        self.add_item_depth_input = input(self.surface, "normal", "Depth", (0, 0, 0, 0), 1, self.background_color, self.text_color, self.font_size)
        self.add_item_amount_input = input(self.surface, "normal", "Amount", (0, 0, 0, 0), 1, self.background_color, self.text_color, self.font_size)
        self.add_until = False
        self.add_until_delay = 10

        self.add_item_action_button = Button(self.surface, (0, 0, 0, 0), "   Add   ", self.background_color, self.text_color,self.font_size)

        # ITEMS LIST
        self.items_list = []
        self.container_dimensions = (1, 1, 1)
        self.container_volume = 0

        # item list section
        self.current_page = 1

        # remove item icon buttons
        self.remove_item_slot = []
        self.remove_item_slot.append(icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_remove_item_icon))
        self.remove_item_slot.append(icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_remove_item_icon))
        self.remove_item_slot.append(icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_remove_item_icon))
        self.remove_item_slot.append(icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_remove_item_icon))
        self.remove_item_slot.append(icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_remove_item_icon))

        # arrows buttons
        self.left_arrow_button = icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_left_arrow_icon)
        self.right_arrow_button = icon_Button(self.surface, (0, 0, 0, 0), self.text_color, self.background_color, draw_right_arrow_icon)

    def show_content(self):
        if self.current_section == "Items list":
            self.items_list_section()
        elif self.current_section == "Random Add":
            self.random_add_section()
        elif self.current_section == "Add item":
            self.add_section()
        self.show_ordinary_content()

    def show_ordinary_content(self):
        points = [
            (61 * self.window_size[0] // 80, self.top_limit),
            (61 * self.window_size[0] // 80, self.top_limit + self.bottom_limit - self.top_limit),
            (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 40, self.top_limit + self.bottom_limit - self.top_limit),
            (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 40, self.top_limit)
        ]

        # title text
        title_bg_rect = (points[0][0], points[0][1], 9 * self.window_size[0] // 40, (self.bottom_limit - self.top_limit) // 8)
        pygame.draw.rect(self.surface, (255, 255, 255), title_bg_rect)
        text = self.font.render(self.current_title, True, self.text_color, self.background_color)
        text_rect = text.get_rect()
        text_rect.center = (7 * self.window_size[0] // 8, self.top_limit + (self.bottom_limit - self.top_limit) // 16)
        self.surface.blit(text, text_rect)

        # icon buttons
        button_rect = (points[0][0], points[0][1] + (self.bottom_limit - self.top_limit) // 8, 9 * self.window_size[0] // 160, (self.bottom_limit - self.top_limit) // 8)
        self.items_list_button.rect = button_rect
        self.items_list_button.display_button()
        self.items_list_button.check_for_action()

        if self.items_list_button.over_status == "over":
            self.current_title = "Items list"
        if self.items_list_button.status == "pressed":
            self.current_section = "Items list"
        if self.current_section == "Items list":
            self.items_list_button.icon_color = (255, 0, 0)

        button_rect = (points[0][0] + 9 * self.window_size[0] // 160, points[0][1] + (self.bottom_limit - self.top_limit) // 8, 9 * self.window_size[0] // 160, (self.bottom_limit - self.top_limit) // 8)
        self.delete_all_items_button.rect = button_rect
        self.delete_all_items_button.display_button()
        self.delete_all_items_button.check_for_action()

        if self.delete_all_items_button.over_status == "over":
            self.current_title = "Delete all items"
        if self.delete_all_items_button.status == "pressed":
            self.items_list = []
            self.current_page = 1

        button_rect = (points[0][0] + 2 * 9 * self.window_size[0] // 160, points[0][1] + (self.bottom_limit - self.top_limit) // 8, 9 * self.window_size[0] // 160, (self.bottom_limit - self.top_limit) // 8)
        self.random_add_button.rect = button_rect
        self.random_add_button.display_button()
        self.random_add_button.check_for_action()

        if self.random_add_button.over_status == "over":
            self.current_title = "Random Add"
        if self.random_add_button.status == "pressed":
            self.current_section = "Random Add"
        if self.current_section == "Random Add":
            self.random_add_button.icon_color = (255, 0, 0)

        button_rect = (points[0][0] + 3 * 9 * self.window_size[0] // 160, points[0][1] + (self.bottom_limit - self.top_limit) // 8, 9 * self.window_size[0] // 160, (self.bottom_limit - self.top_limit) // 8)
        self.add_item_button.rect = button_rect
        self.add_item_button.display_button()
        self.add_item_button.check_for_action()

        if self.add_item_button.over_status == "over":
            self.current_title = "Add item"
        if self.add_item_button.status == "pressed":
            self.current_section = "Add item"
        if self.current_section == "Add item":
            self.add_item_button.icon_color = (255, 0, 0)

        if self.items_list_button.over_status == "not over" and \
            self.delete_all_items_button.over_status == "not over" and \
            self.random_add_button.over_status == "not over" and \
            self.add_item_button.over_status == "not over":
            self.current_title = "Items panel"

        # outline
        pygame.draw.lines(self.surface, (255, 255, 255), True, points, 3)

        # rows
        for i in range(1, 3):
            start_pos = (points[0][0], self.top_limit + i * (self.bottom_limit - self.top_limit) // 8)
            end_pos = (points[3][0], self.top_limit + i * (self.bottom_limit - self.top_limit) // 8)
            pygame.draw.line(self.surface, (255, 255, 255), start_pos, end_pos, 3)

        # cols
        for i in range(1, 4):
            start_pos = (61 * self.window_size[0] // 80 + i * 9 * self.window_size[0] // 160, points[0][1] + (self.bottom_limit - self.top_limit) // 8)
            end_pos = (61 * self.window_size[0] // 80 + i * 9 * self.window_size[0] // 160, points[0][1] + 2 * (self.bottom_limit - self.top_limit) // 8)
            pygame.draw.line(self.surface, (255, 255, 255), start_pos, end_pos, 3)

    def items_list_section(self):
        self.display_items_list()
        # rows
        for i in range(3, 9):
            start_pos = (61 * self.window_size[0] // 80, self.top_limit + i * (self.bottom_limit - self.top_limit) // 8)
            end_pos = (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 40, self.top_limit + i * (self.bottom_limit - self.top_limit) // 8)
            pygame.draw.line(self.surface, (255, 255, 255), start_pos, end_pos, 3)

        start_pos = (61 * self.window_size[0] // 80 + 3 * 9 * self.window_size[0] // 160, self.top_limit + (self.bottom_limit - self.top_limit) // 8)
        end_pos = (61 * self.window_size[0] // 80 + 3 * 9 * self.window_size[0] // 160, self.top_limit + self.bottom_limit - self.top_limit)
        pygame.draw.line(self.surface, (255, 255, 255), start_pos, end_pos, 3)
        
        start_pos = (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 160, self.top_limit + self.bottom_limit - self.top_limit - (self.bottom_limit - self.top_limit) // 8)
        end_pos = (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 160, self.top_limit + self.bottom_limit - self.top_limit)
        pygame.draw.line(self.surface, (255, 255, 255), start_pos, end_pos, 3)
        
    def display_items_list(self):
        item_slot_width = 9 * self.window_size[0] // 160
        item_slot_height = (self.bottom_limit - self.top_limit) // 8
        current_top_margin = self.top_limit + 2 * item_slot_height
        if self.window_size[1] >= 800 and self.window_size[1] <= 1000:
            current_top_margin += 2
            item_slot_height += 1

        for i in range(((self.current_page - 1) * 5), (self.current_page * 5)):
            if len(self.items_list) <= i or len(self.items_list) == 0:
                break
            current_text = self.items_list[i].name + " | " + str(self.items_list[i].width) + " x " + str(self.items_list[i].height) + " x " + str(self.items_list[i].depth)
            text = self.font.render(current_text, True, self.background_color, self.text_color)
            text_rect = text.get_rect()
            text_rect.center = (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 320 + text.get_size()[0] // 2, current_top_margin + item_slot_height // 2)

            self.surface.blit(text, text_rect)
            self.remove_item_slot[i % 5].rect = (61 * self.window_size[0] // 80 + 3 * item_slot_width, current_top_margin, item_slot_width, item_slot_height)
            self.remove_item_slot[i % 5].display_button()
            self.remove_item_slot[i % 5].check_for_action()
            current_top_margin += item_slot_height

            if self.remove_item_slot[i % 5].status == "pressed":
                del self.items_list[i]
                if len(self.items_list) == i:
                    break
        # page nr.
        text = self.font.render("Page " + str(self.current_page), True, self.background_color, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 80, self.top_limit + 15 * item_slot_height // 2)

        self.surface.blit(text, text_rect)

        # arrows
        self.left_arrow_button.rect = (61 * self.window_size[0] // 80, self.top_limit + 7 * item_slot_height, item_slot_width, item_slot_height)
        self.left_arrow_button.display_button()
        self.left_arrow_button.check_for_action()

        if self.left_arrow_button.status == "pressed":
            if self.current_page >= 2:
                self.current_page -= 1

        self.right_arrow_button.rect = (61 * self.window_size[0] // 80 + 3 * item_slot_width, self.top_limit + 7 * item_slot_height, item_slot_width, item_slot_height)
        self.right_arrow_button.display_button()
        self.right_arrow_button.check_for_action()

        if self.right_arrow_button.status == "pressed":
            if self.current_page <= len(self.items_list) // 5:
                self.current_page += 1

    def random_add_section(self):
        text = self.font.render("Soon", True, self.background_color, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (61 * self.window_size[0] // 80 + 63 * self.window_size[0] // 320 - text.get_size()[0] // 2, self.top_limit + 3 * (self.bottom_limit - self.top_limit) // 8)

        self.surface.blit(text, text_rect)

    def add_section(self):
        # pygame.draw.rect(self.surface, (255, 0, 0),(61 * self.window_size[0] // 80,self.top_limit + (self.bottom_limit - self.top_limit) // 4,9 * self.window_size[0] // 40,3 * (self.bottom_limit - self.top_limit) // 4))
        self.add_item_width_input.free_space = (61 * self.window_size[0] // 80, self.font_size + self.top_limit + (self.bottom_limit - self.top_limit) // 4, 9 * self.window_size[0] // 40, 3 * (self.bottom_limit - self.top_limit) // 4)
        self.add_item_width_input.limits = (1, 300)
        self.add_item_width_input.display_input()

        inputs_top_margin = 2 * self.font_size + self.top_limit + (self.bottom_limit - self.top_limit) // 4 + self.add_item_width_input.input_size[1]
        self.add_item_height_input.free_space = (61 * self.window_size[0] // 80, inputs_top_margin, 9 * self.window_size[0] // 40, 3 * (self.bottom_limit - self.top_limit) // 4)
        self.add_item_height_input.limits = (1, 300)
        self.add_item_height_input.display_input()

        inputs_top_margin = inputs_top_margin + self.font_size + self.add_item_height_input.input_size[1]
        self.add_item_depth_input.free_space = (61 * self.window_size[0] // 80, inputs_top_margin, 9 * self.window_size[0] // 40, 3 * (self.bottom_limit - self.top_limit) // 4)
        self.add_item_depth_input.limits = (1, 300)
        self.add_item_depth_input.display_input()

        inputs_top_margin = inputs_top_margin + self.font_size + self.add_item_depth_input.input_size[1]
        self.add_item_amount_input.free_space = (61 * self.window_size[0] // 80, inputs_top_margin, 9 * self.window_size[0] // 40, 3 * (self.bottom_limit - self.top_limit) // 4)
        self.add_item_amount_input.limits = (1, 10000)
        self.add_item_amount_input.display_input()

        inputs_top_margin = inputs_top_margin + 1.5 * self.font_size + self.add_item_amount_input.input_size[1]
        # add until
        # informative text
        text = self.font.render("Add items until", True, self.background_color, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (61 * self.window_size[0] // 80 + 63 * self.window_size[0] // 320 - text.get_size()[0] // 2, inputs_top_margin)

        self.surface.blit(text, text_rect)

        copy_inputs_top_margin = inputs_top_margin
        inputs_top_margin = inputs_top_margin + text.get_size()[1]

        text = self.font.render("items vol = bin vol", True, self.background_color, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (61 * self.window_size[0] // 80 + 63 * self.window_size[0] // 320 - text.get_size()[0] // 2, inputs_top_margin)

        self.surface.blit(text, text_rect)

        inputs_top_margin = inputs_top_margin + text.get_size()[1]

        text = self.font.render("(Ignore amount)", True, self.background_color, self.text_color)
        text_rect = text.get_rect()
        text_rect.center = (61 * self.window_size[0] // 80 + 63 * self.window_size[0] // 320 - text.get_size()[0] // 2, inputs_top_margin)

        self.surface.blit(text, text_rect)

        points = [
            (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 320, copy_inputs_top_margin + (inputs_top_margin - copy_inputs_top_margin) // 4),
            (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 320, copy_inputs_top_margin + 3 * (inputs_top_margin - copy_inputs_top_margin) // 4),
            (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 320 + (inputs_top_margin - copy_inputs_top_margin) // 2, copy_inputs_top_margin + 3 * (inputs_top_margin - copy_inputs_top_margin) // 4),
            (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 320 + (inputs_top_margin - copy_inputs_top_margin) // 2, copy_inputs_top_margin + (inputs_top_margin - copy_inputs_top_margin) // 4),
        ]
        pygame.draw.lines(self.surface, self.background_color, True, points, 3)

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.add_until_delay >= 10:
            if mouse_pos[0] >= points[0][0] and \
                    mouse_pos[0] <= points[2][0] and \
                    mouse_pos[1] >= points[0][1] and \
                    mouse_pos[1] <= points[1][1]:
                self.add_until = bool(abs(self.add_until - 1))
            self.add_until_delay = 0
        else:
            self.add_until_delay += 1

        if self.add_until == True:
            pygame.draw.rect(self.surface, self.background_color, (points[0][0], points[0][1], (inputs_top_margin - copy_inputs_top_margin) // 2, (inputs_top_margin - copy_inputs_top_margin) // 2))

        self.add_item_action_button.status = "not pressed"
        self.add_item_action_button.position = (61 * self.window_size[0] // 80 + 9 * self.window_size[0] // 80, self.bottom_limit - self.font_size - text.get_size()[1])
        self.add_item_action_button.display_button()
        self.add_item_action_button.check_for_action()
        if self.add_item_action_button.status == "pressed":
            if self.add_until == False:
                for i in range(int(self.add_item_amount_input.values)):
                    self.items_list.insert(0, Item("Item", int(self.add_item_width_input.values), int(self.add_item_height_input.values), int(self.add_item_depth_input.values)))
            else:
                aux = self.container_volume
                vol = int(self.add_item_width_input.values) * int(self.add_item_height_input.values) * int(self.add_item_depth_input.values)
                while aux - vol >= 0:
                    self.items_list.insert(0, Item("Item", int(self.add_item_width_input.values), int(self.add_item_height_input.values), int(self.add_item_depth_input.values)))
                    aux -= vol
            self.current_section = "Items list"
            self.current_page = 1

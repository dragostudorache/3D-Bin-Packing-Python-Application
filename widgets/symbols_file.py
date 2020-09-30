import pygame
def draw_items_list_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2
    icon_rect = (rect[0] + rect[2] // 2 - dimension // 2, rect[1] + rect[3] // 2 - dimension // 2, 9 * dimension // 10, dimension)
    pygame.draw.rect(surface, icon_color, icon_rect)
    for i in range(1, 4):
        start_pos = (icon_rect[0] + 2 * dimension // 10, icon_rect[1] + i * dimension // 4)
        end_pos = (icon_rect[0] + 7 * dimension // 10, icon_rect[1] + i * dimension // 4)
        pygame.draw.line(surface, icon_color2, start_pos, end_pos, 3)

def draw_delete_all_items_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2
    # trash bin's handle
    points = [
        (rect[0] + (rect[2] - dimension) // 2 + 3 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + dimension // 4),
        (rect[0] + (rect[2] - dimension) // 2 + 3 * dimension // 8, rect[1] + (rect[3] - dimension) // 2),
        (rect[0] + (rect[2] - dimension) // 2 + 5 * dimension // 8, rect[1] + (rect[3] - dimension) // 2),
        (rect[0] + (rect[2] - dimension) // 2 + 5 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + dimension // 4)
    ]
    pygame.draw.lines(surface, icon_color, False, points, 3)

    # bin's cover
    points = [
        (rect[0] + (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + 2 * dimension // 4),
        (rect[0] + (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 4),
        (rect[0] + rect[2] - (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 4),
        (rect[0] + rect[2] - (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + 2 * dimension // 4)
    ]
    pygame.draw.lines(surface, icon_color, True, points, 3)

    # bin's torso
    points = [
        (rect[0] + (rect[2] - dimension) // 2 + dimension // 8, rect[1] + (rect[3] - dimension) // 2 + 2 * dimension // 4),
        (rect[0] + (rect[2] - dimension) // 2 + dimension // 4, rect[1] + (rect[3] - dimension) // 2 + dimension),
        (rect[0] + (rect[2] - dimension) // 2 + 3 * dimension // 4, rect[1] + (rect[3] - dimension) // 2 + dimension),
        (rect[0] + (rect[2] - dimension) // 2 + 7 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + 2 * dimension // 4)
    ]
    pygame.draw.lines(surface, icon_color, False, points, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + 3 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + 2 * dimension // 4)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + 3 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + 5 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + 2 * dimension // 4)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + 5 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

def draw_random_add_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2
    # first arrow
    start_point = (rect[0] + (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + dimension)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + 3 * dimension // 4, rect[1] + (rect[3] - dimension) // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + dimension // 4)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    # second arrow
    start_point = (rect[0] + (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + 3 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + 3 * dimension // 8)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + 5 * dimension // 8, rect[1] + (rect[3] - dimension) // 2 + 5 * dimension // 8)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + dimension)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + 3 * dimension // 4)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + dimension)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + 3 * dimension // 4, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

def draw_add_item_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2
    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension // 10, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + 9 * dimension // 10, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    dimension = min(rect[2], rect[3]) // 2
    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 10)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + dimension // 2, rect[1] + (rect[3] - dimension) // 2 + 9 * dimension // 10)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

def draw_remove_item_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2

    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension // 10, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + 9 * dimension // 10, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

def draw_left_arrow_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2

    start_point = (rect[0] + rect[2] // 2, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    end_point = (rect[0] + rect[2] // 2, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

def draw_right_arrow_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2

    start_point = (rect[0] + rect[2] // 2, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    end_point = (rect[0] + rect[2] // 2, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

def draw_double_left_arrow_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2

    start_point = (rect[0] + rect[2] // 2, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    end_point = (rect[0] + rect[2] // 2, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + 3 * rect[2] // 4, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension), rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension), rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    end_point = (rect[0] + 3 * rect[2] // 4, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

def draw_double_right_arrow_icon(surface, rect, icon_color, icon_color2):
    dimension = min(rect[2], rect[3]) // 2

    start_point = (rect[0] + rect[2] // 2, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    end_point = (rect[0] + rect[2] // 2, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + rect[2] // 4, rect[1] + (rect[3] - dimension) // 2)
    end_point = (rect[0] + (rect[2] - dimension) // 2 + dimension // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)

    start_point = (rect[0] + (rect[2] - dimension) // 2 + dimension // 2, rect[1] + (rect[3] - dimension) // 2 + dimension // 2)
    end_point = (rect[0] + rect[2] // 4, rect[1] + (rect[3] - dimension) // 2 + dimension)
    pygame.draw.line(surface, icon_color, start_point, end_point, 3)
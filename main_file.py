import pygame
from app_files.control_panel import control_panel
pygame.init()
clock = pygame.time.Clock()

# screen tretching prevention
import os, sys
if os.name != "nt" or sys.getwindowsversion()[0] < 6:
    raise NotImplementedError('this script requires Windows Vista or newer')

try:
    import ctypes
except ImportError:
    print('install ctypes from http://sourceforge.net/projects/ctypes/files/ctypes')
    raise

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# main function
def main():
    global clock

    # create window
    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("3D-binpacking")

    # create a control panel
    current_control_panel = control_panel(surface, (surface.get_size()[0], surface.get_size()[1]))

    run = True
    FPS = 30

    # main loop
    while run:
        # 30 fps
        clock.tick(FPS)

        # quit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        surface.fill((255, 255, 255))

        current_control_panel.show_content()
        if current_control_panel.close_app.status == "pressed":
            run = False
        pygame.display.update()

if __name__ == "__main__":
    main()

    pygame.quit()
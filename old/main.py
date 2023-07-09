import sys
import pygame
import threading
from titlescreen import Title
from basesort.choice_0 import choice_0
from basesort.selectsort import select_sort
from basesort.insertsorting import insert_sort
from mouse.mouse import mouse


def main():
    # 屏幕初始化
    pygame.init()
    pygame.display.set_caption('排序可视化程序', '看不见我')
    screen = pygame.display.set_mode((1024, 512))
    bg_color = (230, 230, 230)
    title = Title(screen, bg_color)
    title.show_title()
    choice_i = 0
    mouse_menu = threading.Thread(target=mouse, args=(screen, bg_color))
    mouse_menu.daemon = True
    mouse_menu.start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    choice_i = title.choice_previous()
                if event.key == pygame.K_s:
                    choice_i = title.choice_next()
                if event.key == pygame.K_RETURN:
                    if choice_i == 0:
                        choice_0(screen, bg_color)
                    elif choice_i == 1:
                        select_sort(screen, bg_color)
                    elif choice_i == 2:
                        insert_sort(screen, bg_color)
            # mouse(screen, bg_color)
            title.all_blit()
            pygame.display.update((0, 18, 1024, 494))


main()

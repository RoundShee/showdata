import pygame
import sys


def mouse(screen, bg_color):
    """尝试加入鼠标的一些操作"""
    font_menu = pygame.font.Font('../misc/Alimama_DongFangDaKai_Regular.ttf', 17)
    menu1 = font_menu.render('开始', True, (0, 0, 0))
    (left, top, width, height) = menu1.get_rect()
    print(height)
    menu2 = font_menu.render('暂停', True, (0, 0, 0))
    menu3 = font_menu.render('重启', True, (0, 0, 0))
    while True:
        screen.fill(bg_color, (0, 0, 1024, 18))
        screen.blit(menu1, (0, 0))
        screen.blit(menu2, (width+5, 0))
        screen.blit(menu3, (width*2+10, 0))
        pygame.display.update(0, 0, 1024, 18)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


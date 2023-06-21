import sys
import pygame
from titlescreen import Title


def main():
    # 屏幕初始化
    pygame.init()
    pygame.display.set_caption('排序可视化程序', '看不见我')
    screen = pygame.display.set_mode((1024, 512))
    title = Title(screen)
    title.show_title()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    title.choice_previous()
                if event.key == pygame.K_s:
                    title.choice_next()
                if event.key == pygame.K_RETURN:
                    print('我没想好')
            title.all_blit()
            pygame.display.flip()


main()

import sys
import pygame
import threading
import queue


def top_menu(bg_color, top_menu_q, event_send, animation_pause):
    """
    顶部菜单栏
    :param animation_pause: 线程的事件控制
    :param bg_color:
    :param top_menu_q: 接收窗口大小变化
    :param event_send: 鼠标事件检测
    :return:
    """
    im_finish_grey = pygame.image.load('../misc/finish_grey.png')
    im_finish_red = pygame.image.load('../misc/finish_red.png')
    im_pause = pygame.image.load('../misc/pause.png')
    im_start = pygame.image.load('../misc/start_button.png')
    im_start_grey = pygame.image.load('../misc/start_grey.png')
    im_pause_grey = pygame.image.load('../misc/pause_grey.png')
    button_size = 30
    buttons = [im_start, im_pause, im_finish_red]
    # 事件必须是有才能触发，影响动画刷新，因此再开一个线程
    mouse_response = threading.Thread(target=event_test, args=(event_send, animation_pause))
    mouse_response.daemon = True
    mouse_response.start()
    while True:
        # 动画显示
        screen, screen_width, screen_height = top_menu_q.get()
        screen.fill(bg_color, rect=(0, 0, screen_width, button_size))
        if animation_pause.is_set():
            buttons = [im_start_grey, im_pause, im_finish_red]
        elif not animation_pause.is_set():
            buttons = [im_start, im_pause_grey, im_finish_red]
        for i in range(3):
            screen.blit(buttons[i], (button_size*i, 0))
        pygame.display.update([(0, 0, screen_width, button_size)])


def event_test(event_send, animation_pause):
    # 抄主菜单逻辑
    flag_down = 0
    flag_up = 0
    while True:
        # 鼠标检测
        event = event_send.get()
        if flag_up == flag_down:  # 防止二次触发
            flag_down = 0
            flag_up = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # pygame.mouse.get_pos()
            for i in range(3):
                if (i*30 < x < (i+1)*30) and (0 < y < 30):
                    flag_down = i + 1
                    break
                else:
                    flag_down = 0
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in range(3):
                if (i*30 < x < (i+1)*30) and (0 < y < 30):
                    flag_up = i + 1
                    break
                else:
                    flag_up = 0
        # 由于生产者消费者的限制，必须生产一个
        if flag_up == flag_down and flag_up == 1:
            animation_pause.set()
        elif flag_up == flag_down and flag_up == 2:
            animation_pause.clear()


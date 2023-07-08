import pygame
import threading


def top_menu(bg_color, top_menu_q, event_send, animation_pause, heap_restart, speed_event):
    """
    顶部菜单栏
    :param speed_event: 长度为3的数组：分别对应down,mid,up
    :param heap_restart: 重启信号
    :param animation_pause: 线程的事件控制
    :param bg_color:
    :param top_menu_q: 接收窗口大小变化
    :param event_send: 鼠标事件检测
    :return:
    """
    im_finish_red = pygame.image.load('./misc/finish_red.png').convert_alpha()
    im_pause = pygame.image.load('./misc/pause.png').convert_alpha()
    im_start = pygame.image.load('./misc/start_button.png').convert_alpha()
    im_start_grey = pygame.image.load('./misc/start_grey.png').convert_alpha()
    im_pause_grey = pygame.image.load('./misc/pause_grey.png').convert_alpha()
    im_speed_up = pygame.image.load('./misc/speed_up.png').convert_alpha()
    im_speed_up_grey = pygame.image.load('./misc/speed_up_grey.png').convert_alpha()
    im_speed_mid = pygame.image.load('./misc/speed_mid.png').convert_alpha()
    im_speed_mid_grey = pygame.image.load('./misc/speed_mid_grey.png').convert_alpha()
    im_speed_down = pygame.image.load('./misc/speed_down.png').convert_alpha()
    im_speed_down_grey = pygame.image.load('./misc/speed_down_grey.png').convert_alpha()
    button_size = 30
    buttons = [im_start, im_pause, im_finish_red]
    # 事件必须是有才能触发，影响动画刷新，因此再开一个线程
    mouse_response = threading.Thread(target=event_test, args=(event_send, animation_pause, heap_restart, speed_event))
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
        # 三个速度调节
        if speed_event[0].is_set():
            buttons.append(im_speed_down_grey)
            buttons.append(im_speed_mid)
            buttons.append(im_speed_up)
        elif speed_event[1].is_set():
            buttons.append(im_speed_down)
            buttons.append(im_speed_mid_grey)
            buttons.append(im_speed_up)
        else:
            buttons.append(im_speed_down)
            buttons.append(im_speed_mid)
            buttons.append(im_speed_up_grey)
        for i in range(6):
            screen.blit(buttons[i], (button_size*i, 0))
        pygame.display.update([(0, 0, screen_width, button_size)])


def event_test(event_send, animation_pause, heap_restart, speed_event):
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
            for i in range(6):
                if (i*30 < x < (i+1)*30) and (0 < y < 30):
                    flag_down = i + 1
                    break
                else:
                    flag_down = 0
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in range(6):
                if (i*30 < x < (i+1)*30) and (0 < y < 30):
                    flag_up = i + 1
                    break
                else:
                    flag_up = 0
        if flag_up == flag_down and flag_up == 1:
            animation_pause.set()
        elif flag_up == flag_down and flag_up == 2:
            animation_pause.clear()
        elif flag_up == flag_down and flag_up == 3:
            heap_restart.set()
        elif flag_up == flag_down and flag_up == 4:
            speed_event[0].set()
            speed_event[1].clear()
            speed_event[2].clear()
        elif flag_up == flag_down and flag_up == 5:
            speed_event[0].clear()
            speed_event[1].set()
            speed_event[2].clear()
        elif flag_up == flag_down and flag_up == 6:
            speed_event[0].clear()
            speed_event[1].clear()
            speed_event[2].set()

import sys
import pygame
import threading
import queue


def main():
    # 默认大小
    screen_size = (1366, 768)
    pygame.init()
    pygame.display.set_caption("排序可视化程序")
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE, 32)  # 可调节窗口
    bg_color = (230, 230, 230)
    push_windows = queue.Queue(maxsize=1)
    # event传递
    pygame_event = queue.Queue(maxsize=20)
    # 通信-获得菜单的操作
    get_operation = queue.Queue(maxsize=1)
    my_menu = threading.Thread(target=menu, args=(get_operation, push_windows, pygame_event))
    my_menu.daemon = True
    my_menu.start()
    while True:
        event = pygame.event.wait()
        pygame_event.put(event)
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            # 重新获取当前大小
            screen_size = event.size
            # 重设
            screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE, 32)
        screen_width, screen_height = screen_size
        # 发送当前窗口大小数据
        push_windows.put((screen, bg_color, screen_height))
        push_windows.task_done()
        # 区域填充，留着后面使用
        screen.fill(bg_color, (140, 0, screen_width-140, screen_height))
        screen.fill(bg_color, (0, 0, 140, screen_height/2.0))
        which_one = get_operation.get()
        if which_one == 1:
            print('1可用')
        elif which_one == 2:
            print('2可用')
        elif which_one == 3:
            print('3可用')
        elif which_one == 4:
            print('4可以同')
        # 区域刷新，目前仅有一块为菜单多线程刷新
        pygame.display.update([(140, 0, screen_width-140, screen_height), (0, 0, 140, screen_height/2.0)])


def menu(get_operation, push_windows, pygame_event):
    # 预留自定义
    menu_font = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 25)
    menu_text_raw = ["冒泡排序", "选择排序", "插入排序", "堆排序"]
    # 字体加载
    how_many = len(menu_text_raw)
    menu_text = []
    for i in range(how_many):
        menu_text.append(menu_font.render(menu_text_raw[i], True, (0, 0, 0)))
    # 字体打印
    two_space = 30
    height = (menu_text[0].get_rect()).height
    # 准备与鼠标检测的通信
    mouse_test_q = queue.Queue(maxsize = 1)
    # 创建线程
    choose_menu = threading.Thread(target=mouse_test, args=(get_operation, mouse_test_q, pygame_event))
    choose_menu.daemon = True
    choose_menu.start()
    while True:
        # 从上一级获取窗口大小进行解算位置信息
        screen, bg_color, screen_height = push_windows.get()
        mouse_test_q.put((screen_height, how_many, two_space, height))
        screen.fill(bg_color, (0, screen_height/2.0, 140, screen_height/2.0))  # 用于后期做动画
        for i in range(how_many):
            screen.blit(menu_text[i], (40, screen_height/2.0+(how_many-i)*(height+two_space)))

        pygame.display.update((0, screen_height/2.0, 140, screen_height/2.0))


def mouse_test(get_operation, mouse_test_q, pygame_event):
    flag_down = 0
    flag_up = 0
    while True:
        screen_height, how_many, two_space, height = mouse_test_q.get()
        event = pygame_event.get()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # pygame.mouse.get_pos()
            for i in range(how_many):
                if (40 < x < 140) and ((screen_height/2.0+(how_many-i)*(height+two_space)) < y < (screen_height/2.0
                                                                                                      +
                                                                                                      (how_many-i+1) *
                                                                                                      (height+two_space))):
                    flag_down = i + 1
                    break
                else:
                    flag_down = 0
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos  # pygame.mouse.get_pos()
            for i in range(how_many):
                if (40 < x < 140) and ((screen_height/2.0+(how_many-i)*(height+two_space)) < y < (screen_height/2.0 +
                                                                                                      (how_many-i+1) *
                                                                                                      (height+two_space))):
                    flag_up = i + 1
                    break
                else:
                    flag_up = 0

        if flag_up == flag_down:
            get_operation.put(int(flag_up))
        else:
            get_operation.put(0)


if __name__ == "__main__":
    main()

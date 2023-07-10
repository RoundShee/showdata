import sys
import pygame
import threading
import queue
from basesort.choice_0 import choice_0
from basesort.selectsort import select_sort
from basesort.insertsorting import insert_sort
from new_sort.heapsort import heap_sort
from new_sort.get_num import get_num


def main():
    # 默认大小
    screen_size = (1366, 768)
    screen_width, screen_height = screen_size
    pygame.init()
    pygame.display.set_caption("排序可视化程序")
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE, 32)  # 可调节窗口
    bg_color = (230, 230, 230)
    push_windows = queue.Queue(maxsize=1)
    # event传递
    pygame_event = queue.Queue(maxsize=1)
    # 通信-获得菜单的操作
    get_operation = queue.Queue(maxsize=1)
    my_menu = threading.Thread(target=menu, args=(get_operation, push_windows, pygame_event))
    my_menu.daemon = True
    my_menu.start()
    while True:
        for event in pygame.event.get():
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
            push_windows.put((screen, bg_color, screen_width, screen_height))
            push_windows.task_done()
            # 区域填充，留着后面使用
            screen.fill(bg_color, (0, 0, 140, screen_height / 2.0))
            screen.fill(bg_color, (140, 0, screen_width - 140, screen_height))
            which_one = get_operation.get()
            if which_one == 1:
                choice_0(screen, bg_color)
            elif which_one == 2:
                select_sort(screen, bg_color)
            elif which_one == 3:
                insert_sort(screen, bg_color)
            elif which_one == 4:
                num = []
                label = 1
                while label:
                    num, screen, label = get_num(screen, num)
                    if not label:
                        break
                    num_copy = num[:]
                    heap_sort(screen, bg_color, num_copy)
        # 区域刷新，目前仅有一块为菜单多线程刷新
        pygame.display.update([(140, 0, screen_width - 140, screen_height), (0, 0, 140, screen_height / 2.0)])


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
    mouse_test_q = queue.Queue(maxsize=1)
    cursor_hover1 = threading.Event()  # 光标悬停事件组准备
    cursor_hover2 = threading.Event()
    cursor_hover3 = threading.Event()
    cursor_hover4 = threading.Event()
    cursor_hover = [cursor_hover1, cursor_hover2, cursor_hover3, cursor_hover4]
    # 右边小世界美化
    screen_information = queue.Queue(maxsize=1)  # 转发信息
    right_display_thread = threading.Thread(target=right_display, args=(screen_information, cursor_hover))
    right_display_thread.daemon = True
    # 创建线程
    choose_menu = threading.Thread(target=mouse_test, args=(get_operation, mouse_test_q, pygame_event, cursor_hover))
    choose_menu.daemon = True
    # 启动线程
    choose_menu.start()
    right_display_thread.start()
    while True:
        # 从上一级获取窗口大小进行解算位置信息
        screen, bg_color, screen_width, screen_height = push_windows.get()
        screen_information.put((screen, bg_color, screen_width, screen_height))
        screen_information.task_done()
        mouse_test_q.put((screen_height, how_many, two_space, height))
        screen.fill(bg_color, (0, screen_height/2.0, 140, screen_height/2.0))  # 用于后期做动画
        for i in range(how_many):
            if cursor_hover[i].is_set():  # 根据鼠标情况改文字位置
                screen.blit(menu_text[i], (45, screen_height / 2.0 + i * (height + two_space)))
            else:
                screen.blit(menu_text[i], (40, screen_height/2.0+i*(height+two_space)))
        pygame.display.update((0, screen_height/2.0, 140, screen_height/2.0))


def mouse_test(get_operation, mouse_test_q, pygame_event, cursor_hover):
    flag_down = 0
    flag_up = 0
    while True:
        if flag_up == flag_down:  # 防止二次触发
            flag_down = 0
            flag_up = 0
        screen_height, how_many, two_space, height = mouse_test_q.get()
        event = pygame_event.get()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # pygame.mouse.get_pos()
            for i in range(how_many):
                if (40 < x < 140) and ((screen_height/2.0+i*(height+two_space)) < y <
                                       (screen_height/2.0+i*(height+two_space)+height)):
                    flag_down = i + 1
                    break
                else:
                    flag_down = 0
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in range(how_many):
                if (40 < x < 140) and ((screen_height/2.0+i*(height+two_space)) < y <
                                       (screen_height/2.0+i*(height+two_space)+height)):
                    flag_up = i + 1
                    break
                else:
                    flag_up = 0
        if event.type == pygame.MOUSEMOTION:  # 光标悬停动画
            x, y = event.pos
            for i in range(how_many):
                if (40 < x < 140) and ((screen_height / 2.0 + i * (height + two_space)) < y <
                                       (screen_height / 2.0 + i * (height + two_space) + height)):
                    cursor_hover[i].set()
                else:
                    cursor_hover[i].clear()
        # 由于生产者消费者的限制，必须生产一个
        if flag_up == flag_down:
            get_operation.put(int(flag_up))
        else:
            get_operation.put(0)


def right_display(screen_information, cursor_hover):
    im_default = pygame.image.load('./misc/default.png').convert_alpha()
    im_heapsort = pygame.image.load('./misc/heapsort.png').convert_alpha()
    im_bulbingsort = pygame.image.load('./misc/bulbingsort.png').convert_alpha()
    im_insertsort = pygame.image.load('./misc/insertsort.png').convert_alpha()
    im_selectsort = pygame.image.load('./misc/selectsort.png').convert_alpha()
    while True:
        screen, bg_color, screen_width, screen_height = screen_information.get()
        # screen.fill(bg_color, (140, 0, screen_width-140, screen_height))  # 使用main中的填充不遮挡文字
        if cursor_hover[0].is_set():
            screen.blit(im_bulbingsort, (140, 0))
        elif cursor_hover[1].is_set():
            screen.blit(im_selectsort, (140, 0))
        elif cursor_hover[2].is_set():
            screen.blit(im_insertsort, (140, 0))
        elif cursor_hover[3].is_set():
            screen.blit(im_heapsort, (140, 0))
        else:
            screen.blit(im_default, (140, 0))
        # pygame.display.update((140, screen_height, screen_width-140, screen_height))  # 怎么没用


if __name__ == "__main__":
    main()

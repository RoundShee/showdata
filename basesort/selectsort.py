import pygame
import sys
from basesort.barmethods import draw_bar, get_nums_display, refresh_wait, pause_wait, swap_cartoon


def select_sort(screen, bg_color):
    """选择排序，把最小打个标签，放到最前面"""
    in_choice_0 = 1  # 处在当前choice_0的信号
    numbers = []
    # 在当前菜单的操作
    while in_choice_0:
        # 接收数据——可视化
        numbers = get_nums_display(screen, bg_color, numbers)
        if numbers == -1:
            in_choice_0 = 0
        # 接着就是魔法
        not_back = 1  # 处在冒泡排序状态不返回编辑状态的信号
        while in_choice_0 and not_back:
            numbers_plus = draw_bar(numbers, screen)  # 折衷方案：重绘 但此处存在资源的浪费
            not_back = start_select_sort(screen, bg_color, numbers_plus)


def start_select_sort(screen, bg_color, numbers_plus):
    """开始冒泡排序的操作，输入的numbers_plus应为副本
        此方法包含暂停，继续以及 重启的返回信号
        运行完毕自行等待
        ****类似 改 ******
    """
    not_back = 1
    total = len(numbers_plus)
    for i in range(total):
        # 统统变灰
        numbers_plus[i].select(0)
    refresh_wait(screen, bg_color, numbers_plus, total, 90)
    decision = 1
    go_into_sort = 1
    while decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    decision = not decision
                elif event.key == pygame.K_ESCAPE:
                    # 回到实时显示编辑模式
                    decision = not decision
                    go_into_sort = 0
                    not_back = 0
    if go_into_sort:
        # 开始
        for i in range(total - 1):
            select_min = i  # 最小标签打上
            numbers_plus[i].long_select()
            for j in range(i+1, total):
                if pause_wait():  # 可控暂停以及重启
                    return not_back
                # 选中动画显示
                numbers_plus[j].select()  # 变绿
                refresh_wait(screen, bg_color, numbers_plus, total, 120)
                if pause_wait():  # 可控暂停以及重启
                    return not_back
                if numbers_plus[select_min].num > numbers_plus[j].num:
                    numbers_plus[j].long_select()  # 变红
                    numbers_plus[select_min].long_select(0)  # 变灰
                    select_min = j
                else:
                    numbers_plus[j].select(0)
                refresh_wait(screen, bg_color, numbers_plus, total, 120)
                if pause_wait():  # 可控暂停以及重启
                    return not_back
            if i != select_min:
                swap_cartoon(screen, bg_color, numbers_plus, total, i, select_min)
                refresh_wait(screen, bg_color, numbers_plus, total, 120)
            numbers_plus[i].done()
            refresh_wait(screen, bg_color, numbers_plus, total, 60)
        numbers_plus[i+1].done()
        refresh_wait(screen, bg_color, numbers_plus, total, 60)
        finish = 1
        while finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        finish = 0  # 回到重绘那里重新开始
        return not_back


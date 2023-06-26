# 这里要冒泡排序
import pygame
import sys
from basesort.barmethods import draw_bar, get_nums_display, refresh_wait, pause_wait, swap_cartoon


def choice_0(screen, bg_color):
    """choice_0为二级菜单的操作"""
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
            # numbers_plus = numbers_plus_bak[:]  # 绝了，浅拷贝
            # numbers_plus = copy.deepcopy(numbers_plus_bak)  # 太难了吧，类拷贝存在问题
            numbers_plus = draw_bar(numbers, screen)  # 折衷方案：重绘 但此处存在资源的浪费
            not_back = start_bubble(screen, bg_color, numbers_plus)


def start_bubble(screen, bg_color, numbers_plus):
    """开始冒泡排序的操作，输入的numbers_plus应为副本
        此方法包含暂停，继续以及 重启的返回信号
        运行完毕自行等待"""
    not_back = 1
    total = len(numbers_plus)
    for i in range(total):
        # 统统变灰
        numbers_plus[i].select(0)
    refresh_wait(screen, bg_color, numbers_plus, total, 90)
    decision = 1
    go_into_bulbing = 1
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
                    go_into_bulbing = 0
                    not_back = 0
    if go_into_bulbing:
        # 开始冒泡
        for i in range(total - 1):
            for j in range(total - 1 - i):
                if pause_wait():  # 可控暂停以及重启
                    return not_back
                # 选中动画显示
                numbers_plus[j].select()
                refresh_wait(screen, bg_color, numbers_plus, total, 120)
                if pause_wait():  # 可控暂停以及重启
                    return not_back
                numbers_plus[j + 1].select()
                refresh_wait(screen, bg_color, numbers_plus, total, 120)
                if pause_wait():  # 可控暂停以及重启
                    return not_back
                if numbers_plus[j].num > numbers_plus[j + 1].num:
                    swap_cartoon(screen, bg_color, numbers_plus, total, j, j+1)
                numbers_plus[j].select(0)
                numbers_plus[j + 1].select(0)
                refresh_wait(screen, bg_color, numbers_plus, total, 120)
                if pause_wait():  # 可控暂停以及重启
                    return not_back
            numbers_plus[total - i - 1].done()
        # 最后上色done
        numbers_plus[0].done()
        numbers_plus[1].done()
        refresh_wait(screen, bg_color, numbers_plus, total, 10)
        finish = 1
        while finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        finish = 0  # 回到重绘那里重新开始
        return not_back



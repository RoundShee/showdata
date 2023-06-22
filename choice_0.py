# 这里要冒泡排序
import pygame
import sys


def choice_0(screen, bg_color):
    """choice_0为二级菜单的操作"""
    # 我想左上角显示一个文本框，输入当前柱子的高度
    # 空格进行下一个切换
    # 退格进行删除 删到空白 就回到上一个柱子
    # 每个柱子输入数字后 立即显示 并且根据非空数据判断有多少
    # 回车后进入下一步操作
    numbers = get_nums_display(screen, bg_color)
    # 接着就是开始排序
    # 这其中涉及到 怎样一步一步的走，交换的动画，选中的高亮
    # 不如设计一个类：基础参数：数值、序号、位置、
    #              被选中的高亮
    #              排完没排的状态
    #              方法： 交换的动画


def get_nums_display(screen, bg_color):
    """用于输入阶段的实时显示"""
    clock = pygame.time.Clock()

    # 数字显示
    font_num = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 20)
    input_text = ""
    numbers = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # 退格键
                    if input_text:
                        # 如果当前输入不为空，则删除最后一个字符
                        input_text = input_text[:-1]
                    else:
                        # 如果当前输入为空，则选定上一个数
                        if numbers:
                            numbers.pop()
                elif event.key == pygame.K_SPACE:
                    # 空格键
                    if input_text:
                        # 如果当前输入不为空，则将其作为一个新的数加入列表
                        try:
                            number = float(input_text)
                            numbers.append(number)
                            input_text = ""
                        except ValueError:
                            # 输入不是有效的浮点数
                            pass
                elif event.key == pygame.K_RETURN:
                    # Enter 键
                    if numbers:
                        return numbers
                else:
                    # 其他按键
                    input_text += event.unicode

        screen.fill(bg_color)
        text_surface = font_num.render("当前输入: " + input_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 450))

        text_surface = font_num.render("已存序列: " + ", ".join(map(str, numbers)), True, (0, 0, 0))
        screen.blit(text_surface, (10, 480))
        draw_bar(numbers, screen)
        pygame.display.flip()
        clock.tick(45)


def get_color_for_value(value, max_value):
    normalized_value = value / max_value
    r = int(normalized_value * 255)
    g = 0
    b = 255 - r
    return r, g, b


def draw_bar(numbers, screen):
    # 柱形图显示
    if numbers:
        num_bars = len(numbers)
        max_value = max(numbers)  # 获取数据中的最大值
        bar_spacing = 10  # 柱形之间的间距
        bar_width = 20  # 默认宽度
        screen_rect = screen.get_rect()  # 为了同一调度，再次解算屏幕宽度
        bar_width_temp = (screen_rect.width - (num_bars + 1) * bar_spacing) / num_bars
        if bar_width_temp > 20:
            bar_width = 20
        else:
            bar_width = (screen_rect.width - (num_bars + 1) * bar_spacing) / num_bars

        # 绘制每个柱形
        for i in range(num_bars):
            bar_height = int((numbers[i] / max_value) * (screen_rect.height - 250))  # 根据数据值计算柱形的高度
            bar_x = (screen_rect.width - bar_width) // 2 + (i - num_bars / 2) * (bar_width + bar_spacing)
            bar_y = screen_rect.height - 90 - bar_height  # 计算柱形的 y 坐标位置

            color = get_color_for_value(numbers[i], max_value)  # 根据数据值获取颜色
            pygame.draw.rect(screen, color, (bar_x, bar_y, bar_width, bar_height))

            # 显示数值大小
            font = pygame.font.Font(None, 24)
            text = font.render(str(numbers[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(bar_x + bar_width / 2, bar_y - 20))
            screen.blit(text, text_rect)

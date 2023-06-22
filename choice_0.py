# 这里要冒泡排序
import pygame
import sys


def choice_0(screen, bg_color):
    """choice_0为二级菜单的操作"""
    # 接收数据——可视化
    numbers_plus = get_nums_display(screen, bg_color)
    # 接着就是魔法
    total = len(numbers_plus)
    for i in range(total):
        # 统统变灰
        numbers_plus[i].select(0)
    refresh_wait(screen, bg_color, numbers_plus, total, 90)
    # 开始冒泡
    for i in range(total-1):
        for j in range(total-1-i):
            # 选中动画显示
            numbers_plus[j].select()
            refresh_wait(screen, bg_color, numbers_plus, total, 120)
            numbers_plus[j+1].select()
            refresh_wait(screen, bg_color, numbers_plus, total, 120)
            if numbers_plus[j].num > numbers_plus[j+1].num:
                temp = numbers_plus[j]
                numbers_plus[j] = numbers_plus[j+1]
                numbers_plus[j+1] = temp
                temp = numbers_plus[j].bar_x
                numbers_plus[j].change_bar_x(numbers_plus[j + 1].bar_x)
                numbers_plus[j + 1].change_bar_x(temp)
                temp = numbers_plus[j].text_x
                numbers_plus[j].change_text_x(numbers_plus[j + 1].text_x)
                numbers_plus[j + 1].change_text_x(temp)
            numbers_plus[j].select(0)
            numbers_plus[j + 1].select(0)
            numbers_plus[total-i-1].done()
            refresh_wait(screen, bg_color, numbers_plus, total, 120)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return 0


def refresh_wait(screen, bg_color, numbers_plus, total, wait_time):
    """临时用用 刷新变化"""
    screen.fill(bg_color)
    for k in range(total):
        numbers_plus[k].blit(screen)
    pygame.display.flip()
    pygame.time.delay(wait_time)


def get_nums_display(screen, bg_color):
    """用于输入阶段的实时显示"""
    clock = pygame.time.Clock()

    # 数字显示
    font_num = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 20)
    input_text = ""
    numbers = []
    numbers_plus = []
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
                        return numbers_plus
                else:
                    # 其他按键
                    input_text += event.unicode

        screen.fill(bg_color)
        text_surface = font_num.render("当前输入: " + input_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 450))

        text_surface = font_num.render("已存序列: " + ", ".join(map(str, numbers)), True, (0, 0, 0))
        screen.blit(text_surface, (10, 480))
        numbers_plus = draw_bar(numbers, screen)
        # 刷新
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
        # numbers非空才执行
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

        # 绘制每个柱,形成对象
        numbers_plus = []
        for i in range(num_bars):
            # 一些 油条bar 的参数计算
            bar_height = int((numbers[i] / max_value) * (screen_rect.height - 250))  # 根据数据值计算柱形的高度
            bar_x = (screen_rect.width - bar_width) // 2 + (i - num_bars / 2) * (bar_width + bar_spacing)
            bar_y = screen_rect.height - 90 - bar_height  # 计算柱形的 y 坐标位置
            color = get_color_for_value(numbers[i], max_value)  # 根据数据值获取颜色
            # 上面的数字
            font = pygame.font.Font(None, 24)
            text = font.render(str(numbers[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(bar_x + bar_width / 2, bar_y - 20))
            fritter = Fritters(numbers[i], color, (bar_x, bar_y, bar_width, bar_height), text, text_rect)
            fritter.blit(screen)
            numbers_plus.append(fritter)
        return numbers_plus


class Fritters:
    """带数字的五彩斑斓的油条"""
    def __init__(self, num, color, bar_rect, text, text_rect):
        self.num = num
        self.color = color
        self.bar_rect = bar_rect  # (bar_x, bar_y, bar_width, bar_height)
        (self.bar_x, self.bar_y, self.bar_width, self.bar_height) = bar_rect
        self.text = text
        self.text_rect = text_rect  # 用于后期交换
        (self.text_x, self.text_y, self.text_width, self.text_height) = text_rect
        # 一些状态
        self.sorted = 0
        self.selected = 0
        self.shifting = (0, 0)

    def blit(self, screen):
        """给我屏幕，直接贴油条 饿"""
        pygame.draw.rect(screen, self.color, self.bar_rect)  # 油条
        screen.blit(self.text, self.text_rect)  # 数字

    def select(self, selected=1):
        """更新被选中的状态"""
        if selected:
            self.selected = 1
            self.color = (0, 205, 0)  # 绿色
        else:
            self.selected = 0
            self.color = (190, 190, 190)  # 灰色

    def done(self, done=1):
        """更新 排序完成"""
        if done:
            self.sorted = 1
            self.color = (255, 215, 0)  # 金色
        else:
            self.sorted = 0
            self.color = (190, 190, 190)  # 灰色
    def change_bar_x(self, new_x):
        self.bar_x = new_x
        self.bar_rect = (self.bar_x, self.bar_y, self.bar_width, self.bar_height)

    def change_text_x(self, new_x):
        self.text_x = new_x
        self.text_rect = (self.text_x, self.text_y, self.text_width, self.text_height)

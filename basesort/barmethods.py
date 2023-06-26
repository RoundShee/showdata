import pygame
import sys

"""
说明：本文件主要写关于柱形图的操作方法


    *****************************************************
    *   get_nums_display(screen, bg_color, numbers)
    *       ....
    *       # Enter 键
    *               if numbers:
    *                   return numbers
    *           elif event.key == pygame.K_ESCAPE:
    *               # 退出到主菜单的返回值
    *               return -1
    *       ....
    *   主要用于输入，传入对应参数可直接显示，numbers用于刷新并返回
    *****************************************************
    
    ******************************************************************
    *   draw_bar(numbers, screen)
    *       if numbers:
    *           ....
    *          return numbers_plus
    *   主要用于将传入的numbers根据屏幕生成fritter类对象列表numbers_plus进行返回
    *   numbers == 0 无用
    ******************************************************************
    
    
    

"""


def swap_cartoon(screen, bg_color, numbers_plus, total, a, b):
    """将i,j进行互换的10帧动画"""
    every_move = (numbers_plus[a].bar_x - numbers_plus[b].bar_x)/10.0
    # 动画效果 的 显示交换
    for i in range(10):
        numbers_plus[a].translate_x(numbers_plus[a].bar_x - every_move)
        numbers_plus[b].translate_x(numbers_plus[b].bar_x + every_move)
        refresh_wait(screen, bg_color, numbers_plus, total, 20)
    # 顺序交换
    temp = numbers_plus[a]
    numbers_plus[a] = numbers_plus[b]
    numbers_plus[b] = temp


def pause_wait(pause=0):
    """用于冒泡排序中及时接收用户操作判断是否暂停
        且在暂停状态下可以判断是否退出或重启"""
    signal = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                pause = not pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # 暂停排序
                    pause = not pause
                elif event.key == pygame.K_ESCAPE:
                    # 重启排序
                    signal = 1
                    pause = not pause
    return signal


def refresh_wait(screen, bg_color, numbers_plus, total, wait_time):
    """临时用用 刷新变化"""
    screen.fill(bg_color)
    for k in range(total):
        numbers_plus[k].blit(screen)
    pygame.display.flip()
    pygame.time.delay(wait_time)


def get_nums_display(screen, bg_color, numbers):
    """用于输入阶段的实时显示
        调用draw_bar将自身的数据及提示最终呈现
        且有接收已有numbers的功能，返回numbers的功能，可以重新对数据进行编辑
        具有退出编辑的信号返回-1，在choice_0用于退出子菜单"""
    clock = pygame.time.Clock()

    # 数字显示
    font_num = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 20)
    input_text = ""
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
                elif event.key == pygame.K_ESCAPE:
                    # 退出到主菜单的返回值
                    return -1
                else:
                    # 其他按键
                    input_text += event.unicode

        screen.fill(bg_color)
        text_surface = font_num.render("当前输入: " + input_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 450))

        text_surface = font_num.render("已存序列: " + ", ".join(map(str, numbers)), True, (0, 0, 0))
        screen.blit(text_surface, (10, 480))
        draw_bar(numbers, screen)
        # 刷新
        pygame.display.flip()
        clock.tick(45)


def get_color_for_value(value, max_value):
    """提升外观的函数
        目前存在问题，负数会出问题"""
    normalized_value = value / max_value
    r = int(normalized_value * 255)
    g = 0
    b = 255 - r
    return r, g, b


def draw_bar(numbers, screen):
    """根据已有numbers智能判断每一个柱子(fritter)的数据，
        进行实例化对象，并blit"""
    # 柱形图显示
    if numbers:
        # numbers非空才执行
        num_bars = len(numbers)
        max_value = max(numbers)  # 获取数据中的最大值
        bar_spacing = 10  # 柱形之间的间距
        # bar_width = 20  # 默认宽度
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
            font = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 12)
            text = font.render(str(numbers[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(bar_x + bar_width / 2, bar_y - 20))
            fritter = Fritters(numbers[i], color, (bar_x, bar_y, bar_width, bar_height), text, text_rect)
            fritter.blit(screen)
            numbers_plus.append(fritter)
        return numbers_plus


class Fritters:
    """带数字的五彩斑斓的油条
        具有自身数据的值,颜色,柱形的rect,头顶文字的rect
        以及配备将其blit的方法,改变状态的方法,进行平移的方法"""
    def __init__(self, num, color, bar_rect, text, text_rect):
        self.num = num
        self.color = color
        self.color_rec = color   # 用于存储变化
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
            self.color_rec = self.color
            self.color = (0, 205, 0)  # 绿色
        else:
            self.selected = 0
            self.color_rec = self.color
            self.color = (190, 190, 190)  # 灰色

    def long_select(self, long_select=1):
        """变成红色"""
        if long_select:
            self.selected = 1
            self.color_rec = self.color
            self.color = (255, 0, 0)  # 红色
        else:
            self.selected = 0
            self.color_rec = self.color
            self.color = (190, 190, 190)  # 灰色

    def done(self, done=1):
        """更新 排序完成"""
        if done:
            self.sorted = 1
            self.color_rec = self.color
            self.color = (255, 215, 0)  # 金色
        else:
            self.sorted = 0
            self.color_rec = self.color
            self.color = (190, 190, 190)  # 灰色

    def recover(self):
        self.color = self.color_rec

    def change_bar_x(self, new_x):
        """平移柱子 只是柱子"""
        self.bar_x = new_x
        self.bar_rect = (self.bar_x, self.bar_y, self.bar_width, self.bar_height)

    def change_text_x(self, new_x):
        """平移上面的 数字"""
        self.text_x = new_x
        self.text_rect = (self.text_x, self.text_y, self.text_width, self.text_height)

    def translate_x(self, new_x):
        """一步整体移动"""
        self.change_bar_x(new_x)
        self.change_text_x(new_x)

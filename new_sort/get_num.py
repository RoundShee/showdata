import queue
import sys
import pygame
import threading
import random


# 全局变量，用于线程通信交流
input_text = ''
numbers = []


def get_num(screen, num=None):
    """
    这是整个界面的入口，传入screen，根据操作情况，返回最终数组
    :param screen:
    :param num:
    :return: numbers, screen
    """
    if num is None:
        num = []
    global numbers, input_text
    numbers = num
    bg_color = (230, 230, 230)
    left, top, screen_width, screen_height = screen.get_rect()
    screen_size = screen_width, screen_height
    # 顶部按钮选择加载
    im_checked = pygame.image.load('./misc/checked.png')
    im_unchecked = pygame.image.load('./misc/unchecked.png')
    im_start_green = pygame.image.load('./misc/start_button.png')
    im_start_grey = pygame.image.load('./misc/start_grey.png')
    im_back = pygame.image.load('./misc/back.png')
    button_size = 30
    text_font = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 18)
    text_user = text_font.render('手动输入', True, (0, 0, 0))
    text_gene = text_font.render('自动生成', True, (0, 0, 0))
    text_start = text_font.render('进入排序', True, (0, 0, 0))
    text_back = text_font.render('返回菜单', True, (0, 0, 0))
    # 鼠标检测准备
    is_done = threading.Event()  # 用于判断是否进入排序
    is_back = threading.Event()  # 用于判断是否要返沪菜单
    is_gene = threading.Event()  # 用于判断是否选中自动生成
    get_num_event = queue.Queue(maxsize=1)
    thread_response = threading.Thread(target=response_for_get_num, args=(get_num_event, is_gene, is_done, is_back))
    thread_response.daemon = True
    # 下部显示线程
    queue_below_get = queue.Queue(maxsize=1)
    thread_get_num_below = threading.Thread(target=get_num_below, args=(queue_below_get, is_gene))
    thread_get_num_below.daemon = True
    # 线程启动
    thread_response.start()
    thread_get_num_below.start()
    im_buttons = []  # 按钮序列
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                # 重新获取当前大小
                screen_size = event.size
                # 重设
                screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE, 32)
            get_num_event.put(event)  # 将事件同时推送给鼠标方向
            screen_width, screen_height = screen_size
        screen.fill(bg_color, rect=(0, 0, screen_width, button_size))
        if not is_gene.is_set():
            im_buttons = [im_checked, text_user, im_unchecked, text_gene]
        elif is_gene.is_set():
            im_buttons = [im_unchecked, text_user, im_checked, text_gene]
        if numbers:  # 开始按钮动态选择
            im_buttons.append(im_start_green)
        else:
            im_buttons.append(im_start_grey)
        im_buttons.append(text_start)  # 开始文字
        im_buttons.append(im_back)  # 返回im
        im_buttons.append(text_back)  # 返回文字
        for i in range(0, len(im_buttons), 2):  # 此处计算，四字长90
            screen.blit(im_buttons[i], (i/2*(30+90), 0))
            screen.blit(im_buttons[i+1], (i/2*(30+90)+30, 4))
        pygame.display.update([(0, 0, screen_width, button_size)])
        queue_below_get.put((screen, screen_width, screen_height))  # 即时给下部显示
        # we are all died!
        if is_done.is_set():
            return numbers, screen, 1
        elif is_back.is_set():
            return numbers, screen, 0


def response_for_get_num(get_num_event, is_gene, is_done, is_back):
    global input_text, numbers  # 全局变量，用于写入
    # 按钮复用
    flag_down = 0
    flag_up = 0
    while True:
        event = get_num_event.get()
        if flag_up == flag_down:  # 防止二次触发
            flag_down = 0
            flag_up = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # pygame.mouse.get_pos()
            for i in range(4):
                if (i*(30+90) < x < i*(30+90)+30) and (0 < y < 30):
                    flag_down = i + 1
                    break
                else:
                    flag_down = 0
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            for i in range(4):
                if (i*(30+90) < x < i*(30+90)+30) and (0 < y < 30):
                    flag_up = i + 1
                    break
                else:
                    flag_up = 0
        # 由于生产者消费者的限制，必须生产一个
        if flag_up == flag_down and flag_up == 1:
            is_gene.clear()
        elif flag_up == flag_down and flag_up == 2:
            is_gene.set()
        elif flag_up == flag_down and flag_up == 3 and numbers:
            is_done.set()
        elif flag_up == flag_down and flag_up == 4:
            is_back.set()
        # 手动输入抄过来
        if not is_gene.is_set() and event.type == pygame.KEYDOWN:
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
                        number = int(input_text)
                        if number >= 0:
                            numbers.append(number)
                            input_text = ""
                    except ValueError:
                        # 输入不是有效的浮点数
                        pass
            elif event.key == pygame.K_RETURN and numbers:
                # Enter 键
                is_done.set()
            elif event.key == pygame.K_ESCAPE:
                # 退出到主菜单的返回值
                is_back.set()
            else:
                # 其他按键
                input_text += event.unicode
        if is_gene.is_set() and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # 退格键
                if input_text:
                    # 如果当前输入不为空，则删除最后一个字符
                    input_text = input_text[:-1]
            elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                               pygame.K_7, pygame.K_8, pygame.K_9]:
                input_text += event.unicode
            elif event.key == pygame.K_RETURN and numbers:
                # Enter 键
                is_done.set()
            elif event.key == pygame.K_ESCAPE:
                # 退出到主菜单的返回值
                is_back.set()
            else:
                pass
            try:
                number = int(input_text)
                if number >= 0:
                    new_numbers = []
                    for _ in range(number):
                        i = random.randint(1, 100)
                        new_numbers.append(i)
                        numbers = new_numbers
            except ValueError:
                # 输入不是有效的正整数数
                pass


def get_num_below(queue_below_get, is_gene):
    bg_color = (230, 230, 230)
    global input_text, numbers  # 全局通信变量，只读取
    font_num = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 20)
    tips_1 = font_num.render('说明：输入数字按下空格加入序列，回车或开始按钮进入排序', True, (1, 1, 1, 100))
    tips_2 = font_num.render('说明：输入生成个数即可，回车或开始按钮进入排序', True, (1, 1, 1, 100))
    while True:
        screen, screen_width, screen_height = queue_below_get.get()
        if not is_gene.is_set():  # 不是自动生成，是手动输入
            screen.fill(bg_color, rect=(0, 30, screen_width, screen_height-30))
            screen.blit(tips_1, (5, screen_height-25))
            text_surface = font_num.render("当前输入: " + input_text, True, (0, 0, 0))
            screen.blit(text_surface, (10, (screen_height-30)/3))

            text_surface = font_num.render("已存序列: ", True, (0, 0, 0))
            screen.blit(text_surface, (10, (screen_height - 30) / 3 + 30))
            row_num = len(numbers) // 10 + 1  # 确定显示的行数
            for i in range(row_num):
                start_index = i * 10
                end_index = start_index + 10
                row_numbers = numbers[start_index:end_index]
                row_text = "     ".join(str(num) for num in row_numbers)
                text_surface = font_num.render(row_text, True, (0, 0, 0))
                screen.blit(text_surface, (110, (screen_height-30)/3+30+i*20))
            pygame.display.update([(0, 30, screen_width, screen_height-30)])
        elif is_gene.is_set():
            screen.fill(bg_color, rect=(0, 30, screen_width, screen_height - 30))
            screen.blit(tips_2, (5, screen_height - 25))
            text_surface = font_num.render("生成数量: " + input_text, True, (0, 0, 0))
            screen.blit(text_surface, (10, (screen_height - 30) / 3))

            text_surface = font_num.render("已存序列: ", True, (0, 0, 0))
            screen.blit(text_surface, (10, (screen_height - 30) / 3 + 30))
            row_num = len(numbers) // 10 + 1  # 确定显示的行数
            for i in range(row_num):
                start_index = i * 10
                end_index = start_index + 10
                row_numbers = numbers[start_index:end_index]
                row_text = "     ".join(str(num) for num in row_numbers)
                text_surface = font_num.render(row_text, True, (0, 0, 0))
                screen.blit(text_surface, (110, (screen_height - 30) / 3 + 30 + i * 20))
            pygame.display.update([(0, 30, screen_width, screen_height - 30)])


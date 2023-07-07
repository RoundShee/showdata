import queue
import sys
import pygame
import threading
import math


"""
将重新接管窗口，返回一个screen_size

"""


def heap_sort(screen, bg_color, num):
    left, top, screen_width, screen_height = screen.get_rect()
    screen_size = screen_width, screen_height
    q_t_size = queue.Queue(maxsize=1)
    heapsort_dis = threading.Thread(target=heapsort_low, args=(num, screen, bg_color, q_t_size))
    heapsort_dis.daemon = True
    heapsort_dis.start()
    while True:
        '''
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            # 重新获取当前大小
            screen_size = event.size
            # 重设
            screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE, 32)
        screen_width, screen_height = screen_size
        q_t_size.put((screen_width, screen_height))
        #screen.fill(bg_color)
        #every_num_data_storage = resolve_position_or_init(screen_width, screen_height, num)
        #draw_heaps(screen, bg_color, every_num_data_storage)
        #pygame.display.update()
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                # 重新获取当前大小
                screen_size = event.size
                # 重设
                screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE, 32)
        screen_width, screen_height = screen_size
        q_t_size.put((screen, screen_width, screen_height))


def heapify(arr, the_end, the_begin, screen, bg_color, every_num_data_storage, q_t_size):
    """
    维护大顶堆的性质，前三个为基本参数，后三个用于线程通信
    :param arr: 数组-原始数据
    :param the_end: 维护到的位置，下标
    :param the_begin: 开始维护的位置，如果实现大顶堆，需要从头维护
    :param screen:
    :param bg_color:
    :param every_num_data_storage:
    :param q_t_size:
    :return:
    """
    screen, screen_width, screen_height = q_t_size.get()
    largest = the_begin
    l_son = 2 * the_begin + 1
    r_son = 2 * the_begin + 2
    if l_son < the_end and arr[the_begin] < arr[l_son]:
        largest = l_son
    if r_son < the_end and arr[largest] < arr[r_son]:
        largest = r_son
    if largest != the_begin:
        circle_x, circle_y, temp = every_num_data_storage[the_begin].circle_x, every_num_data_storage[the_begin].circle_y, (every_num_data_storage[the_begin].lf_connect, every_num_data_storage[the_begin].rt_connect, every_num_data_storage[the_begin].label_num)
        every_num_data_storage[the_begin].change_position(every_num_data_storage[largest].circle_x, every_num_data_storage[largest].circle_y, (every_num_data_storage[largest].lf_connect, every_num_data_storage[largest].rt_connect, every_num_data_storage[largest].label_num))
        every_num_data_storage[largest].change_position(circle_x, circle_y, temp)
        every_num_data_storage[largest], every_num_data_storage[the_begin] = every_num_data_storage[the_begin], every_num_data_storage[largest]
        arr[the_begin], arr[largest] = arr[largest], arr[the_begin]
        screen.fill(bg_color)
        every_num_data_storage = resolve_position_or_init(screen_width, screen_height, arr, 1, every_num_data_storage)
        draw_heaps(screen, bg_color, every_num_data_storage)
        pygame.display.update()
        heapify(arr, the_end, largest, screen, bg_color, every_num_data_storage, q_t_size)


def heapsort_low(arr, screen, bg_color, q_t_size):
    n = len(arr)
    # 初始化对象列表
    screen, screen_width, screen_height = q_t_size.get()
    every_num_data_storage = resolve_position_or_init(screen_width, screen_height, arr)
    for i in range(n // 2 - 1, -1, -1):  # 首次维护
        heapify(arr, n, i, screen, bg_color, every_num_data_storage, q_t_size)
    for i in range(n - 1, 0, -1):  # 将最大的放入最后 再维护
        arr[i], arr[0] = arr[0], arr[i]
        circle_x, circle_y, temp = every_num_data_storage[0].circle_x, every_num_data_storage[0].circle_y, (every_num_data_storage[0].lf_connect, every_num_data_storage[0].rt_connect, every_num_data_storage[0].label_num)
        every_num_data_storage[0].change_position(every_num_data_storage[i].circle_x, every_num_data_storage[i].circle_y, (every_num_data_storage[i].lf_connect, every_num_data_storage[i].rt_connect, every_num_data_storage[i].label_num))
        every_num_data_storage[i].change_position(circle_x, circle_y, temp)
        every_num_data_storage[i], every_num_data_storage[0] = every_num_data_storage[0], every_num_data_storage[i]
        heapify(arr, i, 0, screen, bg_color, every_num_data_storage, q_t_size)
        every_num_data_storage[i].done_sort(every_num_data_storage)
        screen.fill(bg_color)
        draw_heaps(screen, bg_color, every_num_data_storage)
        pygame.display.update()
    every_num_data_storage[0].done_sort(every_num_data_storage)
    screen.fill(bg_color)
    draw_heaps(screen, bg_color, every_num_data_storage)
    pygame.display.update()
    while True:
        screen, screen_width, screen_height = q_t_size.get()
        resolve_position_or_init(screen_width, screen_height, arr, 1, every_num_data_storage)
        screen.fill(bg_color)
        draw_heaps(screen, bg_color, every_num_data_storage)
        pygame.display.update()


def resolve_position_or_init(screen_width, screen_height, num, just_change_position=0, every_num_data_storage=None):
    """
    将接收到的当前屏幕大小解算，安排num中的每一个数据的位置，并返回HeapCircle的对象列表
    :param screen_width:
    :param screen_height:
    :param num: 原始数据列表
    :param just_change_position : 函数两个功能二选一，默认为初始化，num是动态的，需要根据num刷新输出
    :param every_num_data_storage: 如果是初始化，就默认不填，如果是接收到了窗口新变化，使用类方法重新改变位置
    :return: every_num_data_storage
    """
    if every_num_data_storage is None:
        every_num_data_storage = []
    num_lens = len(num)
    radius = 15  # 堆排序的半径
    backspace_x = 5  # 堆球的横向间隔，在圆心相距直径的距离上相加
    backspace_y = 5  # 可进行修改
    heap_levels = calculate_heap_levels(num_lens)  # 层数
    # 基准点 最高层位置
    if heap_levels % 2 == 0:  # 偶数层
        base_point_y = screen_height / 2 - heap_levels / 2 * (radius * 2) - radius - backspace_y * (
                heap_levels - 1) / 2.0
    else:
        base_point_y = screen_height / 2 - (heap_levels / 2.0 - 0.5) * (radius * 2) - backspace_y * (
                heap_levels - 1) / 2.0
    bottom_num = 2 ** (heap_levels - 1)
    bottom_length = bottom_num * radius * 2 + (bottom_num - 1) * backspace_x
    center_x_every_start = screen_width / 2.0 - bottom_length / 2.0
    if just_change_position == 1:
        """这里是仅仅窗口被人为拉伸所设计"""
        # 计算每一个参数
        for i in range(num_lens):
            if i == 0:  # 顶层中间
                center_x = screen_width / 2.0
            elif calculate_heap_levels(i + 1) < heap_levels:  # 中间层
                center_x = center_x_every_start + bottom_length / (2 ** (calculate_heap_levels(i + 1) - 1)) * (
                        calculate_level_and_position(i, 1) - 0.5)
            else:
                center_x = center_x_every_start + bottom_length / (2 ** (heap_levels - 1) - 1) * (
                        calculate_level_and_position(i, 1) - 1)
            center_y = base_point_y + (calculate_heap_levels(i + 1) - 1) * (radius * 2 + backspace_y)  # 后期可加空格
            every_num_data_storage[i].change_position(center_x, center_y)
        return every_num_data_storage
    else:
        """这是初始化的情况"""
        every_num_data_storage = []  # 变为列表对象
        # 计算每一个参数
        for i in range(num_lens):
            if i == 0:  # 顶层中间
                center_x = screen_width / 2.0
            elif calculate_heap_levels(i + 1) < heap_levels:  # 中间层
                center_x = center_x_every_start + bottom_length / (2 ** (calculate_heap_levels(i + 1) - 1)) * (
                        calculate_level_and_position(i, 1) - 0.5)
            else:
                center_x = center_x_every_start + bottom_length / (2 ** (heap_levels - 1) - 1) * (
                        calculate_level_and_position(i, 1) - 1)
            center_y = base_point_y + (calculate_heap_levels(i + 1) - 1) * (radius * 2 + backspace_y)  # 后期可加空格
            # 计算孩子情况
            if i * 2 + 1 <= num_lens - 1:
                lf_connect = 1
            else:
                lf_connect = 0
            if i * 2 + 2 <= num_lens - 1:
                rt_connect = 1
            else:
                rt_connect = 0
            every_num_data_storage.append(HeapCircle(num[i], i, center_x, center_y, lf_connect, rt_connect))
        return every_num_data_storage


def draw_heaps(screen, bg_color, every_num_data_storage):
    """
    将HeapCircle类对象列表全部blit到屏幕，先画线，再画实心圆，再画填充背景圆，再填数字
    :param screen:
    :param bg_color:
    :param every_num_data_storage:
    :return: 无，需要自己去update屏幕
    """
    num_font = pygame.font.SysFont('None', 20)  # 圆圈内数字
    for every in every_num_data_storage:
        if every.lf_connect:
            next_data = every_num_data_storage[every.label_num * 2 + 1]
            pygame.draw.aaline(screen, (0, 0, 0), (every.circle_x, every.circle_y),
                               (next_data.circle_x, next_data.circle_y))
        if every.rt_connect:
            next_data = every_num_data_storage[every.label_num * 2 + 2]
            pygame.draw.aaline(screen, (0, 0, 0), (every.circle_x, every.circle_y),
                               (next_data.circle_x, next_data.circle_y))
        pygame.draw.circle(screen, (0, 0, 0), center=(every.circle_x, every.circle_y), radius=16)
        pygame.draw.circle(screen, every.color, center=(every.circle_x, every.circle_y), radius=15)  # 这个可改变颜色表示状态
        num_display = num_font.render(str(every.num), True, (0, 0, 0))
        screen.blit(num_display, (every.circle_x - 5, every.circle_y - 5))


class HeapCircle:
    def __init__(self, num, label_num, circle_x, circle_y, lf_connect, rt_connect):
        self.num = num
        self.label_num = label_num
        self.circle_x = circle_x
        self.circle_y = circle_y
        self.lf_connect = lf_connect
        self.rt_connect = rt_connect
        self.color = (230, 230, 230)  # 默认背景色

    def change_position(self, circle_x, circle_y, tuple_child_label=()):
        """改变位置，和孩子情况序号情况"""
        self.circle_x = circle_x
        self.circle_y = circle_y
        if tuple_child_label:
            self.lf_connect, self.rt_connect, self.label_num = tuple_child_label

    def lose_child(self, lf_or_rt):
        """断开与孩子的连接"""
        if lf_or_rt == 1:
            self.lf_connect = 0
        elif lf_or_rt == 2:
            self.rt_connect = 0

    def dis_connect(self, every_num_data_storage):
        """断开与父的连接"""
        father_label = (self.label_num-1)//2
        if father_label*2+1 == self.label_num:
            every_num_data_storage[father_label].lose_child(1)
        else:
            every_num_data_storage[father_label].lose_child(2)

    def done_sort(self, every_num_data_storage):
        """完成排序变色，断开连接"""
        self.color = (255, 215, 0)
        self.dis_connect(every_num_data_storage)


def calculate_heap_levels(total):
    """
    输入个数，下标加1
    计算堆一共多少层
    """
    if total <= 0:
        return 0

    levels = int(math.log2(total)) + 1
    return levels


def calculate_level_and_position(index, just_position=0):
    """
    输入从下标从0开始 多情况返回 返回第几层第几个，从1开始
    :param index: 下标，数组下标
    :param just_position: 1的话，只输出在本层的位置，从1计算
    :return:
    """
    level = int(math.log2(index + 1)) + 1
    position = index - (2 ** (level - 1) - 1) + 1
    if just_position:
        return position
    else:
        return level, position


def test():
    screen_size = (1366, 768)
    pygame.init()
    pygame.display.set_caption("排序可视化程序")
    screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE, 32)  # 可调节窗口
    bg_color = (230, 230, 230)
    screen.fill(bg_color)
    num = [4, 3, 8, 9, 10, 7, 2, 9, 9, 4, 3, 5, 3, 2, 5, 8, 4, 2, 9, 9, 4, 3, 5, 3, 2, 5, 8, 4, 2, 4, 3, 8, 9, 10, 7, 2,
           9, 9, 4, 3, 5, 3, 2, 5, 8, 4, 2, 9, 9, 4, 3, 5, 3, 2, 5, 8, 4, 2, 88, 23, 56, 73, 21]
    heap_sort(screen, bg_color, num)


test()

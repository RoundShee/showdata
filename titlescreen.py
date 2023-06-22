import pygame


class Title:

    """Title具有设置主页面所有显示的功能"""
    def __init__(self, screen, bg_color):
        self.screen = screen
        self.bg_color = bg_color

        # 列出想用的字体
        font_title = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 30)
        font_sub = pygame.font.Font('./misc/Alimama_DongFangDaKai_Regular.ttf', 25)

        # 文字设置
        self.text_title = font_title.render("排序可视化", True, (0, 0, 0))
        self.text_title_rect = self.text_title.get_rect()

        self.text_sub1 = font_sub.render('①冒泡排序', True, (0, 0, 0))
        self.text_sub1_rect = self.text_sub1.get_rect()
        self.text_sub2 = font_sub.render('②插入排序', True, (0, 0, 0))
        self.text_sub2_rect = self.text_sub2.get_rect()
        self.text_sub3 = font_sub.render('③选择排序', True, (0, 0, 0))
        self.text_sub3_rect = self.text_sub3.get_rect()

        # 动画选择
        self.arrow = pygame.image.load('./misc/arrow.png')
        self.arrow_rect = self.arrow.get_rect()

        self.choice = [81, 131, 171]
        self.choice_i = 0
        self.arrow_rect_top = 81
        self.arrow_rect_left = 512 - self.text_sub1_rect.width/2.0 - self.arrow_rect.width

    """页面字体显示"""
    def show_title(self):
        # 显示字体
        self.screen.blit(self.text_title, ((1024 - self.text_title_rect.width) / 2.0, 40))
        self.screen.blit(self.text_sub1, ((1024 - self.text_sub1_rect.width) / 2.0, (80 + (self.text_sub1_rect.height +
                                                                                           20) * 1)))
        self.screen.blit(self.text_sub2, ((1024 - self.text_sub2_rect.width) / 2.0, (80 + (self.text_sub2_rect.height +
                                                                                           20) * 2)))
        self.screen.blit(self.text_sub3, ((1024 - self.text_sub3_rect.width) / 2.0, (80 + (self.text_sub3_rect.height +
                                                                                           20) * 3)))

    """将指针向下循环移动"""
    def choice_next(self):
        if self.choice_i == 2:
            self.choice_i = 0
        else:
            self.choice_i += 1
        self.arrow_rect_top = self.choice[self.choice_i]
        return self.choice_i
    """将指针向上循环移动"""
    def choice_previous(self):
        if self.choice_i == 0:
            self.choice_i = 2
        else:
            self.choice_i -= 1
        self.arrow_rect_top = self.choice[self.choice_i]
        return self.choice_i
    """手动刷新screen"""
    def all_blit(self):
        self.screen.fill(self.bg_color)
        self.show_title()
        self.screen.blit(self.arrow, ((self.arrow_rect_left, self.arrow_rect_top), (self.arrow_rect.width, self.arrow_rect.height)))


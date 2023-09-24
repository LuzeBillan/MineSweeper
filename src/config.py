import pygame
import random
import sys
import time

pygame.init()  # 初始化


class Color:
    WHITE = (255, 255, 255)
    GREY = (230, 230, 230)
    DGREY = (200, 200, 200)
    LDDGREY = (180, 180, 180)
    DDGREY = (150, 150, 150)
    LDDDGREY = (120, 120, 120)
    DDDGREY = (100, 100, 100)
    BLACK = (0, 0, 0)
    GOLD = (255, 215, 0)
    YELLOW = (255, 215, 0)
    RED = (255, 68, 68)
    DRED = (200, 10, 10)
    PINK = (255, 51, 187)
    GREEN = (34, 187, 51)
    DGREEN = (50, 180, 50)
    BLUE = (120, 120, 240)
    LBLUE = (119, 153, 255)
    COL_BG = (255, 255, 250)


class Sys:
    version = "2.0.0"
    flag = 0

    row = 15
    column = 10
    quantity = 10

    TEXT_FONT = pygame.font.Font("HarmonyOS_Sans_Regular.ttf", 16)
    NUM_FONT = pygame.font.Font("JetBrainsMono-ExtraBold.ttf", 23)
    TEXT_WIN = TEXT_FONT.render("You wins!", True, Color.GREEN, None)
    TEXT_LOSE = TEXT_FONT.render("You loses.", True, Color.DRED, None)
    TEXT_X = NUM_FONT.render("X", True, Color.DRED, None)

    BLO_WID_STANDARD = 30
    rate = 1
    BLO_WID = BLO_WID_STANDARD * rate
    WIN_WIDTH = column * BLO_WID + 10
    WIN_HEIGHT = row * BLO_WID + 70
    seed_created = False

    main_screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)  # 创建窗口（长，宽，特性，色深）

    menu = None
    events = []
    objects = []
    entities = []
    menu_items = []

    mouse_current = (0, 0)
    left_down = (0, 0)
    left_release = (0, 0)
    middle_down = (0, 0)
    middle_release = (0, 0)
    right_down = (0, 0)
    right_release = (0, 0)
    mice_down = []
    mice_release = []
    object_selected = -1
    entity_selected = -1

    clock = pygame.time.Clock()

    @staticmethod
    def reload():
        Sys.flag = -1
        Sys.entities = []
        Sys.WIN_WIDTH = Sys.column * Sys.BLO_WID + 10
        Sys.WIN_HEIGHT = Sys.row * Sys.BLO_WID + 70
        Sys.left_down = (0, 0)
        Sys.left_release = (0, 0)
        Sys.middle_down = (0, 0)
        Sys.middle_release = (0, 0)
        Sys.right_down = (0, 0)
        Sys.right_release = (0, 0)
        Sys.object_selected = -1
        Sys.entity_selected = -1
        print("Sys.reload()")
        Sys.seed_created = False

    @staticmethod
    def updates():
        for obj in Sys.objects:
            obj.update()
        for entity in Sys.entities:
            entity.update()

    @staticmethod
    # Get input info.
    def event_handler():
        for event in Sys.events:
            Sys.mouse_current = pygame.mouse.get_pos()
            # Force to ignore the discrepancies between declared parameters and actual arguments.
            # noinspection PyArgumentList
            Sys.mice_down = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # 菜单
                    Sys.menu.is_held_left = not Sys.menu.is_held_left
                    Sys.menu.is_released_left = not Sys.menu.is_released_left
                elif event.key == pygame.K_TAB:
                    Sys.object_selected += 1
                elif event.key == pygame.K_F5:  # 新游戏
                    Sys.flag = -1
                elif event.key == pygame.K_F1:  # 答案（命令行）
                    for i in Sys.objects[0: Sys.row * Sys.column]:
                        if i.is_mine:
                            print(i.index, end="\t")
                    print()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Sys.mice_down[1]:
                    Sys.middle_down = Sys.mouse_current
                    return True
                elif event.button == 1:  # 左键
                    Sys.left_down = Sys.mouse_current
                    # print("left mouse downs")
                    return True
                if event.button == 3:  # 右键
                    Sys.right_down = Sys.mouse_current
                    # print("right mouse downs")
                    return True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 左键
                    Sys.left_release = Sys.mouse_current
                    # print("left mouse releases")
                    return True
                if event.button == 3:  # 右键
                    Sys.right_release = Sys.mouse_current
                    # print("right mouse releases")
                    return True


pygame.display.set_caption("Mine Sweeper " + Sys.version)  # 窗口标题

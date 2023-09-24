import pygame
import random
import sys
import time

pygame.init()  # 初始化
version = '1.0.0'
# 变量池
line = 15
row = 10
BLO_WID = 30
# WIN_POI_WID, WIN_POI_HEI = 240, 150
WIN_WID, WIN_HEI = row * BLO_WID + 10, line * BLO_WID + 70
OPT_FONT = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 16)
NUM_FONT = pygame.font.SysFont(None, 30)
X = 0
Y = 0
butType = 0
numMine = 15  # numMine是雷的数量
cli = 0
menuBool = 0
string = []
output = ''
loca = 0
WHITE = (255, 255, 255)
GREY = (230, 230, 230)
DGREY = (200, 200, 200)
DDGREY = (150, 150, 150)
DDDGREY = (100, 100, 100)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
RED = (220, 0, 0)
GREEN = (50, 180, 50)
BLUE = (50, 50, 180)
COL_BG = (255, 255, 250)
LOSE_TEXT = NUM_FONT.render('Lose', True, DDDGREY, None)
WIN_TEXT = NUM_FONT.render('Win!', True, DDDGREY, None)
display = []  # 确定雷周围的数字 大
assis = []  # 确定需要显示的位置 大
button = []  # 确定标记的雷的位置 小

# 定义窗口
# os.environ['SDl_VIDEO_WINDOW_POS'] = "%d, %d" % (WIN_POI_WID, WIN_POI_HEI)  # 固定窗口位置
mainScreen = pygame.display.set_mode((WIN_WID, WIN_HEI), 0, 32)  # 创建窗口（长，宽，特性，色深）
pygame.display.set_caption('MineSweeper')  # 窗口标题


def cornerSolution(beta):
    if beta == 0:
        return [beta + 1, beta + row, beta + row + 1]
    elif beta == row - 1:
        return [beta - 1, beta + row - 1, beta + row]
    elif beta == row * (line - 1):
        return [beta - row, beta - row + 1, beta + 1]
    elif beta == row * line - 1:
        return [beta - row, beta - row - 1, beta - 1]
    elif 0 < beta < row - 1:
        return [beta - 1, beta + 1, beta + row - 1, beta + row, beta + row + 1]
    elif (beta < row * line) and ((beta / row) % 1 == 0):
        return [beta - row, beta - row + 1, beta + 1, beta + row, beta + row + 1]
    elif (beta < row * line - 1) and (((beta + 1) / row) % 1 == 0):
        return [beta - row, beta - row - 1, beta - 1, beta + row - 1, beta + row]
    elif row * (line - 1) < beta < row * line - 1:
        return [beta - 1, beta + 1, beta - row - 1, beta - row, beta - row + 1]
    elif row < beta < row * (line - 1) - 1:
        return [beta - 1, beta + 1, beta - row - 1, beta - row, beta - row + 1, beta + row - 1, beta + row,
                beta + row + 1]
    else:
        return []


# 获取输入信息
def eventCheck():
    global X, Y, butType, assis, menuBool, string, output, loca
    for event in pygame.event.get():
        mouse_pressed = pygame.mouse.get_pressed()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_F5:
                linkStart()
            elif event.key == pygame.K_HOME:
                menuBool = openMenu(menuBool)
                mainDisplay(option)
                pygame.display.update()
            elif menuBool == 1:
                press(event.key, event.unicode)
                optionMenu()
                pygame.display.update()
            elif event.key == pygame.K_F1:
                print(button)
                print(location)
        if (mouse_pressed[0] and mouse_pressed[2]) or mouse_pressed[1]:
            X, Y = pygame.mouse.get_pos()
            butType = 6
            doubleClick()
            return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            output = ''
            loca = 0
            string = []
            if event.button == 1:  # 左键
                X, Y = pygame.mouse.get_pos()
                if 1 <= X <= 130 and 1 <= Y <= 25:
                    menuBool = openMenu(menuBool)
                butType = 1
                mouseDefLe()
                unfold()
                return True
            if event.button == 3:  # 右键
                X, Y = pygame.mouse.get_pos()
                butType = 3
                mouseDefRi()
                return True


def eventCheckTrue():
    while True:
        if eventCheck():
            return


def mineUpdate():
    global line, row, numMine, X, Y
    if 0 < X < 130 and 25 < Y < 50:
        line = output
    elif 0 < X < 130 and 50 < Y < 75:
        row = output
    elif 0 < X < 130 and 75 < Y < 100:
        numMine = output
    if line * row > 1200:
        line = 15
        row = 10
        warningText = OPT_FONT.render('Too much objects on the screen!', True, RED, None)
        mainScreen.blit(warningText, (43, 22))
        pygame.display.update()
        time.sleep(1.00)


def press(key, name):
    global string, output, loca, line, row, numMine, X, Y
    if str(key) == '13':  # enter
        if len(string) != 0:
            output = int(''.join(string))
            mineUpdate()
        Y += 25
        loca = 0
        string = []
        output = ''
        linkStart()
    elif str(key) == '8':  # backspace
        if string != [] and loca != 0:
            string.pop(loca - 1)
            output = ''.join(string)
            loca += -1
    elif str(key) == '127':  # delete
        if string != [] and loca != len(string):
            string.pop(loca)
            output = ''.join(string)
    elif str(key) == '1073741904':  # left
        if loca != 0:
            loca += -1
    elif str(key) == '1073741903':  # right
        if loca != len(string):
            loca += 1
    elif str(key) == '1073741906':  # up
        if len(string) != 0:
            output = int(''.join(string))
            mineUpdate()
        Y += -25
        loca = 0
        string = []
        output = ''
        linkStart()
    elif str(key) == '1073741905':  # down
        if len(string) != 0:
            output = int(''.join(string))
            mineUpdate()
        Y += 25
        loca = 0
        string = []
        output = ''
        linkStart()
    elif str(key) == '1073742050':  # space
        string.insert(loca, ' ')
        output = ''.join(string)
        loca += 1
    elif str(key) == '9':  # tab
        if len(string) != 0:
            output = int(''.join(string))
            mineUpdate()
        Y += 25
        loca = 0
        string = []
        output = ''
        linkStart()
    elif str(key) == '1073742049':  # shift
        pass
    elif name in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9') and len(string) <= 5:
        string.insert(loca, str(name))
        output = ''.join(string)
        loca += 1


def doubleClick():
    global assis, cli, option, firstPress
    if 5 < X < WIN_WID - 5 and 65 < Y < WIN_HEI - 5:
        num = int((X - 5) / 30 // 1 + row * ((Y - 65) / 30 // 1))
    else:
        num = line * row

    for i in cornerSolution(num):
        if not i in button:
            firstPress = 1
            if i in location:
                cli = 1
            else:
                cli = 0
            assis[i] = 1
            endCal()


# 创建地图种子
def seedCre(num):
    global location
    choiceList = list(range(line * row))
    if 0 <= num < line * row:
        choiceList.pop(num)
    location = random.sample(choiceList, numMine)
    for i in range(line * row + 1):
        display.append(0)
        assis.append(0)


# 创建display列表
def disCre():
    for i in range(line * row):
        a = 0
        for j in cornerSolution(i):
            if j in location:
                a += 1
        display[i] = a
    for i in location:
        display[i] = -1


# 绘制网络
def blockDraw():
    for x in range(row):
        for y in range(line):
            pygame.draw.rect(mainScreen, DDDGREY, (x * BLO_WID + 5, y * BLO_WID + 65, BLO_WID, BLO_WID), 1)
            pygame.draw.rect(mainScreen, DGREY, (x * BLO_WID + 6, y * BLO_WID + 66, BLO_WID - 2, BLO_WID - 2), 0)
            pygame.draw.rect(mainScreen, GREY, (x * BLO_WID + 6, y * BLO_WID + 66, BLO_WID - 4, BLO_WID / 15), 0)
            pygame.draw.rect(mainScreen, GREY, (x * BLO_WID + 6, y * BLO_WID + 66, BLO_WID / 15, BLO_WID - 4), 0)
            pygame.draw.rect(mainScreen, DDGREY, (x * BLO_WID + 6, (y + 1) * BLO_WID + 62, BLO_WID - 4, BLO_WID / 15),
                             0)
            pygame.draw.rect(mainScreen, DDGREY, ((x + 1) * BLO_WID + 2, y * BLO_WID + 68, BLO_WID / 15, BLO_WID - 4),
                             0)


# 绘制菜单栏
def menuDraw():
    pygame.draw.line(mainScreen, GREY, (0, 25), (WIN_WID, 25), 1)
    pygame.draw.line(mainScreen, GREY, (129, 2), (129, 22), 1)
    menuText = OPT_FONT.render('Menu', True, DDDGREY, None)
    mainScreen.blit(menuText, (43, 3))
    numMineText = OPT_FONT.render('Number of mines :', True, DDDGREY, None)
    mainScreen.blit(numMineText, (5, 27))
    numMineText = OPT_FONT.render(str(numMine - len(button))+' / '+str(numMine)+' / '+str(line*row), True, DDDGREY, None)
    mainScreen.blit(numMineText, (151, 28))


# 根据display绘制信息
def numDraw():
    for i in range(row * line):
        if option == 2:
            color = GREEN
        else:
            color = RED
        if assis[i] == 1:
            pygame.draw.rect(mainScreen, DDGREY,
                             (BLO_WID * (i % row) + 6, BLO_WID * (i // row) + 66, BLO_WID - 2, BLO_WID - 2), 0)
            if 0 < display[i] < 9:
                NUM_TEXT = NUM_FONT.render(str(display[i]), True, BLACK, None)
                mainScreen.blit(NUM_TEXT, [BLO_WID * (i % row) + 14, BLO_WID * (i // row) + 71])
            elif display[i] == -1:
                pygame.draw.rect(mainScreen, color,
                                 (BLO_WID * (i % row) + 6, BLO_WID * (i // row) + 66, BLO_WID - 2, BLO_WID - 2), 0)
        elif assis[i] == 2:
            NUM_TEXT = NUM_FONT.render('X', True, RED, None)
            mainScreen.blit(NUM_TEXT, (BLO_WID * (i % row) + 13, BLO_WID * (i // row) + 72, BLO_WID, BLO_WID))
        elif assis[i] == 3:
            NUM_TEXT = NUM_FONT.render('?', True, BLUE, None)
            mainScreen.blit(NUM_TEXT, (BLO_WID * (i % row) + 14, BLO_WID * (i // row) + 71, BLO_WID, BLO_WID))


def openMenu(n):
    for j in range(26 * n, 26 + 26 * n * (-1), (-2) * n + 1):
        mainScreen.fill(COL_BG)
        blockDraw()
        menuDraw()
        numDraw()
        pygame.draw.rect(mainScreen, COL_BG, (0, 0, 130, 3 + 6 * j), 0)
        for i in range(5):
            pygame.draw.line(mainScreen, WHITE, (0, 25 + j * i), (129, 25 + j * i), 1)
        pygame.display.update()
        time.sleep(0.008)
    n = (-1) * n + 1
    return n


def optionMenu():
    global menuBool
    pygame.draw.rect(mainScreen, COL_BG, (0, 0, 130, 6 * 25), 0)
    for i in range(5):
        pygame.draw.line(mainScreen, GREY, (0, 25 + 25 * i), (130, 25 + 25 * i), 1)
    pygame.draw.rect(mainScreen, GREY, (0, 0, 130, 150), 1)
    menuText = OPT_FONT.render('Menu', True, DDDGREY, None)
    mainScreen.blit(menuText, (43, 3))
    menuText = OPT_FONT.render('Row:', True, DDDGREY, None)
    mainScreen.blit(menuText, (4, 28))
    menuText = OPT_FONT.render('Column:', True, DDDGREY, None)
    mainScreen.blit(menuText, (4, 53))
    menuText = OPT_FONT.render('Number:', True, DDDGREY, None)
    mainScreen.blit(menuText, (4, 78))
    menuText = OPT_FONT.render('New Game', True, DDDGREY, None)
    mainScreen.blit(menuText, (4, 103))
    menuText = OPT_FONT.render('F5', True, DGREY, None)
    mainScreen.blit(menuText, (107, 103))
    menuText = OPT_FONT.render('Quit', True, DDDGREY, None)
    mainScreen.blit(menuText, (4, 128))
    menuText = OPT_FONT.render('Esc', True, DGREY, None)
    mainScreen.blit(menuText, (100, 128))

    def cursor(n):
        pygame.draw.line(mainScreen, BLACK, (73 + 9 * loca, 29 + 25 * n), (73 + 9 * loca, 46 + 25 * n), 1)

    if 0 < X < 130 and 25 < Y < 50:
        pygame.draw.line(mainScreen, DDGREY, (71, 48), (126, 48), 1)
        inPutText = OPT_FONT.render(output, True, DDGREY, None)
        mainScreen.blit(inPutText, (73, 28))
        cursor(0)
    elif 0 < X < 130 and 50 < Y < 75:
        pygame.draw.line(mainScreen, DDGREY, (71, 73), (126, 73), 1)
        inPutText = OPT_FONT.render(output, True, DDGREY, None)
        mainScreen.blit(inPutText, (73, 53))
        cursor(1)
    elif 0 < X < 130 and 75 < Y < 100:
        pygame.draw.line(mainScreen, DDGREY, (71, 98), (126, 98), 1)
        inPutText = OPT_FONT.render(output, True, DDGREY, None)
        mainScreen.blit(inPutText, (73, 78))
        cursor(2)
    elif 0 < X < 130 and 100 < Y < 125:
        menuBool = openMenu(menuBool)
        linkStart()
    elif 0 < X < 130 and 125 < Y < 150:
        pygame.quit()
        sys.exit()


# 控制展开
def unfold():
    spread = [num]
    for i in spread:
        if display[i] == 0 and butType == 1:
            for j in cornerSolution(i):
                if i == j:
                    assis[j] = 1
                elif (not j in location) and j not in button and assis[j] == 0:
                    assis[j] = 1
                    spread.append(j)
            mainDisplay(option)
            pygame.display.update()
            time.sleep(0.01)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_F5:
                        linkStart()


# 确定光标坐标的含义 左键
def mouseDefLe():
    global X, Y, num, cli, menuBool, firstPress
    if menuBool != 0:
        if not (0 < X < 130 and 0 < Y < 150):
            num = int((X - 5) / 30 // 1 + row * ((Y - 65) / 30 // 1))
            menuBool = 0
    else:
        if 5 < X < WIN_WID - 5 and 65 < Y < WIN_HEI - 5:
            num = int((X - 5) / 30 // 1 + row * ((Y - 65) / 30 // 1))
            firstPress = 1
            if num in button:
                cli = 0
                assis[num] = 0
                button.remove(num)
            else:
                if num in location:
                    cli = 1
                else:
                    cli = 0
                assis[num] = 1


# 确定光标坐标的含义 右键
def mouseDefRi():
    global X, Y, num, cli, menuBool
    if menuBool != 0:
        if not (0 < X < 130 and 0 < Y < 150):
            menuBool = 0
    else:
        if 5 < X < WIN_WID - 5 and 65 < Y < WIN_HEI - 5:
            num = int((X - 5) / 30 // 1 + row * ((Y - 65) / 30 // 1))
            cli = 0
            if assis[num] == 0:
                assis[num] = 2
                if num not in button:
                    button.append(num)
            elif assis[num] == 2:
                cli = 0
                assis[num] = 3
                button.remove(num)
            elif assis[num] == 3:
                assis[num] = 0


# 判断是否有剩下的
def last():
    for i in range(row * line):
        if assis[i] == 0 or assis[i] == 3:
            return False
    return True


# 对于结局的判断
def endCal():
    global option
    if cli == 1 and assis[num] == 1:
        option = 0
    if set(button) == set(location) and last():
        option = 2


# 主显示模块
def mainDisplay(n):
    mainScreen.fill(COL_BG)
    blockDraw()
    menuDraw()
    numDraw()
    if n == 0:
        mainScreen.blit(LOSE_TEXT, (5, 45))
    elif n == 2:
        mainScreen.blit(WIN_TEXT, (5, 45))
    if menuBool == 1:
        optionMenu()


# 主程序

def linkStart():
    global display, assis, button, option, num, X, Y, butType, mainScreen, WIN_WID, WIN_HEI, firstPress, cli
    WIN_WID, WIN_HEI = row * BLO_WID + 10, line * BLO_WID + 70
    mainScreen = pygame.display.set_mode((WIN_WID, WIN_HEI), 0, 32)
    display, assis, button = [], [], []
    option = 1
    num = row * line
    firstPress, butType = 0, 0
    seedCre(num)
    disCre()
    mainDisplay(option)
    pygame.display.update()
    while firstPress == 0:
        eventCheckTrue()
        if butType == 6:
            linkStart()
        while num in location and butType == 1:
            display, assis, button = [], [], []
            seedCre(num)
            disCre()
            assis[num] = 1
        cli = 0
        unfold()
        endCal()
        mainDisplay(option)
        pygame.display.update()
    while option == 1:
        eventCheckTrue()
        endCal()
        mainDisplay(option)
        pygame.display.update()
    while option == 0:
        for i in location:
            assis[i] = 1
            for i in range(20):
                eventCheck()
                time.sleep(0.01)
                mainDisplay(option)
                pygame.display.update()
    while option == 2:
        for i in location:
            assis[i] = 1
            for i in range(20):
                eventCheck()
                time.sleep(0.01)
                mainDisplay(option)
                pygame.display.update()


if __name__ == "__main__":
    linkStart()

from src.block import *
from src.menu import *


# Create a seed.
def create_seed():
    Sys.seed_created = True
    id_range = list(range(Sys.row * Sys.column))
    id_range.pop(Sys.entity_selected)
    mines = random.sample(id_range, Sys.quantity)
    for i in mines:
        Sys.entities[i].is_mine = True
    for i in Sys.entities[0: Sys.row * Sys.column]:
        for j in i.surroundings:
            if Sys.entities[j].is_mine:
                i.mines_surrounding += 1
            i.TEXT = Sys.NUM_FONT.render(str(i.mines_surrounding), True, (30 * i.mines_surrounding, 0, 0), None)
    print("Seed created!")


# Initiate all Sys.entities.
def init_entities():
    for y in range(Sys.row):
        for x in range(Sys.column):
            Block(x * Sys.BLO_WID + 5, y * Sys.BLO_WID + 65)


def init_objects():
    Sys.menu = Menu()
    MenuItem(y=5 + Sys.BLO_WID * 1, text="Row : ")
    MenuItem(y=5 + Sys.BLO_WID * 2, text="Column : ")
    MenuItem(y=5 + Sys.BLO_WID * 3, text="Quantity : ")
    MenuItem(y=5 + Sys.BLO_WID * 4, text="New Game!")
    MenuItem(y=5 + Sys.BLO_WID * 5, text="Auto run.")
    MenuItem(y=5 + Sys.BLO_WID * 6, text="Exit.")
    InputBox(x=105, y=7 + Sys.BLO_WID * 1, target=0, base=[Sys.objects[1]])
    InputBox(x=105, y=7 + Sys.BLO_WID * 2, target=1, base=[Sys.objects[2]])
    InputBox(x=105, y=7 + Sys.BLO_WID * 3, target=2, base=[Sys.objects[3]])


# updates() is whatever runs per frame.
def updates():
    Sys.main_screen.fill(Color.COL_BG)
    Sys.events = pygame.event.get()
    Sys.event_handler()
    for ent in Sys.entities:
        ent.update()
    for obj in Sys.objects:
        obj.update()
    Sys.clock.tick(50)
    # print("A frame.")


def win_check():
    for block in Sys.entities[0: Sys.row * Sys.column]:
        if (block.is_mine and not block.is_marked) or not (block.is_mine or block.is_activated):
            return False
    return True


def main():
    init_objects()
    # A whole game.
    while True:
        # before a new game.
        Sys.main_screen = pygame.display.set_mode((Sys.WIN_WIDTH, Sys.WIN_HEIGHT), 0, 32)  # 创建窗口（长，宽，特性，色深）

        Sys.flag = 0
        init_entities()
        # During the game.
        while Sys.flag == 0:
            updates()
            pygame.display.update()
            if 0 <= Sys.entity_selected < Sys.row * Sys.column:
                create_seed()
                Sys.flag = 1
        while Sys.flag == 1:
            updates()
            pygame.display.update()
            if win_check():
                Sys.flag = 2
        while Sys.flag == 2:
            updates()
            Sys.main_screen.blit(Sys.TEXT_WIN, (5, 45))
            pygame.display.update()
        while Sys.flag == 3:
            updates()
            Sys.main_screen.blit(Sys.TEXT_LOSE, (5, 45))
            pygame.display.update()
        # After a game.
        Sys.reload()


if __name__ == "__main__":
    main()

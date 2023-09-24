import time

from src.entity import *


# The base class of blocks.
class Block(Entity):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_mine = False
        self.is_marked = False
        self.mines_surrounding = 0
        self.surroundings = self.get_surroundings()

    def update(self):
        super(Block, self).update()
        if self.is_activated:
            if Sys.menu.is_switched:
                self.is_held_left = False
                self.is_released_left = False
                self.is_held_right = False
                self.is_released_right = False
            elif self.mouse_handler(Sys.middle_down) and Sys.seed_created:
                self.unfold()
                for surrounding in self.surroundings:
                    if not Sys.entities[surrounding].is_marked:
                        Sys.entities[surrounding].is_switched = True
            self.marked_handler()
            self.unfold_handler()

    def display(self):
        super(Block, self).display()
        if not self.is_switched:
            self.block_skin()
            if self.is_marked:
                Sys.main_screen.blit(Sys.TEXT_X, (self.x + 8, self.y))
        elif not self.is_mine:
            pygame.draw.rect(Sys.main_screen, Color.DDGREY, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 0)
            if self.mines_surrounding != 0:
                Sys.main_screen.blit(self.TEXT, (self.x + 8, self.y))
        else:
            pygame.draw.rect(Sys.main_screen, Color.DRED, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 0)
            if Sys.flag == 1:
                Sys.flag = 3

    def marked_handler(self):
        if self.is_held_right and self.is_released_right:
            self.is_marked = not self.is_marked
            Sys.right_down = (0, 0)
            Sys.right_release = (0, 0)

    def unfold_handler(self):
        if Sys.entity_selected == self.index:
            self.unfold(True)

    def unfold(self, switcher=False):
        if (not self.is_switched or switcher) and Sys.flag == 1:
            self.is_switched = True
            if not self.mines_surrounding:
                for i in self.surroundings:
                    Sys.entities[i].unfold()

    def get_surroundings(self):
        if self.index == 0:
            return [self.index + 1, self.index + Sys.column, self.index + Sys.column + 1]
        elif self.index == Sys.column - 1:
            return [self.index - 1, self.index + Sys.column - 1, self.index + Sys.column]
        elif self.index == Sys.column * (Sys.row - 1):
            return [self.index - Sys.column, self.index - Sys.column + 1, self.index + 1]
        elif self.index == Sys.column * Sys.row - 1:
            return [self.index - Sys.column, self.index - Sys.column - 1, self.index - 1]
        elif 0 < self.index < Sys.column - 1:
            return [self.index - 1, self.index + 1, self.index + Sys.column - 1, self.index + Sys.column, self.index + Sys.column + 1]
        elif (self.index < Sys.column * Sys.row) and ((self.index / Sys.column) % 1 == 0):
            return [self.index - Sys.column, self.index - Sys.column + 1, self.index + 1, self.index + Sys.column,
                    self.index + Sys.column + 1]
        elif (self.index < Sys.column * Sys.row - 1) and (((self.index + 1) / Sys.column) % 1 == 0):
            return [self.index - Sys.column, self.index - Sys.column - 1, self.index - 1, self.index + Sys.column - 1,
                    self.index + Sys.column]
        elif Sys.column * (Sys.row - 1) < self.index < Sys.column * Sys.row - 1:
            return [self.index - 1, self.index + 1, self.index - Sys.column - 1, self.index - Sys.column, self.index - Sys.column + 1]
        elif Sys.column < self.index < Sys.column * (Sys.row - 1) - 1:
            return [self.index - 1, self.index + 1, self.index - Sys.column - 1, self.index - Sys.column, self.index - Sys.column + 1,
                    self.index + Sys.column - 1, self.index + Sys.column,
                    self.index + Sys.column + 1]
        return []

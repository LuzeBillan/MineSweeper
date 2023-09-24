from src.object import *
from src.inputbox import *
from src.autorun import *


class Menu(Object):

    def __init__(self, x=5, y=5, is_activated=True):
        super(Menu, self).__init__(x, y, width=150, is_activated=is_activated)
        self.TEXT = Sys.TEXT_FONT.render("Options", True, Color.BLACK, None)

    def update(self):
        super(Menu, self).update()
        Menu.item_func()

    def display(self):
        super(Menu, self).display()
        if not self.is_switched:
            self.block_skin()
        else:
            pygame.draw.rect(Sys.main_screen, Color.GREY, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 0)
        Sys.main_screen.blit(self.TEXT, (self.x + 46, self.y + 5))

    def switch_handler(self):
        if self.is_held_left and self.is_released_left:
            Sys.object_selected = self.index
            self.is_switched = True
            self.height = Sys.BLO_WID + Sys.BLO_WID * 6
            self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
            for item in Sys.objects[1:]:
                item.is_activated = True
        else:
            Sys.object_selected = -1
            self.is_switched = False
            self.height = Sys.BLO_WID
            self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
            for item in Sys.objects[1:]:
                item.is_activated = False

    @staticmethod
    def item_func():
        if Sys.objects[4].is_switched:
            Sys.reload()
            Sys.objects[4].is_switched = False
        elif Sys.objects[5].is_switched:
            auto_run()
            Sys.objects[5].is_switched = False
        elif Sys.objects[6].is_switched:
            pygame.quit()
            sys.exit()


class MenuItem(Menu):

    def __init__(self, y, text: str):
        super(MenuItem, self).__init__(y=y, is_activated=False)
        self.TEXT = Sys.TEXT_FONT.render(text, True, Color.BLACK, None)

    def update(self):
        super(MenuItem, self).update()

    def display(self):
        super(MenuItem, self).display()
        if self.is_suspended:
            pygame.draw.rect(Sys.main_screen, Color.DGREY, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 0)
        else:
            pygame.draw.rect(Sys.main_screen, Color.GREY, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 0)
        Sys.main_screen.blit(self.TEXT, (self.x + 2, self.y + 6))

    def switch_handler(self):
        if self.is_held_left and self.is_released_left:
            self.is_switched = True
        else:
            self.is_switched = False

    def switch_on_handler(self):
        if self.is_switched:
            Sys.object_selected = self.index
            Sys.left_down = (0, 0)
            Sys.left_release = (0, 0)
            self.menu_item_activated_function()
            self.is_switched = False

    def menu_item_activated_function(self):
        if self.index == 1:
            Sys.row = InputBox(self.x + 100, self.y + 3).event_handler()
        elif self.index == 2:
            Sys.column = InputBox(self.x + 100, self.y + 3).event_handler()
        elif self.index == 3:
            Sys.quantity = InputBox(self.x + 100, self.y + 3).event_handler()
        elif self.index == 4:
            Sys.reload()
        elif self.index == 5:
            auto_run()
        elif self.index == 6:
            pygame.quit()
            sys.exit()

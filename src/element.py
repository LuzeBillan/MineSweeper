from src.config import *


# The base class of all objects.
class Element:

    def __init__(self, x=5, y=5, width=Sys.BLO_WID, height=Sys.BLO_WID, is_activated=True):
        self.x = x  # Its top-left corner.
        self.y = y
        self.width = width
        self.height = height
        self.index = -32768
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_activated = is_activated  # True iff the mouse has clicked on it.
        self.is_suspended = False  # True iff the mouse is suspending on it.
        self.is_switched = False  # True iff it is on used.
        self.is_held_left = False  # True iff the left mouse is downing on it.
        self.is_released_left = False  # True iff the left mouse releases it.
        self.is_held_right = False  # True iff the right mouse is downing on it.
        self.is_released_right = False  # True iff the right mouse releases it.
        self.TEXT = None
        # print(str(self.index), "has been created.")

    def update(self):
        if self.is_activated:
            self.display()
            self.switch_handler()
            self.is_suspended = self.mouse_handler(Sys.mouse_current)
            self.is_held_left = self.mouse_handler(Sys.left_down)
            self.is_released_left = self.mouse_handler(Sys.left_release)
            self.is_held_right = self.mouse_handler(Sys.right_down)
            self.is_released_right = self.mouse_handler(Sys.right_release)

    def mouse_handler(self, condition: list) -> int:  # -> bool
        # return self.x < condition_list[0] < self.x + self.width and self.y < condition_list[1] < self.y + self.height
        return self.collider.collidepoint(condition)

    def switch_handler(self):
        if self.is_held_left and self.is_released_left:
            self.is_switched = not self.is_switched

    def display(self):
        pygame.draw.rect(Sys.main_screen, Color.DDDGREY, self.collider, 0)

    def block_skin(self):
        if not self.is_switched:
            if self.is_suspended:
                pygame.draw.rect(Sys.main_screen, Color.LDDDGREY, (self.x + 3, self.y + 1, self.width - 4, self.height - 2), 0)
                pygame.draw.rect(Sys.main_screen, Color.DGREY, (self.x + 1, self.y + 1, self.width - 4, self.height - 4), 0)
                pygame.draw.rect(Sys.main_screen, Color.LDDGREY, (self.x + 3, self.y + 3, self.width - 6, self.height - 6), 0)
            else:
                pygame.draw.rect(Sys.main_screen, Color.DDGREY, (self.x + 3, self.y + 1, self.width - 4, self.height - 2), 0)
                pygame.draw.rect(Sys.main_screen, Color.GREY, (self.x + 1, self.y + 1, self.width - 4, self.height - 4), 0)
                pygame.draw.rect(Sys.main_screen, Color.DGREY, (self.x + 3, self.y + 3, self.width - 6, self.height - 6), 0)
        else:
            pygame.draw.rect(Sys.main_screen, Color.GREY, (self.x + 1, self.y + 1, self.width - 2, self.height - 2), 0)

from src.object import *


class InputBox(Object):
    default_width = 40

    def __init__(self, x=5, y=5, text="", target=0, base=None):
        super().__init__(x, y)
        self.TEXT = text
        self.color = Color.LBLUE
        self.text_surface = Sys.TEXT_FONT.render(text, True, self.color, None)
        self.width = InputBox.default_width
        self.height = self.text_surface.get_height()
        self.line = pygame.Rect(x, y + self.height, self.width, 1)
        self.target = target
        self.base = base
        print(self.index)

    def event_handler(self):
        for event in Sys.events:
            if event.type == pygame.KEYDOWN:
                if self.is_activated:
                    if event.key == pygame.K_RETURN:
                        if self.TEXT != "":
                            if self.target == 0:
                                Sys.row = int(float(self.TEXT))
                            elif self.target == 1:
                                Sys.column = int(float(self.TEXT))
                            elif self.target == 2:
                                Sys.quantity = int(float(self.TEXT))
                            self.TEXT = ""
                        Sys.reload()
                    elif event.key == pygame.K_BACKSPACE:
                        self.TEXT = self.TEXT[:-1]
                    elif event.unicode in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9") and len(self.TEXT) <= 5:
                        self.TEXT += event.unicode
                    # Re-render the text.
                    self.text_surface = Sys.TEXT_FONT.render(self.TEXT, True, self.color, None)

    def update(self):
        self.is_switched = self.base[0].is_switched
        super(InputBox, self).update()
        if self.is_switched:
            self.event_handler()
            # Resize the box if the text is too long.
            self.width = max(InputBox.default_width, self.text_surface.get_width() + 10)

    def switch_handler(self):
        self.color = Color.GREEN if self.is_switched else Color.LBLUE

    def display(self):
        # Blit the rect.
        pygame.draw.rect(Sys.main_screen, self.color, self.line, 1)
        # Blit the text.
        Sys.main_screen.blit(self.text_surface, (self.collider.x + 5, self.collider.y + 5))

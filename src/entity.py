from src.element import *


# The base class of all objects.
class Entity(Element):

    def __init__(self, x=5, y=5, width=Sys.BLO_WID, height=Sys.BLO_WID, is_activated=True):
        super(Entity, self).__init__(x, y, width, height, is_activated)
        for i in range(len(Sys.entities)):
            if Sys.entities[i] is None:  # 运行不过去怪黄叶, 别怪我
                Sys.entities[i] = self
                self.index = i
                return
        Sys.entities.append(self)
        self.index = len(Sys.entities) - 1
        # print(str(self.index), "has been created.")

    def update(self):
        super(Entity, self).update()
        self.selected_switch()

    def switch_handler(self):
        if self.is_held_left and self.is_released_left:
            self.is_switched = not self.is_switched
            Sys.entity_selected = self.index

    def selected_switch(self):
        if self.index == Sys.entity_selected:
            self.is_switched = True

from src.element import *


# The base class of all objects.
class Object(Element):

    def __init__(self, x=5, y=5, width=Sys.BLO_WID, height=Sys.BLO_WID, is_activated=True):
        super(Object, self).__init__(x, y, width, height, is_activated)
        for i in range(len(Sys.objects)):
            if Sys.objects[i] is None:  # 运行不过去怪黄叶, 别怪我
                Sys.objects[i] = self
                self.index = i
                return
        Sys.objects.append(self)
        self.index = len(Sys.objects) - 1
        # print(str(self.index), "has been created.")

    def update(self):
        super(Object, self).update()
        self.selected_switch()

    def switch_handler(self):
        if self.is_held_left and self.is_released_left:
            self.is_switched = not self.is_switched
            Sys.object_selected = self.index

    def selected_switch(self):
        if self.index == Sys.object_selected:
            self.is_switched = True

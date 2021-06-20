import pygame

class Asset:

    rotation = 0
    img = None
    pos = (0,0)
    name = ""

    def __init__(self, img, name = ""):
        self.img = img
        self.name = name

    def set_pos(x:int, y:int):
        pos = (x, y)
    
    def rotate(self, degrees:int):
        self.rotation += degrees

    def move(self, speed:int):
        raise Exception("not yet implemented")

    def get_image(self):
        return pygame.transform.rotate(self.img, self.rotation)

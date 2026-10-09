import pygame

RIVER_TOP=120
RIVER_BOTTOM=210

class Raft:
    def __init__(self,x):
        self.x=float(x)
        self.rect=pygame.Rect(x,RIVER_TOP,180,RIVER_BOTTOM-RIVER_TOP)
        self.speed=1.5

    def update(self,width):
        self.x+=self.speed
        wrapped=self.x>width
        if wrapped: self.x=-self.rect.width
        self.rect.x=round(self.x)
        return wrapped

    def draw(self,screen):
        pygame.draw.rect(screen,(133,88,46),self.rect,border_radius=8)
        for y in range(self.rect.top+8,self.rect.bottom,16):
            pygame.draw.line(screen,(195,143,77),(self.rect.left+6,y),(self.rect.right-6,y),3)

import pygame
import random

LANE_W=80
COLORS=[(220,60,60),(220,140,40),(140,60,180),(60,180,80),(180,180,40),(60,80,200)]

class Car:
    def __init__(self, lane_x, y, direction, speed):
        self.rect=pygame.Rect(lane_x+10,y,60,80)
        self.direction=direction  # 1=down, -1=up
        self.speed=speed
        self.y=float(y)
        self.color=random.choice(COLORS)

    def update(self):
        self.y+=self.direction*self.speed
        self.rect.y=round(self.y)

    def off_screen(self,height):
        return self.rect.top>height+100 or self.rect.bottom<-100

    def draw(self,screen,night=False):
        if night:
            beam=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
            front=self.rect.bottom if self.direction==1 else self.rect.top
            ahead=front+self.direction*170
            pygame.draw.polygon(beam,(255,244,165,55),[(self.rect.left+8,front),(self.rect.right-8,front),(self.rect.right+35,ahead),(self.rect.left-35,ahead)])
            screen.blit(beam,(0,0))
            for x in (self.rect.left+12,self.rect.right-12):
                pygame.draw.circle(screen,(255,250,200),(x,front),5)
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        pygame.draw.rect(screen,(180,220,240),pygame.Rect(self.rect.x+8,self.rect.y+10,44,22),border_radius=4)
        for wx in [self.rect.x+6,self.rect.right-16]:
            for wy in [self.rect.y+4,self.rect.bottom-16]:
                pygame.draw.rect(screen,(30,30,30),pygame.Rect(wx,wy,10,12),border_radius=3)

def make_car(lane_idx,height,speed):
    x=lane_idx*LANE_W
    direction=1 if lane_idx%2==0 else -1
    y=-90 if direction==1 else height+10
    return Car(x,y,direction,speed)

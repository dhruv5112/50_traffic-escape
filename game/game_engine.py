import pygame
import random
from game.player import Player,LANE_W
from game.traffic import Car,make_car
from game.raft import Raft,RIVER_TOP,RIVER_BOTTOM
from game.high_scores import HighScores

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
BG=(60,60,60)

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.high_scores=HighScores()
        self.reset()

    def reset(self):
        if hasattr(self,"score"): self.save_score()
        self.score_saved=False
        self.player=Player(WIDTH//2,HEIGHT-80)
        self.cars=[]
        self.rafts=[Raft(x) for x in (-160,100,360,620)]
        self.raft_x=float(self.player.rect.x)
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.lives=3
        self.invulnerable=0
        self.game_over=False
        self.won=False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r: self.reset()
        return True

    def update(self):
        if self.game_over or self.won: return
        keys=pygame.key.get_pressed()
        self.player.move(keys,0,WIDTH)
        self.invulnerable=max(0,self.invulnerable-1)
        for raft in self.rafts:
            raft.update(WIDTH)
        on_river=RIVER_TOP<=self.player.rect.centery<RIVER_BOTTOM
        if on_river:
            raft=next((r for r in self.rafts if r.rect.left<=self.player.rect.centerx<r.rect.right),None)
            if raft is None:
                self.lose_life()
            else:
                if abs(self.raft_x-self.player.rect.x)>2: self.raft_x=float(self.player.rect.x)
                self.raft_x+=raft.speed
                self.player.rect.x=round(self.raft_x)
                if self.player.rect.left<0 or self.player.rect.right>WIDTH: self.lose_life()
        else:
            self.raft_x=float(self.player.rect.x)
        self.timer+=1
        if self.timer>=self.spawn_interval:
            lane=random.randint(0,LANES-1)
            self.cars.append(make_car(lane,HEIGHT,self.speed))
            self.timer=0
            self.spawn_interval=max(22,self.spawn_interval-0.2)
        for c in self.cars:
            c.update()
            if self.invulnerable==0 and not (RIVER_TOP<=self.player.rect.centery<RIVER_BOTTOM) and self.player.rect.bottom<HEIGHT-50 and c.rect.colliderect(self.player.rect):
                self.lose_life()
                break
        self.cars=[c for c in self.cars if not c.off_screen(HEIGHT)]
        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)
        if self.player.rect.top<=10:
            self.won=True
            self.score+=1000
            self.save_score()

    def save_score(self):
        if not self.score_saved:
            self.high_scores.add(self.score//10)
            self.score_saved=True

    def lose_life(self):
        self.lives-=1
        if self.lives==0:
            self.game_over=True
            self.save_score()
        else:
            self.player=Player(WIDTH//2,HEIGHT-80)
            self.invulnerable=90
            self.raft_x=float(self.player.rect.x)

    def draw(self):
        self.screen.fill(BG)
        # road markings
        for i in range(LANES+1):
            pygame.draw.line(self.screen,(100,100,100),(i*LANE_W,0),(i*LANE_W,HEIGHT),2)
        for y in range(0,HEIGHT,60):
            for i in range(LANES):
                pygame.draw.rect(self.screen,(200,200,100),pygame.Rect(i*LANE_W+LANE_W//2-3,y,6,30))
        # sidewalks
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,HEIGHT-50,WIDTH,50))
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,0,WIDTH,30))
        for c in self.cars: c.draw(self.screen)
        pygame.draw.rect(self.screen,(35,113,166),(0,RIVER_TOP,WIDTH,RIVER_BOTTOM-RIVER_TOP))
        for raft in self.rafts: raft.draw(self.screen)
        label=self.font.render("RIVER: ride a raft!",True,(240,245,255))
        self.screen.blit(label,(8,RIVER_TOP+4))
        self.player.draw(self.screen)
        hud=pygame.Rect(0,0,WIDTH,30)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        s=self.font.render(f"Score: {self.score//10}  Lives: {self.lives}  R=Restart",True,(220,220,220))
        self.screen.blit(s,(6,4))
        if self.game_over:
            self._msg("CRASHED!",(220,60,60))
        if self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        table="TOP 5: "+" / ".join(str(n) for n in self.high_scores.scores)
        self.screen.blit(self.font.render(table,True,(255,230,130)),(8,HEIGHT-32))
        if self.high_scores.error:
            self.screen.blit(self.font.render(self.high_scores.error,True,(255,120,120)),(8,HEIGHT-58))
        pygame.display.flip()

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,HEIGHT//2+20))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        self.save_score()
        pygame.quit()

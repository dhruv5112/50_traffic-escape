import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import json
import tempfile
import unittest
from pathlib import Path
import pygame
from game.game_engine import GameEngine,HEIGHT
from game.traffic import Car
from game.high_scores import HighScores

class Keys:
    def __init__(self,*keys): self.keys=keys
    def __getitem__(self,key): return key in self.keys

class GameTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'scores.json'
        self.game=GameEngine(self.path)
        self.original=pygame.key.get_pressed
        pygame.key.get_pressed=lambda:Keys()
    def tearDown(self):
        pygame.key.get_pressed=self.original
        pygame.quit()
        self.temp.cleanup()
    def test_bounds(self):
        for _ in range(100): self.game.player.move(Keys(pygame.K_DOWN),0,640)
        self.assertEqual(self.game.player.rect.bottom,HEIGHT)
    def test_three_hits_and_restart(self):
        for lives in (2,1,0):
            self.game.player.rect.y=300
            self.game.invulnerable=0
            car=Car(300,300,1,0)
            self.game.cars=[car]
            self.game.update()
            self.assertEqual(self.game.lives,lives)
            self.assertEqual(self.game.game_over,lives==0)
        self.assertEqual(len(json.loads(self.path.read_text())),1)
        self.game.reset()
        self.assertEqual(self.game.lives,3)
        self.assertFalse(self.game.game_over)
        self.assertEqual(len(self.game.high_scores.scores),1)
    def test_sidewalk_and_respawn_protection(self):
        self.game.cars=[Car(300,490,1,0)]
        self.game.update()
        self.assertEqual(self.game.lives,3)
        self.game.lose_life()
        self.game.player.rect.y=300
        self.game.cars=[Car(300,300,1,0)]
        self.game.update()
        self.assertEqual(self.game.lives,2)
    def test_raft_carries_and_water_costs_life(self):
        self.game.player.rect.center=(150,170)
        x=self.game.player.rect.x
        self.game.update()
        self.assertGreater(self.game.player.rect.x,x)
        self.assertEqual(self.game.lives,3)
        self.game.player.rect.center=(310,170)
        self.game.update()
        self.assertEqual(self.game.lives,2)
    def test_cycle_and_fractional_speed(self):
        self.game.update(29.9);self.assertFalse(self.game.night)
        self.game.update(.1);self.assertTrue(self.game.night)
        self.game.update(30);self.assertFalse(self.game.night)
        car=Car(0,0,1,3.5)
        car.update();car.update()
        self.assertEqual(car.rect.y,7)
    def test_win_and_save_once(self):
        self.game.player.rect.top=0
        self.game.update()
        self.assertTrue(self.game.won)
        self.assertEqual(self.game.high_scores.scores,[100])
        self.game.save_score()
        self.assertEqual(self.game.high_scores.scores,[100])
    def test_top_five_persist_and_bad_file(self):
        scores=HighScores(self.path)
        for n in (10,50,30,90,20,80):scores.add(n)
        self.assertEqual(HighScores(self.path).scores,[90,80,50,30,20])
        self.path.write_text('broken')
        self.assertEqual(HighScores(self.path).scores,[])
        self.path.write_text('[true,-1,"x",40]')
        self.assertEqual(HighScores(self.path).scores,[40])

if __name__=='__main__':unittest.main()

# --- Splashtoon V1.1 ---
# - Created by Sandraev -
# Last update: 14-11-2021
# -----------------------

from kandinsky import *
from random import *
from ion import *
from time import sleep

# Settings that can be changed:

timeout = 80

# Getting system's infos if avaible and
# setting variables

players = []
ok = {}
try:
  fill_circle(0,0,0,(0,0,0))
  ok["circle"] = 1
  ok["size"] = 8
  ok["pos"] = 0
  ok["corrector"] = 0
except:
  ok["circle"] = 0
  ok["size"] = 12
  ok["pos"] = 5
  ok["corrector"] = ok["size"]

colors = {
"violet":(200,50,200),
"red":(200,50,50),
"orange":(200,50,100),
"yellow":(250,250,00),
"green":(0,200,50),
"blue":(50,50,200)}

def reset_screen(x=0,y=0,w=320,h=222):
  if ok["circle"]:
    palette = get_palette()
    fill_rect(x,y,w,h,palette["HomeBackground"])
  else:
    fill_rect(x,y,w,h,(255,255,255))

def reset_players():
  return [
  Player(100,111,1,ok["size"],(200,0,0),(250,100,100),[KEY_FIVE,KEY_FOUR,KEY_SEVEN,KEY_ONE]), #(248, 100, 96)
  Player(220,111,1,ok["size"],(0,200,0),(100,250,100),[KEY_DIVISION,KEY_MULTIPLICATION,KEY_RIGHTPARENTHESIS,KEY_MINUS]) #(96, 248, 96)
  ]

# Definition of the functions

def fill_shape(x,y,size,color):
  if ok["circle"]:
    fill_circle(x,y,int(size),color)
  else:
    fill_rect(x,y,int(size),int(size),color)

def contact(x1,y1,x2,y2,zone):
  if x2-zone<x1<x2+zone and y2-zone<y1<y2+zone:
    return True
  return False

# Definition of the classes

class Player():
  def __init__(self,x,y,speed,size,color,paint_color,keys):
    self.x = x
    self.y = y
    self.speed = speed
    self.size = size
    self.color = color
    self.paint_color = paint_color
    self.keys = keys
    self.freezing = 0
    self.freezed = 0
    self.freeze_timeout = 0
                
  def draw(self):
    fill_shape(self.x,self.y,self.size,self.color)

  def blink(self):
    fill_shape(self.x,self.y,self.size,self.paint_color)

  def play(self):
    if keydown(self.keys[0]) and self.x < 320-self.size:
      self.blink()
      self.x += self.speed
      self.draw()
    if keydown(self.keys[1]) and self.x > -1+self.size-ok["corrector"]:
      self.blink()
      self.x -= self.speed
      self.draw()
    if keydown(self.keys[2]) and self.y > 18+self.size-ok["corrector"]:
      self.blink()
      self.y -= self.speed
      self.draw()
    if keydown(self.keys[3]) and self.y < 222-self.size:
      self.blink()
      self.y += self.speed
      self.draw()
        
      
class Bonus():
  def __init__(self,color,intervale):
    self.color = color
    self.size = ok["size"]-3
    self.counter = 0
    self.intervale = intervale
    self.spawn_time = randint(self.intervale[0],self.intervale[1])
    self.visible = 0
    self.after_effect = 0
    self.randomise()

  def randomise(self):
    self.x = randint(5,315)
    self.y = randint(25,217)
    
  def draw(self):
    fill_shape(self.x,self.y,self.size,self.color)
  
  def count(self):
    if self.counter < self.spawn_time and self.visible == 0:
      self.counter += 1
    else:
      self.counter = 0
      self.spawn_time = randint(self.intervale[0],self.intervale[1])
      self.draw()
      self.visible = 1

class BombBonus(Bonus):
  def play(self,player):
    fill_shape(self.x,self.y,self.size*8,player.paint_color)
    self.visible = 0
    self.randomise()        

  def replay(self,player):
    self.after_effect = 0

class SpeedBonus(Bonus):
  def play(self,player):
    fill_shape(self.x,self.y,self.size*2,player.paint_color)
    player.speed += 1
    self.effect_counter = 0
    self.effect_duration = 700
    self.visible = 0
    self.randomise()
            
  def replay(self,player):
    if self.effect_counter < self.effect_duration:
      self.effect_counter += 1
    else:
      self.effect_counter = 0
      self.after_effect = 0
      player.speed -= 1

class SizeBonus(Bonus):
  def play(self,player):
    fill_shape(self.x,self.y,self.size*2,player.paint_color)
    player.size *= 2
    self.effect_counter = 0
    self.effect_duration = 700
    self.visible = 0
    self.randomise()

  def replay(self,player):
    if self.effect_counter < self.effect_duration:
      self.effect_counter += 1
    else:
      self.effect_counter = 0
      self.after_effect = 0
      player.size += 1
      player.blink()
      player.size -= 1
      player.size /= 2
      player.draw()
      
class FreezeBonus(Bonus):
  def play(self,player):
    fill_shape(self.x,self.y,self.size*2,player.paint_color)
    draw_circle(player.x,player.y,int(player.size+1),(100,100,250))
    self.player = player
    self.player_old_x = player.x
    self.player_old_y = player.y
    self.effect_counter = 0
    self.effect_duration = 1000
    self.visible = 0
    self.randomise()
    self.player.freezing = 1

  def replay(self,player):
    if self.effect_counter < self.effect_duration:
      self.effect_counter += 1
      draw_circle(self.player_old_x,self.player_old_y,int(self.player.size+1),self.player.paint_color)
      self.player.draw()
      draw_circle(self.player.x,self.player.y,int(self.player.size+1),(100,100,250))
      self.player_old_x = self.player.x
      self.player_old_y = self.player.y
    else:
      self.effect_counter = 0
      self.after_effect = 0
      draw_circle(self.player_old_x,self.player_old_y,int(self.player.size+1),self.player.paint_color)
      self.player.freezing = 0
      self.player.draw()

bonus = [
BombBonus(colors["orange"],[1000,2000]),
SpeedBonus(colors["blue"],[2000,4000]),
SizeBonus(colors["yellow"],[1500,2500]),
]

if ok["circle"]:
  bonus.append(FreezeBonus(colors["violet"],[3000,6000]))

def game_turn(players):
  for p in players:
    if not p.freezed:
      p.play()
    else:
      if p.freeze_timeout < 1000:
        p.freeze_timeout += 1
        if p.freeze_timeout%2 != 0:
          fill_shape(p.x,p.y,p.size,(100,100,250))
        else:
          p.draw()
      else:
        p.freezed = 0
    if p.freezing:
      for i in players:
        if i is not p:
          if contact(i.x,i.y,p.x,p.y,p.size):
            i.freezed = 1
            i.freeze_timeout = 0
    for b in bonus:
      b.count()
      if contact(p.x,p.y,b.x,b.y,10) and b.visible:
        b.play(p)
        b.after_effect = 1
      if b.after_effect == 1:
        b.replay(p)

def game_engine(timeout,players):
  timeout *= 100
  players[0].x,players[0].y = 80,111
  players[1].x,players[1].y = 240,111
  fill_rect(0,0,160,222,players[0].paint_color)
  fill_rect(160,0,320,222,players[1].paint_color)
  for i in range(len(players)):
    players[i].draw()
  for i in range(timeout):
    draw_string("Time:                        "+str(100-int((100*i/timeout)))+"  ",0,0)
    game_turn(players)

  score = [0,0]
  for x in range(320):
    for y in range(197):
      pixel = get_pixel(x,y+25)  
      if pixel == (248, 100, 96):
        score[0] += 1
      elif pixel == (96, 248, 96):
        score[1] += 1
    draw_string("Calcul en cours...           "+str(int(100*x/320))+"%",0,0)
  reset_screen()
  draw_string("Red   : "+str(int(score[0]*100/(score[0]+score[1])))+"%",10,10,(250,0,0))
  draw_string("Green : "+str(int(score[1]*100/(score[0]+score[1])))+"%",10,30,(0,250,0))
  if score[0] > score[1]:
    team = "red"
  elif score[0] < score[1]:
    team = "green"
  else:
    team = "both"
  draw_string("The "+team+" win !",10,80)

  sleep(1)
  while not keydown(KEY_OK):
    draw_string("Press [OK]",200,200,(250,50,50))
    sleep(0.1)
    draw_string("Press [OK]",200,200,(250,150,150))
  sleep(0.4)

def menu():
  reset_screen()
  players = reset_players()
  draw_string("SPLASHTOON",110,50)
  players[0].x,players[0].y = -10,40-ok["pos"]
  players[1].x,players[1].y = 330,78-ok["pos"]
  for i in range(220):
    players[0].blink()
    players[0].x += 1
    players[0].draw()
    sleep(0.001)
  for i in range(220):
    players[1].blink()
    players[1].x -= 1
    players[1].draw()
    sleep(0.001)

  draw_string("A game made by Sandraev",50,200,(250,250,50))
  sleep(0.5)
  while not keydown(KEY_OK):
    draw_string("Press [OK] to play",70,130,(250,50,50))
    sleep(0.1)
    draw_string("Press [OK] to play",70,130,(250,150,150))
  sleep(0.4)

  reset_screen()
  game_engine(timeout,players)

while True:
  menu()

# In order to have all the features of
# this game (like the "freeze" bonus),
# you need to use Upsilon instead of
# Numworks' official OS.
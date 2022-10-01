from abc import ABC,abstractclassmethod
import random
from enum import Enum
import pygame
import sys

pygame.init()
WIDTH=1000
HEIGHT=500
CREATURE_SIZE=20
FOOD_SIZE=10
SPEED=40
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN=(0,255,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
step=0
#direction
class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4
    STRAIGHT=0

class creature:

    def __init__(self):
        self.energy=100
        self.life=70
        self.hungry=True
        self.direction=Direction.DOWN
        self.color=random.choice([WHITE,RED,BLUE1,BLUE2])
        self.loc=[random.randint(0,WIDTH),random.randint(0,HEIGHT)]

    def move(self,x,y):
        step=5
        print(self.direction)
        #giving the direction right or left
        if x-self.loc[0]>0:
            self.direction=Direction.RIGHT
        elif x-self.loc[0]<0:
            self.direction=Direction.LEFT
        #moving in the direction right or left
        print(self.direction)
        if self.direction==Direction.RIGHT:
            if self.loc[0]+step>WIDTH:
                self.loc[0]-=10
            self.loc[0]+=step
        elif self.direction==Direction.LEFT:
            if self.loc[0]-step<0:
                self.loc[0]+=10
            self.loc[0]-=step
        #giving the direction up or down
        print(self.direction)
        if y-self.loc[1]>0:
            self.direction=Direction.DOWN
        elif y-self.loc[1]<0:
            self.direction=Direction.UP
        #moving in the direction up or down
        print(self.direction)
        if self.direction==Direction.DOWN:
            if self.loc[1]+step>HEIGHT:
                self.loc[1]-=10
            self.loc[1]+=step
        elif self.direction==Direction.UP:
            if self.loc[1]-step<0:
                self.loc[1]+=10
            self.loc[1]-=step
        self.energy-=1
        self.life-=1

class food:

    def __init__(self) :
        self.energy=100
        self.life=100
        self.location=[random.randint(0,WIDTH),random.randint(0,HEIGHT)]

    def life_process(self):
        self.energy-=1
        self.life-=1

class nature:

    def __init__(self) -> None:
        self.display=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('WORLD')
        self.creature=[]
        self.food=[]
        self.creature_birth()
        self.food_birth()
        self.update_UI()
        self.clock=pygame.time.Clock()

    def play(self):
        self.clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        #moving the creature
        for Living_creature in self.creature:
            try:
                closest_food=[self.food[0],1120]
            except:
                print("Nature ended!!!")
                self.apocalypse()
            for food in self.food:
                distance=(food.location[0]-Living_creature.loc[0])**2+(food.location[1]-Living_creature.loc[1])**2
                distance=distance**0.5
                if distance<=5:
                    Living_creature.energy+=food.energy
                    self.food.pop(self.food.index(food))
                if Living_creature.energy>=150 :
                    Living_creature.energy=50
                    self.creature_birth()
                if distance<closest_food[1]:
                    closest_food=[food,distance]
                if Living_creature.energy<=40:
                    self.creature.pop(self.creature.index(Living_creature))
                    break
            try:
                Living_creature.move(closest_food[0].location[0],closest_food[0].location[1])
            except:
                continue

        #Spoiling the food
        food_death_year=50
        for food in self.food:
            food.life_process()
            if food.life==80:#random.randint(50,80):
                self.food_birth()
                #self.food_birth()
            elif food.life==0:
                self.food.pop(self.food.index(food))

        self.update_UI()

    def update_UI(self):
        self.display.fill(BLACK)
        for Living_creature in self.creature:
            pygame.draw.rect(
                self.display,Living_creature.color,
                pygame.Rect(Living_creature.loc[0],Living_creature.loc[1],CREATURE_SIZE,CREATURE_SIZE)
                )

        for food in self.food:
            pygame.draw.rect(self.display,GREEN,pygame.Rect(food.location[0],food.location[1],FOOD_SIZE,FOOD_SIZE))

        pygame.display.flip()

    def creature_birth(self):
        Creature=creature()
        self.creature.append(Creature)

    def food_birth(self):
        Food=food()
        self.food.append(Food)

    def apocalypse(self):
        sys.exit()


#starting the nature
if __name__=="__main__":
    nature=nature()
    while True:
        nature.play()
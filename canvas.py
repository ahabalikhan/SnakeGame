from random import randint
import pygame
from snake import pixel_converter

class Canvas:
    def __init__(self,screen):
        self.size=[20,20]
        self.background=pygame.image.load("images\grass.bmp").convert_alpha()
        self.background=pygame.transform.scale(self.background,(720,720))
        self.food_positions=[]
        self.food=pygame.image.load("images\\food.bmp")#.convert_alpha()
        self.food.set_colorkey((255,255,255))

        self.angle=0
        self.food=pygame.transform.scale(self.food,(50,50))

        self.screen=screen

        for x in range(3):
            self.add_food()

    def add_food(self):
        if len(self.food_positions)<3: #Atmost 3 food particles can exist at a time
            self.food_positions.append([randint(0,19),randint(0,19)])
            #print(len(self.food_positions))

    def blitme(self):
        self.angle+=1

        food_copy=pygame.transform.rotate(self.food,self.angle)
        self.screen.blit(self.background,(0,0))
        for position in self.food_positions:
            xy=pixel_converter([position[0],position[1]])
            self.screen.blit(food_copy,(xy[0]-int(food_copy.get_width()/3) , xy[1]-int(food_copy.get_height()/3)))
        #pygame.display.flip()


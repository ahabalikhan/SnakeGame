import pygame


def pixel_converter(block_pos):
    return [block_pos[0]*36,block_pos[1]*36]

def block_converter(pixel_pos):
    return [pixel_pos[1]/36,pixel_pos[0]/36]


class Snake:

    class Segment:
        image = pygame.image.load("images\segment.bmp")
        image.set_colorkey((255, 255, 255))
        speed=1
        def __init__(self,leader):
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False

            self.leader=leader

            self.position=[10,10]
            if self.leader!=None: self.position=self.leader.tail
            self.pixels=pixel_converter(self.position)

            self.tail=[10,11]




        def move(self):
            arg=[self.position[0],self.position[1]]
            self.tail=arg

            self.position=self.leader.tail
            self.pixels = pixel_converter(self.position)




    class Head(Segment):
        image0 = pygame.image.load("images\headn.bmp")  # .convert_alpha()
        image0.set_colorkey((255, 255, 255))

        image1 = pygame.image.load("images\heads.bmp")  # .convert_alpha()
        image1.set_colorkey((255, 255, 255))

        image2 = pygame.image.load("images\heade.bmp")  # .convert_alpha()
        image2.set_colorkey((255, 255, 255))

        image3 = pygame.image.load("images\headw.bmp")  # .convert_alpha()
        image3.set_colorkey((255, 255, 255))

        image = image0




        def move(self):

            arg=[self.position[0],self.position[1]]
            self.tail=arg
            if self.moving_up:
                self.image=self.image0
                self.position[1]-=1
            elif self.moving_down:
                self.image=self.image1
                self.position[1]+=1
            elif self.moving_left:
                self.image=self.image2
                self.position[0]-=1
            elif self.moving_right:
                self.image=self.image3
                self.position[0]+=1


            self.pixels=pixel_converter(self.position)

    def __init__(self,screen):
        self.body=[]
        self.body.append(self.Head(None))
        self.screen=screen

        for x in range(3):
            self.add_segment()

    def add_segment(self):
        self.body.append(self.Segment(self.body[-1]))

    def move(self):
        for part in self.body:
            part.move()


    def move_up(self):
        if not self.body[0].moving_down:
            self.body[0].moving_up=True
            self.body[0].moving_left=False
            self.body[0].moving_right=False
    def move_down(self):
        if not self.body[0].moving_up:
            self.body[0].moving_down=True
            self.body[0].moving_left = False
            self.body[0].moving_right = False
    def move_left(self):
        if not self.body[0].moving_right:
            self.body[0].moving_left=True
            self.body[0].moving_up=False
            self.body[0].moving_down=False
    def move_right(self):
        if not self.body[0].moving_left:
            self.body[0].moving_right=True
            self.body[0].moving_up = False
            self.body[0].moving_down = False

    def blitme(self):
        for part in self.body:
            self.screen.blit(part.image,tuple(part.pixels))




"""
snake=Snake(None)

#snake.body[0].position=[10,10]
#snake.move()

for ind in range(4):
    print(snake.body[ind].position)
    print(snake.body[ind].tail)
    print("")

snake.move()

for ind in range(4):
    print(snake.body[ind].position)
    print(snake.body[ind].tail)
    print("")
"""
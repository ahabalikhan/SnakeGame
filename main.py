import pygame
import sys

from time import sleep
from canvas import Canvas
from snake import Snake

def check_events(): #Check Different Input Events

    arg=[False,False,False,False,False,False]

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type==pygame.KEYDOWN:
            if event.key== pygame.K_UP or event.key== pygame.K_w:
                arg[0]=True
            elif event.key== pygame.K_DOWN or event.key== pygame.K_s:
                arg[1]=True
            elif event.key== pygame.K_LEFT or event.key== pygame.K_a:
                arg[2]=True
            elif event.key== pygame.K_RIGHT or event.key== pygame.K_d:
                arg[3]=True
            elif event.key== pygame.K_ESCAPE:
                arg[4]=True
        elif event.type== pygame.MOUSEBUTTONDOWN:
            arg[5]=True
    return arg



def draw_text(font,text,color,surface,xy):
    textobj=pygame.font.Font.render(font,text,True,color)
    text_rect=textobj.get_rect()
    text_rect.topleft=xy
    surface.blit(textobj,text_rect)

def main_menu(font,surface,red,blue,yellow):
    cursor_position=pygame.mouse.get_pos()
    input = check_events()
    arg=True

    if cursor_position[1]>=0 and cursor_position[1]<50:
        draw_text(font, "Start Slithering", yellow, surface, (0, 0))
        draw_text(font, "Quit", blue, surface, (0, 50))
        if input[5]:
            arg=False

    elif cursor_position[1]>=50 and cursor_position[1]<120:
        draw_text(font, "Start Slithering", blue, surface, (0, 0))
        draw_text(font, "Quit", red, surface, (0, 50))
        if input[5]:
            pygame.quit()
            sys.exit()
    else:
        draw_text(font, "Start Slithering", blue, surface, (0, 0))
        draw_text(font, "Quit", blue, surface, (0, 50))

    return arg

def pause_menu(font,surface,red,blue,yellow):
    arg=True
    input=check_events()
    cursor_position=pygame.mouse.get_pos()

    draw_text(font,"PAUSED",red,surface,(270,200))
    if input[4]:
        arg=False
    return arg


def rungame(): # Main Function to Run The game

    pygame.init() #Open Pygame Window

    font = pygame.font.SysFont(None, 80) #Big font
    font_small=pygame.font.SysFont(None, 40) #Small font

    pygame.display.set_caption("Snake Game by Ahab") #Sets window's caption

    screen = pygame.display.set_mode((720, 720)) #Define window's size

    canvas=Canvas(screen)
    snake=Snake(screen)


    score=0
    move_smooth=True #To avoid step wise movement
    red=(255,0,0)
    yellow=(255,255,0)
    blue=(0,0,255)
    game_paused=False

    eat_sound=pygame.mixer.Sound("sounds\\crunch.wav")
    ouch_sound=pygame.mixer.Sound("sounds\\ouch.wav")
    pygame.mixer.music.load('sounds\\african_safari_loop.wav') #Load music file
    pygame.mixer.music.play(-1) #Play music indefinitely

    with open("highscore.txt","r") as h_file:
        highscore=int(h_file.read())


    while True:
        canvas.blitme()
        game_over=main_menu(font,screen,red,blue,yellow)

        draw_text(font,"How to Play?",red,screen,(260,400))
        draw_text(font_small, "* Don't leave the screen", yellow, screen, (275, 460))
        draw_text(font_small, "* Don't Intersect your body", yellow, screen, (275, 500))
        draw_text(font_small, "* Use either Arrow keys or WASD", yellow, screen, (275, 540))
        draw_text(font_small, "* Press ESC to pause", yellow, screen, (275, 580))
        draw_text(font_small, "* Eat more to score more!", yellow, screen, (275, 620))


        while not game_over:

            if not move_smooth: sleep(0.5)
            input = check_events()
            # Input by user is processed as under
            if input[0]:
                snake.move_up()
            elif input[1]:
                snake.move_down()
            elif input[2]:
                snake.move_left()
            elif input[3]:
                snake.move_right()
            if input[4]:
                game_paused=True



            snake.move()
            blitted = False
            while not blitted:
                if move_smooth: sleep(0.005)
                canvas.blitme()
                blitted = snake.blitme()
                draw_text(font_small, "Score: {}".format(score), yellow, screen, (580, 0))
                draw_text(font_small, "Highscore: {}".format(highscore),red,screen,(0,0))
                pygame.display.flip()

            while game_paused:
                game_paused=pause_menu(font,screen,red,blue,yellow)
                pygame.display.flip()

            #Snake's Head is snake.body[0] i.e the first object in the list snake.body

            # If snake's head reaches food it eats and grows
            if snake.body[0].position in canvas.food_positions:
                pygame.mixer.Sound.play(eat_sound)
                canvas.food_positions.remove(snake.body[0].position) #Eats
                score += 10
                if score>highscore:
                    highscore=score
                    with open("highscore.txt","w") as h_file:
                        h_file.write(str(highscore))
                canvas.add_food()
                snake.add_segment() #Grows

            # If snake's head touches its body game is over
            for ind in range(1, len(snake.body)):
                if snake.body[0].position == snake.body[ind].position:
                    game_over = True

            for ind in [0,1]:
                if snake.body[0].position[ind]<0 or snake.body[0].position[ind]>20:
                    game_over=True

            if game_over:
                pygame.mixer.Sound.play(ouch_sound)
                pygame.mixer.music.rewind()
                sleep(1)
            while game_over and True not in check_events():
                draw_text(font, "YOU BLIND!!?", red, screen, (270, 200))
                draw_text(font_small, "  You scored {}".format(score), yellow, screen, (270, 250))
                pygame.display.flip()

        pygame.display.flip()


        if game_over:
            score=0
            del snake
            snake=Snake(screen)



if __name__=="__main__":
    rungame()


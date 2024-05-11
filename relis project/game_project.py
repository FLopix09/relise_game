import pygame
pygame.init()
back = (200,255,255)
mw=pygame.display.set_mode((500,500))
mw.fill(back)
clock = pygame.time.Clock()
racket_x=60
racket_y=200
racket_x2=440
racket_y2=200
dx=3
dy=3

move_right=False
move_left=False

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x,y,width,height)
        self.fill_color = back
        if color:
            self.fill_color = color
    def color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    def outline(self, frame_color, thickness):
        pygame.draw.rect(mw, frame_color, self.rect, thickness)
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0,0,0)):
        self.image = pygame.font.SysFont("verdana" , fsize).render(text, True, text_color)
    def draw(self, shift_x, shift_y):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
class Picture(Area):
    def __init__(self,filename, x=0,y=0,width=10,height=10):
        Area.__init__(self, x=x,y=y,width=width,height=height,color=None)
        self.image=pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image,(self.rect.x,self.rect.y))


ball=Picture("ball.png",160,200,50,50)
platform=Picture("platform.png",racket_x,racket_y,30,100)
platform2=Picture("platform.png",racket_x2,racket_y2,30,100)
RED=(255,0,0)
GREEN=(0,255,0)


game_over=False
while not game_over:
    ball.fill()
    platform.fill()
    platform2.fill()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

    if move_right:
        platform.rect.x +=3
    if move_left:
        platform.rect.x -=3

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.y <0:
        dy *= -1

    if ball.rect.x < 0 or ball.rect.x > 500:
        dx *= -1

    if ball.rect.colliderect(platform.rect):
        dy *= -1
    
    if platform.rect.x <0:
        platform.rect.x +=10
    
    if ball.rect.y > 350:
        lose = Label(150,150,100,50,None)
        lose.set_text("YOU LOSE", 60, RED)
        lose.draw(10,10)
        game_over = True
    
    ball.draw()
    platform.draw()
    platform2.draw()
    pygame.display.update()
    clock.tick(40)
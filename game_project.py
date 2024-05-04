import pygame
pygame.init()
back = (200,255,255)
mw=pygame.display.set_mode((500,500))
mw.fill(back)
clock = pygame.time.Clock()
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x,y,width,height)
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
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0,0,0)):
        self.image = pygame.font.SysFont("verdana" , fsize).render(text, True, text_color)
    def draw(self, shift_x, shift_y):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


game_over=False
while not game_over:
    pygame.display.update()
    clock.tick(40)
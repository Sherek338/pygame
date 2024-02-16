import pygame
import Animation
import Hitbox

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y
        
        self.speed = 10
        self.direction = pygame.math.Vector2()
        
        self.anim_sp = Animation.Sprites()
        self.anim_sp.add_animation("idle", [pygame.image.load(f"./spr/idle/tile{i}.png").convert_alpha() for i in range(0,15)], 4)
        self.anim_sp.add_animation("run", [pygame.image.load(f"./spr/run/tile{i}.png").convert_alpha() for i in range(0,8)], 4)
        
        self.image = self.anim_sp.update()
        
        self.anim_pr = Animation.Property(self.image)
        self.anim_pr.add_animation("anim1", [{"scale": [4, 4], "duration": 80 }, {"scale": [1, 1], "duration": 20}], 2)
        self.anim_pr.add_animation("anim2", [{"scale": [2, 2], "rotate": 360, "duration": 50}, {"scale": [1, 1],"rotate": 0, "duration": 50}], 10)
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.hitbox = Hitbox.HB(pygame.Rect(self.rect.left + 15, self.rect.top + 15,self.rect.width - 30, self.rect.height - 30),
                                [1],
                                [2],
                                lambda mask : print(mask))
        
    def input_update(self):
        keys = pygame.key.get_pressed()
        self.anim_sp.play("run")
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
    def update(self):
        self.input_update()
        self.rect.center += self.direction * self.speed
        
        self.image = self.anim_sp.update()
        self.image = self.anim_pr.update(self.image)
        
        self.hitbox.update(self.rect.center)
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('./spr/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = Hitbox.HB(pygame.Rect(self.rect.left + 15, self.rect.top + 15,self.rect.width - 30, self.rect.height - 30),
                                [2],
                                [1])
        

allSprites = pygame.sprite.Group()
player =  Player(150, 150)
enemy = Enemy((900, 500))
enemy2 = Enemy((900, 450))
allSprites.add(player)
allSprites.add(enemy)
allSprites.add(enemy2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((0, 125, 0))
    
    allSprites.draw(screen)
    allSprites.update()
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
import pygame
from pygame.locals import *
import sys
import random
import time
from time import sleep

SCREEN_SIZE = Rect(0, 0, 1000, 700)
screen = pygame.display.set_mode((1000, 700))

class PlayerSprite(pygame.sprite.Sprite):
    speed = 25
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load("./assets/player4.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_SIZE.bottom-200
        self.rect.left = 400

    def update(self):
        pygame.event.pump()
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_w]:
            self.rect.move_ip(0,-self.speed)
        elif pressed_key[K_s]:
            self.rect.move_ip(0, self.speed)
        elif pressed_key[K_a]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_key[K_d]:
            self.rect.move_ip(self.speed, 0)
        self.rect = self.rect.clamp(SCREEN_SIZE)

class EnemySprite(pygame.sprite.Sprite):
    speed = 20 #可変を予定

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

    def visit(self):
        self.pattern = random.randint(1,4)
        if self.pattern == 1:
            self.image = pygame.image.load("./assets/baeru1.png")
            self.rect = self.image.get_rect()
            self.rect.left = random.randint(0, SCREEN_SIZE.width)
            self.rect.bottom = SCREEN_SIZE.top
        elif self.pattern == 2:
            self.image = pygame.image.load("./assets/baeru4.png")
            self.rect = self.image.get_rect()
            self.rect.top = random.randint(0, SCREEN_SIZE.height)
            self.rect.right = SCREEN_SIZE.left
        elif self.pattern == 3:
            self.image = pygame.image.load("./assets/baeru3.png")
            self.rect = self.image.get_rect()
            self.rect.left = random.randint(0, SCREEN_SIZE.width)
            self.rect.top = SCREEN_SIZE.bottom
        elif self.pattern == 4:
            self.image = pygame.image.load("./assets/baeru2.png")
            self.rect = self.image.get_rect()
            self.rect.top = random.randint(0, SCREEN_SIZE.height)
            self.rect.left = SCREEN_SIZE.right

    def update(self):
        if self.pattern == 1:
            self.rect.move_ip(0, self.speed)
        elif self.pattern == 2:
            self.rect.move_ip(self.speed, 0)
        elif self.pattern == 3:
            self.rect.move_ip(0, -self.speed)
        elif self.pattern == 4:
            self.rect.move_ip(-self.speed, 0)

class Game:

    def __init__(self):
        self.start_time=time.time()
        pygame.init()
        self.sys_font = pygame.font.SysFont(None, 60)
        self.go_text = self.sys_font.render("Game Over...", False, (0,0,0))
        pygame.display.set_caption("💃「止まるんじゃねぇぞ.....」")
        pygame.mixer.music.load("./assets/BGM.ogg")
        pygame.mixer.music.play(-1)
        self.game_over_img = pygame.image.load("./assets/gameover.png").convert_alpha()
        self.dontstop = pygame.mixer.Sound("./assets/gameover_se.ogg")
        self.rect_og_img = self.game_over_img.get_rect()
        self.flag = True
        self.all_sprite = pygame.sprite.RenderUpdates()
        self.oruga = pygame.sprite.Group()
        self.baeru = pygame.sprite.Group()
        self.score = 0
        PlayerSprite.containers = self.all_sprite, self.oruga
        EnemySprite.containers = self.all_sprite, self.baeru
        self.player = PlayerSprite()
        EnemySprite().visit()
        self.main()

    def main(self):
        FPS_CLOCK = pygame.time.Clock()
        screen = pygame.display.set_mode(SCREEN_SIZE.size)
        while(True):
            if self.flag == True:
                FPS_CLOCK.tick(60)
                screen.fill((0,0,255))
                self.update()
                self.all_sprite.draw(screen)
                self.score = pygame.time.get_ticks()
                self.score_text = self.sys_font.render("Score:" + str(self.score), False, (255,255,255))
                screen.blit(self.score_text, (20,100))
                pygame.display.update()
                self.key_handler()
            else:
                FPS_CLOCK.tick(60)
                screen.fill((0,0,0))
                screen.blit(self.game_over_img, self.rect_og_img)
                screen.blit(self.go_text, (20,50))
                pressed_key = pygame.key.get_pressed()
                pygame.display.update()
                self.key_handler()

    def hit_check(self):
        player_hited = pygame.sprite.groupcollide(self.baeru, self.oruga, False, True)
        for enemy in player_hited.keys():
            self.flag = False
            pygame.mixer.music.stop()
            pygame.mixer.music.load("./assets/gameover_bgm.ogg")
            self.dontstop.play()
            sleep(1)
            pygame.mixer.music.play()
            #GameOver
            #pygame.quit()
            #sys.exit()

    def update(self):
        if not random.randrange(15):
            EnemySprite().visit()
        self.all_sprite.update()
        self.hit_check()

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    Game()
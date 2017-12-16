#-*-coding:utf-8-*-
# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random
import random

# 设置游戏屏幕大小
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

class Ball(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        #self.rect=pygame.Rect([0,0,60,60])
        self.rect=pygame.Rect([200,300,60,60])
        self.speed=[10,10] #向下和向右的速度
        self.rotate=0

    def move(self,player1,player2):
        if pygame.sprite.collide_mask(self,player1):
            #if pygame.Rect.clip(self.rect, player1.rect).top - pygame.Rect.clip(self.rect, player1.rect).bottom>-10:
            self.speed = [abs(self.speed[0]), self.speed[1]]
            self.rect.left += self.speed[1]
            self.rect.top += self.speed[0]
            if pygame.Rect.clip(self.rect, player1.rect).bottom>player1.rect.bottom:
                player1.score = player1.score + 1


        if pygame.sprite.collide_mask(self,player2):
            #if pygame.Rect.clip(self.rect, player2.rect).top - pygame.Rect.clip(self.rect, player2.rect).bottom > -10:
            self.speed = [-abs(self.speed[0]), self.speed[1]]
            self.rect.left += self.speed[1]
            self.rect.top += self.speed[0]
            if pygame.Rect.clip(self.rect, player2.rect).bottom<player2.rect.top:
                print(pygame.Rect.clip(self.rect, player2.rect))
                player2.score = player2.score + 1

        if self.rect.top <= 0:
            self.speed=[-self.speed[0],self.speed[1]]
            self.rect.top = 0
            player1.score=player1.score-5
            player2.score = player2.score + 1

        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.speed = [-self.speed[0], self.speed[1]]
            self.rect.top = SCREEN_HEIGHT - self.rect.height
            player2.score=player2.score-5
            player1.score = player1.score + 1

        if self.rect.left <= 0:
            self.speed = [self.speed[0], -self.speed[1]]
            self.rect.left = 0
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.speed = [self.speed[0], -self.speed[1]]
            self.rect.left = SCREEN_WIDTH - self.rect.width
        self.rect.left += self.speed[1]
        self.rect.top += self.speed[0]

# 玩家控制的板的位置
class Player(pygame.sprite.Sprite):
    def __init__(self, img, init_pos=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect=pygame.Rect([0,0,109,21])
        self.rect.topleft = init_pos
        #self.image=self.image.subsurface(self.rect)
        self.speed=8
        self.score=0

    # 向上移动，需要判断边界
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed


    # 向下移动，需要判断边界
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    # 向左移动，需要判断边界
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    # 向右移动，需要判断边界
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed



# 初始化 pygame
pygame.init()

# 设置游戏界面大小、背景图片及标题
# 游戏界面像素大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Play ball')
background = pygame.image.load('background.png').convert()
win = pygame.image.load('win.png').convert_alpha()
# 游戏循环帧率设置
clock = pygame.time.Clock()

# 判断游戏循环退出的参数
running = True
player1=Player("player.png",init_pos=[SCREEN_WIDTH/2-55,0])
player2=Player("player2.png",init_pos=[SCREEN_WIDTH/2-55,SCREEN_HEIGHT-21])
ball=Ball("ball.png")

resultflag=0

def GameState(train=0,action1=[],action2=[]):
    # 控制游戏最大帧率为 60
    #clock.tick(60)
    global resultflag
    if not train:
        clock.tick(60)
    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))
    #奖励部分
    last_score_1=player1.score
    last_score_2 = player2.score
    reward1=0;reward2=0
    #绘制玩家
    screen.blit(player1.image,player1.rect)
    screen.blit(player2.image, player2.rect)
    #绘制球
    ball.move(player1,player2)
    screen.blit(ball.image,ball.rect)
    #screen.blit(player1.image, [0,0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render("player 1:"+str(player1.score), True, (	255,250,240))
    score_text2=score_font.render("player 2:"+str(player2.score), True, (	255,250,240))
    text_rect = score_text.get_rect()
    text_rect2 = score_text.get_rect()
    text_rect.topleft = [10, 30]
    text_rect2.topleft = [10, SCREEN_HEIGHT-66]
    screen.blit(score_text, text_rect)
    screen.blit(score_text2, text_rect2)
    # 获取键盘事件（上下左右按键）
    key_pressed = pygame.key.get_pressed()

    if resultflag:
        ball.speed=[0,0]
        player1.speed=0
        player2.speed=0
        screen.blit(win, (130, 120))
    if resultflag and (key_pressed[K_g] or train):
        resultflag=0
        ball.rect = pygame.Rect([200, 300, 60, 60])
        ball.speed=[(1-2*(random.random()>0.5))*10,(1-2*(random.random()>0.5))*10]
        print(ball.speed)
        player1.speed = 8;player2.speed = 8
        player1.score=0; player2.score=0;
        player1.rect.topleft=[SCREEN_WIDTH/2-55,0]
        player2.rect.topleft=[SCREEN_WIDTH/2-55,SCREEN_HEIGHT-21]

    if action1==[]:
        # 处理键盘事件（移动玩家的位置）
        if key_pressed[K_w]:
            player1.moveUp()
        if key_pressed[K_s]:
            player1.moveDown()
        if key_pressed[K_a]:
            player1.moveLeft()
        if key_pressed[K_d] :
            player1.moveRight()
    else:
        if action1[0]:
            player1.moveUp()
        if action1[1]:
            player1.moveDown()
        if action1[2]:
            player1.moveLeft()
        if action1[3]:
            player1.moveRight()
    if action2==[]:
        if key_pressed[K_RIGHT]:
            player2.moveRight()
        if key_pressed[K_LEFT]:
            player2.moveLeft()
        if key_pressed[K_DOWN]:
            player2.moveDown()
        if key_pressed[K_UP]:
            player2.moveUp()
    else:
        if action2[0]:
            player2.moveUp()
        if action2[1]:
            player2.moveDown()
        if action2[2]:
            player2.moveLeft()
        if action2[3]:
            player2.moveRight()

    ball_state1=[ball.rect.left,ball.rect.right,ball.rect.top,ball.rect.bottom]
    ball_state2 = [ball.rect.left, ball.rect.right,  SCREEN_HEIGHT-ball.rect.bottom,SCREEN_HEIGHT-ball.rect.top]
    state1=[player1.rect.left,player1.rect.right,player1.rect.top,player1.rect.bottom]
    state2 = [player2.rect.left, player2.rect.right, SCREEN_HEIGHT-player2.rect.bottom, SCREEN_HEIGHT-player2.rect.top]
    state1_ob=[player1.rect.left,player1.rect.right,SCREEN_HEIGHT-player1.rect.bottom, SCREEN_HEIGHT-player1.rect.top]
    state2_ob = [player2.rect.left, player2.rect.right, player2.rect.bottom,player2.rect.top]
    reward1=player1.score-last_score_1
    #reward2=-(player1.score-last_score_1)
    reward2=player2.score-last_score_2
    #reward1=-(player2.score-last_score_2)
    if player1.score-player2.score>30:
        # 绘制结果
        result_font = pygame.font.Font(None, 60)
        result_text = result_font.render("Player 1 WIN!" , True, (	233,165,32))
        text_rect = result_text.get_rect()
        text_rect.topleft = [60, 260]
        screen.blit(result_text, text_rect)
        resultflag=1
    elif player1.score-player2.score<-30:
        # 绘制结果
        result_font = pygame.font.Font(None, 60)
        result_text = result_font.render("Player 2 WIN!" , True, (	233,165,32))
        text_rect = result_text.get_rect()
        text_rect.topleft = [60, 260]
        screen.blit(result_text, text_rect)
        resultflag=1
    pygame.display.update()

    return ball_state1,ball_state2,state1,state2,reward1,reward2,state1_ob,state2_ob,resultflag
if __name__=='__main__':
    while 1:
        GameState()
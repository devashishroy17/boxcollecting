# Libraries
import os
import pygame
from pygame.locals import *
import random
import math
import mysql.connector

pygame.init()

# Creates the Pygame window
lent = 500
bret = 600
win = pygame.display.set_mode((lent, bret))
pygame.display.set_caption("Box Collecting Game")
running = False
        
# Colors
white = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]
black = [0, 0, 0]
yellow = [255, 255, 0]
green1 = [100, 255,200]

# In-game FPS
c = pygame.time.Clock()
fps = 64

# Variables
r2_size = 60
r1_size = 60
r1_x = lent//2
r1_y = bret - (r1_size-1)
r2_x = random.randint(0, (lent - lent//6))
r2_y = 0
font = pygame.font.Font(None, 30)
font1 = pygame.font.Font(None, 30)
score = 0
srtlist = []

# Loading Image(background)
pic = pygame.image.load("background.jpg").convert()
pygame.time.wait(500)

con = mysql.connector.connect(host='localhost',
                                     user='root',
                                     password='asuna',
                                     buffered=True)
cursor = con.cursor()
database = ("show databases")
cursor.execute(database)
for i in cursor:
        if "leaderboard" in i:
                hello = True
if hello == True:
        cursor.execute("use leaderboard")
else:
                cursor.execute("create database leaderboard")
                cursor.execute("use leaderboard")
                stack = "CREATE TABLE leaderboard(Score int(100))"
                wht = cursor.execute(stack)

        
# Game Loop
while not running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running =  True
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                                running = True

        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] and (r1_x < (lent-r1_size)):
                        if score <=20:
                                r1_x += 7
                        else:
                                r1_x += 10
                        
        elif keys[K_LEFT] and (r1_x>0):
                        if score <=20:
                                r1_x -= 7
                        else:
                                r1_x -= 10
        win.blit(pic, (0, -1000))
        
        if r2_y >= 0 and r2_y <= bret:
                if score <= 20:
                        r2_y += 7 + score/10
                elif score > 20 and score <= 50:
                        r2_y += 5 + score/5 
                elif score > 50:
                        r2_y += 17 
        else:
                r2_y = 0
                r2_x = random.randint(0, lent-(lent//6))
        
        o = ((r1_x > r2_x) and (r1_x < r2_x + r2_size)) and ((r1_y<r2_y+r2_size and r2_y+r2_size<r1_y+r1_size) or (r2_y>r1_y and r2_y<r1_y+r1_size))
        p = ((r1_x < r2_x) and (r2_x < r1_x + r1_size)) and ((r1_y<r2_y+r2_size and r2_y+r2_size<r1_y+r1_size) or (r2_y>r1_y and r2_y<r1_y+r1_size))

        if  ((r2_y > bret) and (((r2_x > (r1_x + r1_size))) or (((r2_x+(r2_size)) < r1_x)))):
                font1 = pygame.font.Font(None, 35)
                win.blit(pic, (0,-1400))
                S = font1.render("Game Over!", 1, white)
                win.blit(S, (lent//3, bret//3))
                Q = font1.render(str(score), 1, green1)
                win.blit(Q, ((lent - lent//4), bret//2))
                R = font1.render("Score --> ", 1, green1)
                win.blit(R, ((lent//3), bret//2))
                T = font1.render("CONTINUE ?! y/n", 1,red)
                win.blit(T, (lent//3, 400))
                U = font1.render("press c for LEADERBOARD", 1, green)
                win.blit(U, (150, 100))
                V = font1.render("press e to enter score", 1, green)
                win.blit(V, (150, 50))
                pygame.display.update()
                runagain = True
                points = score
                while runagain:
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        running = True
                                        runagain = False
                                if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_y:
                                                runagain = False
                                                score = 0
                                        if event.key == pygame.K_n:
                                                running = True
                                                runagain = False
                                        if event.key == pygame.K_c:
                                                win.blit(pic, (0,-1400))
                                                T = font1.render("CONTINUE ?! y/n", 1,red)
                                                win.blit(T, (lent//3, 50))
                                                ohoho = """select * from leaderboard order by Score desc"""
                                                cursor.execute(ohoho)
                                                m = cursor.fetchall()
                                                count_1 = 0
                                                for j in m:
                                                        count_1 += 1
                                                        t = str(*j)
                                                        print(t)
                                                        SCR = font1.render(t, 1, white)
                                                        win.blit(SCR, (lent//3, 100 + 30*count_1))
                                                pygame.display.update()

                                                if event.key == pygame.K_y:
                                                        runagain = False
                                                        score = 0
                                                if event.key == pygame.K_n:
                                                        running = True
                                                        runagain = False
                                        if event.key == pygame.K_e:
                                                query = "INSERT INTO leaderboard (Score) VALUES (%s)"
                                                cursor.execute(query%points)
                                                con.commit()
                                                
                pygame.time.wait(1000)
        else:
                if o or p:
                        score += 1
                        r2_y = 0
                        r2_x = random.randint(0, lent-(lent//6))
                
        # In-game Score
        NUMBER= font.render(str(score), 1, white)
        SCORE = font.render("Score: ", 1, black)
        win.blit(SCORE, (lent - (3*r1_size), r1_size))
        win.blit(NUMBER, ((lent - r1_size-10), r1_size))

        # Draw Squares 
        pygame.draw.rect(win, green, (r1_x, r1_y, r1_size, r1_size))
        pygame.draw.rect(win, red, (r2_x, r2_y, r2_size, r2_size))

        pygame.display.update()
        c.tick(fps)

pygame.display.quit()



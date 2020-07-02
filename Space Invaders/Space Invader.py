import pygame as py
import random as ran
import math
from pygame import mixer

# Initialise pygame
py.init()

# Create Window
py.display.set_caption("Space Invaders")
icon = py.image.load('game.png')
py.display.set_icon(icon)

win = py.display.set_mode((800, 600))

# Background Image
bg = py.image.load('background.jpg')
# Background Music
mixer.music.load('theme.wav')
mixer.music.play(-1)

# Player
playerImg = py.image.load('ship.png')
playerX = 370
playerY = 520

# Score
score = 0
font = py.font.SysFont("Ariel", 32)
fontX = 10
fontY = 10


def displayFont(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(score_value, (x, y))


def displayPlayer(x, y):
    win.blit(playerImg, (x, y))


# Bullet
bulletImg = py.image.load('security.png')
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 10
bullet_state = "ready"


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bulletImg, (x + 16, y + 10))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_Enemies = 6

for i in range(num_Enemies):
    enemyImg.append(py.image.load('enemy.png'))
    enemyX.append(ran.randint(0, 735))
    enemyY.append(ran.randint(50, 150))
    enemyX_Change.append(2)
    enemyY_Change.append(40)

# Game Over
over_font = py.font.SysFont("Ariel", 100)


def gameOver():
    game_over = over_font.render("GAME OVER!", True, (255, 255, 255))
    final_score = over_font.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(game_over, (190, 150))
    win.blit(final_score, (190, 250))


def displayEnemy(x, y, i):
    win.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Distance
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 27:
        return True
    else:
        return False


# Main Loop

running = True
while running:
    # RGB
    win.fill((0, 0, 0))
    # Background
    win.blit(bg, (0, 0))
    # Detect keystrokes
    keys = py.key.get_pressed()

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    # Fire EVERYTHING
    if keys[py.K_SPACE]:
        if bullet_state == "ready":
            fire_sound = mixer.Sound('fire.wav')
            fire_sound.play()
            bulletX = playerX
            fireBullet(bulletX, bulletY)

    if keys[py.K_ESCAPE]:
        running = False
    # x-Axis Player Movement and BOUNDARIES
    if keys[py.K_RIGHT] and playerX < 735:
        playerX += 4
    if keys[py.K_LEFT] and playerX > 1:
        playerX -= 4

    # Enemy Movement and Boundaries
    for i in range(num_Enemies):
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 2
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 735:
            enemyX_Change[i] = -2
            enemyY[i] += enemyY_Change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 480
            bullet_state = "ready"
            score += 100
            enemyX[i] = ran.randint(0, 735)
            enemyY[i] = ran.randint(50, 150)

        # Game Over
        if enemyY[i] >= 450:  # 550
            for j in range(num_Enemies):
                enemyY[j] = 2000
            gameOver()
            break

        displayEnemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    displayFont(fontX, fontY)
    displayPlayer(playerX, playerY)

    py.display.update()

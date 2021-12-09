# import pygame
import os
import sys

# import self created libraries
from Player import *
from ArmedEnemy import ArmedEnemy
from Enemy import EnemyShip
from Bonus import Bonus
from Star import Star
from Explosion import Explosion
from Boss import Boss
from Bullet import *
from BossAttack import *
from ProgramControl import ProgramControl
from Database import DatabaseManager

pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "{}, {}".format(ProgramControl.windowPos[0], ProgramControl.windowPos[1])
gameWindow = pygame.display.set_mode(ProgramControl.windowSize)
clock = pygame.time.Clock()

musicOn = True
gamingBGM = "./sound/gamingBGM6.mp3"
introBGM = "./sound/gamingBGM4.mp3"

enableAddHP = False


# display string on a pygame screen
def DisplayMessage(text, center_x, center_y, color, fontSize, font="consolas"):
    text = str(text)
    textFont = pygame.font.SysFont(font, fontSize, True)
    textSurf = textFont.render(text, True, color)
    textRec = textSurf.get_rect()
    textRec.center = (center_x, center_y)
    gameWindow.blit(textSurf, textRec)


# used in Game Intro Page
def DrawImageButton(image, position, imageSize, selected):
    gameWindow.blit(pygame.image.load(image), position)
    color = (200, 170, 0)
    if position[0] < pygame.mouse.get_pos()[0] < position[0] + imageSize[0] and \
            position[1] + round(imageSize[1]) / 4 < pygame.mouse.get_pos()[1] < position[1] + imageSize[1] - \
            round(imageSize[1] / 4) and not selected:
        pygame.draw.circle(gameWindow, color, (position[0] - 10, position[1] + round(imageSize[1] / 2)), 9)
        pygame.draw.circle(gameWindow, color, (position[0] + imageSize[0] + 10, position[1] +
                                               round(imageSize[1] / 2)), 9)
        if pygame.mouse.get_pressed()[0]:
            return True
    return False


# use in Choose Ship Page
def DrawImageButton2(image, image2, position, imageSize):
    gameWindow.blit(pygame.image.load(image), position)
    if position[0] < pygame.mouse.get_pos()[0] < position[0] + imageSize[0] and \
            position[1] + round(imageSize[1]) / 4 < pygame.mouse.get_pos()[1] < position[1] + imageSize[1] - \
            round(imageSize[1] / 4):
        gameWindow.blit(pygame.image.load(image2), position)
        if pygame.mouse.get_pressed()[0]:
            return True
    return False


def DrawImageButton3(centerX, centerY, text, textColor):
    buttonImage = pygame.image.load("./image/Button1.png")
    # (300, 68)
    x = centerX - 125
    y = centerY - 29
    fontSize = 30
    gameWindow.blit(buttonImage, (x, y))

    if x < pygame.mouse.get_pos()[0] < x + 250 and y < pygame.mouse.get_pos()[1] < y + 57:
        DisplayMessage(text, centerX, centerY, textColor[1], fontSize + 10)
        if pygame.mouse.get_pressed()[0]:
            return True
    else:
        DisplayMessage(text, centerX, centerY, textColor[0], fontSize)
    return False


# only used in ChooseCharacter page
def DrawImage(window, name, centerX, centerY, player, start):
    width = 280
    height = 200
    thisSize = ProgramControl.bigImageSize[name]
    image = pygame.image.load(name)
    x = centerX - thisSize[0] / 2
    y = centerY - thisSize[1] / 2
    window.blit(image, (x, y))
    if x < pygame.mouse.get_pos()[0] < x + width and y < pygame.mouse.get_pos()[1] < y + height:
        pygame.draw.rect(gameWindow, ProgramControl.shipSelectionColor,
                         ((thisSize[0] - width) / 2 + x, (thisSize[1] - height) / 2 + y, width, height), 4)
        player[0] = name
        if pygame.mouse.get_pressed()[0] == 1 and start:
            player[1] = name


def DisplayInfo(player):
    pygame.draw.rect(gameWindow, ProgramControl.chooseCharacterInfoBarColor,
                     (1050, 85, round(220 * player.hp / player.maxHP), 30))
    pygame.draw.rect(gameWindow, ProgramControl.chooseCharacterInfoBarColor,
                     (1050, 165, round(220 * player.speed / player.maxSpeed), 30))
    pygame.draw.rect(gameWindow, ProgramControl.chooseCharacterInfoBarColor,
                     (1050, 245, round(220 * player.damage / player.maxDamage), 30))
    pygame.draw.rect(gameWindow, ProgramControl.chooseCharacterInfoBarColor,
                     (1050, 325, round(220 * player.mpLoadTime / player.maxMP), 30))
    DescribeSpecialSkill(player.name)


# Used in Choose Ship Page
def DescribeSpecialSkill(player):
    if "A" in player:
        DisplayMessage("Reflect hostile bullets", 1085, 530, ProgramControl.skillInfoColor, 28)
    if "B" in player:
        DisplayMessage("Blast attack", 1085, 530, ProgramControl.skillInfoColor, 28)
    if "C" in player:
        DisplayMessage("Destroy all enemies at once", 1085, 530, ProgramControl.skillInfoColor, 28)
    if "D" in player:
        DisplayMessage("Obtain shield and extra HP", 1085, 530, ProgramControl.skillInfoColor, 28)


def Collide(a, b):
    if b.x - a.size[0] < a.x < b.x + b.size[0] and \
            b.y - a.size[1] < a.y < b.y + b.size[1]:
        return True
    return False


def DrawPentagon(center, length, color, width=None, innerLineWith=0, lineColor=None):
    centerX = center[0]
    centerY = center[1]
    # first point
    one = (centerX, centerY - length[0])
    # second point
    two = (centerX - length[1] * math.cos(math.radians(18)), centerY - length[1] * math.sin(math.radians(18)))
    # third point
    three = (centerX - length[2] * math.sin(math.radians(36)), centerY + length[2] * math.cos(math.radians(36)))
    # fourth point
    four = (centerX + length[3] * math.sin(math.radians(36)), centerY + length[3] * math.cos(math.radians(36)))
    # fifth point
    five = (centerX + length[4] * math.cos(math.radians(18)), centerY - length[4] * math.sin(math.radians(18)))
    if width is not None:
        pygame.draw.polygon(gameWindow, color, (one, two, three, four, five), width)
    else:
        pygame.draw.polygon(gameWindow, color, (one, two, three, four, five))
    if innerLineWith:
        temp = color if lineColor is None else lineColor
        for point in [one, two, three, four, five]:
            pygame.draw.line(gameWindow, temp, center, point, innerLineWith)


def GamePage(name):
    player = PlayerShip(name)
    if "A" in name:
        skillIcon = pygame.image.load("./image/player/player_skill/skillA.png")
        skillIcon2 = pygame.image.load("./image/player/player_skill/skillA2.png")
    elif "B" in name:
        skillIcon = pygame.image.load("./image/player/player_skill/skillB.png")
        skillIcon2 = pygame.image.load("./image/player/player_skill/skillB2.png")
    elif "C" in name:
        skillIcon = pygame.image.load("./image/player/player_skill/skillC.png")
        skillIcon2 = pygame.image.load("./image/player/player_skill/skillC2.png")
    else:
        skillIcon = pygame.image.load("./image/player/player_skill/skillD.png")
        skillIcon2 = pygame.image.load("./image/player/player_skill/skillD2.png")
    stars = [Star() for _ in range(Star.amount)]
    playerBWave = None
    disturbingPlayerShip = None

    playerBullets = []
    enemies = []
    armedEnemies = []
    enemyBullets = []
    bonuses = []
    explosions = []
    boss = None
    bossBullet = []
    knives = []
    bossBullets2 = []
    explosiveBalls = []

    if musicOn:
        pygame.mixer.music.load(gamingBGM)  # set up the background music
        pygame.mixer.music.play(loops=1000)  # play the background music

    moveUp = 0
    moveRight = 0
    timer = -150
    score = 0
    shot = 0
    doubleBullet = False
    doubleBulletTime = -1
    protectTime = -1
    gameEnd = 0
    bigEnemyGeneratingGap = ArmedEnemy.gap
    bigEnemyShootGap = ArmedEnemy.shotGap
    enemyGeneratingGap = EnemyShip.generatingGap
    speedX = 0

    # player skills
    clearAll = False
    protectPlusMedical = False
    aSkillTimeStart = 0

    # boss
    bossMode = False
    bossDieTime = 0
    bossStartTime = 0
    Boss.totalHP = Boss.stdTotalHP
    attacking = ""
    attackMethod = -1
    bossBullet2Num = 0

    # data write to database
    # playerShip, score, time, date, special_skill, destroyed_enemy
    specialSkillUsage = 0
    destroyedEnemy = [0, 0, 0]

    addHP = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveRight = -1
                if event.key == pygame.K_RIGHT:
                    moveRight = 1
                if event.key == pygame.K_UP:
                    moveUp = -1
                if event.key == pygame.K_DOWN:
                    moveUp = 1
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    if musicOn:
                        pygame.mixer.music.load(introBGM)  # set up the background music
                        pygame.mixer.music.play(loops=1000)  # play the background music
                    GameIntroPage()
                if event.key == pygame.K_p:
                    PausedPage()
                if event.key == pygame.K_SPACE and player.mp >= player.mpLoadTime:
                    specialSkillUsage += 1
                    if "C" in name:
                        clearAll = True
                        player.mp = 0
                    if "D" in name:
                        player.mp = 0
                        disturbingPlayerShip = DisturbingShip()
                    if "B" in name:
                        player.mp = 0
                        x = (ProgramControl.windowSize[0] - Blast.size[0]) / 2
                        playerBWave = Blast(x, ProgramControl.windowSize[1])
                    if "A" in name:
                        player.mp = 0
                        aSkillTimeStart = timer
                        player.protection(True)
                        protectTime = timer
                elif event.key == pygame.K_SPACE and 0 < player.mp < player.mpLoadTime and player.hp < player.totalHP \
                        and enableAddHP:
                    addHP = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    moveRight = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    moveUp = 0
                if event.key == pygame.K_SPACE and addHP and enableAddHP:
                    addHP = False

        # set up the black background
        gameWindow.fill(ProgramControl.backgroundColor)

        # draw and move the Stars
        for i in range(len(stars)):
            stars[i].draw(gameWindow)
            stars[i].move()
            if stars[i].y > ProgramControl.windowSize[1]:
                stars[i] = Star(-10)

        # display score on the right up corner
        DisplayMessage("Score: " + str(score), 1230, 70, ProgramControl.scoreColor, 40)

        # draw the player hp, include the gray background and the green bar
        '''pygame.draw.rect(gameWindow, EnemyShip.hpBackgroundColor,
                         ((ProgramControl.windowSize[0] - player.hpBarWidth) / 2, player.hpBarY, player.hpBarWidth,
                          player.hpBarHeight))
        if player.hp >= player.totalHP:
            temp = player.fullHpColor
        elif player.hp >= player.totalHP * 2 / 3:
            temp = player.hpNormalColor
        else:
            temp = player.hpDangerColor
        pygame.draw.rect(gameWindow, temp, ((ProgramControl.windowSize[0] - player.hpBarWidth) / 2, player.hpBarY,
                                            round(player.hpBarWidth * max((player.hp / player.totalHP), 0)),
                                            player.hpBarHeight))

        # draw the MP bar
        pygame.draw.rect(gameWindow, EnemyShip.hpBackgroundColor,
                         ((ProgramControl.windowSize[0] - player.hpBarWidth) / 2, player.mpBarY, player.hpBarWidth,
                          player.hpBarHeight))
        color = PlayerShip.mpBarColor2 if player.mp >= player.mpLoadTime else PlayerShip.mpBarColor
        pygame.draw.rect(gameWindow, color,
                         ((ProgramControl.windowSize[0] - player.hpBarWidth) / 2, player.mpBarY,
                          max(0, round(player.mp / player.mpLoadTime * player.hpBarWidth)), player.hpBarHeight))'''

        # put the hp bar at the up left
        pygame.draw.rect(gameWindow, EnemyShip.hpBackgroundColor, (120, 70, 250, 30))
        pygame.draw.rect(gameWindow,
                         player.hpNormalColor if player.hp >= player.totalHP / 3 else player.hpDangerColor,
                         (120, 70, max(250 * (player.hp / player.totalHP), 0), 30))
    
        # put the skill time count at the up left
        weight = 5
        gameWindow.blit(skillIcon if player.mp == player.mpLoadTime else skillIcon2, (47, 47))    # (47, 47, 80, 80)
        arcEnd = (1 - player.mp / player.mpLoadTime) * math.pi * 2 + math.pi / 2
        # pygame.draw.arc(gameWindow, (255, 255, 255), (47, 47, 86, 86), math.pi / 2, arcEnd, 8)
        for i in range(30):
            pygame.draw.arc(gameWindow, player.mpBarColor2, (47-weight/2, 47-weight/2, 80+weight, 80+weight),
                            math.pi / 2, arcEnd, weight)

        # ============================================================================================================
        # =========================================== draw things ====================================================
        # ============================================================================================================

        # draw the Explosion
        for e in explosions:
            e.draw(gameWindow)
            e.move()

        # draw the disturbing ship
        if disturbingPlayerShip is not None:
            disturbingPlayerShip.draw(gameWindow)
            disturbingPlayerShip.move()

        # draw the player
        player.move(moveRight, moveUp)
        draw = (player.protect and (timer - protectTime <= Bonus.protectorTime - Bonus.protectorWarnTime or
                                    (timer - protectTime) % 50 in range(25, 50))) or \
               (bool(aSkillTimeStart) and (timer - protectTime <= PlayerShip.reflectTime - Bonus.protectorWarnTime or
                                           (timer - protectTime) % 50 in range(25, 50)))
        if not gameEnd and not aSkillTimeStart:
            player.draw(gameWindow, draw)
        elif not gameEnd and aSkillTimeStart:
            player.draw(gameWindow, draw, (255, 193, 37))

        # if playerB use the special skill
        if playerBWave is not None:
            playerBWave.draw(gameWindow)
            playerBWave.move()

        # draw The Armed Enemy and Enemy Bullets
        if timer % round(bigEnemyGeneratingGap) == 0 and timer != 0 and len(armedEnemies) < ArmedEnemy.maxAmount \
                and not bossMode:
            armedEnemy = ArmedEnemy("./image/armedEnemy/ArmedEnemy" + str(random.randint(1, 4)) + ".png", armedEnemies)
            armedEnemies.append(armedEnemy)
        for armedEnemy in armedEnemies:
            armedEnemy.move()
            armedEnemy.draw(gameWindow)
            if armedEnemy.y > ArmedEnemy.stayAtY and (timer % round(bigEnemyShootGap) == 0 or
                                                      timer % round(bigEnemyShootGap) == ArmedEnemy.shotGap2):
                if disturbingPlayerShip is not None:
                    target = disturbingPlayerShip
                else:
                    target = player
                x = armedEnemy.x + (ArmedEnemy.size[0] - Bullet.size[0]) / 2
                y = armedEnemy.y + ArmedEnemy.size[1]
                totalSpeed = 5
                playerCenter = (target.x + target.size[0] / 2, target.y + target.size[1] / 2)
                enemyCenter = (armedEnemy.x + ArmedEnemy.size[0] / 2, armedEnemy.y + ArmedEnemy.size[1] / 2)
                angle = math.atan((playerCenter[1] - y) / (playerCenter[0] - x))
                xSpeed = math.cos(angle) * totalSpeed * (1 if playerCenter[0] > enemyCenter[0] else -1)
                ySpeed = abs(math.sin(angle) * totalSpeed) * (1 if playerCenter[1] > enemyCenter[1] else -1)
                bullet = Bullet(x, y, xSpeed, ySpeed, "./image/bullet/bulletEnemy.png")
                enemyBullets.append(bullet)
        for bullet in enemyBullets:
            bullet.move()
            bullet.draw(gameWindow)

        # draw Enemy
        if timer % round(enemyGeneratingGap) == 0 and timer >= 0 and not bossMode:
            enemy = EnemyShip("./image/enemy/Enemy" + str(random.randint(1, 11)) + ".png", enemies)
            enemies.append(enemy)
        for enemy in enemies:
            if enemy.hp > 0:
                enemy.draw(gameWindow)
                enemy.move()

        # draw the player bullet
        if timer % round(player.shotGap) == 0 and not doubleBullet and not gameEnd:
            bullet = Bullet(player.x + (player.size[0] - Bullet.size[0]) / 2, player.y,
                            speedX, -math.sqrt(169 - speedX ** 2), player.bullet)
            playerBullets.append(bullet)
        elif timer % round(player.shotGap) == 0 and doubleBullet and not gameEnd:
            Vx = speedX
            Vy = -math.sqrt(169 - speedX ** 2)
            a = Bullet(player.x + (player.size[0] - Bullet.size[0]) / 2 + 13, player.y, Vx, Vy, player.bullet)
            b = Bullet(player.x + (player.size[0] - Bullet.size[0]) / 2 - 13, player.y, Vx, Vy, player.bullet)
            playerBullets.append(a)
            playerBullets.append(b)

        # draw and move The Boss Knife
        for i in knives:
            i.draw(gameWindow)
            i.move()

        # draw and move The Boss Explosive Ball
        for i in explosiveBalls:
            i.move()
            i.draw(gameWindow)

        # draw and move Boss Super Bullet
        for i in bossBullets2:
            i.draw(gameWindow)
            i.move()

        # draw and move Bonus
        if timer != 0 and random.randint(0, round(Bonus.gap)) == 0:
            tempBonus = []
            if not doubleBullet:
                tempBonus.append("./image/bonus/BonusWeapon.png")
            if player.hp < player.totalHP:
                tempBonus.append("./image/bonus/BonusMedical.png")
            if not player.protect:
                tempBonus.append("./image/bonus/BonusProtect.png")
            if len(tempBonus) != 0:
                bonuses.append(Bonus(random.choice(tempBonus)))
        for b in bonuses:
            b.move()
            b.draw(gameWindow)

        # ============================================================================================================
        # ============================================= Boss Mode ====================================================
        # ============================================================================================================
        enemyDelete = set()
        playerBulletDelete = set()
        armedEnemyDelete = set()
        enemyBulletDelete = set()
        explosionDelete = set()
        bossBulletDelete = set()
        knivesDelete = set()
        explosiveBallsDelete = set()
        bossBulletDelete2 = set()
        bonusDelete = set()
        disturbingPlayershipDelete = False

        # draw the boss and move it
        if bossMode and boss is None and len(enemies) == 0 and len(armedEnemies) == 0:
            boss = Boss()
            bossStartTime = timer
        if boss is not None:
            boss.draw(gameWindow)
            boss.move()
        bossDelete = False

        # draw the boss bullet
        for i in bossBullet:
            i.draw(gameWindow)
            i.move()

        # boss attack
        attackMethod = random.randint(1, 4) if not attacking else attackMethod
        if attackMethod == 1 and (timer - bossStartTime) % Boss.attackGap == 0 and boss is not None and \
                boss.speed == 0 and len(knives) == 0 and not attacking:
            electricBall1 = Knife(boss.x,
                                  boss.y + Boss.size[1], random.randint(1, 4))
            knives.append(electricBall1)
            electricBall2 = Knife(boss.x + Boss.size[0] - Knife.size[0],
                                  boss.y + Boss.size[1], random.randint(1, 4))
            knives.append(electricBall2)
        elif attackMethod == 2 and (timer - bossStartTime) % Boss.attackGap == 0 and boss is not None and \
                boss.speed == 0 and len(explosiveBalls) == 0 and not attacking:
            a = ExplosiveBall(boss.x + (boss.size[0] - ExplosiveBall.size[0]) / 2,
                              boss.y + Boss.size[1], random.choice([-3, -2, 2, 3]))
            explosiveBalls.append(a)
        elif attackMethod == 3 and (timer - bossStartTime) % Boss.attackGap == 0 and boss is not None and \
                boss.speed == 0 and len(knives) == 0 and not attacking:
            bossBullet2Num = 0
            attacking = "BossBullet"
        elif (timer - bossStartTime) % Boss.attackGap == 0 and boss is not None and boss.speed == 0 and \
                not attacking:
            for i in (-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5):
                a = Bullet(boss.x + (Boss.size[0] - Bullet.size[0]) / 2, boss.y + Boss.size[1],
                           i, math.sqrt(25 - i ** 2), "./image/bullet/bulletBoss.png")
                bossBullet.append(a)

        if attacking == "BossBullet" and timer % 20 == 0 and boss is not None:
            if disturbingPlayerShip is None:
                target = player
            else:
                target = disturbingPlayerShip
            playerCenter = (target.x + target.size[0] / 2, target.y + target.size[1] / 2)
            bossCenter = (boss.x + Boss.size[0] / 2, boss.y + Boss.size[1] / 2)
            x = boss.x + (Boss.size[0] - BossBullet.size[0]) / 2
            y = boss.y + Boss.size[1] - BossBullet.size[1]
            totalSpeed = 7
            angle = math.atan((playerCenter[1] - y) / (playerCenter[0] - x))
            xSpeed = math.cos(angle) * totalSpeed * (1 if playerCenter[0] > bossCenter[0] else -1)
            ySpeed = abs(math.sin(angle) * totalSpeed) * (1 if playerCenter[1] > bossCenter[1] else -1)
            a = BossBullet(x, y, xSpeed, ySpeed)
            bossBullets2.append(a)
            bossBullet2Num += 1
        if bossBullet2Num >= 5:
            attacking = ""

        # if the boss collide with any bullet or player
        for i in range(len(playerBullets)):
            if boss is not None and Collide(playerBullets[i], boss):
                playerBulletDelete.add(i)
                boss.hp -= player.damage if boss.speed == 0 else 0
        if boss is not None and Collide(player, boss) and not player.protect:
            player.hp = -1

        # if the Boss collide with playerB's wave attack
        if playerBWave is not None and boss is not None and Collide(playerBWave, boss):
            boss.hp -= 0.5 if boss.speed == 0 else 0

        # if boss bullet collide with player
        for i in range(len(bossBullet)):
            if Collide(player, bossBullet[i]):
                bossBulletDelete.add(i)
                player.hp -= Boss.bulletDamage if not player.protect else 0
                if aSkillTimeStart:
                    bullet = Bullet(bossBullet[i].x, bossBullet[i].y, -bossBullet[i].speedX, -bossBullet[i].speedY,
                                    "./image/bullet/bulletBoss.png")
                    playerBullets.append(bullet)
            if bossBullet[i].x < -30 or bossBullet[i].x > ProgramControl.windowSize[0] or bossBullet[i].y < -30 or \
                    bossBullet[i].y > ProgramControl.windowSize[1]:
                bossBulletDelete.add(i)
            if clearAll:
                bossBulletDelete.add(i)

        # if the boss lose all HP, then remove it
        if boss is not None and boss.hp <= 0:
            bossDelete = True
            bossMode = False
            bossDieTime = timer
            explosions.append(Explosion(boss.x, boss.y, 0, 0, 2 if musicOn else 0, timer, duration=200))
            a = min(0, Boss.size[1] - 50)
            b = max(0, Boss.size[1] - 50)
            x1 = boss.x + random.randint(a, b)
            x2 = boss.x + random.randint(a, b)
            y1 = boss.y + random.randint(a, b)
            y2 = boss.y + random.randint(a, b)
            explosions.append(Explosion(x1, y1, 0, 0, 2 if musicOn else 0, timer, duration=200))
            explosions.append(Explosion(x2, y2, 0, 0, 2 if musicOn else 0, timer, duration=200))
            Boss.totalHP += 10

        # if electric ball lose all hp, then remove it
        for i in range(len(knives)):
            if knives[i].hp <= 0 or clearAll or (playerBWave is not None and Collide(playerBWave, knives[i])):
                knivesDelete.add(i)
                explosions.append(
                    Explosion(knives[i].x, knives[i].y, knives[i].speedX / 2, knives[i].speedY / 2, 1 if musicOn else 0,
                              timer, duration=200))

        # player bullet that collides with explosive ball
        for i in range(len(explosiveBalls)):
            for j in range(len(playerBullets)):
                if Collide(playerBullets[j], explosiveBalls[i]):
                    playerBulletDelete.add(j)
                    explosiveBalls[i].hp -= player.damage
        for i in range(len(explosiveBalls)):
            if explosiveBalls[i].hp <= 0 or clearAll or \
                    (playerBWave is not None and Collide(playerBWave, explosiveBalls[i])):
                explosiveBallsDelete.add(i)
                explosions.append(Explosion(explosiveBalls[i].x, explosiveBalls[i].y, explosiveBalls[i].speedX / 2,
                                            explosiveBalls[i].speedY / 2, 1 if musicOn else 0, timer, duration=200))
                center = (explosiveBalls[i].x + ExplosiveBall.size[0], explosiveBalls[i].y + ExplosiveBall.size[1])
                for j in [-5, -3, -1, 1, 3, 5]:
                    speedY = math.sqrt(25 - j ** 2)
                    a = Bullet(center[0] + j * 2, center[1] + speedY * 2, j, speedY, "./image/bullet/bulletBoss.png")
                    b = Bullet(center[0] + j * 2, center[1] - speedY * 2, j, -speedY, "./image/bullet/bulletBoss.png")
                    bossBullet.append(a)
                    bossBullet.append(b)

        # if the player collide with explosive ball
        if len(explosiveBalls) != 0 and Collide(player, explosiveBalls[0]):
            explosiveBallsDelete.add(0)
            explosions.append(Explosion(explosiveBalls[0].x, explosiveBalls[0].y, 0, 0, 1 if musicOn else 0, timer,
                                        duration=200))
            player.hp -= ExplosiveBall.damage if not player.protect else 0
            center = (explosiveBalls[0].x + ExplosiveBall.size[0], explosiveBalls[0].y + ExplosiveBall.size[1])
            for j in [-5, -3, -1, 1, 3, 5]:
                speedY = math.sqrt(25 - j ** 2)
                a = Bullet(center[0] + j * 2, center[1] + speedY * 2, j, speedY, "./image/bullet/bulletBoss.png")
                b = Bullet(center[0] + j * 2, center[1] - speedY * 2, j, -speedY, "./image/bullet/bulletBoss.png")
                bossBullet.append(a)
                bossBullet.append(b)

        # boss bullet 2 collide with the player
        for i in range(len(bossBullets2)):
            if Collide(player, bossBullets2[i]):
                bossBulletDelete2.add(i)
                if not player.protect:
                    player.hp -= BossBullet.damage
            if clearAll or (playerBWave is not None and Collide(playerBWave, bossBullets2[i])):
                bossBulletDelete2.add(i)

        # if playerC use the speical skill (clearAll = True)
        if clearAll and boss is not None:
            boss.hp -= 15

        # if boss bullet collide with playerB's blast attack
        for i in range(len(bossBullet)):
            if playerBWave is not None and Collide(playerBWave, bossBullet[i]):
                bossBulletDelete.add(i)

        # ============================================================================================================
        # ========================================== Remove things ===================================================
        # ============================================================================================================

        # the bullet that moves out of window
        for i in range(len(playerBullets)):
            playerBullets[i].draw(gameWindow)
            playerBullets[i].move()
            if playerBullets[i].y < -20:
                playerBulletDelete.add(i)

        # enemy bullets go out of the window or collied with the player
        for i in range(len(enemyBullets)):
            if enemyBullets[i].y > ProgramControl.windowSize[1] + Bullet.size[1] + 20 or enemyBullets[i].x < -20 or \
                    enemyBullets[i].x > ProgramControl.windowSize[0] + 10:
                enemyBulletDelete.add(i)
            if Collide(enemyBullets[i], player):
                enemyBulletDelete.add(i)
                if not player.protect:
                    player.hp -= ArmedEnemy.damage
                if aSkillTimeStart:
                    bullet = Bullet(enemyBullets[i].x, enemyBullets[i].y, -enemyBullets[i].speedX,
                                    -enemyBullets[i].speedY, "./image/bullet/bulletEnemy.png")
                    playerBullets.append(bullet)
                shot += 1
            if clearAll:
                enemyBulletDelete.add(i)
            if playerBWave is not None and Collide(playerBWave, enemyBullets[i]):
                enemyBulletDelete.add(i)

        # the enemy that collide with the player or moves out of the window or lose all HP
        for i in range(len(enemies)):
            if Collide(player, enemies[i]):
                if not player.protect:
                    player.hp -= 2
                shot += 1
                enemyDelete.add(i)
                explosions.append(Explosion(enemies[i].x, enemies[i].y, 0, 2, 1 if musicOn else 0, timer, duration=200))
            if enemies[i].y > ProgramControl.windowSize[1]:
                enemyDelete.add(i)
            if enemies[i].hp <= 0:
                enemyDelete.add(i)
                explosions.append(Explosion(enemies[i].x, enemies[i].y, 0, 2, 1 if musicOn else 0, timer, duration=200))
            if clearAll:
                enemyDelete.add(i)
                explosions.append(Explosion(enemies[i].x, enemies[i].y, 0, 2, 1 if musicOn else 0, timer, duration=200))
            if playerBWave is not None and Collide(playerBWave, enemies[i]):
                enemyDelete.add(i)

        # the bullet that collide with the enemy
        for i in range(len(playerBullets)):
            for j in range(len(enemies)):
                if Collide(playerBullets[i], enemies[j]):
                    enemies[j].getShot(player)
                    playerBulletDelete.add(i)

        # the bullet that collide with the armed enemy
        for i in range(len(playerBullets)):
            for j in range(len(armedEnemies)):
                if Collide(playerBullets[i], armedEnemies[j]):
                    playerBulletDelete.add(i)
                    armedEnemies[j].getShot(player)

        # high level enemy that lose all HP or collide with the player
        for i in range(len(armedEnemies)):
            if armedEnemies[i].hp <= 0:
                armedEnemyDelete.add(i)
                explosions.append(Explosion(armedEnemies[i].x, armedEnemies[i].y, 0, 0, 1 if musicOn else 0, timer,
                                            duration=200))
            if Collide(player, armedEnemies[i]):
                if not player.protect:
                    player.hp -= EnemyShip.damage
                shot += 1
                armedEnemyDelete.add(i)
                explosions.append(Explosion(armedEnemies[i].x, armedEnemies[i].y, 0, 0, 1 if musicOn else 0, timer,
                                            duration=200))
            if clearAll:
                armedEnemyDelete.add(i)
                explosions.append(Explosion(armedEnemies[i].x, armedEnemies[i].y, 0, 0, 1 if musicOn else 0, timer,
                                            duration=200))
            if playerBWave is not None and Collide(playerBWave, armedEnemies[i]):
                armedEnemyDelete.add(i)
                explosions.append(Explosion(armedEnemies[i].x, armedEnemies[i].y, 0, 0, 1 if musicOn else 0, timer,
                                            duration=200))

        # the knives that collide with player or player bullet
        for i in range(len(knives)):
            if Collide(player, knives[i]):
                knivesDelete.add(i)
                explosions.append(Explosion(knives[i].x, knives[i].y, knives[i].speedX / 2, knives[i].speedY / 2,
                                            1 if musicOn else 0, timer, duration=200))
                if not player.protect:
                    player.hp -= knives[i].damage
            for j in range(len(playerBullets)):
                if Collide(playerBullets[j], knives[i]):
                    playerBulletDelete.add(j)
                    knives[i].hp = max(knives[i].hp - player.damage, 0)

        # bonus out of window or collide with player
        for i in range(len(bonuses)):
            if bonuses[i].y > ProgramControl.windowSize[1] + Bonus.size[1] + 30:
                bonusDelete.add(i)
            if Collide(player, bonuses[i]):
                bonusDelete.add(i)
                if musicOn:
                    sound = pygame.mixer.Sound("./sound/GetBonus.wav")
                    sound.set_volume(1.3)
                    sound.play()
                if bonuses[i].function == "./image/bonus/BonusMedical.png":
                    player.hp = min(player.totalHP, player.hp + Bonus.addLives)
                elif bonuses[i].function == "./image/bonus/BonusWeapon.png" and not doubleBullet:
                    doubleBullet = True
                    doubleBulletTime = timer
                elif bonuses[i].function == "./image/bonus/BonusProtect.png" and not player.protect:
                    player.protection(True)
                    protectTime = timer

        # explosion that run out of time
        for i in range(len(explosions)):
            if explosions[i].delete(timer):
                explosionDelete.add(i)

        # playerB's wave attack goes out of window
        if playerBWave is not None and playerBWave.y <= -250:
            playerBWave = None

        # if the disturb ship collide anything
        if disturbingPlayerShip is not None:
            # collide with enemy
            for i in range(len(enemies)):
                if Collide(disturbingPlayerShip, enemies[i]):
                    enemyDelete.add(i)
                    explosions.append(Explosion(enemies[i].x, enemies[i].y, 0, 2, 1 if musicOn else 0, timer,
                                                duration=200))
                    disturbingPlayerShip.hp -= EnemyShip.damage
            # collide with armed_enemy_bullet
            for i in range(len(enemyBullets)):
                if Collide(disturbingPlayerShip, enemyBullets[i]):
                    enemyBulletDelete.add(i)
                    disturbingPlayerShip.hp -= ArmedEnemy.damage
            # collide with boss_small_bullet
            for i in range(len(bossBullet)):
                if Collide(disturbingPlayerShip, bossBullet[i]):
                    bossBulletDelete.add(i)
                    disturbingPlayerShip.hp -= Boss.bulletDamage
            # collide with boss_big_bullet
            for i in range(len(bossBullets2)):
                if Collide(disturbingPlayerShip, bossBullets2[i]):
                    bossBulletDelete2.add(i)
                    disturbingPlayerShip.hp -= BossBullet.damage
            # collide with boss_knives
            for i in range(len(knives)):
                if Collide(disturbingPlayerShip, knives[i]):
                    knivesDelete.add(i)
                    disturbingPlayerShip.hp -= knives[i].damage
                    explosions.append(Explosion(knives[i].x, knives[i].y, knives[i].speedX / 2, knives[i].y / 2,
                                                1 if musicOn else 0, timer, duration=200))
            # collide with boss_explosiveBall
            for i in range(len(explosiveBalls)):
                if Collide(disturbingPlayerShip, explosiveBalls[i]):
                    explosiveBallsDelete.add(i)
                    disturbingPlayerShip.hp -= ExplosiveBall.damage
                    explosions.append(Explosion(explosiveBalls[0].x, explosiveBalls[0].y, 0, 0, 1 if musicOn else 0,
                                                timer, duration=200))
                    center = (explosiveBalls[i].x + ExplosiveBall.size[0], explosiveBalls[i].y + ExplosiveBall.size[1])
                    for j in [-5, -3, -1, 1, 3, 5]:
                        speedY = math.sqrt(25 - j ** 2)
                        a = Bullet(center[0] + j * 2, center[1] + speedY * 2, j, speedY,
                                   "./image/bullet/bulletBoss.png")
                        b = Bullet(center[0] + j * 2, center[1] - speedY * 2, j, -speedY,
                                   "./image/bullet/bulletBoss.png")
                        bossBullet.append(a)
                        bossBullet.append(b)

        # if the disturb ship lose all hp
        if disturbingPlayerShip is not None and disturbingPlayerShip.hp <= 0:
            disturbingPlayershipDelete = True
            explode = Explosion(disturbingPlayerShip.x, disturbingPlayerShip.y, 0, 0, 1 if musicOn else 0, timer,
                                sound="PlayerDie.wav", duration=200)
            explosions.append(explode)

        # now remove the things that should be remove
        for i in reversed(sorted(enemyDelete)):
            enemies.pop(i)
            score += EnemyShip.score
            destroyedEnemy[0] += 1
        for i in reversed(sorted(playerBulletDelete)):
            playerBullets.pop(i)
        for i in reversed(sorted(armedEnemyDelete)):
            armedEnemies.pop(i)
            score += ArmedEnemy.score
            destroyedEnemy[1] += 1
        for i in reversed(sorted(enemyBulletDelete)):
            enemyBullets.pop(i)
        for i in reversed(sorted(bonusDelete)):
            bonuses.pop(i)
        for i in reversed(sorted(explosionDelete)):
            explosions.pop(i)
        for i in reversed(sorted(bossBulletDelete)):
            bossBullet.pop(i)
        for i in reversed(sorted(knivesDelete)):
            knives.pop(i)
        for i in reversed(sorted(explosiveBallsDelete)):
            explosiveBalls.pop(i)
        for i in reversed(sorted(bossBulletDelete2)):
            bossBullets2.pop(i)
        if bossDelete:
            boss = None
            score += Boss.score
            destroyedEnemy[2] += 1
        if disturbingPlayershipDelete:
            disturbingPlayerShip = None

        # ============================================================================================================
        # =========================================== other things ===================================================
        # ============================================================================================================

        # check if the player has used out of their lives
        if player.hp < 0 and not gameEnd:
            gameEnd = timer
            explosions.append(Explosion(player.x, player.y, 0, 0, 3 if musicOn else 0, timer, duration=200,
                                        sound="PlayerDie.wav"))
        if timer - gameEnd >= ProgramControl.gameEndWaitTime and gameEnd:
            pygame.mixer.music.stop()
            Star.speedRange = Star.stdSpeedRange
            StatisticsPage(player.name, score, round(timer / ProgramControl.frequency, 2), specialSkillUsage,
                           destroyedEnemy)

        # check if the game should level up
        if timer % ProgramControl.levelUp == 0 and timer != 0:
            increment = 0.9
            increment2 = 0.85
            if timer % ProgramControl.slowLevelUp == 0 and timer != 0:
                increment = min(increment * 1.01, 0.95)
                increment2 = min(increment2 * 1.01, 0.9)
            which = random.randint(1, 3)
            if which == 1:
                enemyGeneratingGap = max(enemyGeneratingGap * increment, 30)
            if which == 2:
                bigEnemyShootGap = max(bigEnemyShootGap * increment2, 50)
            if which == 3:
                bigEnemyGeneratingGap = max(bigEnemyGeneratingGap * increment, 100)

        # check if double weapon time is finished
        if timer - doubleBulletTime >= Bonus.weaponDoubleTime:
            doubleBullet = False

        # check if the protect time is finished
        if timer - protectTime >= Bonus.protectorTime and player.protect and not aSkillTimeStart:
            player.protection(False)

        # add the protection and the medical effect to playerD
        if protectPlusMedical:
            player.protection(True)
            protectTime = timer + Bonus.protectorTime
            player.hp = min(player.totalHP, player.hp * 1.5)

        # reset the skills
        clearAll = False
        protectPlusMedical = False

        if aSkillTimeStart and timer - aSkillTimeStart >= PlayerShip.reflectTime:
            aSkillTimeStart = 0

        # add player's mp
        if (("D" in name and disturbingPlayerShip is None) or ("B" in name) or ("C" in name) or
            (not aSkillTimeStart and "A" in name)) and not addHP:
            player.mp = min(player.mp + 1, player.mpLoadTime)

        # speed up the background
        if timer % 1800 == 0 and timer != 0:
            a = Star.speedRange[0] + 1
            b = Star.speedRange[1] + 2
            Star.speedRange = (a, b)

        # check if the boss should come
        if timer - bossDieTime >= Boss.gap and timer != 0:
            bossMode = True

        # check if the hp should be added
        if addHP and player.hp < player.totalHP and player.mp > 0:
            player.hp += player.recoverySpeed
            player.mp -= 2

        # update
        timer += 1
        if timer % 120 == 0:
            score += 1
        pygame.display.update()
        clock.tick(ProgramControl.frequency)


def ChooseShipPage():
    player = ["", ""]
    width = 280
    height = 200
    start = False
    timer = 0
    global musicOn
    changedTime = -1
    changingAllowed = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GameIntroPage()

        # draw the background and the stars
        gameWindow.fill(ProgramControl.introBackgroundColor)

        image = pygame.image.load("./image/musicButton.png")
        x = 1250
        y = 630
        size = (80, 80)
        gameWindow.blit(image, (x, y))
        if x < pygame.mouse.get_pos()[0] < x + size[0] and y < pygame.mouse.get_pos()[1] < y + size[1] and \
                pygame.mouse.get_pressed()[0] and changingAllowed:
            musicOn = not musicOn
            changedTime = timer
            changingAllowed = False
            if musicOn:
                pygame.mixer.music.play(loops=100)
            elif not musicOn:
                pygame.mixer.music.stop()
        if not musicOn:
            pygame.draw.line(gameWindow, (255, 0, 0), (x, y), (x + size[0], y + size[1]), 5)
        if timer - changedTime >= 30:
            changingAllowed = True

        player = ["", player[1]]

        DrawImage(gameWindow, "./image/player/PlayerShipDisplayA.png", 250, 170, player, start)
        DrawImage(gameWindow, "./image/player/PlayerShipDisplayB.png", 620, 170, player, start)
        DrawImage(gameWindow, "./image/player/PlayerShipDisplayC.png", 250, 450, player, start)
        DrawImage(gameWindow, "./image/player/PlayerShipDisplayD.png", 620, 450, player, start)

        if player[1] == "./image/player/PlayerShipDisplayA.png" and start:
            thisSize = ProgramControl.bigImageSize["./image/player/PlayerShipDisplayA.png"]
            pygame.draw.rect(gameWindow, ProgramControl.shipConfirmColor,
                             ((thisSize[0] - width) / 2 + 250 - thisSize[0] / 2,
                              (thisSize[1] - height) / 2 + 170 - thisSize[1] / 2,
                              width, height), 5)
        if player[1] == "./image/player/PlayerShipDisplayB.png" and start:
            thisSize = ProgramControl.bigImageSize["./image/player/PlayerShipDisplayB.png"]
            pygame.draw.rect(gameWindow, ProgramControl.shipConfirmColor,
                             ((thisSize[0] - width) / 2 + 620 - thisSize[0] / 2,
                              (thisSize[1] - height) / 2 + 170 - thisSize[1] / 2,
                              width, height), 5)
        if player[1] == "./image/player/PlayerShipDisplayC.png" and start:
            thisSize = ProgramControl.bigImageSize["./image/player/PlayerShipDisplayC.png"]
            pygame.draw.rect(gameWindow, ProgramControl.shipConfirmColor,
                             ((thisSize[0] - width) / 2 + 250 - thisSize[0] / 2,
                              (thisSize[1] - height) / 2 + 450 - thisSize[1] / 2,
                              width, height), 5)
        if player[1] == "./image/player/PlayerShipDisplayD.png" and start:
            thisSize = ProgramControl.bigImageSize["./image/player/PlayerShipDisplayD.png"]
            pygame.draw.rect(gameWindow, ProgramControl.shipConfirmColor,
                             ((thisSize[0] - width) / 2 + 620 - thisSize[0] / 2,
                              (thisSize[1] - height) / 2 + 450 - thisSize[1] / 2,
                              width, height), 5)

        if pygame.mouse.get_pressed()[0] == 0:
            start = True

        if DrawImageButton2("./image/text/chooseShipConfirm.png", "./image/text/chooseShipConfirm2.png",
                            (270, 540), (400, 200)) and player[1] != "":
            name = "./image/player/PlayerShip" + player[1].split(".")[1].split(".")[0][-1] + ".png"
            GamePage(name)

        # def DisplayMessage(text, center_x, center_y, color, fontSize):
        DisplayMessage("     HP", 955, 100, ProgramControl.chooseCharacterTextColor, 38)
        DisplayMessage("  Speed", 955, 175, ProgramControl.chooseCharacterTextColor, 38)
        DisplayMessage(" Damage", 955, 260, ProgramControl.chooseCharacterTextColor, 38)
        DisplayMessage("     CD", 955, 335, ProgramControl.chooseCharacterTextColor, 38)

        pygame.draw.rect(gameWindow, ProgramControl.chooseCharacterInfoBarBackgroundColor, (1050, 85, 220, 30))
        pygame.draw.rect(gameWindow, ProgramControl.chooseCharacterInfoBarBackgroundColor, (1050, 165, 220, 30))
        pygame.draw.rect(gameWindow, ProgramControl.chooseCharacterInfoBarBackgroundColor, (1050, 245, 220, 30))
        pygame.draw.rect(gameWindow, ProgramControl.chooseCharacterInfoBarBackgroundColor, (1050, 325, 220, 30))
        pygame.draw.rect(gameWindow, ProgramControl.skillRectColor, (860, 455, 450, 150), 5)
        DisplayMessage("Special Skill", 930, 435, ProgramControl.skillTitleColor, 30)

        if player[0] != "":
            tempPlayer = PlayerShip("./image/player/PlayerShip" + player[0].split(".")[1].split(".")[0][-1] + ".png")
            DisplayInfo(tempPlayer)

        elif player[1] != "":
            tempPlayer = PlayerShip("./image/player/PlayerShip" + player[1].split(".")[1].split(".")[0][-1] + ".png")
            DisplayInfo(tempPlayer)

        timer += 1
        pygame.display.update()
        clock.tick(ProgramControl.frequency)


def DrawEdge(i):
    selectionRectHeight = 500
    mousePos = pygame.mouse.get_pos()
    x = (i + 1) * 40 + i * 300
    y = 40
    selectedShip = False
    if x < mousePos[0] < x + 300 and y < mousePos[1] < y + selectionRectHeight:
        pygame.draw.rect(gameWindow, (84, 255, 159), (x, y, 300, selectionRectHeight), 5)
        if pygame.mouse.get_pressed()[0]:
            selectedShip = ["playerA", "playerB", "playerC", "playerD"][i]
    else:
        pygame.draw.rect(gameWindow, (100, 100, 100), (x, y, 300, selectionRectHeight), 5)
    return selectedShip


def ChooseShipPage2():
    selectionRectHeight = 500
    selectedShip = None
    startToChoose = False

    playerA = PlayerShip("./image/player/PlayerShipA.png")
    playerA.x, playerA.y = 190 - playerA.size[0] / 2, 40 + selectionRectHeight * 0.2 - playerA.size[1] / 2
    playerB = PlayerShip("./image/player/PlayerShipB.png")
    playerB.x, playerB.y = 530 - playerB.size[0] / 2, 40 + selectionRectHeight * 0.2 - playerB.size[1] / 2
    playerC = PlayerShip("./image/player/PlayerShipC.png")
    playerC.x, playerC.y = 870 - playerC.size[0] / 2, 40 + selectionRectHeight * 0.2 - playerC.size[1] / 2
    playerD = PlayerShip("./image/player/PlayerShipD.png")
    playerD.x, playerD.y = 1210 - playerD.size[0] / 2, 40 + selectionRectHeight * 0.2 - playerD.size[1] / 2
    players = [playerA, playerB, playerC, playerD]

    timer = 0
    global musicOn
    changedTime = -1
    changingAllowed = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        gameWindow.fill(ProgramControl.introBackgroundColor)

        # draw the music button
        image = pygame.image.load("./image/musicButton.png")
        x = 1250
        y = 630
        size = (80, 80)
        gameWindow.blit(image, (x, y))
        if x < pygame.mouse.get_pos()[0] < x + size[0] and y < pygame.mouse.get_pos()[1] < y + size[1] and \
                pygame.mouse.get_pressed()[0] and changingAllowed:
            musicOn = not musicOn
            changedTime = timer
            changingAllowed = False
            if musicOn:
                pygame.mixer.music.play(loops=100)
            elif not musicOn:
                pygame.mixer.music.stop()
        if not musicOn:
            pygame.draw.line(gameWindow, (255, 0, 0), (x, y), (x + size[0], y + size[1]), 5)
        if timer - changedTime >= 30:
            changingAllowed = True

        if pygame.mouse.get_pressed()[0] == 0:
            startToChoose = True

        # draw the edge of the selection, width = 300, gap = 40, height = 400
        '''mousePos = pygame.mouse.get_pos()
        for i in range(4):
            x = (i + 1) * 40 + i * 300
            y = 40
            if x < mousePos[0] < x + 300 and y < mousePos[1] < y + selectionRectHeight:
                pygame.draw.rect(gameWindow, (84, 255, 159), (x, y, 300, selectionRectHeight), 5)
                if pygame.mouse.get_pressed()[0] and startToChoose:
                    selectedShip = [playerA, playerB, playerC, playerD][i]
            else:
                pygame.draw.rect(gameWindow, (100, 100, 100), (x, y, 300, selectionRectHeight), 5)'''

        # Display confirm button
        if DrawImageButton3(ProgramControl.windowSize[0] / 2, 650, "Let's Go", ((255, 0, 100), (255, 255, 0))) and \
                selectedShip is not None:
            GamePage(selectedShip.name)

        # draw the edge of the selection, width = 300, gap = 40, height = 400
        a = DrawEdge(0)
        b = DrawEdge(1)
        c = DrawEdge(2)
        d = DrawEdge(3)
        if a == "playerA" and startToChoose:
            selectedShip = playerA
        elif b == "playerB" and startToChoose:
            selectedShip = playerB
        elif c == "playerC" and startToChoose:
            selectedShip = playerC
        elif d == "playerD" and startToChoose:
            selectedShip = playerD
        elif pygame.mouse.get_pressed()[0]:
            selectedShip = None

        # draw the selection rect
        if selectedShip == playerA:
            pygame.draw.rect(gameWindow, (255, 255, 0), (40, 40, 300, selectionRectHeight), 5)
        if selectedShip == playerB:
            pygame.draw.rect(gameWindow, (255, 255, 0), (380, 40, 300, selectionRectHeight), 5)
        if selectedShip == playerC:
            pygame.draw.rect(gameWindow, (255, 255, 0), (720, 40, 300, selectionRectHeight), 5)
        if selectedShip == playerD:
            pygame.draw.rect(gameWindow, (255, 255, 0), (1060, 40, 300, selectionRectHeight), 5)

        # display the ships
        playerA.draw(gameWindow, False)
        playerB.draw(gameWindow, False)
        playerC.draw(gameWindow, False)
        playerD.draw(gameWindow, False)

        radarShift = 75
        # display the info of each player ship
        for i in range(len(players)):
            line1 = 100 * (players[i].minShotGap - players[i].maxShotGap) / \
                    (players[i].shotGap - players[i].maxShotGap)
            if enableAddHP:
                line1 = 100 * (players[i].recoverySpeed - players[i].minRecoverySpeed) / \
                        (players[i].maxRecoverySpeed - players[i].minRecoverySpeed)
            line2 = 100 * players[i].totalHP / players[i].maxHP
            line3 = 100 * players[i].speed / players[i].maxSpeed
            line4 = 100 * players[i].damage / players[i].maxDamage
            line5 = 100 * (players[i].mpLoadTime - players[i].minMP) / (players[i].maxMP - players[i].minMP)
            # DrawPentagon((190 + i * 340, 400), [line1, line2, line3, line4, line5], (0, 0, 100), innerLineWith=1,
            # lineColor=(150, 205, 205))
            DrawPentagon((190 + i * 340, 300 + radarShift), [line1, line2, line3, line4, line5], (0, 0, 255))

        # display the base pentagon and title ("CD", "HP", "shoot speed", "damage", "speed"
        for i in range(4):
            DrawPentagon((190 + i * 340, 300 + radarShift), [100 for _ in range(5)], (150, 205, 205), 3, True)
            DrawPentagon((190 + i * 340, 300 + radarShift), [66 for _ in range(5)], (150, 205, 205), 1, True)
            DrawPentagon((190 + i * 340, 300 + radarShift), [33 for _ in range(5)], (150, 205, 205), 1, True)
            DisplayMessage("recovery" if enableAddHP else "shoot speed", 190 + i * 340, 190 + radarShift,
                           (150, 205, 205), 20)
            DisplayMessage("HP", 80 + i * 340, 265 + radarShift, (150, 205, 205), 20)
            DisplayMessage("CD", 300 + i * 340, 265 + radarShift, (150, 205, 205), 20)
            DisplayMessage("speed", 120 + i * 340, 395 + radarShift, (150, 205, 205), 20)
            DisplayMessage("damage", 270 + i * 340, 395 + radarShift, (150, 205, 205), 20)

        # draw the "show more" button
        '''for i in range(4):
            width = 160
            height = 35
            x = 40 + 300 / 2 - width / 2 + 340 * i
            y = 450
            mousePos = pygame.mouse.get_pos()
            normalColor = (190, 190, 190)
            hoverColor = (255, 255, 0)
            if x < mousePos[0] < x + width and y < mousePos[1] < y + height:
                pygame.draw.rect(gameWindow, hoverColor, (x, y, width, height))
                DisplayMessage("show more", x + width / 2, y + height / 2, normalColor, 22)
            else:
                pygame.draw.rect(gameWindow, normalColor, (x, y, width, height))
                DisplayMessage("show move", x + width / 2, y + height / 2, hoverColor, 22)'''

        timer += 1
        pygame.display.update()
        clock.tick(ProgramControl.frequency)


def StatisticsPage(playerShip, score, time, specialSkillUsage, destroyed):
    if musicOn:
        pygame.mixer.Sound("./sound/GameEnd.wav").play()
        pygame.mixer.music.load(introBGM)  # set up the background music
        pygame.mixer.music.play(loops=1000)  # play the background music
    databaseManager = DatabaseManager()
    databaseManager.insert(playerShip, score, time, specialSkillUsage, destroyed)
    databaseManager.disconnect()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                GameIntroPage()

        gameWindow.fill(ProgramControl.introBackgroundColor)

        DisplayMessage("Score: {}".format(score), ProgramControl.windowSize[0] / 2, 150,
                       ProgramControl.statsWindowFontColor, 50)
        DisplayMessage("Time: {}s".format(time), ProgramControl.windowSize[0] / 2,
                       300, ProgramControl.statsWindowFontColor, 50)
        DisplayMessage("Destroyed Enemy: {}".format(sum(destroyed)), ProgramControl.windowSize[0] / 2, 450,
                       ProgramControl.statsWindowFontColor, 50)
        DisplayMessage("Press Enter to Continue", ProgramControl.windowSize[0] / 2, 650,
                       ProgramControl.statsWindowFontColor2,
                       ProgramControl.statsWindowFontSize)

        pygame.display.update()
        clock.tick(ProgramControl.frequency)


def GameIntroPage():
    timer = 0
    global musicOn
    changingAllowed = True
    changedTime = -1
    textColor1 = (255, 0, 0)
    textColor2 = (0, 255, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

        gameWindow.fill(ProgramControl.introBackgroundColor)

        image = pygame.image.load("./image/musicButton.png")
        x = 1250
        y = 630
        size = (80, 80)
        gameWindow.blit(image, (x, y))
        if x < pygame.mouse.get_pos()[0] < x + size[0] and y < pygame.mouse.get_pos()[1] < y + size[1] and \
                pygame.mouse.get_pressed()[0] and changingAllowed:
            musicOn = not musicOn
            changedTime = timer
            changingAllowed = False
            if musicOn:
                pygame.mixer.music.play(loops=100)
            elif not musicOn:
                pygame.mixer.music.stop()
        if not musicOn:
            pygame.draw.line(gameWindow, (255, 0, 0), (x, y), (x + size[0], y + size[1]), 5)
        if timer - changedTime >= 30:
            changingAllowed = True

        gameWindow.blit(pygame.image.load("./image/text/title1.png"), (140, 10))

        if DrawImageButton3(ProgramControl.windowSize[0] / 2, ProgramControl.windowSize[1] / 2 + 20,
                            "Start", (textColor1, textColor2)):
            ChooseShipPage2()

        if DrawImageButton3(ProgramControl.windowSize[0] / 2, ProgramControl.windowSize[1] / 2 + 120,
                            "High Score", (textColor1, textColor2)):
            HighScorePage()

        if DrawImageButton3(ProgramControl.windowSize[0] / 2, ProgramControl.windowSize[1] / 2 + 220,
                            "Exit", (textColor1, textColor2)):
            sys.exit()

        timer += 1
        pygame.display.update()
        clock.tick(ProgramControl.frequency)


def HighScorePage():
    imageLabelRightX = 400
    infoRectColor = (255, 255, 255)
    databaseManager = DatabaseManager()
    timer = 0
    global musicOn
    changingAllowed = True
    changedTime = -1

    playerAImage = pygame.image.load("./image/player/PlayerShipA.png")
    playerBImage = pygame.image.load("./image/player/PlayerShipB.png")
    playerCImage = pygame.image.load("./image/player/PlayerShipC.png")
    playerDImage = pygame.image.load("./image/player/PlayerShipD.png")
    playerASize = (135, 85)
    playerBSize = (134, 87)
    playerCSize = (142, 86)
    playerDSize = (123, 90)
    playerALocation = (imageLabelRightX - playerASize[0], ProgramControl.windowSize[1] * 0.2 - playerASize[1] / 2)
    playerBLocation = (imageLabelRightX - playerBSize[0], ProgramControl.windowSize[1] * 0.4 - playerBSize[1] / 2)
    playerCLocation = (imageLabelRightX - playerCSize[0], ProgramControl.windowSize[1] * 0.6 - playerCSize[1] / 2)
    playerDLocation = (imageLabelRightX - playerDSize[0], ProgramControl.windowSize[1] * 0.8 - playerDSize[1] / 2)

    score = ""
    time = ""
    date = ""
    totalDestroyed = ""
    dataA = databaseManager.getHighScoreByShip("./image/player/PlayerShipA.png")
    dataB = databaseManager.getHighScoreByShip("./image/player/PlayerShipB.png")
    dataC = databaseManager.getHighScoreByShip("./image/player/PlayerShipC.png")
    dataD = databaseManager.getHighScoreByShip("./image/player/PlayerShipD.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                databaseManager.disconnect()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    databaseManager.disconnect()
                    return
        gameWindow.fill(ProgramControl.introBackgroundColor)

        # draw the image labels
        gameWindow.blit(playerAImage, playerALocation)
        gameWindow.blit(playerBImage, playerBLocation)
        gameWindow.blit(playerCImage, playerCLocation)
        gameWindow.blit(playerDImage, playerDLocation)

        # draw the rectangle that surround the info
        pygame.draw.rect(gameWindow, infoRectColor, (imageLabelRightX + 20, 97, 600, 558), 5)

        # display the info title
        DisplayMessage("Highest Score: ", 680, 200, (255, 255, 255), 40)
        DisplayMessage("Time used: ", 685, 300, (255, 255, 255), 40)
        DisplayMessage("Destroyed Enemy: ", 690, 400, (255, 255, 255), 40)
        DisplayMessage("Date: ", 630, 500, (255, 255, 255), 40)

        # display the info content
        DisplayMessage(score, 860, 200, (0, 200, 255), 40)
        DisplayMessage(str(time) + "s" if isinstance(time, int) else "", 830, 300, (0, 200, 255), 40)
        DisplayMessage(totalDestroyed, 880, 400, (0, 200, 255), 40)
        DisplayMessage(date, 800, 500, (0, 200, 255), 40)

        # draw the button effect
        mousePos = pygame.mouse.get_pos()
        if playerALocation[0] < mousePos[0] < playerALocation[0] + playerASize[0] and \
                playerALocation[1] < mousePos[1] < playerALocation[1] + playerASize[1]:
            pygame.draw.rect(gameWindow, infoRectColor, (playerALocation[0] - 10, playerALocation[1] - 10,
                                                         playerASize[0] + 30, playerASize[1] + 20), 5)
            pygame.draw.rect(gameWindow, ProgramControl.introBackgroundColor,
                             (playerALocation[0] + playerASize[0] + 17, playerALocation[1] - 7, 6, playerASize[1] + 14))
            _, score, date, time, _, normal, armed, boss = dataA
            totalDestroyed = int(normal) + int(armed) + int(boss)
            date = "{}-{} {}:{}".format(date.month, date.day, date.hour, date.minute) if date != 0 else "N/A"
        elif playerBLocation[0] < mousePos[0] < playerBLocation[0] + playerBSize[0] and \
                playerBLocation[1] < mousePos[1] < playerBLocation[1] + playerBSize[1]:
            pygame.draw.rect(gameWindow, infoRectColor, (playerBLocation[0] - 10, playerBLocation[1] - 10,
                                                         playerBSize[0] + 30, playerBSize[1] + 20), 5)
            pygame.draw.rect(gameWindow, ProgramControl.introBackgroundColor,
                             (playerBLocation[0] + playerBSize[0] + 17, playerBLocation[1] - 7, 6, playerBSize[1] + 14))
            _, score, date, time, _, normal, armed, boss = dataB
            totalDestroyed = int(normal) + int(armed) + int(boss)
            date = "{}-{} {}:{}".format(date.month, date.day, date.hour, date.minute) if date != 0 else "N/A"
        elif playerCLocation[0] < mousePos[0] < playerCLocation[0] + playerCSize[0] and \
                playerCLocation[1] < mousePos[1] < playerCLocation[1] + playerCSize[1]:
            pygame.draw.rect(gameWindow, infoRectColor, (playerCLocation[0] - 10, playerCLocation[1] - 10,
                                                         playerCSize[0] + 30, playerCSize[1] + 20), 5)
            pygame.draw.rect(gameWindow, ProgramControl.introBackgroundColor,
                             (playerCLocation[0] + playerCSize[0] + 17, playerCLocation[1] - 7, 6, playerCSize[1] + 14))
            _, score, date, time, _, normal, armed, boss = dataC
            totalDestroyed = int(normal) + int(armed) + int(boss)
            date = "{}-{} {}:{}".format(date.month, date.day, date.hour, date.minute) if date != 0 else "N/A"
        elif playerDLocation[0] < mousePos[0] < playerDLocation[0] + playerDSize[0] and \
                playerDLocation[1] < mousePos[1] < playerDLocation[1] + playerDSize[1]:
            pygame.draw.rect(gameWindow, infoRectColor, (playerDLocation[0] - 10, playerDLocation[1] - 10,
                                                         playerDSize[0] + 30, playerDSize[1] + 20), 5)
            pygame.draw.rect(gameWindow, ProgramControl.introBackgroundColor,
                             (playerDLocation[0] + playerDSize[0] + 17, playerDLocation[1] - 7, 6, playerDSize[1] + 14))
            _, score, date, time, _, normal, armed, boss = dataD
            totalDestroyed = int(normal) + int(armed) + int(boss)
            date = "{}-{} {}:{}".format(date.month, date.day, date.hour, date.minute) if date != 0 else "N/A"
        else:
            score = ""
            time = ""
            date = ""
            totalDestroyed = ""

        image = pygame.image.load("./image/musicButton.png")
        x = 1250
        y = 630
        size = (80, 80)
        gameWindow.blit(image, (x, y))
        if x < pygame.mouse.get_pos()[0] < x + size[0] and y < pygame.mouse.get_pos()[1] < y + size[1] and \
                pygame.mouse.get_pressed()[0] and changingAllowed:
            musicOn = not musicOn
            changedTime = timer
            changingAllowed = False
            if musicOn:
                pygame.mixer.music.play(loops=100)
            elif not musicOn:
                pygame.mixer.music.stop()
        if not musicOn:
            pygame.draw.line(gameWindow, (255, 0, 0), (x, y), (x + size[0], y + size[1]), 5)
        if timer - changedTime >= 30:
            changingAllowed = True

        timer += 1
        pygame.display.update()
        clock.tick(ProgramControl.frequency)


def PausedPage():
    pauseText = pygame.image.load("./image/text/pause.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return
                if event.key == pygame.K_ESCAPE:
                    GameIntroPage()

        gameWindow.fill((0, 0, 0))

        gameWindow.blit(pauseText, (310, 250))

        pygame.display.update()
        clock.tick(ProgramControl.frequency)


pygame.mixer.music.load(introBGM)  # set up the background music
pygame.mixer.music.play(loops=1000)  # play the background music
GameIntroPage()

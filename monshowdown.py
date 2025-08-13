import pgzrun
import os
import time
import random
from pgzhelper import *
                                                        
#initialize values
TILE_SIZE = 18
WIDTH = TILE_SIZE * 25
HEIGHT = TILE_SIZE * 27
ENEMY_SPEED = 3
timer = 0
numMonsters = 3
showMessage = True
gameReset = False
gamePaused = False

#theme song of the game
music.play('theme')
music.set_volume(0.5) 

##start screen logo
start = Actor('logo',pos = (222.5,240))
start.scale = 0.80

#initalize setting screen buttons
minusButton = Actor("minusbutton.png", pos = (370,160))
minusButton.scale = 0.35
plusButton = Actor("plusbutton.png", pos = (60,160))
plusButton.scale = 0.4
startButton = Actor("startbutton.png", pos = (225,417.5))
startButton.scale = 0.5
backButton = Actor("backbutton.png", pos = (75,420))
backButton.scale = 0.5
settingsknight = Actor("settingsknight.png", pos = (220,220))
settingsknight.scale = 1
settingsbar = Actor("settingsbar.png", pos = (225,50))
settingsbar.scale = 0.5
exit = Actor("exit.png", pos = (370,420))
exit.scale = 0.4

#initalize victory screen
victory = Actor("victory.png", pos = (190,340))
victory.scale = 0.8
finaltime = Actor("finaltime.png", pos = (237.5,450))
finaltime.scale = 0.5
finalchests= Actor("finalchest.png", pos = (220,400))
finalchests.scale = 0.5
restartend = Actor("restartend.png", pos = (390,345))
restartend.scale = 0.15

#initialize player actor 
player = Actor("player", anchor = (0, 0), pos = (0 * TILE_SIZE, 1 * TILE_SIZE))

#initalize enemies
enemies = []
enemy_images = ['enemy.png','enemy1.png','enemy2.png','enemy3.png','enemy4.png','enemy5.png','enemy6.png','enemy7.png','enemy8.png','enemy9.png','enemy10.png','enemy11.png','enemy12.png','enemy13.png','enemy14.png','enemy15.png']

#initialize chest actor
chest = Actor('close')
chests = []
#chest counter
chestCollect = 0

#initialize death actor; wright is used as placeholder to switch image
death = Actor("wright", anchor = (0, 0), pos = (0 * TILE_SIZE, 9 * TILE_SIZE))

#initalize cage actor
cage = Actor('cage', anchor=(0, 0), pos = (22.25 * TILE_SIZE, 24 * TILE_SIZE))
cage.scale = 0.15

#initalize coin actor and images for animation
coin = Actor('c1', anchor=(0, 0), pos=(0, 450))
coin.images = ['c1', 'c2', 'c3', 'c4','c5','c6','c7']
coin.scale = 0.05  
frame = 0

#initalize hourglass actor and images for animation
hourglass = Actor('t1', anchor=(0, 0), pos=(135, 447.5))
hourglass.images = ['t1', 't2', 't3', 't4','t5','t6','t7','t8','t9','t10']
hourglass.scale = 0.070

#initalize heart actor and images for animation
heart = Actor('h1', anchor=(0, 0), pos=(80, 457))
heart.images = ['h1', 'h2', 'h3', 'h4','h5','h6','h7','h8']
heart.scale = 1.6
lives = 1


#INDEX:     0       1     2      3        4       5      6     7     8      9       10     11     12    13    14    15    16    17    18    19    20    21     22     23
tiles = ['black','wall','wup','wright','wleft','wdown','wtl','wtr','wtdl','wtdr','bvert','bhorz','btl','btr','bbl','bbr','bb3','bb4','bb5','bb7','bb8','bb9','door','empty']


#maze of the game; each number corresponds to the index (image) above
maze = [
    [6,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,7],
    [0,0,0,0,0,10,0,0,0,0,0,0,10,0,0,0,10,0,10,0,0,0,0,0,4],
    [3,11,11,0,17,19,11,11,11,11,13,0,10,0,12,11,3,0,10,0,17,11,13,0,4],
    [3,0,0,0,0,0,0,0,0,0,10,0,10,0,10,0,10,0,10,0,0,0,10,0,4],
    [3,0,12,11,11,20,18,0,21,0,10,0,10,0,10,0,10,0,10,0,17,11,3,0,4],
    [3,0,10,0,0,10,0,0,10,0,0,0,10,0,10,0,10,0,10,0,0,0,10,0,4],
    [3,0,10,0,17,1,11,11,11,11,13,0,10,0,10,0,10,0,14,11,11,0,10,0,4],
    [3,11,3,0,0,10,0,0,0,0,10,0,10,0,10,0,0,0,0,0,0,0,10,0,4],
    [3,0,14,11,0,14,20,11,18,0,16,0,16,0,14,11,13,0,21,0,12,11,15,0,4],
    [3,0,0,0,0,0,10,0,0,0,0,0,0,0,0,0,10,0,10,0,16,0,0,0,4],
    [3,0,12,11,11,0,16,0,21,0,21,0,17,11,11,11,15,0,10,0,0,0,17,11,4],
    [3,0,10,0,0,0,0,0,10,0,10,0,0,0,0,0,0,0,10,0,21,0,0,0,4],
    [3,17,19,18,0,12,11,11,3,0,14,11,11,20,11,18,0,12,3,0,4,11,13,0,4],
    [3,0,0,0,0,10,0,0,10,0,0,0,0,10,0,0,0,4,2,11,3,0,14,11,4],
    [3,0,12,11,11,15,0,12,15,0,17,13,0,10,0,17,11,15,0,0,16,0,0,0,4],
    [3,0,16,0,0,0,0,10,0,0,0,10,0,10,0,0,0,0,21,0,0,0,21,0,4],
    [3,0,0,0,12,13,0,10,0,21,0,10,0,4,18,0,21,0,16,0,17,11,3,0,4],
    [3,11,11,11,19,15,0,10,0,10,0,10,0,10,0,0,10,0,0,0,0,0,10,0,4],
    [3,0,0,0,0,0,0,4,11,19,11,10,0,14,11,11,11,11,11,11,13,0,14,13,4],
    [3,0,12,11,13,0,12,3,0,0,0,10,0,0,0,0,0,0,0,0,10,0,0,16,14],
    [3,0,16,0,10,0,14,15,0,17,11,1,18,0,12,11,11,11,13,0,14,13,0,22],
    [3,0,0,0,10,0,0,0,0,0,0,10,0,0,10,0,0,0,10,0,0,4,13],
    [3,11,11,11,15,0,12,18,0,21,0,14,11,11,15,0,21,0,14,13,0,14,19,13,12],
    [3,0,0,0,0,0,10,0,0,10,0,0,0,0,0,0,10,0,0,10,0,0,0,10,4],
    [8,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,9,9],
    [23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23],
    [23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23],
    ]
    
    
def on_mouse_down(pos):
    '''if player clicks on a button using mouse, perform a command'''
    global numMonsters, mode, chestCollect, timer, showMessage, lives
    #if player clicks exit button in the start or settings screen, play a sound and exit the game completely
    if mode == 'start' or mode == 'settings':
        if exit.collidepoint(pos):
            sounds.select.play()
            quit()
            
    if mode == 'victory':
        #if player clicks restart button in the victory screen, switch the mode to start and reset the properties of the game
        if restartend.collidepoint(pos):
            sounds.victory.stop()
            sounds.restart.play()
            mode = 'start'
            timer = 0
            chestCollect = 0
            player.x = 0
            player.y = TILE_SIZE
            showMessage = True
            music.play('theme')
            music.set_volume(0.5)
            #if end is reached, increase lives by one
            lives += 1
            resetGame()
            
    if mode == 'settings':
        #if player clicks minus button on settings screen, decrease the number of monster spawns in game by one
        if minusButton.collidepoint(pos):
            sounds.select.play()
            numMonsters = max(0, numMonsters - 1)
        #if player clicks plus button on settings screen, increase the number of monster spawns in game by one
        elif plusButton.collidepoint(pos):
            sounds.select.play()
            numMonsters += 1
        #if player clicks back button in settings screen, go back to start screen
        elif backButton.collidepoint(pos):
            sounds.select.play()
            mode = 'start'
        #if player clicks start button in settings screen, switch mode to game and play fight sound effect
        elif startButton.collidepoint(pos):
            sounds.fight.play()
            mode = 'game'

        if mode == 'game':
            #if mode is game, decrease or increase number of monsters according to switches above
            for enemy in range(numMonsters):
                    #choose random enemy image from enemy images list
                    enemy_image = random.choice(enemy_images)
                    #anchor enemy to middle of tile and add randomized enemy image in
                    enemy = Actor(enemy_image, anchor=(0,0))
                    #randomly selects black tile and return row and column indices.
                    row, column = randomBlackTile()
                    #determines x-axis where enemy is located.
                    enemy.x = column * TILE_SIZE
                    #determines y-axis where enemy is located.
                    enemy.y = row * TILE_SIZE
                    #append enemy into enemy list
                    enemies.append(enemy)
            
                
def on_key_down(key):
    '''allows the player to move around the maze using WASD and reset the game using ENTER'''
    global mode, showMessage, timer, chestCollect, chestVisible, gameReset
    #if the player clicks space in start menu, switch Monshowdown to game mode 
    if mode == 'start':
        if key == keys.SPACE:
            mode = 'settings'
            sounds.teleport.play()
            sounds.teleport.set_volume(0.40)
    #once in game mode, perform the commands below
    elif mode == 'game':
        #calculates the row and column values of the player's current position 
        row = int(player.y / TILE_SIZE)
        column = int(player.x / TILE_SIZE)
        #if up arrow is pressed, move up one and play a walking sound effect
        if key == keys.UP:
            row = row - 1
            sounds.step.play()
        #if down arrow is pressed, move down one and play a walking sound effect
        if key == keys.DOWN:
            row = row + 1
            sounds.step.play()
        #if left arrow is pressed, move left one and play a walking sound effect
        if key == keys.LEFT:
            column = column - 1
            player.image = 'player1'
            sounds.step.play()
        #if right arrow is pressed, move right one and play a walking sound effect
        if key == keys.RIGHT:
            column = column + 1
            player.image = 'player'
            sounds.step.play()
            
        #retrieves the row and column using the values from up above
        tile = tiles[maze[row][column]]
        
        #updates the player's x and y coordinates to position them on the black tile
        if tile == 'black':  
            player.x = column * TILE_SIZE
            player.y = row * TILE_SIZE
        #if player reaches the door at the end of the maze, switch modes
        elif tile == 'door':
            sounds.door.play()
            mode = 'victory'
        #if player hits the return key when game is able to be resetted, reset the timer, player position, music and message
        if gameReset == True:
            if key == keys.RETURN:
                mode = 'start'
                timer = 0
                chestCollect = 0
                player.x = 0
                player.y = TILE_SIZE
                showMessage = True
                music.play('theme')
                music.set_volume(0.5)
                resetGame()
                
            
def isBlackTile(row, column):
    '''detects if a given position is a black tile; 0 means black tile, othewise position is not black tile'''
    if maze[row][column] == 0:
        return True
    return False


def randomBlackTile():
    '''finds random black tile position'''
    while True:
        #chooses random row and column
        row = random.randint(0, len(maze) - 1)
        column = random.randint(0, len(maze[row]) - 1)
        #if tile is black, return the row and column
        if isBlackTile(row, column):
            return row, column
        

#spawn 5 chest randomly
for chest in range(5):
    #anchor chest to middle of tile
    chest = Actor('close', anchor=(0, 0))
    #randomly selects black tile and return row and column indices.
    row, column = randomBlackTile()
    #determines x-axis where chest is located.
    chest.x = column * TILE_SIZE
    #determines y-axis where chest  is located.
    chest.y = row * TILE_SIZE
    #append chest into chest list
    chests.append(chest)


def chestOpen():
    '''switches the image of the chest if collided'''
    global chestCollect
    for chest in chests:
        if chest.collidepoint(player.x, player.y) and chest.image == 'close':
            #if player hits the chest, switch the chest image from closed to open
            chest.image = 'open'
            #add to the counter for every chest collected
            chestCollect += 1
            #play audio for every chest collected
            sounds.pickup.play()
            sounds.pickup.set_volume(0.40)
        
                    
def deathPlayer():
    '''if player collides with enemy, kill the player'''
    global lives, showMessage,gameReset, timer, gamePaused 
    for enemy in enemies:
        if enemy.collidepoint(player.x,player.y):
            #if player dies, death banner pops up saying 'you died'
            death.image = 'deathbanner'
            #teleport player to bottom right of the screen to cage upon death
            player.pos = (22.75 * TILE_SIZE, 25.75 * TILE_SIZE)
            #if player dies, stop playing music
            music.stop()
            #play monster and death sound effect when dead
            sounds.monster.play()
            sounds.playerdead.play()
            sounds.death.play()
            #reduce lives counter
            lives -= 1
            #hides current message if player dies
            showMessage = False
            #if player dies, game can be resetted
            gameReset = True
            #if player dies, game pause and freeze time
            gamePaused = True
          
            
def resetGame():
    '''allows game to replayed by resetting values'''
    global enemies, chests, death, numMonsters, gameReset, gamePaused
    #reset inital values
    chests = []
    death.image = "wright"
    player.image = "player"
    enemies.clear()
    #game is not able to be resetted 
    gameReset = False
    #game is not able to be paused 
    gamePaused = False
    #reset the positions of the chests
    for chest in range(5):
        chest = Actor('close', anchor=(0, 0))
        row, column = randomBlackTile()
        chest.x = column * TILE_SIZE
        chest.y = row * TILE_SIZE
        chests.append(chest)
        

def update():
    global timer, gamePaused
    #if mode is game, game does not pause and timer increases
    if mode == 'game' and gamePaused == False:
        timer += 1 / 60
    chestOpen()
    coin.animate()
    hourglass.animate()
    deathPlayer()
    

def draw():
    '''draws each actor and other ui elements'''

    #clears the screen and allows for new images to be drawn
    screen.clear()
    
    #if mode is victory, draw end screen
    if mode == 'victory':
        screen.blit('bg',(30,0))
        music.stop()
        sounds.victory.play()
        victory.draw()
        finaltime.draw()
        finalchests.draw()
        screen.draw.text("" + str(chestCollect), (352.5,392.5))
        screen.draw.text("" + str(round(timer, 2)), (352.5,445))
        restartend.draw()
       
    #if mode is start, draw the Monshodown and buttons
    if mode == 'start':
        start.draw()
        
    #if mode is settings, draw buttons
    elif mode == 'settings':
        screen.fill((0, 0, 0))
        minusButton.draw()
        startButton.draw()
        plusButton.draw()
        backButton.draw()
        exit.draw()
        settingsknight.draw()
        settingsbar.draw()
        screen.draw.text("" + str(numMonsters), (215, 212))
    
    
    #if mode is game, draw the maze
    elif mode == 'game':
        #returns the number of rows in the maze list
        for row in range(len(maze)):
            #returns the number of columns in the current row
            for column in range(len(maze[row])):
                #determines where to place the tile horizontally on the screen
                x = column * TILE_SIZE
                #determines where to place the tile vertically on the screen
                y = row * TILE_SIZE
                #retrieves the tile value for the current maze position from the tiles dictionary
                tile = tiles[maze[row][column]]
                #draws the tile image on to the screen
                screen.blit(tile, (x, y))

        #draws the player
        player.draw()
        
        #draw counter right next to coin symbol
        coin.draw()
        screen.draw.text("" + str(chestCollect), (40, 462.5))
        
        #draw timer rounded to two decimals going up right next to coin symbol 
        hourglass.draw()
        screen.draw.text(str(round(timer, 2)), (177.5, 462.5))
        
        #draws the cage 
        cage.draw()
        
        #draw counter right next to heart symbol
        heart.draw()
        screen.draw.text("" + str(lives), (115, 462.5))
        
        
        #if player is alive, display movement instructions, else tell player to restart using enter key
        if showMessage == True:
            alive = screen.draw.text("PRESS ARROWS TO MOVE", (235, 465), fontsize=16)
        else:
            dead = screen.draw.text("PRESS ENTER TO RESTART", (235, 465), fontsize=16)
    
        
        #draw each enemy
        for enemy in enemies:
            enemy.draw()
            
        #draw each chest
        for chest in chests:
            chest.draw()
            
        death.draw()
  
  
mode = 'start'
pgzrun.go()


"""
Title: lorbit.py
Created by: Noah Libeskind
Date: 12/12/18
"""

import pygame
import random
import time

# Importing each image for the characters and transforming them to the right size
meteor = pygame.image.load('meteor.png') 
meteor = pygame.transform.scale(meteor, (90, 100))
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (1278,720))
rocket = pygame.image.load('rocket.png')
rocket = pygame.transform.scale(rocket, (52, 67))
rocket_crash = pygame.image.load('rocket_crash.png')
rocket_crash = pygame.transform.scale(rocket_crash, (52, 67))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """ Makes a meteor """
        super().__init__() # Allows class to be accesable by other classes
        self.image = meteor # Sprite image
        self.rect = self.image.get_rect() # Set the sprite's shape to that image
        self.rect.x = x # x coordinate
        self.rect.y = y # y coordinate

    def move(self, xspeed, yspeed):
        """ Controls the movement of the meteor """
        self.rect.x += xspeed # Add speed factor to x coordinate
        self.rect.y += yspeed # Add speed factor to y coordinate

    def getX(self):
        """ Returns the x coordinate of the meteor """
        return self.rect.x 
    
    def getY(self):
        """ Returns the y coordinate of the meteor """
        return self.rect.y
         
class Spaceship(pygame.sprite.Sprite):
  
    change_x = 0
	
    def __init__(self, x, y):
        """ Makes the spaceship that you control """
        super().__init__() # Allows class to be accesable by other classes
        self.image = rocket # Sprite image
        self.rect = self.image.get_rect() # Set the sprite's shape to that image
        self.rect.x = x # x coordinate
        self.rect.y = y # y coordinate

        self.collide_rect =  pygame.rect.Rect((x, y), (15, 15)) # Special rect to make collision
        self.collide_rect.center = self.rect.center # zone smaller than the actual image borders
        
        
    def changespeed(self, x):
        """ Controls the speed adjustment to the spaceship """
        self.change_x = x
        
    def move(self, obstacles):
        """ Controls the actual movement of the spaceship """
        self.rect.x += self.change_x # Add x speed to the x coordinate
        self.collide_rect.x += self.change_x # Also move the collision rect
        
    def getX(self):
        """ Returns the x coordinate of the spaceship """
        return self.rect.x

    def getY(self):
        """ Returns the y coordinate of the spaceship """
        return self.rect.y
      
    def crashed(self, x, y):
        """ Rocket crash image"""
        self.image = rocket_crash
        self.rect = self.image.get_rect()
        self.rect.x = x # x coordinate
        self.rect.y = y # y coordinate
 
class Space(object):
    def __init__(self):
        """ Makes all the meteors in the space field """
        super().__init__() # Allows class to be accesable by other classes
        self.obstacle_list = pygame.sprite.Group() # Creates an empty sprite list of all the meteors
        obstacle_list = [[-400, 10], [-400, 10], [-400, 10], [-400, 10], [-400, 10], [-400, 10]] 
        for aspect in obstacle_list: # Runs through the list of meteor parameters
            obstacle = Obstacle(aspect[0], aspect[1]) # Makes each meteor
            self.obstacle_list.add(obstacle) # Adds the meteors to the sprite list

    def getobstacle(self):
        """ Returns the list of all the meteors """
        return self.obstacle_list
    
def main():
    """ Controls the actual game """
    pygame.init() # Allows built in pygame functions to be read
    screen = pygame.display.set_mode([800,600]) # Screen display dimensions
    pygame.display.set_caption('Lorbit') # Title of the game
    clock = pygame.time.Clock() # Built in timing function
    start_time = pygame.time.get_ticks() # Starting time in milliseconds
    player = Spaceship(400,460) # Creates the spaceship
    space = Space() # Creates space with all the meteors
    space = space.getobstacle() # Retrieves list of meteors
    sprites = pygame.sprite.Group() # Makes list for all sprites
    sprites.add(player) 
    for obstacle in space: 
        sprites.add(obstacle)
    text = open(str('highscore.txt'), 'r') # Highscore system
    hs = text.read() 
    text.close()
    newhs = hs
    challenge = 1 # Challenge factor
    over = False # State of game
    while not over:  
        clock.tick(60) # Run the clock at normal speed
        challenge *= 1.001 # Increase challenge factor slightly for each new frame
        player.rect.clamp_ip(screen.get_rect()) # Keeps the craft from going off the screen
        player.move(space) # Enables player movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # End game if you quit
                over = True
            # Control movement with arrow keys    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-10)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(10)
            if event.type == pygame.KEYUP: 
                player.changespeed(0)
        for obstacle in space: # Runs the following for each meteor
            if obstacle.rect.colliderect(player.collide_rect): # Check for collision
                player.crashed(player.rect.x, player.rect.y)
                over = True # Game over           
            if obstacle.getY() > 600: # When meteor goes below the page
                obstacle.rect.y = random.randint(-3000,-50) # Make meteors start at different heights
                obstacle.rect.x = random.randint(30,750) #Choose different positions to come down the page
            else: # Normal meteor behavior
                obstacle.move(0, challenge*random.randint(5,8)) # No x velocity, y veloctiy randomized
        font = pygame.font.SysFont("Sans", 20) # Message font
        # Highscore function
        if int(hs) <= (pygame.time.get_ticks() - start_time):
            newhs = str(pygame.time.get_ticks() - start_time)
            score = 'Score: ' + newhs + '   Highscore: ' + newhs
        else:
            score = 'Score: ' + str(pygame.time.get_ticks() - start_time) + '   Highscore: ' + newhs
        screen.blit(background, (0,0)) # Backdrop
        screen.blit(font.render(score, True, (255,255,255)), (20, 20)) # Score message
        sprites.draw(screen) # Display sprites
        pygame.display.flip() # Update screen
    time.sleep(5) # Wait 5 sec before closing window
    pygame.quit() # Quit
    # Write in new highscore
    text = open(str('highscore.txt'), 'w')
    text.write(newhs)
    text.close()
    
main()
    











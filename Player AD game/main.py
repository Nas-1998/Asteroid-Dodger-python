import pygame
import os
import os.path
import time
import random
pygame.init()

#Some variables below

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
VEL = 5
WIDTH, HEIGHT = 750, 750

# These are images i have for the player and for the obstacles
Sprite_Image = pygame.image.load(os.path.join("Player_Ship.png"))
Obstacle_Image = pygame.image.load(os.path.join("obstacle.png"))

# this part is supposed to be opening and reading the file i want adn to create it if it doesnt exist


# Just some font
FONT = pygame.font.SysFont("comicsans", 30)

# This is for the window 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")
 
# I created a class here for the player 
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = Sprite_Image 
        self.mask = pygame.mask.from_surface(self.sprite) # this assigns the image to the player
    
    def draw(self, win): #This function is to draw the player on to the screen
        win.blit(self.sprite, (self.x, self.y))
        
    def get_width(self):
        return self.sprite.get_width()



class Obstacles: #This class is for the obstacles similar to the player
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = Obstacle_Image 
        self.mask = pygame.mask.from_surface(self.sprite)

    def move(self, vel): #obstacles can only move in the y direction
        self.y += vel

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def get_width(self): #This is to get the width of the player
        return self.sprite.get_width()
    
    def get_height(self):
        return self.sprite.get_height()


def collide(obj1, obj2): #This is a function to be used when checking if two objects collide with each other
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None #If two masks overlap then the collision is true

def main_menu():#This crates a main menu at the begining 
    title_font = pygame.font.SysFont("comicsans", 30)
    run = True
    while run: 
        WIN.fill(BLACK) 
        title_label = title_font.render("Press the mouse to start", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: #When you press down on the mouse its suppsoed to launch main
                main()
    pygame.quit()

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        # You can add other pause-related functionality here, such as displaying a pause menu or message
        pygame.display.update()

def main(): 
    run = True
    FPS = 60
    Score = 0
    file_path = "highscore.txt"
    HighScore = 0 # Set a default value for HighScore
    
    if os.path.isfile(file_path): # Check if the file exists
        with open(file_path, "r") as file:
            contents = file.read().strip() # Remove any leading/trailing white spaces

            if contents.isdigit(): # Check if the contents are digits only
                HighScore = int(contents)
            else:
                print("Error: The contents of the file are not valid integers.")
                # Handle the error as needed
    else:
        print(f"The file '{file_path}' does not exist. Using default value for HighScore.")
        

    Chosen = Player(300, 650) #This is the player we spawn them in this location
    clock = pygame.time.Clock()
    lost_font = pygame.font.SysFont("comicsans", 60)
 
    obstacles = [] #This creates a list for the obstacles

    def draw(): #Here we start drawing everything on to the screen 
        WIN.fill(BLACK) 
        Score_label = FONT.render(f"SCORE: {Score}", 1, (255, 255, 255)) # This gets the score 
        High_score_label = FONT.render(f"HIGH SCORE: {HighScore}", 1, (255, 255, 255))#This gets the Highscore 

        WIN.blit(Score_label, (10, 10)) #This puts the score value on the screen adn the one below does the Highscore
        WIN.blit(High_score_label, (WIDTH - High_score_label.get_width() - 10, 10))
        
        for obstacle in obstacles: #This draws the obstacle 
            obstacle.draw(WIN)

        Chosen.draw(WIN) #This draws the player

        pygame.display.update()
    
    obstacle_timer = 0  # variable to track time elapsed since last obstacle added
    alive = True

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # add new obstacle if enough time has elapsed
        if alive:
            obstacle_timer += clock.get_time() / 1000  # convert milliseconds to seconds
            if obstacle_timer > 1:
                obstacle = Obstacles(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))
                obstacles.append(obstacle)
                obstacle_timer = 0
        
        draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # set run variable to False to exit loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()  # pause the game if user presses ESC key
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and Chosen.x - VEL + Chosen.get_width() < WIDTH:
            Chosen.x += VEL
        if keys[pygame.K_LEFT] and Chosen.x + VEL > 0:
            Chosen.x -= VEL
        
        for obstacle in obstacles[:]:
            obstacle.move(VEL)
            if obstacle.y + obstacle.get_height() > HEIGHT:
                Score += 1
                obstacles.remove(obstacle)

            # check for collision with player
            if alive and collide(obstacle, Chosen):
                obstacles.remove(obstacle)
                #alive = False
        
        if not alive:
            # write high score to file if it's a new record
            if Score > HighScore:
                with open("highscore.txt", "w") as f:
                    f.write(str(Score))
                HighScore = Score
            
            # display game over screen with score and high score
            WIN.fill(BLACK)
            High_score_label = FONT.render(f"HIGH SCORE: {HighScore}", 1, (255, 255, 255))
            WIN.blit(High_score_label, (WIDTH - High_score_label.get_width() - 10, 10))
            Score_label = FONT.render(f"SCORE: {Score}", 1, (255, 255, 255))
            WIN.blit(Score_label, (10, 10))
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            pygame.display.update()
            pygame.time.delay(2000)  # pause for 2 seconds before restarting game

            obstacles.clear()
            Score = 0
            obstacle_timer = 0  # reset timer for adding obstacles
    pygame.quit()
    
if __name__ == '__main__':
    main()
    

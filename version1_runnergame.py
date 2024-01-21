# ABOUT THIS VERSION:
    # 1 Player, walking in a steady pace
    # 2 obstacles: train with noel carriage and black trousers
    # Score: calculated in terms of the number of presents that got to be delivered

import pygame
from sys import exit # there are many ways to exit from the while loop such as break command. however the most secure way is to use built in sys functions
from random import randint, choice

class Player(pygame.sprite.Sprite): # you will add all your specifications regarding the player to this sprite, then ad it to the group and then draw it in the game bit. It will make the code cleaner
    # declaring methods (in def parts)
    def __init__(self): # the things we want to access outside of the player methods we need 'self' in the varibale definition. self should be thought as whatever name you will be giving to the group (assigning)
        super().__init__()
         
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1_new.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2_new.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump_new.png').convert_alpha()
        
        #self.image = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom =(80,300))
        # pygame doesnot draw sprites automatically. Create sprite > place sprites in Group or GroupSingle > draw/update all sprites in that group
        # pygame has different kinds of groups. Group: a group for mulitple sprites (flies and snails). Groupsingle: A group with a single sprite (our player) self contained. we need them in different groups so that we can check for collision.
        self.gravity = 0 # to be used in another function in the same class
        
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.4)
        
    def player_input(self): # originally this bit was in the event loop to collect the player input. Now we are creating a function for it in the sprite class by changing the 'player' in the original bit by 'self'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            
    def apply_gravity(self): # originally this bit was in the game loop but we are creating a function for this
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        # originally in this bit we used def and global methods but we dont need to use it anymore since we have self now
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
            
    def update(self): # instead of calling each method individually in the game bit we are creating this update method and put all the methods we created in it and then we will call it to update our player in the game bit
        self.player_input()
        self.apply_gravity()
        self.animation_state()
            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type): # we need type argument too this time because there is more than one variable in this class
        super().__init__()
    
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/pants1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/pants2.png').convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/snail/train1.png').convert_alpha()
            snail_frame_1 = pygame.transform.rotozoom(snail_frame_1,0,1.25)
            snail_frame_2 = pygame.image.load('graphics/snail/train2.png').convert_alpha()
            snail_frame_2 = pygame.transform.rotozoom(snail_frame_2,0,1.25)
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos = 300
      
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
        
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
        
    def destroy(self):
        if self.rect.x <= -100:
           self.kill() # to destroy the obstacles that are outside of the screen
        
def display_score():
    global current_time
    current_time = int((pygame.time.get_ticks()-start_time)/1000) # will give our time in miliseconds NOW
    time_surface = test_font.render(f'# of Presents: {current_time}',False,(64,64,64)) #to make it a string
    time_rect = time_surface.get_rect(center = (400,50))
    screen.blit(time_surface,time_rect)
    return current_time 

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False): # if true the obstacle will be deleted
        obstacle_group.empty() # to prevent them from spawning in the same place in the comeback
        return False
    else: return True

pygame.init() # this has to be run before any other pygame code. Essentially starts pygame and initiates all the subparts of pygame.

width = 800 #width of the game window that will be created
height = 400 #height of the game window that will be created
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Runner') # give a name to the screen, you could also change the icon if you care so much
clock = pygame.time.Clock()
fps_intended=60 # if you make it bigger the objects will appear to move faster etc
fonttype = 'font/Pixeltype.ttf'
test_font = pygame.font.Font(fonttype,50) # second argument is font size
text_color = (64,64,64)
box_color = '#c0e8ec'
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/daydream.mp3')
bg_music.play(loops = -1) # loop forever


# Groups
#player = Player() # creating an instance of this class. If I do that only the game will run as it is but it is not actually activating the sprite.
player = pygame.sprite.GroupSingle() # this way we are going to create a group, the group will contain the sprite and this way we will be able to access it.
player.add(Player())

obstacle_group = pygame.sprite.Group() # we can not add all of it right away. we have to add it when the time ticks happen.

sky_surface = pygame.image.load('graphics/sky_pink.png').convert() #anytime you import an image you kep it in a separate surface
ground_surface = pygame.image.load('graphics/GroundOrange.png').convert()

score_surface = test_font.render('SCORE',False,text_color)
score_rect = score_surface.get_rect(center = (400,50))

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand_new.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,1.6)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('RUNNER',False,(255,172,176))
game_name_rect=game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(255,172,176))
game_message_rect = game_message.get_rect(center = (400,330))

#Timer
obstacle_timer = pygame.USEREVENT + 1 # there are events reserved for pygame itself. to avoid conflict with those we always need to include that plus 1
pygame.time.set_timer(obstacle_timer,2400) # which event you want to trigger and how often


while True:
    
        for event in pygame.event.get():
                
          if event.type == pygame.QUIT: # if the event is an event that means to close in the documentation
            pygame.quit()
            exit()
                        
                  
          if game_active:
            if event.type == obstacle_timer: 
                    obstacle_group.add(Obstacle(choice(['fly','snail','snail','fly']))) # choice will choose one of these four items so 24 percent chance to get a fly
         
          else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				           game_active = True
				           start_time = int(pygame.time.get_ticks())
           
        if game_active:    
            
            
            screen.blit(sky_surface,(0,0)) # the coordinates of x and y starting from the left upper corner
            screen.blit(ground_surface,(0,300)) #replacement to the coordinates is necessary
            score = display_score() # this way we can access the value of our score anytime
    
            player.draw(screen) # to draw the player sprite within the group. If not it will not be drawn automatically
            player.update() # sprite groups in pygame have two main functions. 1: is to draw 2: update. here we are using those to call all the methods we created for our player sprite. instead of caling each method individually (jump etc) we are defining a new func update. This will be used to run the all of the other code in the player sprite
        
            obstacle_group.draw(screen)
            obstacle_group.update()
            
            game_active = collision_sprite()
            
            
        
        else: # game is not active
            screen.fill((246,223,233))
            screen.blit(player_stand,player_stand_rect)
            
            score_message = test_font.render(f'# of Presents Delivered: {score}',False,(255,172,176))
            score_message_rect = score_message.get_rect(center = (400,300))
            screen.blit(game_name,game_name_rect)
            if score == 0:
               screen.blit(game_message,game_message_rect)
            else:
               screen.blit(score_message,score_message_rect)
               
            
    
        # update everything
        pygame.display.update() 

        clock.tick(fps_intended) 
    
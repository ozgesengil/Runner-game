import pygame
from sys import exit # there are many ways to exit from the while loop such as break command. however the most secure way is to use built in sys functions
from random import randint 

# displaying the score (time alive in the game). pygame.time.get_ticks() gives the miliseconds since the game started technically since we called pygame.init()
# we need to update score on every frame, put that on a surface, and display that surface
def display_score():
    #global current_time #to make the variable accessible from everywhere to use it in the score show
    current_time = int((pygame.time.get_ticks()-start_time)/1000) # will give our time in miliseconds NOW
    time_surface = test_font.render(f'Score: {current_time}',False,(64,64,64)) #to make it a string
    time_rect = time_surface.get_rect(center = (400,50))
    screen.blit(time_surface,time_rect)
    return current_time #to use it in the score show

def obstacle_movement(obstacle_list):
    
    if obstacle_list: # if our list is empty this if statement is not going to run in python
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5 # every single obstacle in the list will be moved to a little bit of left in every cycle of our game.
            
            if obstacle_rect.bottom == 300: screen.blit(snail_surface,obstacle_rect)
            else: screen.blit(fly_surface,obstacle_rect)
            
            #screen.blit(snail_surface,obstacle_rect) # then we draw the surface in the same position
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # we will only include an item in the list if x is greater than zero. that way if the obstacle is not in the screen the obstacle will be deleted from the list 
        
        return obstacle_list # to make the list variable in the function above a global one if not it will stay as local
    else: return []
    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surface,player_index
    
    if player_rect.bottom < 300: # jump
        player_surface = player_jump
    else:
        player_index += 0.1 # you want to increase it bit by bit to not make the walk too fast
        if player_index >= len(player_walk):player_index=0 # to make sure it only takes thevalues 0 and 1
        player_surface = player_walk[int(player_index)]
    # play walking animation if the player is on floor
    # display the jump surface when player is not on floor

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
game_active = True
start_time = 0
score = 0

#test_surface = pygame.Surface((100,200)) # wi and height
#test_surface.fill('Red')
#displaying the images across framerates you can notice the images are not deleted from the display just displayed on top of each other in each frame. so be careful with small surfaces. Draw a proper background!!!!
#sky_surface = pygame.image.load('graphics/Sky.png') #anytime you import an image you kep it in a separate surface
#ground_surface = pygame.image.load('graphics/ground.png')
#text_surface = test_font.render('RUNNER',False,'Black') # 3 args here the text you want to display whether or nor to smoosh the edges of the text (if your text is not pixel art always say True for such projects) and the font color
# you can convert the images from png to a format that python can handle FASTER after importing them so add this line everytime after iöportant images
sky_surface = pygame.image.load('graphics/Sky.png').convert() #anytime you import an image you kep it in a separate surface
ground_surface = pygame.image.load('graphics/ground.png').convert()

#text_surface = test_font.render('RUNNER',False,'Black') # 3 args here the text you want to display whether or nor to smoosh the edges of the text (if your text is not pixel art always say True for such projects) and the font color
score_surface = test_font.render('SCORE',False,text_color)
score_rect = score_surface.get_rect(center = (400,50))

# OBSTACLES
#snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #the image had black and white outliners so convert it by respecting alpha values
#snail_x_pos = 600 # to allow us to change the position we assigned an object to it
# update the snail by using a rectangle
#snail_rect = snail_surface.get_rect(midbottom = (700,300))

#fly_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

#Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index=0
snail_surface = snail_frames[snail_frame_index]
#Fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []



# RECTANGLES you kind of split your image variable into two and manage them together to control the position from other points too beside the top left corner. (use of rectangles) SPRITE CLASS
#player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
#player_rect = player_surface.get_rect(midbottom = (80,300)) # will create a rectangle that is the size of the image and then choose its positioning in the display. You can use midleft, center etc to adjust positioning
# you can crate a SPRITE class and not deal with two separate variables (rectangels and surfaces)

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))

# RECTANGLES are also good to control collisions. rect1.colliderect(rect2)
# different types of collisions to check for. i.e. rect1.collidepoint((x,y)) -- checks if one point collides with the rectangle. If you have mouse clicks for something it will be so imp but we are not going to use it that much. 
# how to get the mouse position then? (to check for collisions etc) 2 ways: pygame.mouse or event loop. both basically do the same thing
# another func of rect is that it can be used to draw.

# for the player character we need to collect keyboard input and a jump+gravity mechanic. to do these we need some kind of floor. these three are independent of each other.
# keyboard input can be get by pygame.key and event loop just like mouse input.
# so you can collect input in the game itself or in the event loop. When using classes you want the controls inside of the relevant class. pygame.mouse or pygame.keys are great for that (within the game). For more general stuff like closing the game, the event loop is the ideal place.

# pygame.draw can be used to draw things

# in jumping mechanic we also need gravity. in reality the gravity is exponential. We need to imitate that or replicate it.
# will first create a variable of gravity that just increases constantly and then add this to our player's y axis so it will look like it is falling faster and faster.
# gravity += somevalue, and player.y += gravity. Not exponential but somehow similar.
player_gravity = 0
# creatin the floor: check the collision between player and floor. move player up if collision occurs. BUT we dont need a complex set up like that
# for creating the floor all we really need is to check the y position of the player
# something like if player bottom > 300 : player bottom = 300

#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
#player_stand = pygame.transform.scale2x(player_stand) #scaled as 2x bigger
#rotozoom:scales,rotates,filters, makes it a little bit smoother
player_stand = pygame.transform.rotozoom(player_stand,0,4)
player_stand_rect = player_stand.get_rect(center = (400,200))
game_name = test_font.render('RUNNER',False,(111,196,169))
game_name_rect=game_name.get_rect(center = (400,80))


game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))


# game over state. collision mech is ok. but we can have a game over state and start over the game.
# this brings us to state management in pygame.
# we had our current game. all we need to do if game_active: current game, else (collision): game_ over kind of if statement.

# transforming surfaces is important. rotate flip etc. 

# TIMER
#better enemy logic. TIMERS. we create a custom user event that is triggered in certain time intervals.
#we are saying pygame to use timers to create custom user events.
#to do that first create a custom user event. then tell pygame to trigger that event continously. and add code in the event loop.
obstacle_timer = pygame.USEREVENT + 1 # there are events reserved for pygame itself. to avoid conflict with those we always need to include that plus 1
pygame.time.set_timer(obstacle_timer,1600) # which event you want to trigger and how often
# so we create a list of obstacles. and everytime the timer triggers we add a new rectangle to that list. Then we move every rectangle in that list to the left on every frame. We delete rectangles too far left

# for PLAYER ANIMATION: we create our own timer that updates the surface
# for ostacle animation: we rely on the inbuild timers to update all obstacle surfaces
# for obstacle animation: we will use an inbuild timer (like the ones we used to spawn the obstacles). evereytime it triggers we update all the surfaces for all flies or all snails (each have their own timer)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,500)

while True:
    
        for event in pygame.event.get():
          if event.type == pygame.QUIT: # if the event is an event that means to close in the documentation
            pygame.quit()
            exit()
          #if event.type == pygame.MOUSEMOTION: # mouse position can be recorded as another type of event
            #print(event.pos) # you can see the mouse position in coordinates printed 
           #if player_rect.collidepoint(event.pos):
               #print('mouse and player collision')
               #if event.type == pygame.MOUSEBUTTONDOWN: # not that efficient check for collision first and then mouse button press
                   #player_gravity = -20
          #if event.type == pygame.MOUSEBUTTONUP: # if mouse button is pressed at the moment give me heads up
            #print('mouse up')
            
          #if event.type == pygame.KEYUP:
            #print('key up')
            
          # if stays like that you can jump in the air too
          #if event.type == pygame.MOUSEBUTTONDOWN: # if mouse button is pressed at the moment give me heads up
            #print('mouse down')
            #if player_rect.collidepoint(event.pos):
                #player_gravity = -20   
          #if event.type == pygame.KEYDOWN: # to check if any key is down
            #print('key up')
            #if event.key == pygame.K_SPACE: #to check if a specific key is down
               #print('jump')
               #player_gravity = -20 # if spacebar is pressed, start the gravity from minus so that it will jump first and then fall
          if game_active:
              # to avoid jumping in the air mech
              if event.type == pygame.MOUSEBUTTONDOWN: 
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                   player_gravity = -20   
              if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300: #to check if a specific key is down
                   player_gravity = -20 
          else:
              if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                  game_active = True # in theory it is ok. but now the snail is in the same posiiton as player and collision happens in the first frame. will work on that
                  #snail_rect.right = 800 
                  start_time = pygame.time.get_ticks()
                  
          if game_active:
              if event.type == obstacle_timer: 
                    if randint(0,2):
                      obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                    else:
                      obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),210)))
         
              if event.type == snail_animation_timer:
                    if snail_frame_index ==0: snail_frame_index = 1
                    else: snail_frame_index = 0
                    snail_surface = snail_frames[snail_frame_index]
                    
              if event.type == fly_animation_timer:
                    if fly_frame_index == 0: fly_frame_index == 1
                    else: fly_frame_index == 0
                    fly_surface = fly_frames[fly_frame_index]
           
        if game_active:          
            # draw all our elements
            #screen.blit(test_surface,(100,200))
            screen.blit(sky_surface,(0,0)) # the coordinates of x and y starting from the left upper corner
            #the order you draw things on toop of each other matters
            screen.blit(ground_surface,(0,300)) #replacement to the coordinates is necessary
            #to create text first create a font (style and text size) then write text on a surface and then blit the text surface
            #screen.blit(text_surface,(300,50))
            #each surface is put in position in each frame. animating each surface would mean to change their position in every frame
    
            #pygame.draw.rect(screen,box_color,score_rect,10) #with border of 10
            #pygame.draw.rect(screen,box_color,score_rect)
            #pygame.draw.line(sky_surface,'Pink',(0,0),(800,0),10)
            #pygame.draw.line(screen,'Gold',(0,0),pygame.mouse.get_pos(),10) # !!!! you can use this one in final game dynamic to interact with player!!!!
            #pygame.draw.ellipse(screen,'Brown',pygame.Rect(50,200,100,100))
            #screen.blit(score_surface,score_rect)
            score = display_score() # this way we can access the value of our score anytime
    
            #screen.blit(snail_surface,(snail_x_pos,250)) # used this line before using rectangle
            #snail_x_pos -= 4 #everytime the frame is renewed our snail will move to the right a bit. if you want this to move left -=
            #if snail_x_pos < -100: snail_x_pos = 800
            
            #this bit wont be needed when new enemy logic is introduced
            #snail_rect.x -= 4
            #if snail_rect.right < 0: snail_rect.left = 800
            #screen.blit(snail_surface,snail_rect)
    
            #PLAYER
            player_gravity += 1
            player_rect.y += player_gravity
            #print(player_rect.left) # measure the left of the player in the command window, this info could be helpful to measure things. 
            #player_rect.left += 1 # move the left of the player to right (MOVE THE PLAYER to the right)
            #screen.blit(player_surface,(80,200)) #now we can use rectangel and position accordingly so we dont need to use it like that
            if player_rect.bottom >= 300: player_rect.bottom = 300 #creating the floor illusion
            player_animation()
            screen.blit(player_surface,player_rect)
    
            #if player_rect.colliderect(snail_rect) # will give either 1 or 0 if there is a collision or not. And that info we can use in an if statement. by printing this line by adding print you can see for yourself if there is a collision form time to time or not
            #print('collision') # you can use this info to end the game for example as a dying mechanism etc
        
            # check if our mouse is colliding with the player. During the game if mouse collides with the player it wil print collision
            #mouse_pos = pygame.mouse.get_pos()
            #if player_rect.collidepoint(mouse_pos):
                #print('collision')
                #print(pygame.mouse.get_pressed()) # boolean press value for each of my mouse buttons. which mouse button I am pressing will be true and others will be false out of the three buttons
    
            #keys = pygame.key.get_pressed() # all the keys list whether they wer epressed or not
            #if keys[pygame.K_SPACE]:print('jump') # check for a specific input
    
            # OBSTACLE MOVEMENT
            obstacle_rect_list = obstacle_movement(obstacle_rect_list)
    
            
            # collision
            #if snail_rect.colliderect(player_rect):
                #to end it all including the window
                #pygame.quit()
                #exit()
                #game_active = False # if no else statement is created then nothing gets to updated anymore and the game freezes there in the collision.
            game_active = collisions(player_rect,obstacle_rect_list)
        
        else: # game is not active
            screen.fill((94,129,162))
            screen.blit(player_stand,player_stand_rect)
            obstacle_rect_list.clear()
            player_rect.midbottom = (80,300)
            player_gravity = 0
            
            score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
            score_message_rect = score_message.get_rect(center = (400,300))
            screen.blit(game_name,game_name_rect)
            if score == 0:
               screen.blit(game_message,game_message_rect)
            else:
               screen.blit(score_message,score_message_rect)
               
            
            
            
            
            
            # !!!!CHECK HERE LATER TO SEE IF IT WORKS
            #for event in pygame.event.get():
                #if event.type == pygame.MOUSEBUTTONDOWN:
                    #game_active = True
            #if pygame.MOUSEBUTTONDOWN: game_active = True
             
            
            
        # update everything
        pygame.display.update() # we want to display everything we are doing inside this loop to the screeni you only need to call it at the beginning

# controlling the framerate or how fast the game will go is soo important. A perfectly constant framerate is ideal.
# for this game we will keep it contant at 60 fps (frame per second). you need to come up with ceiling and floor values. ceiling is easy because you can tell computer to wait in between the frames so go slower. floor is tricky. really hard to get a computer run faster. you need to change the game to ensure it runs well.
    
        clock.tick(fps_intended) # telling the pygame that the while loop should not run faster than 60 fps so update it every 17 miliseconds.
    
#essentially 2 different type of surfaces here. 1 the display surface. 2 any regular surface to display there such as single colors rendered texts or something important


import pygame
from registries.colors import *
import registries.animations
import registries.elements
import registries.buttons
import registries.gui
import registries.item

#pygame initialization
pygame.init()
gameStarted = False
class Player:
    #Initial Player attribute assignment
    def __init__(currentImage):
        Player.defaultSpeed = 11
        Player.jumpsound = pygame.mixer.Sound("src/main/assets/sounds/jump.wav")
        Player.jumpsound.set_volume(0.25)
        Player.deathSound = pygame.mixer.Sound("src\main/assets\sounds\death.mp3")
        Player.deathSound.set_volume(0.25)
        Player.hurtSound = pygame.mixer.Sound("src\main/assets\sounds\hurt.mp3")
        Player.hurtSound.set_volume(0.25)
        Player.speed = Player.defaultSpeed
        Player.jumpvar = 16 #Important for jumping calculation
        Player.facingRight = True
        Player.facingLeft = False
        Player.standing = True
        Player.jumping = False
        Player.walking = False
        Player.collidingLeft = False
        Player.collidingRight = False
        Player.rect = pygame.Rect((800, 562),(100, 200)) # Create the players hitbox
        Player.animationFrameUpdate = 1
        Player.debuggingMode = False
        Player.visible = True
        Player.movementLocked = False
        Player.locked = False
        Player.debuggingMenu = False
        Player.flying = 0
        Player.colliding = 0
        Player.defaultHealth = 6 #most of the time it's 6
        Player.health = Player.defaultHealth
        Player.dead = False
        Player.playedDeathSound = False
        Player.chatOpen = False

    def keybinds(self,camera_pos):
        global player_x
        global player_y
        self.doorhandling = 0 #Door mechanics
        player_x = self.rect.x #Camera following the player
        player_y = self.rect.y

        player_x, player_y = camera_pos #Assign variables to the camera position

        key = pygame.key.get_pressed() #Receive keyboard input
        if key[pygame.K_UP] and Player.jumpvar == 16 and Player.visible == True and Player.movementLocked == False and Player.locked == False: #Jumping
            Player.jumpvar = -14.3
        elif key[pygame.K_SPACE] and Player.jumpvar == 16 and Player.visible == True and Player.movementLocked == False and Player.locked == False: #Alternative jumping keybind
            Player.jumpvar = -14.3

        if Player.jumpvar == -14.3: #Play jump sound when the player jumps
            pygame.mixer.Sound.play(Player.jumpsound)

        if Player.jumpvar <= 15: #Jumping movement
            n = -1
            if Player.jumpvar < 0:
                n = 1
            Player.rect.y -= (Player.jumpvar**2)*0.17*n
            Player.jumping = True
            Player.jumpvar += 1
        else:
            Player.jumpvar = 16
            Player.jumping = False

        if key[pygame.K_RIGHT] and Player.visible == True and Player.collidingRight == True and Player.movementLocked == False and Player.movementLocked == False and Player.locked == False: #Player walking
            Player.facingLeft = False
            Player.facingRight = True
        elif key[pygame.K_RIGHT] and Player.collidingRight == False and Player.movementLocked == False and Player.locked == False:
            Player.facingLeft = False
            Player.facingRight = True
            Player.standing = False
            self.rect.x += Player.speed
        else:
            Player.standing = True
            Player.walking = False

        if key[pygame.K_LEFT] and Player.visible == True and Player.collidingLeft == True and Player.movementLocked == False and Player.locked == False: #Player walking
            Player.facingLeft = True
            Player.facingRight = False
        elif key[pygame.K_LEFT] and Player.collidingLeft == False and Player.movementLocked == False and Player.collidingLeft == False and Player.locked == False:
            Player.facingLeft = True
            Player.facingRight = False
            Player.standing = False
            self.rect.x -= Player.speed
        else:
            Player.standing = True
            Player.walking = False

        if Player.collidingLeft == True:
            print("colliding left")
        if Player.collidingRight == True:
            print("colliding right")

        #Debug mode to help developers
        if key[pygame.K_d] and Player.debuggingMode == False and Player.locked == False:
            pygame.time.wait(200)
            Player.debuggingMode = True
        elif key[pygame.K_d] and Player.debuggingMode == True and Player.debuggingMenu == False and Player.locked == False:
            pygame.time.wait(200)
            Player.debuggingMode = False
        
        #The chat    
        if key[pygame.K_c] and Player.chatOpen == False and Player.debuggingMenu == False:
            pygame.time.wait(200)
            Player.chatOpen = True
            
        elif key[pygame.K_ESCAPE] and Player.chatOpen == True:
            pygame.time.wait(200)
            Player.chatOpen = False

        if key[pygame.K_0] and Player.debuggingMode == True and Player.debuggingMenu == False and Player.locked == False:
            pygame.time.wait(200)
            Player.movementLocked = True
            Player.debuggingMenu = True
        elif key[pygame.K_0] or key[pygame.K_ESCAPE] and Player.debuggingMode == True and Player.locked == False:
            pygame.time.wait(200)
            Player.movementLocked = False
            Player.debuggingMenu = False

        if key[pygame.K_DOWN] and Player.visible == True and Player.debuggingMode == True and Player.movementLocked == False and Player.flying == 1 and Player.locked == False:
            Player.standing = False
            Player.facingLeft = False
            Player.facingRight = True
            self.rect.y += Player.speed 
        else:
            Player.standing = True
            Player.walking = False
            
        if key[pygame.K_u] and Player.visible == True and Player.debuggingMode == True and Player.movementLocked == False and Player.flying == 1 and Player.locked == False:
            Player.standing = False
            Player.facingLeft = False
            Player.facingRight = True
            self.rect.y -= Player.speed 
        else:
            Player.standing = True
            Player.walking = False
    
    #End of debugging mode functions

        if key[pygame.K_LEFT] and Player.visible == True and Player.movementLocked == False and Player.locked == False or key[pygame.K_RIGHT] and Player.visible == True  and Player.movementLocked == False and Player.locked == False: #Walking animations
            Player.walking = True

        if Player.walking == True and key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT] and Player.locked == False: #Sprinting
            Player.speed = 18
            Player.countUp = 2
        else:
            Player.speed = Player.defaultSpeed

        return (-self.rect.x + 680, -self.rect.y + 450) # Return new player position
    
    def render(self,screen): #Player and player hitbox rendering
        if Player.visible == True:
            Player.currentSprite = pygame.transform.scale(Player.currentSprite,(32 * 8,32 * 8))
            screen.blit(self.currentSprite,(self.rect.x - 75,self.rect.y-50)) #Drawing the player to the screen
            if Player.debuggingMode == True:
                pygame.draw.rect(screen, (0, 255, 0), Player.rect, 4) #Drawing the hitbox to the screen

    def renderDebugMenu(self):
        if Player.debuggingMenu == True:
            pygame.draw.rect(screen, BLUISH_GRAY, debug_menu, 10000)
            if toggleAdvMove.drawToggle(screen):
                if Player.flying > 1:
                    Player.flying = 0
                Player.flying += 1
                if Player.flying == 1:
                    print("selected")
                if Player.flying == 2:
                    print("not selected") 
            screen.blit(toggleAdvMoveText, (100, 135))
            if damage.draw(screen, -35, -7.5):
                print("button pressed")
                if Player.health > 0:
                    Player.health -= 1
                    if Player.health > 0.5:
                        pygame.mixer.Sound.play(Player.hurtSound)
            if heal.draw(screen, -60, -7.5):
                print("pressed other button")
                if Player.health < Player.defaultHealth:
                    Player.health += 1
            if toggleCollisions.drawToggle(screen):
                if Player.colliding > 1:
                    Player.colliding = 0
                Player.colliding += 1
                if Player.colliding == 1:
                    print("selected")
                if Player.colliding == 2:
                    print("not selected") 
            screen.blit(toggleCollisionsText, (80, 235))

    def collisions(self):
        #Wall collisions, do not delete!!!!
        if Player.rect.x < 700:
            Player.collidingLeft = True
        else:
            Player.collidingLeft = False
    


#Loading element textures
placeholder = registries.elements.registerElements("environment/blocks/cobble", 5)
wooden_sign = registries.elements.registerElements("environment/blocks/wooden_sign", 5)
tree_stump = registries.elements.registerElements("environment/blocks/tree_stump", 5)
placeholder3 = registries.elements.registerElements("environment/blocks/cobble", 5)

grassElement = pygame.image.load("src\main/assets/textures\elements\Environment/blocks\grass_dirt.png")
grassElementScaled = pygame.transform.scale(grassElement, (grassElement.get_width() * 3, grassElement.get_width() * 3))
dirtElement = pygame.image.load("src\main/assets/textures\elements\Environment/blocks\dirt.png")
dirtElementScaled = pygame.transform.scale(dirtElement, (dirtElement.get_width() * 3, dirtElement.get_width() * 3))
cobbleElement = pygame.image.load("src\main/assets/textures\elements\Environment/blocks\cobble.png")
cobbleElementScaled = pygame.transform.scale(cobbleElement, (cobbleElement.get_width() * 3, cobbleElement.get_width() * 3))

health = pygame.image.load("src\main/assets/textures/elements\gui\player\heart.png")
healthScaled = pygame.transform.scale(health, (health.get_width() * 3, health.get_height() * 3))

halfHealth = pygame.image.load("src\main/assets/textures/elements\gui\player\half_heart.png")
halfHealthScaled = pygame.transform.scale(halfHealth, (halfHealth.get_width() * 3, halfHealth.get_height() * 3))

emptyHealth = pygame.image.load("src\main/assets/textures/elements\gui\player\empty_heart.png")
emptyHealthScaled = pygame.transform.scale(emptyHealth, (emptyHealth.get_width() * 3, emptyHealth.get_height() * 3))

#Loading element hitboxes
placeholder_hitbox = pygame.Rect((400, 700),(int(placeholder.get_width()), int(placeholder.get_height())))
tree_stump_hitbox = pygame.Rect((800, 730),(int(placeholder.get_width()), int(placeholder.get_width())))

#Loading floor and background
floor = pygame.image.load("src\main/assets/textures\levels\grass_floor.png")
floor_width = floor.get_width()
floor_height = floor.get_height()
floor = pygame.transform.scale(floor, (int(floor_width * 8), int(floor_height * 8)))
floor_hitbox = pygame.Rect((0, 850), (floor_width * 8, floor_height * 8))

font = pygame.font.SysFont('joystixmonospaceregular', 25)
debugMenuText = font.render("Press 0 to open/close the debug menu", True, DARK_ORANGE)
debugModeText = font.render("Press d to enter/leave debug mode", True, BLUE)

debug_menu = pygame.Rect((70, 70), (300, 400))

damage = registries.buttons.registerButton("button", 225, 325,  4.0, "damage", BLACK, "joystixmonospaceregular")
heal = registries.buttons.registerButton("button", 225, 425,  4.0, "heal", BLACK, "joystixmonospaceregular")

toggleCollisionsText = font.render("collides", True, BLACK)
toggleCollisions = registries.buttons.registerButton("toggle", 300, 250,  12.0, "", BLACK, "")

toggleAdvMoveText = font.render("flying", True, BLACK)
toggleAdvMove = registries.buttons.registerButton("toggle", 300, 150,  12.0, "", BLACK, "")

screen_width = 1000
screen_height = 800

chatBackground = registries.gui.registerGui(110, 100, 800, 600, False, None)
chat = registries.gui.registerChat(6, 30, BLACK, BLACK, BLACK, BLACK, 170, 110, 100, 800, 600, 140, 575, 735, 100)
chat.inputLocked = True
exitChat = registries.gui.registerExitButton(85, 80, None)

hotbar = registries.gui.registerSlots(4, 0, 0, 'slot')

item = registries.item.registerItem("item", "Item", "Environment\decoration\poppy", 800, 562)

"""game_map = [[0,0,0,2,2,2,0,0,2,2,2,2,0,0,2,2,2,2,0],
            [0,0,1,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0],
            [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [2,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,2,2,2,2,0,0,2,2,2,2,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
            [0,0,0,2,2,2,0,2,2,2,2,2,0,0,2,2,2,2,0]]""" #Lovely css map

game_map = [[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [00,00,00,00,00,00,00,00,00,00, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 2,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 1, 2,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 1, 1, 2,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 1, 1, 1, 2,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00],
            [ 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

def Start(surface):
    running = True
    startButton = registries.gui.registerButton("button", 6.0, "start", BLACK, "joystixmonospaceregular")
    optionsButton = registries.gui.registerButton("button", 6.0, "options", BLACK, "joystixmonospaceregular")
    quitButton = registries.gui.registerButton("button", 6.0, "quit", BLACK, "joystixmonospaceregular")
    
    while running:
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                exit()
        startFont = registries.gui.registerFont(40, "YET-BE-NAMED-GAME", DARKER_GRAY, surface.get_width()//2 - 250, surface.get_height()//9)
        screen.fill(BLUISH_GRAY)
        if startButton.drawAnimated(surface, surface.get_width()//2, surface.get_height()//8 * 2.75, registries.animations.startButton, 0, 0, 6, -125, -25, 0, 0):
            Main(screen, clock)
        if optionsButton.drawAnimated(surface, surface.get_width()//2, surface.get_height()//2, registries.animations.optionsButton, 48, 48, 6, -125, -25, 0, 0):
            print("NYI")
        if quitButton.drawAnimated(surface, surface.get_width()//2, surface.get_height()//8 * 5.25, registries.animations.quitButton, 0, 0, 6, -125, -25, 0, 0):
            pygame.quit()
            running = False
            exit()
            
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            running = False
            exit()
            
        startFont.drawFont(screen)
        #print(str(screen.get_width()) + str(screen.get_height()))
        pygame.display.flip()
        
def Main(screen,clock):
    world = pygame.Surface((8000,8000)) # Create Map
    player = Player() # Initialize Player Class
    camera_pos = (0, 0) #camera starting position

    #values for animation calculation
    idleValue = 0
    walkingValue = 0
    
    running = True
    
    while running:
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                exit()
            chat.event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and Player.chatOpen == False and Player.debuggingMenu == False:
                Start(screen)
        
        #idle animation calculation
        if idleValue >= len(registries.animations.idle_sprite):
            idleValue = 0

        #loading the idle animation
        Player.currentSprite = registries.animations.idle_sprite[idleValue]
        
        if walkingValue >= len(registries.animations.walking_sprite):
            walkingValue = 0
        
        #Player movement
        camera_pos = player.keybinds(camera_pos) 

        #Movement animation rendering
        if Player.walking == True:
            Player.currentSprite = registries.animations.walking_sprite[walkingValue]
        if Player.facingLeft == True:
            Player.currentSprite = pygame.transform.flip(Player.currentSprite, True, False)

        #Render background
        world.fill(AQUA)

        #Fill the background outside of the map
        screen.fill(AQUA)

        tile_rects = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile != 00:
                    tileRect = pygame.Rect(x * dirtElementScaled.get_width(), y * dirtElementScaled.get_width(), dirtElementScaled.get_width(), dirtElementScaled.get_width())
                    tile_rects.append(tileRect)
                if tile == 1:
                    world.blit(dirtElementScaled, (tileRect.x, tileRect.y))
                    if Player.debuggingMode == True:
                        pygame.draw.rect(world, (255, 255, 255), tileRect, 2)
                if tile == 2:
                    world.blit(grassElementScaled, (tileRect.x, tileRect.y))
                    if Player.debuggingMode == True:
                        pygame.draw.rect(world, (255, 255, 255), tileRect, 2)
                if tile == 3:
                    world.blit(cobbleElementScaled, (tileRect.x, tileRect.y))
                    if Player.debuggingMode == True:
                        pygame.draw.rect(world, (255, 255, 255), tileRect, 2)
                x += 1
            y += 1

        if key[pygame.K_9]:
            Player.rect.y = tileRect.y
            Player.rect.x = tileRect.x

        #Render the player
        player.render(world)
        
        player.collisions()

        #Render the map to the screen
        screen.blit(world, (player_x,player_y))

        if Player.debuggingMode == True:
            screen.blit(debugMenuText, (440, 90))
            
        screen.blit(debugModeText, (440, 30))

        #Rendering the debug menu
        player.renderDebugMenu()	
        
        #print(str(Player.rect.x) + ", " + str(Player.rect.y)) Player coordinates
        #print(str(tileRect.x) + ", " + str(tileRect.y)) World generator last generation coordinate
        
        for i in range(Player.defaultHealth):
            if (i % 2) == 0:
                screen.blit(emptyHealthScaled, (i * emptyHealthScaled.get_width()//2 , 100))
        
        for i in range(Player.health):
            if (i % 2) == 0:
                screen.blit(halfHealthScaled, (i * halfHealthScaled.get_width()//2, 100))
            else:
                screen.blit(healthScaled, (i * healthScaled.get_width()//2 - halfHealthScaled.get_width()//2, 100))
                
        hotbar.drawSlots(screen, BLACK)
        
        if Player.health > Player.defaultHealth:
            Player.health = Player.defaultHealth
            
        if Player.health <= 0 and Player.defaultHealth != 0:
            Player.dead = True
        else:
            Player.dead = False
            
        if Player.dead == True:
            Player.movementLocked = True
        else:
            Player.movementLocked = False
            
        if Player.dead == True and Player.playedDeathSound == False:
            pygame.mixer.Sound.play(Player.deathSound)
            Player.playedDeathSound = True

        elif Player.dead == False:
            Player.playedDeathSound = False

        #Idle animations
        if Player.standing == True:
            idleValue += 1
        if Player.walking == True:
            walkingValue += Player.animationFrameUpdate
        
        item.drawItem(world)
            
        #print(str(Player.rect.x) + ", " + str(Player.rect.y))
        if Player.chatOpen == True:
            chatBackground.draw(screen, BLUISH_GRAY)
            chat.drawChat(screen)
            chat.inputLocked = False
            Player.locked = True
            if exitChat.draw(screen):
                Player.chatOpen = False
        else:
                chat.inputLocked = True
                Player.locked = False

        clock.tick(200)
        pygame.display.flip()

if __name__ in "__main__":
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("CameraView")
    clock = pygame.time.Clock()
    Start(screen)
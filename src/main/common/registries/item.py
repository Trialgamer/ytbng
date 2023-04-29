import pygame

pygame.init()

class registerItem():
    def __init__(self, id, name, texturePath, x, y):
        self.id = id
        self.pickedUp = False
        self.texture = pygame.image.load("src\main/assets/textures\elements/" + texturePath + ".png")
        self.texture = pygame.transform.scale(self.texture, (self.texture.get_width() * 2.5, self.texture.get_height() * 2.5))
        self.hitbox = pygame.Rect((x, y), (self.texture.get_width(), self.texture.get_height()))
    
    def drawItem(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.texture, (self.hitbox.x, self.hitbox.y))
        if self.pickedUp == True:
            self.hitbox.x, self.hitbox.y = pygame.mouse.get_pos()
            self.hitbox.x -= self.texture.get_width()//2
            self.hitbox.y -= self.texture.get_height()//2
        if self.hitbox.collidepoint(pos):
            #pygame.draw.rect(surface, (255, 255, 255), self.hitbox, 3)
            if pygame.mouse.get_pressed()[0] == 1 and self.pickedUp == False:
                self.pickedUp = True
                print("item collides")
            elif pygame.mouse.get_pressed()[0] == 1 and self.pickedUp == True:
                self.pickedUp = False
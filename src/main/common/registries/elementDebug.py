import pygame

#button class

class registerElements():
	def __init__(self, elementLocation, x, y, scale):
		image = pygame.image.load("src\main/assets/textures\elements/" + elementLocation + ".png")
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = pygame.Rect((x, y),(int(width * scale), int(height * scale)))

	def draw(self, surface, player):
			surface.blit(self.image, (self.rect.x, self.rect.y))
			pygame.draw.rect(surface, (0, 255, 0), player, 4)
			if player.colliderect(self.rect):
				print("e")
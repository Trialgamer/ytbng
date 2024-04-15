import pygame

pygame.init()


class registerGui():
    def __init__(self, x, y, width, height, backgroundImage, imagePath=None):
        if backgroundImage == True:
            self.bgImage = pygame.image.load(
                "src/main/assets/textures/elements/background/" + imagePath + ".png")
            self.backgroundImage = True
        else:
            self.backgroundImage = False
        self.window = pygame.Surface((width, height))
        self.x, self.y = x, y

    def draw(self, surface, color=None):
        surface.blit(self.window, (self.x, self.y))
        if color == None:
            self.window.fill((0, 0, 0))
        elif color == "default":
            self.window.fill((124, 133, 156))
        else:
            self.window.fill(color)
        if self.backgroundImage == True:
            self.window.blit(self.bgImage, (0, 0))

class registerObject():
    def __init__(self, x, y, width, height, color, borderWidth):
        self.color = color
        self.width = width
        self.height = height
        self.borderWidth = borderWidth
        self.rect = pygame.Rect(x, y, width, height)

    def drawObject(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, self.borderWidth)


class registerButton():
	clock = pygame.time.Clock()

	def __init__(self, button_name, scale):
		image = pygame.image.load('src//main//assets//textures//elements//gui//' + button_name + '.png')
		self.value = 0
		selected_image = pygame.image.load('src//main//assets//textures//elements//gui//' + button_name + '_selected.png')
		width = image.get_width()
		height = image.get_height()
		self.selected_image = pygame.transform.scale(selected_image, (int(width * scale), int(height * scale)))
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))); self.current = self.image
		self.clicked = False
		self.toggled = False
		self.selected = False
		self.test = 0  # Important for toggle buttons

	# draw function is not used atm
	def draw(self, surface, x, y, xTextOffset, yTextOffset, xTextureOffset, yTextureOffset, display_text, text_color, font_type):
		action = False
		# get mouse position
		pos = pygame.mouse.get_pos()
		smallfont = pygame.font.SysFont(font_type, 35)
		self.display_text1 = smallfont.render(display_text, True, text_color)
		self.selected_display_text4 = smallfont.render(
		    display_text, True, (255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# check mouseover and clicked conditions
		surface.blit(self.image, (self.rect.x - xTextureOffset,self.rect.y - yTextureOffset))
		if not self.rect.collidepoint(pos):
			surface.blit(self.display_text1, (self.rect.x - xTextOffset -xTextureOffset, self.rect.y - yTextOffset - yTextureOffset))
		elif self.rect.collidepoint(pos):
			pygame.draw.rect(surface, (255, 255, 255), (self.rect.x - xTextureOffset,self.rect.y - yTextureOffset, self.rect.width, self.rect.height), 5)
			surface.blit(self.selected_display_text4, (self.rect.x - xTextOffset -xTextureOffset, self.rect.y - yTextOffset - yTextureOffset))
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action

	def drawAnimated(self, surface, x, y, animationArray, xOffset, yOffset, scale, xTextOffset, yTextOffset, display_text, text_color, font_type):
		action = False
		pos = pygame.mouse.get_pos()
		image = animationArray[self.value]
		width = image.get_width()
		height = image.get_height()
		buttonSprite = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		smallfont = pygame.font.SysFont(font_type, 35)
		self.display_text1 = smallfont.render(display_text, True, text_color)
		self.selected_display_text1 = smallfont.render(display_text, True, (56, 56, 56))
		self.selected_display_text2 = smallfont.render(display_text, True, (80, 80, 80))
		self.selected_display_text3 = smallfont.render(display_text, True, (171, 171, 171))
		self.selected_display_text4 = smallfont.render(display_text, True, (255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		if self.value >= len(animationArray) - 1 and self.selected == True:
			self.value = len(animationArray) - 2
		elif self.selected == False:
			self.value = 0

		if not self.rect.collidepoint(pos):
			surface.blit(self.image, (self.rect.x, self.rect.y))
			surface.blit(self.display_text1, (self.rect.x -xTextOffset, self.rect.y - yTextOffset))
			self.selected = False
		else:
			self.selected = True
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if self.selected == True and self.value < len(animationArray) - 1:
			self.value += 1

		if self.selected == True:
			surface.blit(buttonSprite, (self.rect.x - xOffset, self.rect.y - yOffset))

		if self.value < len(animationArray)/4 * 1:
			surface.blit(self.selected_display_text1, (self.rect.x -xTextOffset, self.rect.y - yTextOffset))
		elif self.value < len(animationArray)/4 * 2:
			surface.blit(self.selected_display_text2, (self.rect.x -xTextOffset, self.rect.y - yTextOffset))
		elif self.value < len(animationArray)/4 * 3:
			surface.blit(self.selected_display_text3, (self.rect.x -xTextOffset, self.rect.y - yTextOffset))
		elif self.value > len(animationArray)/4 * 3:
			surface.blit(self.selected_display_text4, (self.rect.x -xTextOffset, self.rect.y - yTextOffset))

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action

	def drawToggle(self, surface, x, y, xTextureOffset, yTextureOffset):
		action = False
		pos = pygame.mouse.get_pos()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y); surface.blit(self.current, (self.rect.x - xTextureOffset, self.rect.y - yTextureOffset))

		if self.toggled == False or self.test == 0:
			self.current = self.image
		if self.toggled == True and self.test == 1:
			self.current = self.selected_image
			self.selected = True
		if self.toggled == True and self.test > 1:
			self.test = 0
			self.selected = False

		if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.rect.collidepoint(pos):
			self.test += 1
			self.toggled = True
			action = True
			pygame.time.wait(100)

		if self.rect.collidepoint(pos):
			pygame.draw.rect(surface, (255, 255, 255), (self.rect.x - xTextureOffset,self.rect.y - yTextureOffset, self.rect.width, self.rect.height), 4)

		return action

	clock.tick(60)
 
class registerText():
    def __init__(self, fontSize, displayText, color, x, y):
        self.font = pygame.font.Font("src/main/assets/fonts/joystixmonospaceregular.otf", fontSize)
        self.text = self.font.render(displayText, True, color)
        self.rect = self.text.get_rect()
        self.rect.center = (x, y)
        
    def drawText(self, surface):
        surface.blit(self.text, (self.rect.center))
    
class registerVanishedText():
    def __init__(self, fontSize, colorVanished, color1, color2, color3, color4, color5):
         self.font = pygame.font.Font("src/main/assets/fonts/joystixmonospaceregular.otf", fontSize)
         self.vanishCounter = 0
         self.colorVanished = colorVanished
         self.color1 = color1
         self.color2 = color2
         self.color3 = color3
         self.color4 = color4
         self.color5 = color5

    def drawVanishedText(self, surface, displayText, x, y):
        self.x, self.y = x, y
        self.textVanished = self.font.render(displayText, True, self.colorVanished)
        self.text1 = self.font.render(displayText, True, self.color1)
        self.text2 = self.font.render(displayText, True, self.color2)
        self.text3 = self.font.render(displayText, True, self.color3)
        self.text4 = self.font.render(displayText, True, self.color4)
        self.text5 = self.font.render(displayText, True, self.color5)
        if self.vanishCounter < 300:
             self.vanishCounter += 1
        if self.vanishCounter <= 50:
             surface.blit(self.textVanished, (self.x, self.y))
        if self.vanishCounter <= 100 and self.vanishCounter > 50:
             surface.blit(self.text1, (self.x, self.y))
        if self.vanishCounter <= 150 and self.vanishCounter > 100:
             surface.blit(self.text2, (self.x, self.y))
        if self.vanishCounter <= 200 and self.vanishCounter > 150:
             surface.blit(self.text3, (self.x, self.y))
        if self.vanishCounter <= 250 and self.vanishCounter > 200:
             surface.blit(self.text4, (self.x, self.y))
        if self.vanishCounter <= 300 and self.vanishCounter > 250:
             surface.blit(self.text5, (self.x, self.y))
        print(self.vanishCounter)

        if self.vanishCounter > 300:
            self.vanishCounter += 1
            if self.vanishCounter <= 350 and self.vanishCounter > 300:
                surface.blit(self.text5, (self.x, self.y))
            if self.vanishCounter <= 400 and self.vanishCounter > 350:
                surface.blit(self.text4, (self.x, self.y))
            if self.vanishCounter <= 450 and self.vanishCounter > 400:
                surface.blit(self.text3, (self.x, self.y))
            if self.vanishCounter <= 500 and self.vanishCounter > 450:
                surface.blit(self.text2, (self.x, self.y))
            if self.vanishCounter <= 550 and self.vanishCounter > 500:
                surface.blit(self.textVanished, (self.x, self.y))

class registerImages():
	def __init__(self, imagePath):
		self.image = pygame.image.load("src/main/assets/textures/" + imagePath + ".png")
	
	def drawImage(self, surface, x, y):
		surface.blit(self.image, (x, y))
  
class registerChat():
    def __init__(self, lines, fontSize, textColor, markerColor, frameColor, chatBoxColor, markerDefaultPos, frameX, frameY, frameWidth, frameHeight, chatBoxX, chatBoxY, chatBoxWidth, chatBoxHeight):
        self.linesLoaded = []
        self.keyBlacklist = ()
        self.userInput = ""
        self.markerColor = markerColor
        self.sample = "i"
        self.inputLocked = False
        self.selected = True
        self.frame = pygame.Rect((frameX, frameY), (frameWidth, frameHeight))
        self.chatBox = pygame.Rect((chatBoxX, chatBoxY), (chatBoxWidth, chatBoxHeight))
        self.font = pygame.font.Font("src/main/assets/fonts/joystixmonospaceregular.otf", fontSize)
        self.textColor = textColor
        self.frameColor = frameColor
        self.chatBoxColor = chatBoxColor
        self.renderMarker = 0
        self.lessThanOneChar = True
        self.markerDefaultPos = markerDefaultPos
        self.x = self.markerDefaultPos
        self.lines = lines
        self.sentMessage = False
    
    def event(self, event): # this has to be executed withing the event for loop look at main_gui for an example
        if event.type == pygame.KEYDOWN and self.inputLocked == False:
            if event.key == pygame.K_BACKSPACE and self.lessThanOneChar == False:
                self.userInput = self.userInput[0:-1]
                self.x -= self.sampleText.get_width()
            elif event.key == pygame.K_TAB and self.userText.get_width() < self.chatBox.width - self.sampleText.get_width() * 4:
                self.userInput += "    "
                self.x += self.sampleText.get_width() * 4
            elif not event.key == pygame.K_ESCAPE and not event.key == pygame.K_BACKSPACE and not event.key == pygame.K_LALT and not event.key == pygame.K_RALT and not event.key == pygame.K_LSHIFT and not event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT and not event.key == pygame.K_UP and not event.key == pygame.K_DOWN and not event.key == pygame.K_LCTRL and not event.key == pygame.K_RCTRL and not event.key == pygame.K_RSHIFT and not event.key == pygame.K_RETURN and self.userText.get_width() < self.chatBox.width - self.sampleText.get_width() * 4:
                self.userInput += event.unicode
                self.x += self.sampleText.get_width()
                
            if event.key == pygame.K_RETURN and self.lessThanOneChar == False:
                for i in range(self.lines): # len in main_gui is 3
                        self.linesLoaded[self.lines - i] = self.linesLoaded[self.lines - i - 1]
                self.linesLoaded[0] = self.userInput
                self.userInput = ""
                self.x = self.markerDefaultPos
                self.sentMessage = True
            else:
                self.sentMessage = False
            
    def drawChat(self, surface):
        self.sampleText = self.font.render(self.sample, False, (0, 0, 0))
        self.userText = self.font.render(self.userInput, True, self.textColor)
        
        for i in range(self.lines + 1):
            self.line = ""
            self.linesLoaded.append(self.line)
        
        for i in range(self.lines):
            self.message_text = self.font.render(self.linesLoaded[i], True, self.textColor)
            surface.blit(self.message_text, (self.markerDefaultPos, self.chatBox.y - 75 - 75 * i))
            
        surface.blit(self.userText, (self.markerDefaultPos ,600))
        pygame.draw.rect(surface, self.frameColor, self.frame, 5)
        pygame.draw.rect(surface, self.chatBoxColor, self.chatBox, 5)
        
        if self.userText.get_width() >= self.sampleText.get_width():
            self.lessThanOneChar = False
        else:
            self.lessThanOneChar = True
            
        if self.renderMarker >= 99:
            self.renderMarker = 0
        else:
            pygame.time.wait(10)
            self.renderMarker += 1

        if self.renderMarker <= 40 and self.inputLocked == False:
            pygame.draw.line(surface, self.markerColor, (self.x, 600), (self.x, 600 + self.userText.get_height()), 5)
        
    def clear(self):
        self.userInput = ""
        for i in range(self.lines):
            self.linesLoaded[i] = ""
        self.x = self.markerDefaultPos
"""
class registerSlots():
    def __init__(self, slotCount, x, y, texture=None):
        self.slotCount = slotCount
        self.slots = []
        self.texture = texture
        for i in range(self.slotCount):
            self.rect = pygame.Rect((x + 60 * i, y), (60, 60))
            self.slots.append(self.rect)
            print(i)
        if texture != None:
         self.texture = pygame.image.load('src/main/assets/textures/elements/gui/' + texture + '.png') # weird indentation
         self.texture = pygame.transform.scale(self.texture, (60, 60))
    
    def drawSlots(self, surface, slotColor):
        for i in range(self.slotCount):
            pygame.draw.rect(surface, slotColor, self.slots[i], 6)
            if self.texture != None:
                surface.blit(self.texture, self.slots[i])
"""
class registerExitButton():
    def __init__(self, x, y, texturePath = None):
        self.x = x
        self.y = y
        self.clicked = False
        if texturePath == None:
            self.texture = pygame.image.load("src/main/assets/textures/elements/gui/exit_button.png")
            self.textureSelected = pygame.image.load("src/main/assets/textures/elements/gui/exit_button_selected.png")
        else:
            self.texture = pygame.image.load("src/main/assets/textures/elements/" + texturePath + ".png")
            self.textureSelected = pygame.image.load("src/main/assets/textures/elements/" + texturePath + ".png")
        self.textureScaled = pygame.transform.scale(self.texture, (self.texture.get_width() * 3.5, self.texture.get_height() * 3.5))
        self.textureSelectedScaled = pygame.transform.scale(self.textureSelected, (self.textureSelected.get_width() * 3.5, self.textureSelected.get_height() * 3.5))
        self.rect = pygame.Rect((self.x, self.y), (self.texture.get_width() * 3.5, self.texture.get_height() * 3.5))

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        if not self.rect.collidepoint(pos):
            surface.blit(self.textureScaled, (self.rect.x, self.rect.y))
        elif self.rect.collidepoint(pos):
            surface.blit(self.textureSelectedScaled, (self.rect.x, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
            else:
                self.clicked = False
            return self.clicked
        
class registerTextBox():
    def __init__(self, fontSize, textColor, markerColor, chatBoxColor, markerDefaultPos, textBoxX, textBoxY, textBoxWidth, textBoxHeight):
        self.keyBlacklist = ()
        self.userInput = ""
        self.markerColor = markerColor
        self.sample = "i"
        self.inputLocked = False
        self.selected = True
        self.chatBox = pygame.Rect((textBoxX, textBoxY), (textBoxWidth, textBoxHeight))
        self.font = pygame.font.Font("src/main/assets/fonts/joystixmonospaceregular.otf", fontSize)
        self.textColor = textColor
        self.chatBoxColor = chatBoxColor
        self.renderMarker = 0
        self.lessThanOneChar = True
        self.markerDefaultPos = markerDefaultPos
        self.x = self.markerDefaultPos
    
    def event(self, event): # this has to be executed withing the event for loop look at main_gui for an example
        if event.type == pygame.KEYDOWN and self.inputLocked == False:
            if event.key == pygame.K_BACKSPACE and self.lessThanOneChar == False:
                self.userInput = self.userInput[0:-1]
                self.x -= self.sampleText.get_width()
            elif event.key == pygame.K_TAB and self.userText.get_width() < self.chatBox.width - self.sampleText.get_width() * 4:
                self.userInput += "    "
                self.x += self.sampleText.get_width() * 4
            elif not event.key == pygame.K_ESCAPE and not event.key == pygame.K_BACKSPACE and not event.key == pygame.K_LALT and not event.key == pygame.K_RALT and not event.key == pygame.K_LSHIFT and not event.key == pygame.K_RIGHT and not event.key == pygame.K_LEFT and not event.key == pygame.K_UP and not event.key == pygame.K_DOWN and not event.key == pygame.K_LCTRL and not event.key == pygame.K_RCTRL and not event.key == pygame.K_RSHIFT and not event.key == pygame.K_RETURN and self.userText.get_width() < self.chatBox.width - self.sampleText.get_width() * 4:
                self.userInput += event.unicode
                self.x += self.sampleText.get_width()
    
    def draw(self, surface):
        self.sampleText = self.font.render(self.sample, False, (0, 0, 0))
        self.userText = self.font.render(self.userInput, True, self.textColor)
        
        surface.blit(self.userText, (self.markerDefaultPos, self.chatBox.height))
        pygame.draw.rect(surface, self.chatBoxColor, self.chatBox, 5)
        print(self.chatBox.y)
        if self.userText.get_width() >= self.sampleText.get_width():
            self.lessThanOneChar = False
        else:
            self.lessThanOneChar = True
            
        if self.renderMarker >= 99:
            self.renderMarker = 0
        else:
            pygame.time.wait(10)
            self.renderMarker += 1

        if self.renderMarker <= 70 and self.inputLocked == False:
            pygame.draw.line(surface, self.markerColor, (self.x, self.chatBox.height), (self.x, self.chatBox.height + self.userText.get_height()), 5)

        print(self.renderMarker)
    
    def clear(self):
        self.userInput = ""
        self.x = self.markerDefaultPos
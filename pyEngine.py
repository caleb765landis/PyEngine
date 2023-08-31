"""
pyEngine.py
Simplifies creating 2D game projects
"""

import pygame
import math
from dataclasses import dataclass
pygame.init()

# ----------------------------- create constants ----------------------------- #
# bounds constants
WRAP = 0
BOUNCE = 1
STOP = 2
HIDE = 3
CONTINUE = 4

class Game(object):
    def __init__(self):
        # ------------------------------ initialize app ------------------------------ #
        pygame.init()
        self.window = pygame.display.set_mode((1080, 720))
        self.setTitle("PyEngine is working!")
        self.scenes = {}

        # ------------------------------- default game ------------------------------- #
        # default map
        background = Map()

        # default scene
        sampleScene = Scene(self, background)

        # default sprite
        sampleSprite = Sprite(sampleScene)
        sampleSprite.setImage("dvd.jpeg")
        sampleSprite.setBoundAction(BOUNCE)
        sampleSprite.setMoveAngle(230)
        sampleSprite.setSpeed(4)
        sampleSprite.setPosition((350, 350))

        sampleScene.addSprite(sampleSprite)
        self.addScene("sampleScene", sampleScene)
        self.setCurrentScene("sampleScene")

    def start(self):
        self.currentScene.start()

    def stop(self):
        self.currentScene.stop()

    def addScene(self, sceneKey, scene):
        self.scenes[sceneKey] = scene

    def setCurrentScene(self, sceneKey):
        self.currentScene = self.scenes[sceneKey]

    def setWindowSize(self, width, height):
        self.window = pygame.display.set_mode((width, height))

    def getWindowWidth(self):
        return pygame.display.get_window_size()[0]

    def getWindowHeight(self):
        return pygame.display.get_window_size()[1]

    def getWindowSize(self):
        return pygame.display.get_window_size()

    # sets title of the window
    def setTitle(self, title):
        pygame.display.set_caption(title)

    def goToScene(self, sceneKey):
        if sceneKey in self.scenes:
            self.currentScene.stop()
            self.currentScene = self.scenes[sceneKey]
            self.currentScene.start()


class Scene(object):

    # scene gets access to the game it is a part of
    # also takes a map to set as background
    def __init__(self, game, map):
        # --------------------------- initialize background -------------------------- #
        self.game = game
        self.map = map
        self.backgroundMap = map.image
        self.boundsMap = map.boundsMap
        self.numTilesAdded = 0  # number of tiles added to self.tiles[]
        self.mapPos = (0, 0)
        self.surface = game.window

        # ----------------------------- initialize groups ---------------------------- #
        self.sprites = []
        self.groups = []
        self.tiles = []

        # ------------------------ initialize other attributes ----------------------- #
        self.framerate = 30
        self.clock = pygame.time.Clock()

    # ----------------------------- scene management ----------------------------- #

    # sets up sprite groups, game clock, and main loop

    def start(self):
        # set up sprite groups
        self.mainSprites = pygame.sprite.OrderedUpdates(self.sprites)
        self.groups.append(self.mainSprites)

        # blit map to game's surface at initial position
        self.surface.blit(self.backgroundMap, self.mapPos)
        self.drawTiles()

        for group in self.groups:
            group.clear(self.surface, self.backgroundMap)
            group.update()
            group.draw(self.surface)

        # start main loop
        self.keepGoing = True
        while self.keepGoing:
            self.__mainLoop()

    # stops scene by ending its mainLoop
    def stop(self):
        self.keepGoing = False

    """
        private method: main loop that runs scene
        ticks at set framerate
        checks pygame events and user's overriden checkEvents__ abstract method
        updates game based on user's overriden update__ abstract method
        draws all groups
    """

    def __mainLoop(self):
        self.clock.tick(self.framerate)

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keepGoing = False
            self.checkEvents__(event)

        # update scene
        self.update__()

        # draw tiles
        self.drawTiles()

        # draw sprites
        for group in self.groups:
            group.clear(self.surface, self.backgroundMap)
            group.update()
            group.draw(self.surface)

        pygame.display.flip()

    def checkEvents__(self, event):
        pass

    def update__(self):
        pass

    def setFramerate(self, framerate):
        self.framerate = framerate

    # ----------------------------- group management ----------------------------- #

    def drawTiles(self):
        # blits bounds map tiles if they are set to visible
        # also adds tile rectangles to tiles[] for checking collisions
        # used for debugging bounds collisions
        tileW = self.map.tileW
        tileH = self.map.tileH
        tileY = 0
        r = 0
        for row in self.boundsMap:
            tileX = 0
            c = 0
            for col in row:
                currentTile = col
                if (currentTile != 0):
                    tile = self.boundsMap[r][c]
                    sprite = Sprite(self)
                    sprite.image = tile
                    #tileRect = sprite.get_rect()
                    #tileRect.x = tileX
                    #tileRect.y = tileY
                    sprite.x = tileX + (.5 * tile.get_width())
                    sprite.y = tileY + (tile.get_height())
                    sprite.rect = tile.get_rect(center=(sprite.x, sprite.y))
                    sprite.displayedImgWidth = tile.get_width()
                    sprite.displayedImgHeight = tile.get_height()
                    sprite.displayedImageCenter = tile.get_rect().center

                    if (self.numTilesAdded < self.map.numTiles):
                        self.tiles.append(sprite)
                        self.numTilesAdded += 1

                    if (self.map.isBoundsMapVisible()):
                        self.surface.blit(tile, (tileX, tileY))
                c += 1
                tileX += tileW
            r += 1
            tileY += tileH

    def addSprite(self, sprite):
        self.sprites.append(sprite)

    # creates a sprite group whose clear, update, and draw methods will be automatically handled once added to groups
    def createSpriteGroup(self, sprites):
        return pygame.sprite.OrderedUpdates(sprites)

    # adds a sprite group to groups for automatic processing during each iteration of loop
    def addGroup(self, group):
        self.groups.append(group)

    # ------------------------------ map management ------------------------------ #

    def setBackgroundMap(self, map):
        self.backgroundMap = map.image

    def setMapPos(self, x, y):
        self.mapPos = (x, y)

    # --------------------------------- controls --------------------------------- #

    def hideCursor(self):
        pygame.mouse.set_visible(False)

    def showCursor(self):
        pygame.mouse.set_visible(True)

    def isMouseVisible(self):
        return pygame.mouse.get_visible()

    def getMousePos(self):
        return pygame.mouse.get_pos()


class Sprite(pygame.sprite.Sprite):

    # ----------------------------- sprite management ---------------------------- #

    def __init__(self, scene):
        # initialize pygame sprite
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene

        # ----------------------------- create constants ----------------------------- #
        # bounds constants
        self.WRAP = 0
        self.BOUNCE = 1
        self.STOP = 2
        self.HIDE = 3
        self.CONTINUE = 4

        # -------------------------- init sprite attributes -------------------------- #
        # motion and position attributes
        self.x = 200
        self.y = 200
        self.dx = 0
        self.dy = 0
        self.acceleration = 0
        self.speed = 0
        self.maxSpeed = 10
        self.minSpeed = 0
        self.imgAngle = 0
        self.moveAngle = 0

        # event attributes
        self.boundAction = self.WRAP
        self.collidable = True
        self.pressed = False

        """
            default placeholders for sprite appearance attributes
            font used for placeholder image and ui extended from sprite
            image is actual sprite image
            displayedImage is what is displayed to player after rotation and position updates
            rect is image's rectangle
            imageCenter is original image's center
            displayedImageCenter is center of image displayed to player
            visible draws sprite if True
        """
        self.font = pygame.font.Font("freesansbold.ttf", 30)
        self.imageMaster = self.font.render(
            "DVD", True, (0, 0, 0), (0xFF, 0xFF, 0xFF))
        self.image = self.imageMaster
        self.rect = self.imageMaster.get_rect()

        # imageMaster dimensions
        self.imgWidth = self.rect.width
        self.imgHeight = self.rect.height
        self.imgCenter = self.rect.center

        # image dimensions
        self.displayedImgWidth = self.imgWidth
        self.displayedImgHeight = self.imgHeight
        self.displayedImageCenter = self.imgCenter

        # cropped image dimensions
        self.croppedLeft = 0
        self.croppedTop = 0
        self.croppedWidth = self.rect.width
        self.croppedHeight = self.rect.height

        # animation
        self.animate = False
        self.animationSpeed = 1
        self.animationTickCounter = 0
        self.animationTickSpeed = 1
        self.currentAnimationFrame = 0
        self.currentAnimation = "default"
        self.animations = {
            "default": [self.image]
        }

        self.visible = True
        # remembers x and y from before they were hidden
        self.hiddenX = 200
        self.hiddenY = 200

    # abstract method for users to add events to actors extended from sprite class
    def checkEvents__(self):
        pass

    def update(self):
        # check user defined events
        self.checkEvents__()

        self.__animate()

        # rotate displayedImage
        self.image = pygame.transform.rotate(self.image, self.imgAngle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.displayedImgWidth = self.rect.width
        self.displayedImgHeight = self.rect.height
        self.displayedImageCenter = self.rect.center

        # calculate motion vector
        theta = self.moveAngle / 180.0 * math.pi
        self.dx = math.cos(theta) * self.speed
        self.dy = math.sin(theta) * self.speed
        self.dy *= -1

        # caluculate position
        self.x += self.dx
        self.y += self.dy

        self.checkBounds()

        # get new center again
        self.rect.center = (self.x, self.y)
        self.displayedImageCenter = self.rect.center

        # check bounds
        #self.checkBounds()

    # ---------------------- image management and visibility --------------------- #

    def setImage(self, image):
        self.imageMaster = pygame.image.load(image)
        self.imageMaster = self.imageMaster.convert_alpha()
        self.rect = self.imageMaster.get_rect()

        # imageMaster dimensions
        self.imgWidth = self.rect.width
        self.imgHeight = self.rect.height
        self.imgCenter = self.rect.center

        # image dimensions
        self.displayedImgWidth = self.imgWidth
        self.displayedImgHeight = self.imgHeight
        self.displayedImageCenter = self.imgCenter

        # cropped image dimensions
        self.croppedLeft = 0
        self.croppedTop = 0
        self.croppedWidth = self.rect.width
        self.croppedHeight = self.rect.height

        self.image = self.imageMaster

    def setDisplayedImageAsMaster(self):
        self.imageMaster = self.image

    """
        sets self.image to a cropped sprite image based off imageMaster
        left, top: coordinates of original image for where to put top left corner of new cropped image
        width, height: dimensions of new cropped image
        use setDisplayedImageAsMaster() to set cropped image to master
    """

    def crop(self, left, top, width, height):
        if ((left < self.imgWidth) and (top < self.imgHeight)):
            self.croppedLeft = left
            self.croppedTop = top
        else:
            self.croppedLeft = 0
            self.croppedTop = 0

        if ((width < self.imgWidth) and (height < self.imgHeight)):
            self.croppedWidth = width
            self.croppedHeight = height
        else:
            self.croppedWidth = self.imgWidth
            self.croppedHeight = self.imgHeight

        self.image = self.imageMaster.subsurface(
            (self.croppedLeft, self.croppedTop, self.croppedWidth, self.croppedHeight))
        self.rect = self.image.get_rect(center=self.rect.center)

    def cropReset(self):
        self.croppedLeft = 0
        self.croppedTop = 0
        self.croppedWidth = self.imgWidth
        self.croppedHeight = self.imgHeight

    # wrapper for pygame.transform.scale
    # only scales displayed image, not imageMaster or any of current animations set
    def scale(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))

    # wrapper for pygame.transform.scale_by
    # only scales displayed image, not imageMaster or any of current animations set
    def scaleBy(self, scalar):
        self.image = pygame.transform.scale_by(self.image, scalar)

    def hide(self):
        self.visible = False
        self.hiddenX, self.hiddenY = self.x, self.hiddenY
        self.x, self.y = -10000, -10000
        self.speed = 0

    def show(self):
        self.visible = True
        self.x, self.hiddenY = self.hiddenX, self.hiddenY

    def isVisible(self):
        return self.visible

    # --------------------------------- animation -------------------------------- #

    def createAnimation(self, name, numCells, cellWidth, cellHeight, cellLeft=0, cellTop=0, cellScalar=1):
        # generate list of cells as images
        animation = []
        left = cellLeft
        for i in range(numCells):
            # create cell using imageMaster as spritesheet
            cell = self.imageMaster.subsurface(
                (left, cellTop, cellWidth, cellHeight))
            cell = pygame.transform.scale_by(cell, cellScalar)
            animation.append(cell)

            # start next cell at top right corner of this cell
            left += cellWidth

        # add to animations dictionary
        self.animations[name] = animation

    def __animate(self):
        if (self.animate == True):
            animation = self.animations[self.currentAnimation]
            self.image = animation[self.currentAnimationFrame]

            # image dimensions
            self.rect = self.image.get_rect()
            self.displayedImgWidth = self.imgWidth
            self.displayedImgHeight = self.imgHeight
            self.displayedImageCenter = self.imgCenter

            # increment current animation frame if counter has reached required number of ticks
            if (self.animationTickCounter >= self.animationSpeed):
                self.currentAnimationFrame += self.animationTickSpeed
                if self.currentAnimationFrame == len(animation):
                    self.currentAnimationFrame = 0

            # increment animation tick counter
            self.animationTickCounter += 1
            if self.animationTickCounter > self.animationSpeed:
                self.animationTickCounter = 0

    # starts animation
    # removes any cropping to image done before animation starts unless cropped image has been set to imageMaster
    def playAnimation(self):
        self.animate = True

    def pauseAnimation(self):
        self.animate = False

    def resetAnimation(self):
        self.currentAnimationFrame = 0

    # sets current animation's speed where speed is based upon how many frames to wait until next animation cell
    # expects an int for speed
    # animation speed must be less than or equal toframerate
    def setAnimationSpeed(self, speed, animationTickSpeed):
        if (speed <= self.scene.framerate):
            self.animationSpeed = speed
        self.animationTickSpeed = animationTickSpeed

    # checks to see if animation name is in animations
    # expects a string
    # if name is not in dict, nothing happens
    def setCurrentAnimation(self, name):
        if name in self.animations:
            self.currentAnimation = name

    # ---------------------------- motion and position --------------------------- #

    def setSpeed(self, speed):
        self.speed = speed

    def speedUp(self, amount):
        self.speed += amount
        if self.speed < self.minSpeed:
            self.speed = self.minSpeed
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed

    def setPosition(self, position):
        self.x = position[0]
        self.y = position[1]

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setImgAngle(self, angle):
        self.imgAngle = angle

    def rotateImg(self, angle):
        self.imgAngle += angle

    def setMoveAngle(self, angle):
        self.moveAngle = angle

    def setDX(self, dx):
        self.dx = dx
        self.updateVector()

    def setDY(self, dy):
        self.dy = dy
        self.updateVector()

    def addDX(self, amount):
        self.dx += amount
        self.updateVector()

    def addDY(self, amount):
        self.dy += amount
        self.updateVector()

    def moveBy(self, dx, dy):
        self.x += dx
        self.y += dy
        self.checkBounds()

    def moveForward(self, amount):
        radians = self.moveAngle * math.pi / 180
        dx = amount * math.cos(radians)
        dy = amount * math.sin(radians) * -1

        self.x += dx
        self.y += dy
        self.checkBounds()

    def setMotionVector(self, speed, angle):
        self.speed = speed
        self.moveAngle = angle

    def addForce(self, amount, angle):
        radians = angle * math.pi / 180
        self.dx += amount * math.cos(radians)
        self.dy += amount * math.sin(radians) * -1

        self.updateVector()

    # calculate new speed and move angle based on dx, dy
    # call this any time you change dx or dy directly without a built in pyEngine method
    def updateVector(self):
        self.speed = math.sqrt((self.dx * self.dx) + (self.dy * self.dy))

        dx = self.dx
        dy = self.dy * -1
        radians = math.atan2(dy, dx)

        self.moveAngle = radians / math.pi * 180

    # --------------------------- bounds and collisions -------------------------- #

    """ 
        sets action for window and boundary tile collisions
        Values are:
        self.WRAP (wrap around edge - default)
        self.BOUNCE (bounce off screen changing direction)
        self.STOP (stop at edge of screen)
        self.HIDE (move off-stage and stop)
        self.CONTINUE (move on forever)
        Any other value allows the sprite to move on forever
    """

    def setBoundAction(self, action):
        self.boundAction = action

    def checkBounds(self):
        window_width = self.scene.surface.get_width()
        window_height = self.scene.surface.get_height()

        offRight = offLeft = offTop = offBottom = offScreen = False
        
        def tileCollision(self, tile):
            if (((self.x - (.5 * self.displayedImgWidth) - self.speed) <= tile.x + (.5 * tile.displayedImgWidth)) and # left of sprite
                ((self.x + (.5 * self.displayedImgWidth) + self.speed) >= tile.x - (.5 * tile.displayedImgWidth)) and # right of sprite
                ((self.y - (.5 * self.displayedImgHeight) - self.speed) <= tile.y) and # top of sprite
                ((self.y + (.5 * self.displayedImgHeight) + self.speed) >= tile.y - (tile.displayedImgHeight))):  # bottom of sprite

                return True
            return False
        
        collidingTile = None

        for tile in self.scene.tiles:
            if tileCollision(self, tile):
                collidingTile = tile 
                break

        if collidingTile != None:
            tile = collidingTile

            # right of sprite collides with left of tile
            if ((self.x + (.5 * self.displayedImgWidth) + self.speed) >= tile.x - (.5 * tile.displayedImgWidth)):
                offRight = True
            # left of sprite collides with right of tile
            if ((self.x - (.5 * self.displayedImgWidth) - self.speed) <= tile.x + (.5 * tile.displayedImgWidth)):
                offLeft = True
            # bottom of sprite collides with top of tile
            if ((self.y + (.5 * self.displayedImgHeight) + self.speed) >= tile.y - tile.displayedImgHeight):
                offBottom = True
            # top of sprite collides with bottom of tile
            if ((self.y - (.5 * self.displayedImgHeight) - self.speed) <= tile.y):
                offTop = True
        

        # check to see if sprite is out of bounds anywhere else in window
        if ((self.x + (.5 * self.displayedImgWidth)) >= window_width):
            offRight = True
        if ((self.x - (.5 * self.displayedImgWidth)) <= 0):
            offLeft = True
        if ((self.y + (.5 * self.displayedImgHeight)) >= window_height):
            offBottom = True
        if ((self.y - (.5 * self.displayedImgHeight)) <= 0):
            offTop = True

        # if it is out of bounds anywhere, then it is off-screen
        if offRight or offLeft or offTop or offBottom:
            offScreen = True

        # wrap sprite to opposite side if bounds action is wrap
        if self.boundAction == self.WRAP:
            if self.x > window_width:
                self.x = 0
            if self.x < 0:
                self.x = window_width
            if self.y > window_height:
                self.y = 0
            if self.y < 0:
                self.y = window_height

        # bounce sprite off of edge of window if bounds action is bounce
        elif self.boundAction == self.BOUNCE:

            if offLeft or offRight:
                self.dx *= -1
                self.updateVector()
            if offTop or offBottom:
                self.dy *= -1

            self.updateVector()

        # stop sprite from moving if bounds action is stop
        elif self.boundAction == self.STOP:
            if offScreen:
                self.speed = 0

        # make sprite invisible and stop it from moving if its bounds action is hide
        elif self.boundAction == self.HIDE:
            if offScreen:
                self.speed = 0
                self.x, self.y = -10000, -10000
                self.visible = False

    def collidesWith(self, sprite):
        collision = False
        if sprite.isCollidable():
            if self.rect.colliderect(sprite.rect):
                collision = True
        return collision

    def collidesWithGroup(self, group):
        if pygame.sprite.spritecollideany(self, group) != None:
            return True
        return False
        #return pygame.sprite.spritecollideany(self, group)

    def isCollidable(self):
        return self.collidable

    # ------------------------------ extra utilities ----------------------------- #

    def isPressed(self):
        self.pressed = False
        if (pygame.mouse.get_pressed() == (1, 0, 0)):
            if (self.rect.collidepoint(pygame.mouse.get_pos())):
                self.pressed = True

        return self.pressed

    def isClicked(self):
        clicked = False
        if (pygame.mouse.get_pressed() == (1, 0, 0)):
            pygame.event.wait()
            if (pygame.mouse.get_pressed() == (0, 0, 0)):
                if (self.rect.collidepoint(pygame.mouse.get_pos())):
                    clicked = True

        return clicked

    def distanceToPoint(self, point):
        dx = self.x - point[0]
        dy = self.y - point[1]

        return math.sqrt((dx * dx) + (dy * dy))

    def angleToPoint(self, point):
        dx = self.x - point[0]
        dy = (self.y - point[1]) * -1
        radians = math.atan2(dy, dx)

        return ((radians * 180 / math.pi) + 180)


class Map(pygame.sprite.Sprite):
    def __init__(self):
        self.imageMaster = pygame.Surface((1080, 720))
        self.imageMaster.fill((0, 0, 0))
        self.image = self.imageMaster
        self.rect = self.imageMaster.get_rect()

        self.numRows = 1
        self.numCols = 1
        self.numTiles = 0
        self.tileW = 0
        self.tileH = 0
        self.tileMap = [[0]]
        self.boundsMap = self.tileMap
        self.tilesVisible = False

    def setMapImage(self, image):
        self.imageMaster = pygame.image.load(image)
        self.imageMaster = self.imageMaster.convert()
        self.image = self.imageMaster
        self.rect = self.imageMaster.get_rect()

    """
        creates a grid of boundary tiles where each tile is a rectangular surface
        tileMap2DList is a 2-D array where each item in every collumn and row is either a 1 or a 0
        1 signifies that the tile in that location is a boundary
        0 signifies that the tile in that location is not a boundary
        if an item does not have either a 1 or a 0, there will be no boundary in that specific location on the grid
        creating a bounds map overwrites any existing bounds map, so it is also a setBoundsMap() method
        also requires game so it can determine the width and height of the tiles
    """

    def createBoundsMap(self, tileMap2DList, game):
        self.tileMap = tileMap2DList
        self.boundsMap = self.tileMap

        self.numRows = len(self.tileMap)

        maxCol = 0
        for r in self.tileMap:
            for c in r:
                cLen = len(self.tileMap[c])
                if (cLen > 0):
                    maxCol = cLen
        self.numCols = maxCol

        self.tileW = round(game.getWindowWidth() / self.numCols)
        self.tileH = round(game.getWindowHeight() / self.numRows)
        r = 0
        for row in self.tileMap:
            c = 0
            for col in row:
                if (col == 1):
                    tile = pygame.Surface((self.tileW, self.tileH))
                    tile.fill((255, 0, 0))
                    self.boundsMap[r][c] = tile
                    self.numTiles += 1
                else:
                    self.boundsMap[r][c] = 0
                c += 1
            r += 1

    def isBoundsMapVisible(self):
        return self.tilesVisible

    # shows the collideable boundary rectangles over the entire map
    # if there is no tile map set, no tiles will be shown
    def showTiles(self):
        self.tilesVisible = True

    # hides collidable boundary rectangles
    # if tiles are not visible, nothing happens
    def hideTiles(self):
        self.tilesVisible = False


class Label(Sprite):
    def __init__(self, scene, text=""):
        Sprite.__init__(self, scene)

        self.text = text
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.fgColor = "black"
        self.bgColor = "white"
        self.width = 200
        self.height = 50

        #self.center = (700, 700)

    def update(self):
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bgColor)

        labelText = self.font.render(
            self.text, True, self.fgColor, self.bgColor)

        # center the text
        x = .5 * (self.displayedImgWidth - labelText.get_width())
        y = .5 * (self.displayedImgHeight - labelText.get_height())

        # blit text onto label's surface
        self.image.blit(labelText, (x, y))
        self.rect = self.image.get_rect(center=self.rect.center)

        # rotate label
        self.image = pygame.transform.rotate(self.image, self.imgAngle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.displayedImgWidth = self.rect.width
        self.displayedImgHeight = self.rect.height
        self.displayedImageCenter = self.rect.center

        # get new center location again
        self.rect.center = (self.x, self.y)
        self.displayedImageCenter = self.rect.center

    def setFont(self, font="freesansbold.ttf", size=20):
        self.font = pygame.font.Font(font, size)

    def setTextColor(self, color="black"):
        self.fgColor = color

    def setBackgroundColor(self, color="white"):
        self.bgColor = color


class Button(Label):
    def __init__(self, scene, text=""):
        Label.__init__(self, scene, text)
        self.clicked = False

    def update(self):
        Label.update(self)

        if (self.isClicked()):
            self.clicked = True

    def btnClicked(self):
        if (self.isClicked()):
            return True
        
        return False


class Sound():
    def __init__(self, filename):
        pygame.mixer.init()
        pygame.mixer.music.load(filename)

    def play(self):
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def fadeOut(self):
        pygame.mixer.music.fadeOut()


class Timer():
    def __init__(self):
        self.duration = 0
        self.startTime = 0
        self.stopTime = 0
        self.currentTime = 0
        self.elapsedTime = 0

    # resets all attributes of timer to 0 except clock and duration
    def reset(self):
        self.startTime = 0
        self.stopTime = 0
        self.currentTime = 0
        self.elapsedTime = 0

    # start timer
    def start(self):
        self.startTime = pygame.time.get_ticks()
    
    """
        stops timer
        sets current time to time when timer was stopped
        sets elapsed time to how long the timer was active in milliseconds
    """
    def stop(self):
        self.stopTime = pygame.time.get_ticks()
        self.currentTime = self.stopTime
        self.elapsedTime = self.stopTime - self.startTime

    # gets current time since start of timer
    def getCurrentTime(self):
        self.currentTime = pygame.time.get_ticks() - self.startTime
        return self.currentTime

    # creates an event after a set duration of time
    def setEventTimer(self, event, duration):
        pygame.time.set_timer(event, duration)


if __name__ == "__main__":
    # all you need to start building your game is two lines
    game = Game()
    game.start()

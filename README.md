# PyEngine Documentation
Created by Caleb Landis

# Game Engine Goals
The goal of PyEngine is to make 2D game development and organization in Python as quick and efficient as possible by extending the functionality of PyGame. PyEngine streamlines the creation of game levels by managing different aspects of a level through separate, powerful objects.

# Getting Started with PyEngine

## Dependencies 
- Python
- [PyGame](https://www.pygame.org)

## Using PyEngine
To use PyEngine, add a copy of PyEngine.py to the folder that will house your game project. Please make sure that you have PyGame installed, as that is what this engine is centered around. To make sure PyEngine is working, you can run "python3 pyengine.py" to view the sample bouncing DVD screen.

# PyEngine Classes and Methods

## Game 
Manages the game's window and its dimensions. Also keeps track of all scenes and switching between them.
Game takes no arguments upon construction.

- start()
-- Starts main loop of current scene.
- stop()
-- Stops main loop of current scene.
- addScene(sceneKey, scene)
-- Adds a scene object to dictionary of other scenes.
-- Takes a sceneKey to reference scene being inserted into dictionary.
- setCurrentScene(sceneKey)
-- Sets current scene from scenes dictionary to that of which has the same key as passed argument.
- setWindowSize(width, height)
-- Sets the window size of PyGame window.
- getWindowWidth()
-- Gets current game window width.
- getWindowHeight()
-- Gets current game window height.
- getWindowSize()
-- Returns list of window dimensions.
- setTitle(tile)
-- Sets the caption of the game window's top bar.
- goToScene(sceneKey)
-- Stops the current scene, changes current scene to whatever scene in scenes dictionary has the same key as sceneKey, and plays that scene.

## Scene 
Controls the game loop for the level that inherits from this object. Keeps track of a level's physics and its current world environment such as background, other objects, and sprites.
Inherit from Scene to take advantage of overwriting its checkEvents__ and update__ methods to organize your scene.
Takes the game instance the scene belongs to and an instance of map as arguments.

### Scene Management
- start()
-- Sets up sprite groups, game clock, and main loop.
- stop()
-- Stops scene by ending its mainloop.
- checkEvents__()
-- A method designed to be overriden by its child classes for organizing event checking and handling.
- update__()
-- A method designed to be overriden by its child classes for updating the state of the level and its sprites.
- setFramerate(framerate)
-- Sets the interval in which the in-game clock ticks.
### Group Management
- drawTiles()
-- drawTiles is automatically called within the main loop, but calling it again will ensure that the tiles set by the Scene's Map instance will be blitted to the game's surface.
- addSprite(sprite)
-- Adds a sprite instance to the list of sprites to be drawn.
- createSpriteGroup(sprites)
-- Creates a group of Sprite instances for better organization.
- addGroup(group)
-- Adds sprite group to list of groups of to be drawn each iteration of the loop.
### Map Management
- setBackgroundMap(map)
-- Takes an instance of Map as argument to set the background image of the scene.
- setMapPos(x, y)
-- sets position of background image in the scene.
### Controls
- hideCursor()
-- Hides mouse cursor.
- showCursor()
-- Shows mouse cursor.
- isMouseVisible()
-- Returns true if mouse cursor is visible, false if not.
- getMousePos()
-- Returns coordinates of mouse cursor.

## Sprite 
An actor for a in-game objects such as characters, props, and projectiles. Each sprite has its own motion and animation capabilities.
Takes the scene instance it belongs to as an argument.
Use checkEvents() to add extra functionality to sprites when inheriting from Sprite.

## Image Management and Visibility
- setImage(image)
-- Sets sprite master image. If animating the sprite, set the image to the sprite's animation sheet.
- setDisplayedImageAsMaster()
-- Sets whatever image is currently being displayed as the sprite's master image.
- crop(left, top, width, height)
-- Sets displayed image to a cropped version of master image based on the values listed as parameters.
- cropReset()
-- Sets displayed sprite image dimensions back master image's.
- scale(width, height)
-- Scales displayed image's dimensions by using width and height parameters as scalars.
- scaleBy(scalar)
-- Scales displayed image's width and height by the same scalar.
- hide()
-- Makes the sprite invisible and noncollidable.
- show()
-- Makes the sprite visible and collidable again.
- isVisible()
-- Returns true if sprite is visible, false if not.
### Animation
- createAnimation(name, numCells, cellWidth, cellHeight, cellLeft, cellTop, cellScalar)
-- Creates a sprite animation and adds it to animations dictionary using 'name' as key. 'numCells' specifies how many cell frames there will be in the animation with 'cellWidth' and 'cellHeight' as the frame's dimensions. 'cellLeft' and 'cellTop' are the coordinates of where the top left corner of the new animation image frames will start at based off of the sprite sheet set as the sprite's master image. The sprite can also be rescaled using 'cellScalar'.
- playAnimation()
-- Plays the current animation.
- pauseAnimation()
-- Stops animating the sprite at the current cell frame.
- resetAnimation()
-- Sets the animation back to the first cell frame.
- setAnimationSpeed(speed, animationTickSpeed)
-- 'speed' specifies how many animation ticks to wait until moving to the next animation frame. 'animationTickSpeed' sets the speed of these ticks.
- setCurrentAnimation(name)
-- Sets the current animation to one with the same value as 'name' key in animations dictionary.
### Motion and Position
- setSpeed(speed)
-- Sets speed to 'speed'.
- speedUp(amount)
-- Adds amount to speed.
- setPostion(position)
-- Sets positions to (x, y) coordinates.
- setX(x)
-- Sets sprite's x position to 'x'.
- setY(y)
-- Sets sprite's x position to 'x'.
- setImgAngle(angle)
-- Sets only the displayed image's rotation angle to 'angle' given in degrees.
- rotateImg(angle)
-- Adds 'angle' to displayed image's rotation angle given in degrees.
- setMoveAngle(angle)
-- Sets the directional angle in which the sprite will move to 'angle'.
- setDX(dx)
-- Sets sprite's change in x to 'dx'.
- setDY(dy)
-- Sets sprite's change in y to 'dy'.
- addDX(amount)
-- Add's 'amount' to sprite's change in x.
- addDY(amount)
-- Add's 'amount' to sprite's change in y.
- moveBy(dx, dy)
-- Moves sprite horizontally and vertically by 'dx' and 'dy' amounts.
- moveForward(amount)
-- Moves the sprite in the direction of its move angle by 'amount'.
- setMotionVector(speed, angle)
-- Sets sprite's speed and movement angle.
- addForce(amount, angle)
-- Changes sprite's change in x and y by 'amount' at specified angle.
### Bounds and Collisions
- setBoundAction(action)
-- Sets action for window and boundary tile collisions.
Values are:
self.WRAP (wrap around edge - default)
self.BOUNCE (bounce off screen changing direction)
self.STOP (stop at edge of screen)
self.HIDE (move off-stage and stop)
self.CONTINUE (move on forever)
Any other value allows the sprite to move on forever
- checkBounds()
-- Checks to see if sprite is colliding with any tiles or the edge of the game window. The sprite will react according to its bound action.
- collidesWith(sprite)
-- Returns true if this sprite is colliding with 'sprite'.
- collidesWithGroup(group)
-- Returns true if this sprite is colliding with any of the sprites in 'group'.
- isCollidable()
-- Returns true if the sprite is collidable.
### Extra Utilities
- isPressed()
-- Returns true if the mouse cursor is over the sprite and left mouse button is pressed down.
- isClicked()
-- Returns true if the mouse cursor is over the sprite and left mouse button has been pressed and released.
- distanceToPoint(point)
-- Returns the distance from sprite's position to (x,y) 'point'.
- angleToPoint(point)
-- Returns the angle from sprite's position to (x,y) 'point'.

## Map 
Contains the background and world design for a scene. Map also creates rectangular tile-maps for boundaries and collisions through a user inputted 2-D array.
Map takes no arguments upon construction.

- setMapImage(image)
-- Sets map's background image to 'image'.
- createBoundsMap(tileMap@DList, game)
-- Creates a grid of boundary tiles where each tile is a rectangular PyGame surface. 'tileMap2DList' is a 2-D array where each item in every collumn and row is either a 1 or a 0. 1 signifies that the tile in that location is a boundary. 0 signifies that the tile in that location is not a boundary. Also requires game instance so it can determine the width and height of the tiles.
- isBoundsMapVisible()
-- Returns true if the tiles are visible.
- showTiles()
-- Makes the tiles in bounds map visible.
- hideTiles()
-- Makes the tiles in bounds map invisible.

## Sound 
PyEngine's sound class simplifies playing sounds by extending PyGame's mixer object.
Sound takes the filename of the audio file as its only argument upon construction.

- play()
-- Plays the sound once.
- stop()
-- Stops playing the sound.
- fadeOut()
-- Fades out the sound. Great for long music sounds.

## Timer 
Like Sound, Timer makes using PyGame's time objects much simpler and easier. Timer keeps track of when the timer started as well as where it ended. You can also see how much time has passed since the start of the timer.
Timer takes no arguments upon construction.

- reset()
-- Resets timer's start time, stop time, current time, and elapsed time.
- start()
-- Sets the start time of the timer.
- stop()
-- Sets the stop time of the timer and calculates elapsed time.
- getcurrentTime()
-- Returns current time since timer started.
- setEventTimer(event, duration)
-- Sets an event to happen after a 'duration' of time has passed.

## PyEngine's UI Classes
PyEngine also has Label and Button classes for displaying information to the player as well as adding an extra method for user input.

### Label
Takes scene instance it belongs to and the text to display as arguments. Label inherits from Sprite, so it can be used as such.

- setFont(font)
-- Sets label text's font.
- setTextColor(color)
-- Sets label text's color.
- setBackgroundColor(color)
-- Set label's background color.

### Button
Takes scene instance it belongs to and the text to display as arguments. Label inherits from Sprite, so it can be used as an enhance sprite and label.

- btnClicked()
-- Returns true if button has been clicked.

import pyEngine, pygame
pygame.init()


class startScene(pyEngine.Scene):
    def __init__(self, game):
        self.game = game
        map = pyEngine.Map()
        map.setMapImage("stadium.jpeg")
        pyEngine.Scene.__init__(self, game, map)

        label = pyEngine.Label(self, "pyEngine Runner")
        label.setPosition(((.5 * game.getWindowWidth()), 200))
        label.setTextColor("white")
        label.setBackgroundColor("#23637e")
        self.addSprite(label)

        self.button = pyEngine.Button(self, "Start Game")
        self.button.setPosition(((.5 * game.getWindowWidth()), (.5 * game.getWindowHeight())))
        self.addSprite(self.button)

    def checkEvents__(self, event):
        if (self.button.btnClicked()):
            self.game.goToScene("gameScene")

class gameScene(pyEngine.Scene):
    def __init__(self, game):
        map = pyEngine.Map()
        map.setMapImage("track.jpeg")

        # example of a fully fleshed out tileMap
        #tileMap = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #           [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        #           [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        #           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # bounds map for floor for this game
        tileMap = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        map.createBoundsMap(tileMap, game)
        #map.showTiles()

        pyEngine.Scene.__init__(self, game, map)


        self.runner = pyEngine.Sprite(self)
        self.runner.setImage("runnerSpritesheet.png")
        self.runner.setPosition((150, 520))
        self.runner.setSpeed(0)
        self.runner.setMoveAngle(90)
        self.runner.setBoundAction(pyEngine.STOP)
        self.runner.createAnimation("running", 9, 64, 64, 0, 705, 2)
        self.runner.setCurrentAnimation("running")
        self.runner.playAnimation()
        self.addSprite(self.runner)

        self.hurdle = pyEngine.Sprite(self)
        self.hurdle.setImage("hurdle.png")
        self.hurdle.setPosition((900, 540))
        self.hurdle.setSpeed(15)
        self.hurdle.setMoveAngle(180)
        self.addSprite(self.hurdle)

        self.score = 0
        self.addScore = True
        self.scoreLabel = pyEngine.Label(self, "Score: {}".format(self.score))
        self.scoreLabel.setPosition((200, 200))
        #self.addSprite(self.scoreLabel)

        self.gameOverLabel = pyEngine.Label(self, "Game Over!")
        self.gameOverLabel.setPosition((500, 200))
        self.gameOverLabel.hide()
        self.addSprite(self.gameOverLabel)
        
        self.tileGroup = self.createSpriteGroup(self.tiles)
        
        self.jumpSound = pyEngine.Sound("Jump.wav")

        self.end = False
        self.init = False

    def checkEvents__(self, event):
        if self.end == False:
            keys = pygame.key.get_pressed()
            if self.runner.y >= 520:
                if keys[pygame.K_SPACE]:
                    self.runner.addDY(-6)
                    self.jumpSound.play()

            if self.hurdle.collidesWithGroup(self.tileGroup and self.addScore):
                print("collided tiles")
                self.score += 1
                self.scoreLabel.text = "Score: {}".format(self.score)
                self.addScore = False

            if (self.hurdle.x > 800):
                self.addScore = True

            
            if self.runner.collidesWith(self.hurdle):
                self.gameOverLabel.show()

            self.init = True

    def update__(self):
        # runner gravity
        if (self.runner.y < 520):
            self.runner.addDY(.65)
        self.scoreLabel.text = "Score: {}".format(self.score)

def main():
    game = pyEngine.Game()
    game.setTitle("pyEngine Runner")

    start = startScene(game)
    scene = gameScene(game)

    game.addScene("startScene", start)
    game.addScene("gameScene", scene)

    game.setCurrentScene("startScene")
    game.start()

if __name__ == "__main__":
    main()
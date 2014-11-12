import os, sys
import pygame

from box import *
from image import *
from level import *
from lifeCounter import *
from colour import *

class App():
    def __init__( self ):
        # Initialise PyGame
        pygame.init()
        pygame.mixer.init( frequency=20050, size=16, channels=2, buffer=2048 )

        # Create window
        self.size = width, height = 640, 480
        self.screen = pygame.display.set_mode( self.size )
        pygame.display.set_caption("Blue | GGJ 2014 | The Stuck Pixels")

        # Life counter
        self.lives = 3
        self.lifeCounter = LifeCounter()

        #Death
        self.deathSound = pygame.mixer.Sound("sound/Death.wav")
        self.finishSound = pygame.mixer.Sound("sound/Finish.wav")

        # Clock for FPS limit
        self.clock = pygame.time.Clock()

        #Sprite
        self.box1 = Box( blue, self.screen.get_rect().center )

        # Final screen
        self.finalImage = Image( "img/final.bmp", (0,0) )
        self.gameOverImage = Image( "img/gameOver.bmp", (0,0) )

        # Dictionary for key states
        self.kState = { pygame.K_UP:False }

    def Game( self, levelNum ):
        self.box1 = Box( blue, self.screen.get_rect().center )
        self.lvl = Level( "lvl/%s.bmp" % (levelNum), levelNum )

        # Main loop
        while True:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.kState[event.key] = True
                if event.type == pygame.KEYUP:
                    self.kState[event.key] = False

            # Update physics & handle input
            try:
                self.box1.Update( self.kState, self.lvl )
                self.lvl.Update( self.kState )
                self.lifeCounter.Update( self.lives )
            except KeyError:
                if self.box1.isDead:
                    if self.lives > 1:
                        self.lives -= 1
                        pygame.mixer.Sound.play( self.deathSound )
                        self.Game( levelNum )
                    else:
                        self.GameOver()
                        pygame.quit()
                        sys.exit()
                else:
                    pygame.mixer.Sound.play( self.finishSound )
                    pygame.time.wait( 500 )
                    return

            # Limit FPS
            self.clock.tick( 60 )

            # Clear screen
            self.screen.fill( black )

            # Render items
            self.lvl.Render( self.screen )
            self.box1.Render( self.screen )
            self.lifeCounter.Render( self.screen )

            # Display changes
            pygame.display.flip()
    def Final( self ):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill( black )
            self.finalImage.Render( self.screen )
            pygame.display.flip()
    def GameOver( self ):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.mixer.Sound.play( self.deathSound )
            self.screen.fill( black )
            self.gameOverImage.Render( self.screen )
            pygame.display.flip()


if __name__ == "__main__":
    fileList = os.listdir( "lvl/" )
    app = App()
    for i in xrange( 1, len( fileList ) ):
        if len( str( i ) ) == 1:
            app.Game( "0%d" % (i) )
        else:
            app.Game( "%d" % (i) )
    app.Final()

#    Main()

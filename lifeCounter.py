import pygame, sys
from image import *
from colour import *

# Box class, image-less sprite
class LifeCounter( pygame.sprite.Sprite ):
    def __init__( self ):
        # Subclass sprite
        pygame.sprite.Sprite.__init__( self )

        # Load image
        self.heart = Image( "img/heart.bmp", (16,16) )
        self.heart.Move( (-self.heart.rect.w,0 ) )

        # Number of lives to display
        self.lives = 3

    # Render to dest
    def Render( self, dest ):
        for i in range( 0, self.lives ):
            self.heart.Move( (self.heart.rect.w+4,0) )
            self.heart.Render( dest )
        for i in range( 0, self.lives ):
            self.heart.Move( (-(self.heart.rect.w+4),0) )

    # Update state
    def Update( self, lives ):
        self.lives = lives

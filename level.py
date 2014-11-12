import pygame

from colour import *

class Level( pygame.sprite.Sprite ):
    def __init__( self, filename, lNum, pos=(0,0), colKey=magicPink ):
        # Subclass sprite
        pygame.sprite.Sprite.__init__( self )

        # Load image
        try:
            self.image = pygame.image.load( filename ).convert()
        except pygame.error, message:
            print "Error: Cannot load image: %s" % (filename)
            raise SystemExit

        # Colour key image, create transparent areas
        if colKey != None:
            self.image.set_colorkey( colKey, pygame.RLEACCEL )

        # Get bounding box
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Zero velocity
        self.xVel = 0
        self.yVel = 0

        self.num = int(lNum)

    # Displace by delta
    def Move( self, delta ):
        self.rect = self.rect.move( delta[0], delta[1] )

    # Render to dest at pos
    def Render( self, dest ):
        dest.blit( self.image, self.rect )

    # Update state
    def Update( self, kState ):
        try:
            if kState[pygame.K_LEFT]:
                self.xVel = 5
        except KeyError:
            pass
        try:
            if kState[pygame.K_RIGHT]:
                self.xVel = -5
        except KeyError:
            pass

        fric = 0.3
        self.xVel = self.xVel-fric if self.xVel > 0 else self.xVel+fric
        self.Move( (self.xVel,self.yVel) )

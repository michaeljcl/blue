import pygame

from colour import *

class Image( pygame.sprite.Sprite ):
    def __init__( self, filename, pos, colKey=magicPink ):
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

    # Displace by delta
    def Move( self, delta ):
        self.rect = self.rect.move( delta[0], delta[1] )

    # Render to dest at pos
    def Render( self, dest ):
        dest.blit( self.image, self.rect )

import pygame

from color import magicPink

class SpriteSheet():
    def __init__( self, filename ):
        try:
            self.sheet = pygame.image.load( filename ).convert()
        except pygame.error, message:
            print "Error: Could not load: %s" % (filename)
            raise SystemExit
        self.frame = 0
        self.rect = self.sheet.get_rect()
    def Image( self, index, colKey=magicPink ):
        rect = pygame.Rect( (32*index-32,0,32,32) )
        image = pygame.Surface( rect.size ).convert()
        image.blit( self.sheet, (0,0), rect )
        if colKey != None:
            if colKey == -1:
                colKey = image.get_at( (0,0) )
            image.set_colorkey( colKey, pygame.RLEACCEL )
        return image
    def Next( self ):
        self.frame += 1
        if self.frame == self.rect.right/32:
            self.frame = 1
        print (32*self.frame-32,0,32,32)
        return self.Image( self.frame )
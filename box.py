import pygame, sys
from colour import *

# Box class, image-less sprite
class Box( pygame.sprite.Sprite ):
    def __init__( self, colour, pos, size=(32,32) ):
        # Subclass sprite
        pygame.sprite.Sprite.__init__( self )

        # Create box
        self.image = pygame.Surface( size )
        self.image.fill( colour )
        self.image.set_colorkey( magicPink, pygame.RLEACCEL )

        # Initialize PyGame Audio and Allocation
        pygame.mixer.init(frequency=20050, size=-16, channels=2, buffer=2048)
        self.jumpSound = pygame.mixer.Sound("sound/Jump.wav")

        # Move to position
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Clipping mask
        self.mask = pygame.mask.from_surface( self.image )


        # Zero velocity
        self.xVel = 0
        self.yVel = 0

        # State variables
        self.isDead = False
        self.canJump = False

        # Physics values
        self.jumpStr = 10
        self.fric = 0.3
        self.grav = 0.5

    # Displace box by delta
    def Move( self, delta ):
        self.rect = self.rect.move( delta[0], delta[1] )

    # Render to dest
    def Render( self, dest ):
        dest.blit( self.image, self.rect )

    # Update state
    def Update( self, kState, lvl ):
        # This is messy
        try:
            if kState[pygame.K_UP] and self.canJump:
                pygame.mixer.Sound.play(self.jumpSound)
                self.yVel -= self.jumpStr
                self.canJump = False
        except KeyError:
            pass
        try:
            if kState[pygame.K_SPACE] and self.canJump:
                pygame.mixer.Sound.play(self.jumpSound)
                self.yVel -= self.jumpStr
                self.canJump = False
        except KeyError:
            pass

        fric = self.fric
        # Bring xVel friction amount closer to zero
        self.xVel = self.xVel-fric if self.xVel > 0 else self.xVel+fric
        # Apply x velocity to actual position
        self.Move( (self.xVel,0) )

        # If at end of level, gravity is flipped
        grav = self.grav if lvl.rect.x > -(lvl.rect.w-400) else -self.grav
        # Accelerate downwards
        self.yVel += grav
        # Apply gravity
        self.Move( (0,self.yVel) )

        # Collision detection
        # Generate mask from lvl image, overlap it with mask of player
        lvlMask = pygame.mask.from_surface( lvl.image )
        offsetX = lvl.rect.x - self.rect.x
        offsetY = lvl.rect.y - self.rect.y
        # If overlap
        if self.mask.overlap( lvlMask, (offsetX, offsetY) ):
            # Get the mask of the overlap
            self.yVel = 0
            area = self.mask.overlap_mask( lvlMask, (offsetX, offsetY) )
            rect = area.get_bounding_rects()
            # Move Blue up by the height of the overlap + the height of blue
            if len(rect) > 0:
                rect = rect[0]
                self.Move( (0,rect.y-32) )
                self.canJump = True # Enable jumping

        # Level end conditions
        if self.rect.y > 480: # Death
            self.isDead = True
            raise KeyError
        if self.rect.y < -128: # Winner
            self.isDead = False
            raise KeyError
        if lvl.num == 20:
            if lvl.rect.x < -1150:
                self.isDead = False
                raise KeyError
        return

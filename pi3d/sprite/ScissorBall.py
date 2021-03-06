import ctypes
from numpy import dot

from pi3d.constants import *

from pi3d.sprite.Ball import Ball
from pi3d.Display import Display

class ScissorBall(Ball):
  """ This class is basically the same as pi3d.sprite.Ball but uses glScissor
  to only render the small area of Display around itself
  """
  def __init__(self, camera=None, light=None, shader=None, texture=None,
               radius=0.0, x=0.0, y=0.0, z=1000, vx=0.0, vy=0.0, decay=0.001):
    super(ScissorBall, self).__init__(camera=camera, light=light, shader=shader,
        texture=texture, radius=radius, x=x, y=y, z=z, vx=vx, vy=vy, decay=decay)
    self.w = 2.0 * radius
    self.h = 2.0 * radius
    self.or_x = Display.INSTANCE.width / 2.0 # coord origin
    self.or_y = Display.INSTANCE.height / 2.0
    opengles.glEnable(GL_SCISSOR_TEST)

  def repaint(self, t):
    self.move()
    self.bounce_wall(Display.INSTANCE.width, Display.INSTANCE.height)
    if t == 0: #TODO this is not good but there needs to be a way to say last ball!
      opengles.glScissor(0, 0, ctypes.c_int(int(Display.INSTANCE.width)), 
                        ctypes.c_int(int(Display.INSTANCE.height)))
      #NB the screen coordinates for glScissor have origin in BOTTOM left
    else:
      opengles.glScissor(ctypes.c_int(int(self.or_x + self.unif[0] - self.radius - 5)),
                        ctypes.c_int(int(self.or_y + self.unif[1] - self.radius - 5)),
                        ctypes.c_int(int(self.w + 10)), ctypes.c_int(int(self.h + 10)))
    self.draw()

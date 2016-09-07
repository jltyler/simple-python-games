import pyglet
import math

# Global variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHIP_MAX_SPEED = 1200.0
SHIP_MAX_SPEED_2 = SHIP_MAX_SPEED ** 2
SHIP_ACCELERATION = 50.0
SHIP_FRICTION = 10.0

# Other globals
BATCH = pyglet.graphics.Batch()
GROUP_FORE = pyglet.graphics.Group(0)
ship_image = pyglet.resource.image("ship.png")

# Class definitions
class Vector2():
	"""Wraps an x, y, and some useful calculations"""
	def __init__(self, x = 0.0, y = 0.0):
		self.x = x
		self.y = y

	# Get magnitude (length) of vector
	def get_mag(self):
		return math.hypot(self.x, self.y)

	# Get magnitude (length) of vector squared
	def get_mag2(self):
		return ((self.x ** 2) + (self.y ** 2))

	# Set magnitude of vector
	def set_mag(self, s_mag = 0.0):
		mag = math.hypot(self.x, self.y)
		if mag == 0:
			self.x = s_mag
		else:
			self.x = (self.x / mag) * s_mag
			self.y = (self.y / mag) * s_mag

	# Set direction and magnitude
	def set_dir_mag(self, s_dir, s_mag = 1.0):
		s_dir = math.radians(s_dir)
		self.x = math.cos(s_dir) * s_mag
		self.y = math.sin(s_dir) * s_mag

	# Resize if longer than max_mag
	def clamp(self, max_mag):
		if self.get_mag2() > max_mag * max_mag:
			self.set_mag(max_mag)

	# Subtract s_sub pixels from length
	def subtract(self, s_sub):
		mag = math.hypot(self.x, self.y)
		if mag < s_sub or mag == 0:
			self.x = 0
			self.y = 0
			return
		multi = (mag - s_sub) / mag
		self.x *= multi
		self.y *= multi

class Ship(pyglet.sprite.Sprite):
	"""Player class"""
	def __init__(self, x, y):
		pyglet.sprite.Sprite.__init__(self, ship_image)
		self.x = x
		self.y = y
		self.speed = Vector2()
		self.accel = Vector2()

	def update(self, dt):
		# Check for acceleration and apply friction if no acceleration
		if self.accel.x == 0 and self.accel.y == 0:
			self.speed.subtract(SHIP_FRICTION * dt)
		else:
			# clamp acceleration at 1 pixel length
			self.accel.clamp(1.0)
			self.speed.x += self.accel.x * SHIP_ACCELERATION * dt
			self.speed.y += self.accel.y * SHIP_ACCELERATION * dt
			self.speed.clamp(SHIP_MAX_SPEED)

		self.x += self.speed.x
		self.y += self.speed.y

		# Wrap if over edge
		if self.x < 0:
			self.x += SCREEN_WIDTH
		elif self.x > SCREEN_WIDTH:
			self.x -= SCREEN_WIDTH
		if self.y < 0:
			self.y += SCREEN_HEIGHT
		elif self.y > SCREEN_HEIGHT:
			self.y -= SCREEN_HEIGHT

		
WINDOW = pyglet.window.Window(width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
PLAYER = None

@WINDOW.event
def on_key_press(key, mods):
	if key == pyglet.window.key.UP:
		PLAYER.accel.y += 1
	elif key == pyglet.window.key.DOWN:
		PLAYER.accel.y -= 1
	elif key == pyglet.window.key.RIGHT:
		PLAYER.accel.x += 1
	elif key == pyglet.window.key.LEFT:
		PLAYER.accel.x -= 1

@WINDOW.event
def on_key_release(key, mods):
	if key == pyglet.window.key.UP:
		PLAYER.accel.y -= 1
	elif key == pyglet.window.key.DOWN:
		PLAYER.accel.y += 1
	elif key == pyglet.window.key.RIGHT:
		PLAYER.accel.x -= 1
	elif key == pyglet.window.key.LEFT:
		PLAYER.accel.x += 1

@WINDOW.event
def on_draw():
	WINDOW.clear()
	BATCH.draw()
	PLAYER.draw()


ASTEROID_LIST = []
BULLET_LIST = []

def game_setup():
	global PLAYER
	PLAYER = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

def game_update(dt):
	PLAYER.update(dt)


game_setup()

pyglet.clock.schedule(game_update)
pyglet.app.run()
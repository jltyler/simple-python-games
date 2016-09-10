import pyglet
import math

# Global variables
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SHIP_MAX_SPEED = 600.0
SHIP_MAX_SPEED_2 = SHIP_MAX_SPEED ** 2
SHIP_ACCELERATION = 450.0
SHIP_FRICTION = 200.0
SHIP_ROTATION = 215.0
SHIP_FIRE_RATE = 0.35

BULLET_SPEED = 750.0
BULLET_INHERIT = 1.0
BULLET_LIST = []

# Other globals
BATCH = pyglet.graphics.Batch()
GROUP_FORE = pyglet.graphics.Group(1) # Using groups is crashing for some reason so this is unused

# Set up ship sprite
ship_image = pyglet.image.load("ship.png")
ship_image.anchor_x = ship_image.width // 2
ship_image.anchor_y = ship_image.height // 2
# Set up bullet sprite
bullet_image = pyglet.image.load("bullet.png")
bullet_image.anchor_x = bullet_image.width // 2
bullet_image.anchor_y = bullet_image.height // 2
# Set up asteroid sprite
asteroid_image = pyglet.image.load("asteroid.png")
asteroid_image.anchor_x = asteroid_image.width // 2
asteroid_image.anchor_y = asteroid_image.height // 2

# Class definitions

# Vector class to help with movement
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

class Bullet(pyglet.sprite.Sprite):
	"""Bullet fired from ship. Travels in one direction at a constant speed"""
	def __init__(self, x, y, angle, speed):
		super().__init__(bullet_image, batch = BATCH)
		self.x = x
		self.y = y
		self.rotation = angle
		# set speed upon construction
		self.speed_x = math.cos(math.radians(angle)) * speed
		self.speed_y = math.sin(math.radians(angle)) * speed
		self.garbage = False

	def update(self, dt):
		# update position
		self.x += self.speed_x * dt
		# NEGATIVE Y BECAUSE INCONSISTENCY
		self.y -= self.speed_y * dt

		# check if out of bounds
		if (self.x < -32 or self.x > SCREEN_WIDTH + 32 or
			self.y < -32 or self.y > SCREEN_HEIGHT + 32):
			self.garbage = True
		

# Player controlled ship that moves around
class Ship(pyglet.sprite.Sprite):
	"""Player class"""
	def __init__(self, x, y):
		super().__init__(ship_image, batch = BATCH)
		self.x = x
		self.y = y
		self.speed = Vector2()
		# Calculate halves just once
		self.half_width = self.width//2
		self.half_height = self.height//2
		# Controls
		self.accelerating = 0
		self.rotating = 0
		self.firing = False
		# Fire rate (bullet) timer
		self.btimer = 0

	def update(self, dt):
		# Check for acceleration and apply friction if no acceleration
		if self.accelerating != 0:
			self.accelerate(self.accelerating * dt)
		else:
			self.speed.subtract(SHIP_FRICTION * dt)

		# check for rotation
		if self.rotating != 0:
			self.rotation += SHIP_ROTATION * dt * self.rotating

		# Add speed vector to position
		self.x += self.speed.x * dt
		self.y += self.speed.y * dt

		# Wrap if entirely over edge
		if self.x + self.half_width < 0:
			self.x += SCREEN_WIDTH + self.width
		elif self.x > SCREEN_WIDTH + self.half_width:
			self.x -= SCREEN_WIDTH + self.width
		if self.y + self.half_height < 0:
			self.y += SCREEN_HEIGHT + self.height
		elif self.y > SCREEN_HEIGHT + self.half_height:
			self.y -= SCREEN_HEIGHT + self.height

		# Check for firing and refire timer
		# Check if able to fire
		if self.btimer <= 0:
			if self.firing:
				b = Bullet(self.x, self.y, self.rotation, + BULLET_SPEED) # + (self.speed.get_mag() * BULLET_INHERIT)
				BULLET_LIST.append(b)
				self.btimer = SHIP_FIRE_RATE
		else:
			self.btimer -= dt


	def accelerate(self, multi):
		# Add acceleration vector to speed vector
		self.speed.x += math.cos(math.radians(self.rotation)) * (SHIP_ACCELERATION * multi)
		# Negative Y because of backwards thinking library devs
		# (pyglet does clockwise rotation whereas normal trig uses counter-clockwise rotation)
		# Honestly unfathomable why someone would write it different from the norm
		self.speed.y -= math.sin(math.radians(self.rotation)) * (SHIP_ACCELERATION * multi)
		# Limit max speed
		self.speed.clamp(SHIP_MAX_SPEED)


# Create player var ahead of time so I can reference it
PLAYER = None
# Make pyglet window
WINDOW = pyglet.window.Window(width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
# Label to draw FPS and pther debug stuff
LABEL = pyglet.text.Label('LABELLOL', 'Courier New', 14.0,
	True, False, (255, 255, 255, 255), 5, SCREEN_HEIGHT - 5,
	SCREEN_WIDTH - 10, anchor_y = 'top', multiline = True, batch = BATCH)

# Function to change the label text on each draw
def update_label():
	LABEL.text = 'FPS: {:.1f}'.format(pyglet.clock.get_fps())
	LABEL.text += '\nPlayer: {:.2f}, {:.2f} Speed: {:.2f}, {:.2f} ({:.2f})'.format(PLAYER.x, PLAYER.y, PLAYER.speed.x, PLAYER.speed.y, PLAYER.speed.get_mag())
	LABEL.text += '\nTotal Bullets: {}'.format(len(BULLET_LIST))

# Hooks
# Left right controls are reversed because stupid pyglet does clockwise rotation
@WINDOW.event
def on_key_press(key, mods):
	if key == pyglet.window.key.UP:
		PLAYER.accelerating += 1
	elif key == pyglet.window.key.DOWN:
		PLAYER.accelerating -= 1
	elif key == pyglet.window.key.RIGHT:
		PLAYER.rotating += 1
	elif key == pyglet.window.key.LEFT:
		PLAYER.rotating -= 1
	elif key == pyglet.window.key.Z:
		PLAYER.firing = True

@WINDOW.event
def on_key_release(key, mods):
	if key == pyglet.window.key.UP:
		PLAYER.accelerating -= 1
	elif key == pyglet.window.key.DOWN:
		PLAYER.accelerating += 1
	elif key == pyglet.window.key.RIGHT:
		PLAYER.rotating -= 1
	elif key == pyglet.window.key.LEFT:
		PLAYER.rotating += 1
	elif key == pyglet.window.key.Z:
		PLAYER.firing = False

@WINDOW.event
def on_draw():
	WINDOW.clear()
	BATCH.draw()
	PLAYER.draw()
	update_label()

def game_setup():
	global PLAYER
	PLAYER = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Main loop
def game_update(dt):
	PLAYER.update(dt)
	i = 0
	while i < len(BULLET_LIST):
		b = BULLET_LIST[i]
		# check and delete garbage before updating
		if b.garbage:
			BULLET_LIST.pop(i)
			continue
		else:
			b.update(dt)
			i += 1
			continue


game_setup()

pyglet.clock.schedule(game_update)
pyglet.app.run()
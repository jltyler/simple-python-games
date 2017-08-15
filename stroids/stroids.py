import pyglet
import math
import random

# Global variables and settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
DEBUG_PRINTOUT = False
RESPAWN_WAIT = 3.0
RESPAWN_TIMER = RESPAWN_WAIT
RESTART = False

SHIP_MAX_SPEED = 650.0
SHIP_MAX_SPEED_2 = SHIP_MAX_SPEED ** 2
SHIP_ACCELERATION = 420.0
SHIP_FRICTION = 80.0
SHIP_ROTATION = 225.0
SHIP_FIRE_RATE = 0.20

SCORE = 0
ACCURACY = 0
ACCURACY_MULTIPLER = 5.0
SHOTS_FIRED = 0
SHOTS_HIT = 0

BULLET_SPEED = 800.0
BULLET_INHERIT = 1.0
global BULLET_LIST
BULLET_LIST = []

ASTEROID_MAX_SPEED = 175.0
ASTEROID_MIN_SPEED = 25.0
ASTEROID_MAX_SPIN = 400.0
ASTEROID_MIN_SPIN = 45.0
ASTEROID_MED_SPEED = 1.4
ASTEROID_SMALL_SPEED = 2.1
ASTEROID_SCORE = 5

ASTEROID_LIST = []
MAX_ASTEROIDS = 30
SPAWN_WAIT_MIN = 0.9
SPAWN_WAIT_MAX = 3.0
SPAWN_TIMER = SPAWN_WAIT_MIN

# Other globals
BATCH = pyglet.graphics.Batch()
GROUP_FORE = pyglet.graphics.Group(1) # Using groups is crashing for some reason so this is unused

# Set up ship sprite
ship_image = pyglet.image.load("ship.png")
ship_image.anchor_x = ship_image.width // 2
ship_image.anchor_y = ship_image.height // 2
SHIP_RADIUS = ship_image.anchor_x
# adding a bit of radius to be generous about collisions
SHIP_RADIUS2 = (SHIP_RADIUS+7) ** 2

# Set up bullet sprite
bullet_image = pyglet.image.load("bullet.png")
bullet_image.anchor_x = bullet_image.width // 2
bullet_image.anchor_y = bullet_image.height // 2
BULLET_RADIUS = bullet_image.anchor_x
BULLET_RADIUS2 = (BULLET_RADIUS + 4) ** 2

# Set up asteroid sprites
asteroid_image = pyglet.image.load("asteroid.png")
asteroid_image.anchor_x = asteroid_image.width // 2
asteroid_image.anchor_y = asteroid_image.height // 2
asteroid_image.half_width = asteroid_image.width // 2
asteroid_image.half_height = asteroid_image.height // 2
ASTEROID_RADIUS = asteroid_image.half_width
ASTEROID_RADIUS2 = [None, None, None, ASTEROID_RADIUS ** 2]

asteroid_med_image = pyglet.image.load("asteroid_med.png")
asteroid_med_image.anchor_x = asteroid_med_image.width // 2
asteroid_med_image.anchor_y = asteroid_med_image.height // 2
ASTEROID_MED_RADIUS2 = asteroid_med_image.anchor_x ** 2
ASTEROID_RADIUS2[2] = ASTEROID_MED_RADIUS2

asteroid_small_image = pyglet.image.load("asteroid_small.png")
asteroid_small_image.anchor_x = asteroid_small_image.width // 2
asteroid_small_image.anchor_y = asteroid_small_image.height // 2
ASTEROID_SMALL_RADIUS2 = asteroid_small_image.anchor_x ** 2
ASTEROID_RADIUS2[1] = ASTEROID_SMALL_RADIUS2

# STEALING JOHN'S WORK AND NOT GIVING HIM CREDIT xDDDDD
def sprite_sheet_anim(sprite_sheet, rows, columns, period=0.05, loop=True):
	"""Pass it a sprite sheet, how many rows and columns the sheet has, a period for frames,
		and if the animation loops; returns a Sprite of the sheet animation if return_what is 1,
		returns an animation image if return_what is 0."""
	return pyglet.image.Animation.from_image_sequence(pyglet.image.ImageGrid(sprite_sheet, rows, columns), period, loop)

explosion_big_sheet = pyglet.image.load("explosion_big.png")
explosion_big_anim = sprite_sheet_anim(explosion_big_sheet, 1, 8, 0.1, False)

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

	# Multiply length
	def scale(self, s_scale):
		self.x *= s_scale
		self.y *= s_scale

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

class Asteroid(pyglet.sprite.Sprite):
	"""Asteroid to shoot. Asteroids will have the collision checking"""
	def __init__(self, x, y, angle, speed, size = 3):
		super().__init__(asteroid_image, batch = BATCH)
		self.x = x
		self.y = y
		# 3 = big asteroid
		self.size = size
		self.speed = Vector2()
		self.speed.set_dir_mag(angle, speed)
		# Increase speed for smaller roids
		if size == 2:
			self.speed.scale(random.uniform(1.0, ASTEROID_MED_SPEED))
			self.image = asteroid_med_image
		elif size == 1:
			self.speed.scale(random.uniform(ASTEROID_MED_SPEED, ASTEROID_SMALL_SPEED))
			self.image = asteroid_small_image
		self.garbage = False
		# Some random spin
		self.spin = random.uniform(ASTEROID_MIN_SPIN, ASTEROID_MAX_SPIN - ASTEROID_MIN_SPIN)
		self.spin *= random.choice([1, -1])

	def update(self, dt):
		self.x += self.speed.x * dt
		self.y += self.speed.y * dt

		self.rotation += self.spin * dt

		# Wrap if entirely over edge
		if self.x + asteroid_image.width < 0:
			self.x = SCREEN_WIDTH + self.width
		elif self.x > SCREEN_WIDTH + self.width:
			self.x = -self.width
		if self.y + asteroid_image.height < 0:
			self.y = SCREEN_HEIGHT + self.height
		elif self.y > SCREEN_HEIGHT + self.height:
			self.y = -self.height

		# Bullet collisions
		for b in BULLET_LIST:
			if b.garbage: continue
			# Get x,y difference
			diff_x = b.x - self.x
			diff_y = b.y - self.y
			# Check distance
			if diff_x ** 2 + diff_y ** 2 < ASTEROID_RADIUS2[self.size] + BULLET_RADIUS2:
				global SHOTS_HIT, ACCURACY, SCORE
				# hit
				SHOTS_HIT += 1
				ACCURACY = SHOTS_HIT / SHOTS_FIRED
				# mediums are worth 2x base score and small worth 3x base score
				# then multiplied by accuracy and flat multiplier
				points = (ASTEROID_SCORE + (3 - self.size) * ASTEROID_SCORE) * max(1.0, ACCURACY * ACCURACY_MULTIPLER)
				# >80% accuracy = double score
				if ACCURACY > 0.8:
					points *= 2
				SCORE += round(points)
				if self.size >= 2:
					spawn_asteroid(self.x, self.y, self.size - 1)
					spawn_asteroid(self.x, self.y, self.size - 1)
				if self.size == 2:
					spawn_asteroid(self.x, self.y, self.size - 1)
				self.garbage = True
				b.garbage = True

		# Ship collision
		diff_x = PLAYER.x - self.x
		diff_y = PLAYER.y - self.y
		if not PLAYER.dead and diff_x ** 2 + diff_y ** 2 < ASTEROID_RADIUS2[self.size] + SHIP_RADIUS2:
			self.garbage = True
			PLAYER.death()

# Helper to tidy things a bit
def spawn_asteroid(x = None, y = None, size=None):
	spawn_x = x
	spawn_y = y
	spawn_angle = random.randrange(360)
	spawn_speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED - ASTEROID_MIN_SPEED)

	# You can use size paramter to force a certain size
	if size == None:
		size = random.randrange(0, 100)
		if size > 95:
			size = 1
		elif size > 85:
			size = 2
		else:
			size = 3

	if x == None or y == None:
		pos = random.choice([0, 1]) # Choose between horizontal and vertical
		if pos == 0:
			spawn_x = SCREEN_WIDTH + asteroid_image.half_width
			spawn_y = random.randrange(SCREEN_HEIGHT)
			spawn_angle = random.uniform(110, 240) + random.choice([0, 180])
		else:
			spawn_x = random.randrange(SCREEN_WIDTH)
			spawn_y = SCREEN_HEIGHT + asteroid_image.half_height
			spawn_angle = random.uniform(30, 150) + random.choice([0, 180])

	ASTEROID_LIST.append(Asteroid(spawn_x, spawn_y, spawn_angle, spawn_speed, size))



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
		self.dead = False

	def update(self, dt):
		if self.dead: return
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
				global SHOTS_FIRED
				SHOTS_FIRED += 1
		else:
			self.btimer -= dt

	def death(self):
		self.x -= 24
		self.y -= 24
		self.dead = True
		self.image = explosion_big_anim
		self.rotation = 0
		self.speed.x = 0
		self.speed.y = 0


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
DEBUG_LABEL = pyglet.text.Label('', 'Courier New', 14.0,
						True, False, (255, 150, 50, 255),
						5, SCREEN_HEIGHT - 5, SCREEN_WIDTH - 10,
						anchor_y = 'top', multiline = True, batch = BATCH)

# Score label on other side
SCORE_LABEL = pyglet.text.Label('', 'Courier New', 20.0,
						True, False, (150, 130, 255, 255),
						SCREEN_WIDTH - 5, SCREEN_HEIGHT - 5, SCREEN_WIDTH - 10, 100,
						'right', 'top', 'right', True, batch = BATCH)

# Death label and timer
RESPAWN_LABEL = pyglet.text.Label('', 'Comic Sans MS', 40.0,
								False, False, (255, 255, 255, 255),
								SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, 200,
								'center', 'center','center', multiline = True, batch = BATCH)

# Function to change the label text on each draw
def update_label():
	SCORE_LABEL.text = 'SCORE: {}\nMulti: {:.1f}x ({:.0f}%)'.format(SCORE, ACCURACY_MULTIPLER * ACCURACY, ACCURACY * 100)
	if DEBUG_PRINTOUT:
		DEBUG_LABEL.text = 'FPS: {:.1f}'.format(pyglet.clock.get_fps())
		DEBUG_LABEL.text += '\nPlayer: {:.2f}, {:.2f} Speed: {:.2f}, {:.2f} ({:.2f})'.format(PLAYER.x, PLAYER.y, PLAYER.speed.x, PLAYER.speed.y, PLAYER.speed.get_mag())
		DEBUG_LABEL.text += '\nTotal Bullets: {}'.format(len(BULLET_LIST))
		DEBUG_LABEL.text += '\nTotal Asteroids: {} Timer {:.1f}'.format(len(ASTEROID_LIST), SPAWN_TIMER)

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
	elif key == pyglet.window.key.P:
		spawn_asteroid()
	elif key == pyglet.window.key.O:
		global DEBUG_PRINTOUT
		DEBUG_PRINTOUT = not DEBUG_PRINTOUT
		DEBUG_LABEL.text = ''

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
	global SPAWN_TIMER, BULLET_LIST, ASTEROID_LIST
	PLAYER.update(dt)
	i = 0
	# update bullets
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

	# update roids
	i = 0
	while i < len(ASTEROID_LIST):
		a = ASTEROID_LIST[i]
		# check and delete garbage before updating
		if a.garbage:
			ASTEROID_LIST.pop(i)
			continue
		else:
			a.update(dt)
			i += 1
			continue

	# Check for player death
	if PLAYER.dead:
		global RESPAWN_TIMER, SCORE, ACCURACY, SHOTS_FIRED, SHOTS_HIT
		# PLAYER.visible = False
		RESPAWN_TIMER -= dt
		RESPAWN_LABEL.text = 'YOU LOSE MANG!\nSCORE: {}'.format(SCORE)
		RESPAWN_LABEL.color = (random.randrange(255), random.randrange(255), random.randrange(255), 255)
		if RESPAWN_TIMER <= 0:
			RESPAWN_TIMER = RESPAWN_WAIT
			PLAYER.dead = False
			PLAYER.x = SCREEN_WIDTH // 2
			PLAYER.y = SCREEN_HEIGHT // 2
			PLAYER.image = ship_image
			BULLET_LIST = []
			ASTEROID_LIST = []
			SCORE = 0
			SHOTS_FIRED = 0
			SHOTS_HIT = 0
			ACCURACY = 0
			RESPAWN_LABEL.text = ''



	if SPAWN_TIMER <= 0:
		SPAWN_TIMER = random.uniform(SPAWN_WAIT_MIN, SPAWN_WAIT_MAX)
		if len(ASTEROID_LIST) < MAX_ASTEROIDS:
			spawn_asteroid()
	else:
		SPAWN_TIMER -= dt



game_setup()

pyglet.clock.schedule(game_update)
pyglet.app.run()

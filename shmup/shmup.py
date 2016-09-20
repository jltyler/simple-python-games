import pyglet
import math

# Set up globals
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 800
SCREEN_WIDTH_HALF = SCREEN_WIDTH // 2
SCREEN_HEIGHT_HALF = SCREEN_HEIGHT // 2
DEBUG_PRINTOUT = False
GAME_TIMER = 0

PLAYER_MOVE_SPEED = 250.0
PLAYER_DIAGONAL_MOD = 0.70710678118 # root of 2 over 2
PLAYER_SLOW_MOD = 0.5
PLAYER_FIRE_RATE = 0.25
PLAYER_HIT_RADIUS = 4
PLAYER_HIT_X = 0
PLAYER_HIT_Y = 4

PLAYER_BULLET_SPEED = 450.0
PLAYER_BULLET_DAMAGE = 20.0
PLAYER_BULLET_LIST = []

ENEMY_SPEED = 100.0
ENEMY_HEALTH = 100.0
ENEMY_LIST = []
ENEMY_BULLET_LIST = []
WAVE_SPAWN_WAIT = 3.0

BATCH = pyglet.graphics.Batch()

# Controls
KEY_UP = pyglet.window.key.UP
KEY_DOWN = pyglet.window.key.DOWN
KEY_LEFT = pyglet.window.key.LEFT
KEY_RIGHT = pyglet.window.key.RIGHT
KEY_SHOOT = pyglet.window.key.Z
KEY_SLOW = pyglet.window.key.X

# Load and set up sprites
ship_image = pyglet.image.load("ship.png")
ship_image.anchor_x = ship_image.width // 2
ship_image.anchor_y = ship_image.height // 2

bullet_image = pyglet.image.load("bullet.png")
bullet_image.anchor_x = bullet_image.width // 2
bullet_image.anchor_y = bullet_image.height // 2

enemy_image = pyglet.image.load("enemy.png")
enemy_image.anchor_x = enemy_image.width // 2
enemy_image.anchor_y = enemy_image.height // 2

class Player(pyglet.sprite.Sprite):
	"""Player ship that moves n shoots"""
	def __init__(self):
		super().__init__(ship_image, batch = BATCH)
		self.moving = [0, 0] # move x, y
		self.x = SCREEN_WIDTH_HALF
		self.y = 48
		self.shooting = False
		self.speed_multi = 1.0
		self.btimer = 0

	def update(self, dt):
		# Terrible movement code
		if self.moving[0] != 0:
			self.x += self.moving[0] * PLAYER_MOVE_SPEED * self.speed_multi * dt
		if self.moving[1] != 0:
			self.y += self.moving[1] * PLAYER_MOVE_SPEED * self.speed_multi * dt

		# SHooties
		self.btimer -= dt
		if self.shooting:
			if self.btimer <= 0:
				self.btimer = PLAYER_FIRE_RATE
				PLAYER_BULLET_LIST.append(PlayerBullet(self.x, self.y))

class PlayerBullet(pyglet.sprite.Sprite):
	"""Bullet shot by player, collides with enemies"""
	def __init__(self, x, y):
		super().__init__(bullet_image, batch = BATCH)
		self.x = x
		self.y = y
		self.garbage = False

	def update(self, dt):
		# Go up
		self.y += PLAYER_BULLET_SPEED * dt
		if self.y > SCREEN_HEIGHT:
			self.garbage = True

class Enemy(pyglet.sprite.Sprite):
	"""Basic enemy move n shooter"""
	def __init__(self, x, y):
		super().__init__(enemy_image, batch = BATCH)
		self.x = x
		self.y = y
		self.garbage = False
		print("Kerspawned {}, {}".format(x, y))

	def update(self, dt):
		# Go down
		self.y -= ENEMY_SPEED * dt
		if self.y <= -32:
			self.garbage = True
		
class EnemyPattern():
	"""Spawning pattern for enemies"""
	def __init__(self, x_list, time_list):
		self.x_list = x_list # List of x locations to spawn at
		self.time_list = time_list # List of times between spawns
		self.timer = self.time_list.pop(0) # Grab first time length
		self.finished = False

	def update(self, dt):
		self.timer -= dt
		if self.timer <= 0:
			ENEMY_LIST.append(Enemy(self.x_list.pop(0), SCREEN_HEIGHT + 32)) # Spawn
			if len(self.time_list) == 0: # If on last one we're finished
				self.finished = True
			else:
				self.timer = self.time_list.pop(0)

class LevelPattern():
	"""Container and timer for executing enemy pattern spawns"""
	def __init__(self, patterns):
		self.patterns = patterns # List of EnemyPattern instances
		self.timer = WAVE_SPAWN_WAIT # Time between waves
		self.spawning = False
		self.active = None # Active pattern

	def update(self, dt):
		if self.spawning:
			self.active.update(dt)
			if self.active.finished:
				self.spawning = False
				self.active = None
			else:
				return
		if self.timer <= 0:
			self.active = self.patterns.pop(0)
			self.spawning = True
			self.timer = WAVE_SPAWN_WAIT
			print("{} waves left".format(len(self.patterns)))
		else:
			self.timer -= dt
		
WAVE_1 = EnemyPattern([SCREEN_WIDTH - 64] * 8, [0.8] * 8)
WAVE_2 = EnemyPattern([64] * 8, [0.8] * 8)
WAVE_3 = EnemyPattern([64 + i*42 for i in range(12)], [1.0] * 12)

TEST_LEVEL = LevelPattern([WAVE_1, WAVE_2, WAVE_3])

WINDOW = pyglet.window.Window(width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
PLAYER = Player()

# Always with the labels
DEBUG_LABEL = pyglet.text.Label('ffff', 'Courier New', 14.0,
						True, False, (255, 150, 50, 255),
						5, SCREEN_HEIGHT - 5, SCREEN_WIDTH - 10,
						anchor_y = 'top', multiline = True)

def update_debug_label(dt):
	DEBUG_LABEL.text = "FPS: {:.2f} (dt:{:.5f})".format(pyglet.clock.get_fps(), dt)
	DEBUG_LABEL.text += "\nPlayer {}, {} |Bullets: {}".format(PLAYER.x, PLAYER.y, len(PLAYER_BULLET_LIST))
	DEBUG_LABEL.text += "\nEnemies: {} |Bullets: {}".format(len(ENEMY_LIST), len(ENEMY_BULLET_LIST))


# Controls implemented
@WINDOW.event
def on_key_press(key, mods):
	if key == KEY_RIGHT:
		PLAYER.moving[0] += 1
	elif key == KEY_LEFT:
		PLAYER.moving[0] -= 1
	elif key == KEY_UP:
		PLAYER.moving[1] += 1
	elif key == KEY_DOWN:
		PLAYER.moving[1] -= 1
	elif key == KEY_SHOOT:
		PLAYER.shooting = True
	elif key == KEY_SLOW:
		PLAYER.speed_multi = PLAYER_SLOW_MOD

@WINDOW.event
def on_key_release(key, mods):
	if key == KEY_RIGHT:
		PLAYER.moving[0] -= 1
	elif key == KEY_LEFT:
		PLAYER.moving[0] += 1
	elif key == KEY_UP:
		PLAYER.moving[1] -= 1
	elif key == KEY_DOWN:
		PLAYER.moving[1] += 1
	elif key == KEY_SHOOT:
		PLAYER.shooting = False
	elif key == KEY_SLOW:
		PLAYER.speed_multi = 1.0

# Drawing loop
@WINDOW.event
def on_draw():
	WINDOW.clear()
	BATCH.draw()
	DEBUG_LABEL.draw()

# Set everything up
def game_setup():
	pass

# Update a list func
def update_list(ulist, dt):
	i = 0
	while i < len(ulist):
		obj = ulist[i]
		if obj.garbage:
			ulist.pop(i)
		else:
			obj.update(dt)
			i += 1

# Main update loop
def game_update(dt):
	global GAME_TIMER
	PLAYER.update(dt)
	TEST_LEVEL.update(dt)
	update_list(PLAYER_BULLET_LIST, dt)
	update_list(ENEMY_LIST, dt)
	# update_list(ENEMY_BULLET_LIST)
	GAME_TIMER += dt
	update_debug_label(dt)

# Off we go then
game_setup()
pyglet.clock.schedule(game_update)
pyglet.app.run()
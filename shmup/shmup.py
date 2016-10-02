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
PLAYER_HIT_RADIUS = 3
PLAYER_HIT_RADIUS2 = PLAYER_HIT_RADIUS ** 2
PLAYER_HIT_X = 0
PLAYER_HIT_Y = 5

PLAYER_BULLET_SPEED = 450.0
PLAYER_BULLET_DAMAGE = 10.0
PLAYER_BULLET_LIST = []
PLAYER_BULLET_RADIUS = 3
PLAYER_BULLET_RADIUS2 = PLAYER_BULLET_RADIUS**2
PLAYER_GUN_OFFSET_LEFT = (-8, 11)
PLAYER_GUN_OFFSET_RIGHT = (8, 11)
PLAYER_GUN_OFFSET_LEFT2 = (-14, 6)
PLAYER_GUN_OFFSET_RIGHT2 = (14, 6)

ENEMY_GARBAGE_BORDER = -300 # if enemy.y < this_value: enemy.garbage = True
ENEMY_LIST = []
ENEMY_BULLET_LIST = []
WAVE_SPAWN_WAIT = 0.01 # 3.0

ENEMY_BULLET_SPEED = 250.0
ENEMY_BULLET_RADIUS = 6
ENEMY_BULLET_RADIUS2 = ENEMY_BULLET_RADIUS**2

ENEMY1_Y_SPEED = -95.0
ENEMY1_HEALTH = 30.0

ENEMY2_HEALTH = 45.0
ENEMY2_SPREAD = 4
ENEMY2_BULLETS = 4
ENEMY2_FIRE_RATE = 1.3
ENEMY2_FIRE_ANGLE = 270 - (ENEMY2_SPREAD * (ENEMY2_BULLETS - 1)) / 2

ENEMY3_HEALTH = 300.0
ENEMY3_SPEED = 120.0
ENEMY3_FIRE_RATE = 1.2
ENEMY3_FIRE_FUNC = lambda t: t*30
ENEMY3_TARGET_Y = SCREEN_HEIGHT - 150
ENEMY3_TARGET_X = 150
ENEMY3_BULLETS = 18
ENEMY3_SPREAD = 20.0

ENEMY4_HEALTH = 30.0
ENEMY4_SPEED = 120.0
ENEMY4_FIRE_RATE = 0.5
ENEMY4_BULLETS = 3
ENEMY4_SPREAD = 10.0
ENEMY4_SPREAD_OFF = (ENEMY4_SPREAD * (ENEMY4_BULLETS - 1)) / 2

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

player_bullet_image = pyglet.image.load("player_bullet.png")
player_bullet_image.anchor_x = player_bullet_image.width // 2
player_bullet_image.anchor_y = player_bullet_image.height // 2

bullet_image = pyglet.image.load("bullet.png")
bullet_image.anchor_x = bullet_image.width // 2
bullet_image.anchor_y = bullet_image.height // 2

enemy_image = pyglet.image.load("enemy.png")
enemy_image.anchor_x = enemy_image.width // 2
enemy_image.anchor_y = enemy_image.height // 2

enemy_shooter_image = pyglet.image.load("enemy_shoot.png")
enemy_shooter_image.anchor_x = enemy_shooter_image.width // 2
enemy_shooter_image.anchor_y = enemy_shooter_image.height // 2

enemy_stop_image = pyglet.image.load("enemy_stop.png")
enemy_stop_image.anchor_x = enemy_stop_image.width // 2
enemy_stop_image.anchor_y = enemy_stop_image.height // 2

enemy_aim_image = pyglet.image.load("enemy_aim.png")
enemy_aim_image.anchor_x = enemy_aim_image.width // 2
enemy_aim_image.anchor_y = enemy_aim_image.height // 2

# Weapon firing functions
def fire_weapon_1(player):
	PLAYER_BULLET_LIST.append(PlayerBullet(player.x + PLAYER_GUN_OFFSET_LEFT[0], player.y + PLAYER_GUN_OFFSET_LEFT[1]))
	PLAYER_BULLET_LIST.append(PlayerBullet(player.x + PLAYER_GUN_OFFSET_RIGHT[0], player.y + PLAYER_GUN_OFFSET_RIGHT[1]))

def fire_weapon_2(player):
	fire_weapon_1(player)
	PLAYER_BULLET_LIST.append(PlayerBullet(player.x + PLAYER_GUN_OFFSET_LEFT2[0], player.y + PLAYER_GUN_OFFSET_LEFT2[1]))
	PLAYER_BULLET_LIST.append(PlayerBullet(player.x + PLAYER_GUN_OFFSET_RIGHT2[0], player.y + PLAYER_GUN_OFFSET_RIGHT2[1]))


class Player(pyglet.sprite.Sprite):
	"""Player ship that moves n shoots"""
	def __init__(self):
		super().__init__(ship_image) #, batch = BATCH)
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
				fire_weapon_1(self)

class PlayerBullet(pyglet.sprite.Sprite):
	"""Bullet shot by player, collides with enemies"""
	def __init__(self, x, y, damage = PLAYER_BULLET_DAMAGE):
		super().__init__(player_bullet_image, batch = BATCH)
		self.x = x
		self.y = y
		self.garbage = False
		self.damage = damage

	def update(self, dt):
		# Go up
		self.y += PLAYER_BULLET_SPEED * dt
		if self.y > SCREEN_HEIGHT:
			self.garbage = True

class EnemyBullet(pyglet.sprite.Sprite):
	"""Bullet shot by enemy. Travels in a straight line."""
	def __init__(self, x, y, speed, angle):
		super().__init__(bullet_image, batch = BATCH)
		self.x = x
		self.y = y
		self.speed_x = math.cos(math.radians(angle)) * speed
		self.speed_y = math.sin(math.radians(angle)) * speed
		self.garbage = False

	def update(self, dt):
		self.x += self.speed_x * dt
		self.y += self.speed_y * dt

		if (self.x > SCREEN_WIDTH or self.x < 0 or
			self.y > SCREEN_HEIGHT or self.y < 0):
			self.garbage = True

class Spawner():
	"""Spawns bullets with a pattern"""
	def __init__(self, attached, base_angle = 270, fire_rate = 0.25, base_speed = 350, bullets = 1, angle_offset = 15):
		self.attached = attached
		self.base_angle = base_angle
		self.fire_rate = fire_rate
		self.base_speed = base_speed
		self.bullets = bullets
		self.angle_offset = angle_offset
		self.btimer = fire_rate
		self.speed_func = lambda t: 0
		self.angle_func = lambda t: 0
		self.active = True
		self.timer = 0.0

	def spawn(self, timer):
		speed = self.base_speed + abs(self.speed_func(timer))
		angle = self.base_angle + self.angle_func(timer)
		for i in range(self.bullets):
			ENEMY_BULLET_LIST.append(EnemyBullet(self.attached.x, self.attached.y, speed, angle + i * self.angle_offset))

	def update(self, dt):
		if not self.active: return
		self.btimer -= dt
		self.timer += dt
		if self.btimer <= 0:
			self.spawn(self.timer)
			self.btimer = self.fire_rate

class Enemy(pyglet.sprite.Sprite):
	"""Basic enemy mover"""
	def __init__(self, x, y, image = enemy_image):
		super().__init__(image, batch = BATCH)
		self.x = x
		self.y = y
		self.garbage = False
		self.base_x_speed = 0
		self.base_y_speed = ENEMY1_Y_SPEED
		self.x_speed_func = lambda t: 0
		self.y_speed_func = lambda t: 0
		self.health = ENEMY1_HEALTH
		self.box = [image.width // 2, image.height // 2]

	def update(self, dt):
		# Go down
		self.x += (self.base_x_speed + self.x_speed_func(GAME_TIMER)) * dt
		self.y += (self.base_y_speed + self.y_speed_func(GAME_TIMER)) * dt
		if self.y <= ENEMY_GARBAGE_BORDER:
			self.garbage = True

	def impact(self, bullet):
		if bullet.garbage: return
		self.health -= bullet.damage
		if self.health <= 0:
			self.death()

	def death(self):
		self.garbage = True
		self.visible = False
		
class EnemyShoots(Enemy):
	"""Enemy that fires triples at a fixed angle"""
	def __init__(self, x, y):
		super().__init__(x, y, enemy_shooter_image)
		self.health = ENEMY2_HEALTH
		self.weapon = Spawner(self, ENEMY2_FIRE_ANGLE, ENEMY2_FIRE_RATE, ENEMY_BULLET_SPEED, ENEMY2_BULLETS, ENEMY2_SPREAD)

	def update(self, dt):
		super().update(dt)
		if self.garbage: return
		self.weapon.update(dt)

class EnemyStops(Enemy):
	"""Goes to a point on the screen then stops and starts firing"""
	def __init__(self, x, y, target_x = None, target_y = None):
		super().__init__(x, y, enemy_stop_image)
		if target_x == None:
			if x < ENEMY3_TARGET_X:
				target_x = ENEMY3_TARGET_X
			else:
				target_x = SCREEN_WIDTH - ENEMY3_TARGET_X
		self.target_x = target_x
		if target_y == None:
			target_y = ENEMY3_TARGET_Y
		self.target_y = target_y
		self.weapon = Spawner(self, 270 - 15, ENEMY3_FIRE_RATE, ENEMY_BULLET_SPEED, ENEMY3_BULLETS, ENEMY3_SPREAD)
		self.weapon.angle_func = ENEMY3_FIRE_FUNC
		self.stopped = False
		self.health = ENEMY3_HEALTH

	def update(self, dt):
		if self.stopped:
			self.weapon.update(dt)
		else:
			dx = self.target_x - self.x
			dy = self.target_y - self.y
			move_tick = ENEMY3_SPEED * dt
			self.x += math.copysign(move_tick, dx)
			self.y += math.copysign(move_tick, dy)
			if abs(dx) < move_tick and abs(dy) < move_tick:
				self.stopped = True
				self.x = self.target_x
				self.y = self.target_y

def get_dir(x1, y1, x2, y2):
		dx = x2 - x1
		dy = y2 - y1
		# lets not divide by zero now
		if dy == 0:
			return 0.0 if dx >= 0 else 180.0
		elif dx == 0:
			return 90.0 if dy >= 0 else 270.0
		# get angle and convert to degrees
		raw_deg = math.degrees(math.atan2(dy , dx))
		# math.atan2 gives us negatives so we convert to between 0 and 360
		return raw_deg if raw_deg >= 0 else (360+raw_deg)

class EnemyAims(Enemy):
	"""Enemy that moves down like others but aims at the player when it fires it's weapon"""
	def __init__(self, x, y):
		super().__init__(x, y, enemy_aim_image)
		self.weapon = Spawner(self, 0, ENEMY4_FIRE_RATE, ENEMY_BULLET_SPEED, ENEMY4_BULLETS, ENEMY4_SPREAD)
		self.health = ENEMY4_HEALTH
		self.weapon.angle_func = lambda t: get_dir(self.x, self.y, PLAYER.x, PLAYER.y) - ENEMY4_SPREAD_OFF
	
	def update(self, dt):
		self.y -= ENEMY4_SPEED * dt
		# self.weapon.base_angle = get_dir(self.x, self.y, PLAYER.x, PLAYER.y)
		self.weapon.update(dt)
		
		
class EnemyPattern():
	"""Spawning pattern for enemies"""
	def __init__(self, enemy_list, x_list, time_list):
		self.enemy_list = enemy_list # List of enemy types to spawn
		self.x_list = x_list # List of x locations to spawn at
		self.time_list = time_list # List of times between spawns
		self.timer = self.time_list.pop(0) # Grab first time length
		self.finished = False

	def update(self, dt):
		self.timer -= dt
		while self.timer <= 0:
			etype = self.enemy_list.pop(0)
			ENEMY_LIST.append(etype(self.x_list.pop(0), SCREEN_HEIGHT + 32)) # Spawn
			if len(self.time_list) == 0: # If on last one we're finished
				self.finished = True
				self.timer = 999.9
			else:
				self.timer = self.time_list.pop(0)

class LevelPattern():
	"""Container and timer for executing enemy pattern spawns"""
	def __init__(self, patterns):
		self.patterns = patterns # List of EnemyPattern instances
		self.timer = WAVE_SPAWN_WAIT # Time between waves
		self.spawning = False
		self.active = None # Active pattern
		self.last = False

	def update(self, dt):
		if self.spawning:
			self.active.update(dt)
			if self.active.finished:
				self.spawning = False
				self.active = None
			else:
				return
		if self.timer <= 0:
			if self.last: return
			self.active = self.patterns.pop(0)
			if len(self.patterns) == 0:
				self.last = True
			self.spawning = True
			self.timer = WAVE_SPAWN_WAIT
			print("{} waves left".format(len(self.patterns)))
		else:
			self.timer -= dt
		
WAVE_AIM = EnemyPattern([EnemyAims] * 4, [SCREEN_WIDTH // 2] * 4, [0.8] * 4)
WAVE_STOP = EnemyPattern([EnemyStops] * 2, [96, SCREEN_WIDTH - 96], [1.0, 0.0])
WAVE_1 = EnemyPattern([Enemy] * 8, [SCREEN_WIDTH - 64] * 8, [0.8] * 8)
WAVE_2 = EnemyPattern([Enemy] * 8, [64] * 8, [0.8] * 8)
WAVE_3 = EnemyPattern([Enemy, EnemyShoots] * 6, [64 + i*42 for i in range(12)], [1.0] * 12)
WAVE_4 = EnemyPattern([Enemy, EnemyShoots] * 6, [SCREEN_WIDTH - 64 - i*42 for i in range(12)], [1.0] * 12)
WAVE_DOUBLE = EnemyPattern([Enemy, EnemyShoots, EnemyShoots, Enemy] * 4, [SCREEN_WIDTH - 64, 64] * 8, [1.5, 0] * 8)

TEST_LEVEL = LevelPattern([WAVE_AIM, WAVE_STOP, WAVE_1, WAVE_STOP, WAVE_2, WAVE_3, WAVE_4, WAVE_DOUBLE])

WINDOW = pyglet.window.Window(width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
PLAYER = Player()

# Always with the labels
DEBUG_LABEL = pyglet.text.Label('ffff', 'Courier New', 14.0,
						True, False, (255, 150, 50, 255),
						5, SCREEN_HEIGHT - 5, SCREEN_WIDTH - 10,
						anchor_y = 'top', multiline = True)

def update_debug_label(dt):
	DEBUG_LABEL.text = "FPS: {:.2f} (dt:{:.5f})".format(pyglet.clock.get_fps(), dt)
	DEBUG_LABEL.text += "\nPlayer {:.1f}, {:.1f} |Bullets: {}".format(PLAYER.x, PLAYER.y, len(PLAYER_BULLET_LIST))
	DEBUG_LABEL.text += "\nEnemies: {} |Bullets: {}".format(len(ENEMY_LIST), len(ENEMY_BULLET_LIST))

def player_collision_tick(dt):
	px = PLAYER.x + PLAYER_HIT_X
	py = PLAYER.y + PLAYER_HIT_Y
	for b in ENEMY_BULLET_LIST:
		dx = b.x - px
		dy = b.y - py
		# Check radii
		if dx**2 + dy**2 < PLAYER_HIT_RADIUS2 + ENEMY_BULLET_RADIUS2:
			print("DEAD PLAYER")
			b.garbage = True

def enemy_collision_tick(dt):
	for e in ENEMY_LIST:
		for b in PLAYER_BULLET_LIST:
			if b.garbage: continue
			cx = min(max(b.x, e.x - e.box[0]), e.x + e.box[0])
			cy = min(max(b.y, e.y - e.box[1]), e.y + e.box[1])
			if (cx - b.x)**2 + (cy - b.y)**2 < PLAYER_BULLET_RADIUS2:
				e.impact(b)
				b.garbage = True


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
	PLAYER.draw()
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
	GAME_TIMER += dt

	PLAYER.update(dt)
	TEST_LEVEL.update(dt)

	update_list(PLAYER_BULLET_LIST, dt)
	update_list(ENEMY_LIST, dt)
	update_list(ENEMY_BULLET_LIST, dt)

	player_collision_tick(dt)
	enemy_collision_tick(dt)
	
	update_debug_label(dt)

# Off we go then
game_setup()
pyglet.clock.schedule(game_update)
pyglet.app.run()
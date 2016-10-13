import pyglet
import math
import random

# Set up globals
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 800
SCREEN_WIDTH_HALF = SCREEN_WIDTH // 2
SCREEN_HEIGHT_HALF = SCREEN_HEIGHT // 2
DEBUG_PRINTOUT = False
GAME_TIMER = 0
GAME_OVER = False

# Player settings
PLAYER_MOVE_SPEED = 250.0
PLAYER_DIAGONAL_MOD = 0.70710678118 # root of 2 over 2 (not used yet)
PLAYER_SLOW_MOD = 0.5
PLAYER_FIRE_RATE = 0.25
PLAYER_HIT_RADIUS = 3
PLAYER_HIT_RADIUS2 = PLAYER_HIT_RADIUS ** 2
PLAYER_HIT_X = 0
PLAYER_HIT_Y = 5
PLAYER_LIVES = 3
PLAYER_INVULNERABLE = 1.5
PLAYER_RESPAWN_TIMER = 2.0
PLAYER_SPAWN = [SCREEN_WIDTH_HALF, 150]

# Weapon stuff
PLAYER_GUN_OFFSET_LEFT = (-8, 11)
PLAYER_GUN_OFFSET_RIGHT = (8, 11)
PLAYER_GUN_OFFSET_LEFT2 = (-14, 6)
PLAYER_GUN_OFFSET_RIGHT2 = (14, 6)

PLAYER_BULLET_SPEED = 450.0
PLAYER_BULLET_DAMAGE = 10.0
PLAYER_BULLET_RADIUS = 3
PLAYER_BULLET_RADIUS2 = PLAYER_BULLET_RADIUS**2

PLAYER_BIGBULLET_SPEED = 480.0
PLAYER_BIGBULLET_DAMAGE = 35.0
PLAYER_BIGBULLET_RADIUS = 4.5
PLAYER_BIGBULLET_RADIUS2 = PLAYER_BIGBULLET_RADIUS ** 2

# Diagonal bullet
PLAYER_DIAGBULLET_SPEED = 450.0
PLAYER_DIAGBULLET_ANGLE = math.radians(50.0)
PLAYER_DIAGBULLET_DAMAGE = 15.0
PLAYER_DIAGBULLET_RADIUS = 4.5
PLAYER_DIAGBULLET_RADIUS2 = PLAYER_DIAGBULLET_RADIUS ** 2


# Enemy settings
ENEMY_GARBAGE_BORDER = -300 # if enemy.y < this_value: enemy.garbage = True
WAVE_SPAWN_WAIT = 0.01 # 3.0 # How long between waves
WAVE_SPAWN_Y = SCREEN_HEIGHT + 32
START_SPAWN_WAIT = 0.1 # 3.0

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
ENEMY4_SPEED = 100.0
ENEMY4_FIRE_RATE = 0.8
ENEMY4_BULLETS = 3
ENEMY4_SPREAD = 4.0
ENEMY4_SPREAD_OFF = (ENEMY4_SPREAD * (ENEMY4_BULLETS - 1)) / 2

# Boss settings
BOSS_INTRO_SPEED = 720 # 90
BOSS_INTRO_TIME = 0.5 # 4.0

BOSS_MAIN_RADIUS = 48
BOSS_MAIN_RADIUS2 = BOSS_MAIN_RADIUS ** 2

BOSS_X_RANGE_S1 = 100
BOSS_WEAPON_WAIT_S1 = 1.0 # 4.0
BOSS_WEAPON_BURST_S1 = 3.5 # 3.5


# Powerup settings
POWERUP_MOVE_SPEED = 150.0
POWERUP_MOVE_TIMER = 0.8
POWERUP_RADIUS = 32
POWERUP_RADIUS2 = POWERUP_RADIUS ** 2

# Entity lists
PLAYER_BULLET_LIST = []
ENEMY_LIST = []
ENEMY_BULLET_LIST = []
MISC_LIST = []

BATCH = pyglet.graphics.Batch()

# Controls
KEY_UP = pyglet.window.key.UP
KEY_DOWN = pyglet.window.key.DOWN
KEY_LEFT = pyglet.window.key.LEFT
KEY_RIGHT = pyglet.window.key.RIGHT
KEY_SHOOT = pyglet.window.key.Z
KEY_SLOW = pyglet.window.key.X
KEY_CHEAT_POWERUP = pyglet.window.key.P

# ======== LOADING GRAPHICS ========
# STEALING JOHN'S WORK AND NOT GIVING HIM CREDIT xDDDDD
def sprite_sheet_anim(sprite_sheet, rows, columns, period=0.05, loop=True):
	return pyglet.image.Animation.from_image_sequence(pyglet.image.ImageGrid(sprite_sheet, rows, columns), period, loop)

def center_anchor(image):
	image.anchor_x = image.width // 2
	image.anchor_y = image.height // 2

def prepare_image(file):
	image = pyglet.image.load(file)
	center_anchor(image)
	return image

def prepare_anim(file, rows, columns, period = 0.05, loop = True):
	sheet = pyglet.image.load(file)
	anim = sprite_sheet_anim(sheet, rows, columns, period, loop)
	# Gotta set anchor for each frame
	for f in anim.frames:
		center_anchor(f.image)
	return anim, sheet

ship_image = prepare_image("img/ship.png")
player_bullet_image = prepare_image("img/player_bullet.png")
player_bigbullet_image = prepare_image("img/player_bigbullet.png")
player_diagbullet_image = prepare_image("img/player_diagbullet.png")
player_diagbullet_image_flip = player_diagbullet_image.get_texture().get_transform(flip_x = True)
bullet_image = prepare_image("img/bullet.png")
enemy_image = prepare_image("img/enemy.png")
enemy_shooter_image = prepare_image("img/enemy_shoot.png")
enemy_stop_image = prepare_image("img/enemy_stop.png")
enemy_aim_image = prepare_image("img/enemy_aim.png")
boss_image = prepare_image("img/boss_wip.png")
boss_mini_image = prepare_image("img/boss_mini.png")

powerup_anim, powerup_sheet = prepare_anim("img/powerup1.png", 1, 8, 0.125)
explode64_anim, explode64_sheet = prepare_anim("img/explode64.png", 1, 8, 0.04)



# Weapon firing functions
def fire_weapon_0(player):
	PLAYER_BULLET_LIST.append(PlayerBullet(player.x + PLAYER_GUN_OFFSET_LEFT[0], player.y + PLAYER_GUN_OFFSET_LEFT[1]))
	PLAYER_BULLET_LIST.append(PlayerBullet(player.x + PLAYER_GUN_OFFSET_RIGHT[0], player.y + PLAYER_GUN_OFFSET_RIGHT[1]))

def fire_weapon_1(player):
	fire_weapon_0(player)
	PLAYER_BULLET_LIST.append(PlayerBullet(player.x + PLAYER_GUN_OFFSET_LEFT2[0], player.y + PLAYER_GUN_OFFSET_LEFT2[1]))
	PLAYER_BULLET_LIST.append(PlayerBullet(player.x + PLAYER_GUN_OFFSET_RIGHT2[0], player.y + PLAYER_GUN_OFFSET_RIGHT2[1]))

def fire_weapon_2(player):
	fire_weapon_0(player)
	PLAYER_BULLET_LIST.append(PlayerBigBullet(player.x + PLAYER_GUN_OFFSET_LEFT2[0], player.y + PLAYER_GUN_OFFSET_LEFT2[1]))
	PLAYER_BULLET_LIST.append(PlayerBigBullet(player.x + PLAYER_GUN_OFFSET_RIGHT2[0], player.y + PLAYER_GUN_OFFSET_RIGHT2[1]))

def fire_weapon_3(player):
	fire_weapon_2(player)
	PLAYER_BULLET_LIST.append(PlayerDiagBullet(player.x + PLAYER_GUN_OFFSET_LEFT2[0], player.y + PLAYER_GUN_OFFSET_LEFT2[1], True))
	PLAYER_BULLET_LIST.append(PlayerDiagBullet(player.x + PLAYER_GUN_OFFSET_RIGHT2[0], player.y + PLAYER_GUN_OFFSET_RIGHT2[1]))


# Fire function array
fire_weapon = [fire_weapon_0, fire_weapon_1, fire_weapon_2, fire_weapon_3]

class Player(pyglet.sprite.Sprite):
	"""Player ship that moves n shoots"""
	def __init__(self):
		super().__init__(ship_image) #, batch = BATCH)
		self.moving = [0, 0] # move x, y
		self.x = PLAYER_SPAWN[0]
		self.y = PLAYER_SPAWN[1]
		self.shooting = False
		self.speed_multi = 1.0
		self.btimer = 0
		self.power_level = 0
		self.dead = False
		self.lives = PLAYER_LIVES
		self.invunerable = PLAYER_INVULNERABLE
		self.respawn_timer = PLAYER_RESPAWN_TIMER

	def update(self, dt):
		if self.dead:
			self.respawn_timer -= dt
			if self.respawn_timer <= 0:
				self.dead = False
				self.invunerable = PLAYER_INVULNERABLE
				self.x = PLAYER_SPAWN[0]
				self.y = PLAYER_SPAWN[1]
				self.visible = True

			return				
		self.invunerable -= dt
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
				fire_weapon[min(self.power_level, len(fire_weapon) - 1)](self)

	def death(self):
		self.visible = False
		MISC_LIST.append(Explode(self.x, self.y))
		if self.lives == 0:
			global GAME_OVER
			GAME_OVER = True
			return
		self.dead = True
		self.lives-= 1
		self.respawn_timer = PLAYER_RESPAWN_TIMER


class PlayerBullet(pyglet.sprite.Sprite):
	"""Bullet shot by player, collides with enemies"""
	def __init__(self, x, y, damage = PLAYER_BULLET_DAMAGE, image = player_bullet_image):
		super().__init__(image, batch = BATCH)
		self.x = x
		self.y = y
		self.garbage = False
		self.damage = damage

	def update(self, dt):
		# Go up
		self.y += PLAYER_BULLET_SPEED * dt
		if self.y > SCREEN_HEIGHT:
			self.garbage = True

class PlayerBigBullet(PlayerBullet):
	"""Big bullet does more damage and travels slightly faster"""
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_BIGBULLET_DAMAGE, player_bigbullet_image)

	def update(self, dt):
		self.y += PLAYER_BIGBULLET_SPEED * dt
		if self.y > SCREEN_HEIGHT:
			self.garbage = True
		
class PlayerDiagBullet(PlayerBullet):
	"""Bullet that shoots out diagonally"""
	def __init__(self, x, y, flip = False):
		# Flip a rooney dooney
		super().__init__(x, y, PLAYER_DIAGBULLET_DAMAGE, player_diagbullet_image_flip if flip else player_diagbullet_image)
		self.speed_x = math.cos(math.pi - PLAYER_DIAGBULLET_ANGLE if flip else PLAYER_DIAGBULLET_ANGLE) * PLAYER_DIAGBULLET_SPEED
		self.speed_y = math.sin(PLAYER_DIAGBULLET_ANGLE) * PLAYER_DIAGBULLET_SPEED

	def update(self, dt):
		self.x += self.speed_x * dt
		self.y += self.speed_y * dt
		if self.y > SCREEN_HEIGHT:
			self.garbage = True
		

class PowerUp(pyglet.sprite.Sprite):
	"""WISE FWUM YO GWAVE"""
	def __init__(self, x, y):
		super().__init__(powerup_anim, batch = BATCH)
		self.x = x
		self.y = y
		self.timer = POWERUP_MOVE_TIMER
		self.new_dir()
		self.garbage = False

	def update(self, dt):
		self.x += self.speed_x * dt
		self.y += self.speed_y * dt
		self.timer -= dt
		if self.timer <= 0:
			self.timer = POWERUP_MOVE_TIMER
			self.new_dir()

	def new_dir(self):
		angle = random.uniform(0, 2*math.pi)
		self.speed_x = math.cos(angle) * POWERUP_MOVE_SPEED
		self.speed_y = math.sin(angle) * POWERUP_MOVE_SPEED

class EnemyBullet(pyglet.sprite.Sprite):
	"""Bullet shot by enemy. Travels in a straight line."""
	def __init__(self, x, y, speed, angle, vector = None):
		super().__init__(bullet_image, batch = BATCH)
		self.x = x
		self.y = y
		if vector == None:
			self.speed_x = math.cos(math.radians(angle)) * speed
			self.speed_y = math.sin(math.radians(angle)) * speed
		else:
			self.speed_x = vector[0]
			self.speed_y = vector[1]
		self.garbage = False

	def update(self, dt):
		self.x += self.speed_x * dt
		self.y += self.speed_y * dt

		if (self.x > SCREEN_WIDTH or self.x < 0 or
			self.y > SCREEN_HEIGHT or self.y < 0):
			self.garbage = True

class Spawner():
	"""Spawns bullets with a pattern"""
	def __init__(self, attached, base_angle = 270, fire_rate = 0.25, base_speed = 350, bullets = 1, angle_offset = 15, x_scale = 1.0, y_scale = 1.0):
		self.attached = attached
		self.base_angle = base_angle
		self.fire_rate = fire_rate
		self.base_speed = base_speed
		self.bullets = bullets
		self.angle_offset = angle_offset
		self.x_scale = x_scale
		self.y_scale = y_scale
		self.btimer = fire_rate
		self.speed_func = lambda t, b: 0
		self.angle_func = lambda t: 0
		self.active = True
		self.timer = 0.0
		self.x_offset = 0
		self.y_offset = 0

	def spawn(self, timer):
		angle = self.base_angle + self.angle_func(timer)
		for i in range(self.bullets):
			speed = self.base_speed + abs(self.speed_func(timer, i))
			i_angle = angle + i * self.angle_offset
			i_x = math.cos(i_angle) * speed * self.x_scale
			i_y = math.sin(i_angle) * speed * self.y_scale
			ENEMY_BULLET_LIST.append(EnemyBullet(self.attached.x + self.x_offset, self.attached.y + self.y_offset, 0, 0, [i_x, i_y]))

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
		self.x_speed_func = lambda t, y: 0
		self.y_speed_func = lambda t, y: 0
		self.health = ENEMY1_HEALTH
		self.box = [image.width // 2, image.height // 2]
		self.offscreen = False
		self.timer = 0

	def update(self, dt):
		# Go down
		self.timer += dt
		self.x += (self.base_x_speed + self.x_speed_func(self.timer, max(0, SCREEN_HEIGHT - self.y))) * dt
		self.y += (self.base_y_speed + self.y_speed_func(self.timer, max(0, SCREEN_HEIGHT - self.y))) * dt
		if self.y <= ENEMY_GARBAGE_BORDER:
			self.offscreen = True
			self.garbage = True

	def impact(self, bullet):
		if bullet.garbage: return
		self.health -= bullet.damage
		if self.health <= 0:
			self.death()

	def death(self):
		self.garbage = True
		self.visible = False
		MISC_LIST.append(Explode(self.x, self.y))
		
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
		super().update(dt)
		if self.garbage: return
		# self.weapon.base_angle = get_dir(self.x, self.y, PLAYER.x, PLAYER.y)
		self.weapon.update(dt)
	
class Boss(pyglet.sprite.Sprite):
	"""Big ol blastro"""
	def __init__(self):
		super().__init__(boss_image, batch = BATCH)
		self.x = SCREEN_WIDTH_HALF
		self.y = SCREEN_HEIGHT + 200
		self.stage = 0
		self.health = 1000
		self.timer = 0
		self.update_stage = [self.update_s0, self.update_s1, self.update_s2]
		self.weapons = [0]

		# Weapon sets for stage 1
		weapons_s1 = []

		weapon_a = Spawner(self, 0, 0.05, ENEMY_BULLET_SPEED, 2, math.pi)
		weapon_a.angle_func = lambda t: t * 3
		weapon_a.x_offset = -60
		weapon_a.y_offset = 30
		weapon_b = Spawner(self, 0, 0.05, ENEMY_BULLET_SPEED, 2, math.pi, -1)
		weapon_b.angle_func = lambda t: t * 3
		weapon_b.x_offset = 60
		weapon_b.y_offset = 30
		weapons_s1.append([weapon_a, weapon_b])

		weapon_a = Spawner(self, math.radians(270), 0.3, ENEMY_BULLET_SPEED, 4, 0)
		weapon_a.angle_func = lambda t: 0.2 * math.sin(t * 3)
		weapon_a.speed_func = lambda t, b: b * 10
		weapon_a.x_offset = -60
		weapon_a.y_offset = 30
		weapon_b = Spawner(self, math.radians(270), 0.3, ENEMY_BULLET_SPEED, 4, 0, -1)
		weapon_b.angle_func = lambda t: 0.2 * math.sin(t * 3)
		weapon_b.speed_func = lambda t, b: b * 10
		weapon_b.x_offset = 60
		weapon_b.y_offset = 30
		weapons_s1.append([weapon_a, weapon_b])

		weapon_a = Spawner(self, math.radians(270), 0.2, ENEMY_BULLET_SPEED, 72, math.radians(20))
		weapon_a.angle_func = lambda t: t * .2
		weapon_a.speed_func = lambda t, b: (b+1) // 18 * 8
		weapon_a.x_offset = 0
		weapon_a.y_offset = 0
		weapons_s1.append([weapon_a])

		# Stage 2 weapons


		self.weapons.append(weapons_s1)
		self.weapon_timer = BOSS_WEAPON_WAIT_S1
		self.firing = False
		self.active = None

	def update(self, dt):
		self.timer += dt
		self.weapon_timer -= dt
		self.update_stage[self.stage](dt)

	def impact(self, bullet):
		self.health -= bullet.damage

	def next_stage(self):
		self.stage += 1
		self.timer = 0

	def update_s0(self, dt):
		self.y -= BOSS_INTRO_SPEED * dt
		if self.timer >= BOSS_INTRO_TIME:
			self.next_stage()

	def update_s1(self, dt):
		self.x = SCREEN_WIDTH_HALF + ( BOSS_X_RANGE_S1 * math.sin(self.timer) )
		if self.weapon_timer <= 0:
			self.weapon_timer = BOSS_WEAPON_WAIT_S1 if self.firing else BOSS_WEAPON_BURST_S1
			self.firing = not self.firing
			self.active = random.choice(self.weapons[self.stage])
		if self.firing:
			for w in self.active:
				w.update(dt)

	def update_s2(self, dt):
		pass

class EnemyPattern():
	"""Spawning pattern for enemies"""
	def __init__(self, enemy_list, x_list, y_list, x_func_list, timer = WAVE_SPAWN_WAIT):
		biggest = max(len(enemy_list), len(x_list), len(y_list), len(x_func_list))
		self.enemy_list = enemy_list # List of enemy types to spawn
		self.fill(self.enemy_list, biggest)
		self.x_list = x_list # List of x locations to spawn at
		self.fill(self.x_list, biggest)
		self.y_list = y_list # List of y locations to spawn at
		self.fill(self.y_list, biggest)
		self.x_func_list = x_func_list
		self.fill(self.x_func_list, biggest)
		self.timer = timer

	def spawn(self):
		wave = []
		for etype, x, y, x_func in zip(self.enemy_list, self.x_list, self.y_list, self.x_func_list):
			enemy = etype(x, WAVE_SPAWN_Y + y)
			enemy.x_speed_func = x_func
			wave.append(enemy)
		return wave

	def fill(self, flist, length):
		# If list is too short: populate with duplicates of the last item
		while len(flist) < length:
			flist.append(flist[len(flist) - 1])

class LevelPattern():
	"""Container and timer for executing enemy pattern spawns"""
	def __init__(self, patterns, boss):
		self.patterns = patterns # List of EnemyPattern instances
		self.timer = START_SPAWN_WAIT # Time between waves
		self.waiting = True
		self.active = None # Active pattern
		self.last = False
		self.waves = []
		self.powerup = []
		self.boss_class = boss
		self.boss = None

	def update(self, dt):
		self.timer -= dt
		if self.timer <= 0:
			if self.last:
				self.boss = self.boss_class()
				self.timer = 999
			else:
				pattern = self.patterns.pop(0)
				if len(self.patterns) == 0:
					self.last = True
				self.waiting = False
				self.waves.append(pattern.spawn())
				self.powerup.append(True)
				self.timer = pattern.timer
		i = 0
		if self.boss != None:
			self.boss.update(dt)
		# Jesus what a mess
		while i < len(self.waves):
			w = self.waves[i]
			if len(w) == 0:
				self.waves.pop(i)
				if self.powerup.pop(i):
					MISC_LIST.append(PowerUp(SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF))
				continue
			else:
				ii = 0
				while ii < len(w):
					obj = w[ii]
					if obj.garbage:
						# if enemy died from being offscreen no powerup is spawned
						if obj.offscreen:
							self.powerup[i] = False
						w.pop(ii)
					else:
						obj.update(dt)
						ii += 1
				i += 1
		
class Explode(pyglet.sprite.Sprite):
	"""Stationary explosion"""
	def __init__(self, x, y, image = explode64_anim):
		super().__init__(image, batch = BATCH)
		self.x = x
		self.y = y
		pyglet.clock.schedule_once(self.death, self.image.get_duration())
		self.garbage = False

	def update(self, dt):
		return

	def death(self, dt):
		self.garbage = True
		self.visible = False

# Helpers for making enemy formations
def triangle_formation(base, x, y, x_offset, y_offset, flip = False):
	x_list = []
	y_list = []
	layer = base
	while layer > 0:
		for i in range(layer):
			x_list.append(x - (0.5 * (layer - 1) * x_offset) + x_offset * i)
			y_list.append(y + (base - layer if flip else layer) * y_offset)
		layer -= 1
	return x_list, y_list

def rectangle_formation(width, height, x, y, x_offset, y_offset):
	x_list = []
	y_list = []
	for h in range(height):
		for w in range(width):
			x_list.append(x - (width - 1) * x_offset * 0.5 + x_offset * w)
			y_list.append(y + y_offset * h)
	return x_list, y_list


tri_4_x, tri_4_y = triangle_formation(4, SCREEN_WIDTH_HALF, 0, 64, 96)
rect_4_x, rect_4_y = rectangle_formation(4, 4, SCREEN_WIDTH_HALF, 0, 64, 96)

# Level 
WAVE_MOVE_TRI = EnemyPattern([Enemy], tri_4_x, tri_4_y, [lambda t, y: 100*math.sin(y*0.02)], 1.0)
WAVE_MOVE_RECT = EnemyPattern([Enemy], rect_4_x, rect_4_y, [lambda t, y: 100*math.sin(y*0.02)], 1.0)
WAVE_SINGLE_ENEMY = EnemyPattern([Enemy], [SCREEN_WIDTH_HALF], [0], [lambda t, y: 0], 0.1)

# WAVE_AIM = EnemyPattern([EnemyAims] * 4, [SCREEN_WIDTH // 2] * 4, [0.8] * 4)
# WAVE_STOP = EnemyPattern([EnemyStops] * 2, [96, SCREEN_WIDTH - 96], [1.0, 0.0])
# WAVE_1 = EnemyPattern([Enemy] * 8, [SCREEN_WIDTH - 64] * 8, [0.8] * 8)
# WAVE_2 = EnemyPattern([Enemy] * 8, [64] * 8, [0.8] * 8)
# WAVE_3 = EnemyPattern([Enemy, EnemyShoots] * 6, [64 + i*42 for i in range(12)], [1.0] * 12)
# WAVE_4 = EnemyPattern([Enemy, EnemyShoots] * 6, [SCREEN_WIDTH - 64 - i*42 for i in range(12)], [1.0] * 12)
# WAVE_DOUBLE = EnemyPattern([Enemy, EnemyShoots, EnemyShoots, Enemy] * 4, [SCREEN_WIDTH - 64, 64] * 8, [1.5, 0] * 8)

# TEST_LEVEL = LevelPattern([WAVE_AIM, WAVE_STOP, WAVE_1, WAVE_STOP, WAVE_2, WAVE_3, WAVE_4, WAVE_DOUBLE])
TEST_LEVEL = LevelPattern([WAVE_SINGLE_ENEMY], Boss)

WINDOW = pyglet.window.Window(width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
PLAYER = Player()

CURRENT_LEVEL = TEST_LEVEL

# Always with the labels
DEBUG_LABEL = pyglet.text.Label('DEBUGGEROO', 'Courier New', 14.0,
						True, False, (255, 150, 50, 255),
						5, SCREEN_HEIGHT - 5, SCREEN_WIDTH - 10,
						anchor_y = 'top', multiline = True)

# Score label on other side
SCORE_LABEL = pyglet.text.Label('SCORESTUFFS', 'Courier New', 20.0,
						True, False, (150, 130, 255, 255),
						SCREEN_WIDTH - 5, SCREEN_HEIGHT - 5, SCREEN_WIDTH - 10, 100,
						'right', 'top', 'right', True)

# Center label
CENTER_LABEL = pyglet.text.Label('', 'Comic Sans MS', 40.0,
								False, False, (255, 255, 255, 255),
								SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, 200,
								'center', 'center','center', multiline = True, batch = BATCH)

def update_debug_label(dt):
	DEBUG_LABEL.text = "FPS: {:.2f} (dt:{:.5f})".format(pyglet.clock.get_fps(), dt)
	DEBUG_LABEL.text += "\nPlayer {:.1f}, {:.1f} |Bullets: {} |D: {}".format(PLAYER.x, PLAYER.y, len(PLAYER_BULLET_LIST), PLAYER.dead)
	DEBUG_LABEL.text += "\nEnemies: {} |Bullets: {}".format(len(ENEMY_LIST), len(ENEMY_BULLET_LIST))

def update_score_label():
	SCORE_LABEL.text = "Score: {}\nGuys: {}".format(0, PLAYER.lives)


def player_collision_tick(dt):
	if PLAYER.dead or PLAYER.invunerable > 0: return
	px = PLAYER.x + PLAYER_HIT_X
	py = PLAYER.y + PLAYER_HIT_Y
	for b in ENEMY_BULLET_LIST:
		dx = b.x - px
		dy = b.y - py
		# Check radii
		if dx**2 + dy**2 < PLAYER_HIT_RADIUS2 + ENEMY_BULLET_RADIUS2:
			print("DEAD PLAYER")
			PLAYER.death()
			b.garbage = True
			update_score_label()

	for e in MISC_LIST:
		if issubclass(e.__class__, PowerUp):
			dx = e.x - px
			dy = e.y - py
			# Check radii
			if dx**2 + dy**2 < PLAYER_HIT_RADIUS2 + POWERUP_RADIUS2:
				print("POWAH UP!")
				PLAYER.power_level += 1
				e.garbage = True
				e.visible = False



def enemy_collision_tick(dt):
	for w in CURRENT_LEVEL.waves:
		for e in w:
			for b in PLAYER_BULLET_LIST:
				if b.garbage: continue
				cx = min(max(b.x, e.x - e.box[0]), e.x + e.box[0])
				cy = min(max(b.y, e.y - e.box[1]), e.y + e.box[1])
				if (cx - b.x)**2 + (cy - b.y)**2 < PLAYER_BULLET_RADIUS2:
					e.impact(b)
					b.garbage = True
	if CURRENT_LEVEL.boss != None:
		boss = CURRENT_LEVEL.boss
		for b in PLAYER_BULLET_LIST:
			if b.garbage: continue
			if (boss.x - b.x)**2 + (boss.y - b.y)**2 < PLAYER_BULLET_RADIUS2 + BOSS_MAIN_RADIUS2:
				boss.impact(b)
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
	elif key == KEY_CHEAT_POWERUP:
		MISC_LIST.append(PowerUp(200, 200))

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
	update_score_label()
	DEBUG_LABEL.draw()
	SCORE_LABEL.draw()

# Set everything up
def game_setup():
	pass

def game_over():
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

	if GAME_OVER:
		CENTER_LABEL.text = "Unacceptable.\nYou have failed."
	else:
		PLAYER.update(dt)
	TEST_LEVEL.update(dt)

	update_list(PLAYER_BULLET_LIST, dt)
	# update_list(ENEMY_LIST, dt)
	update_list(ENEMY_BULLET_LIST, dt)
	update_list(MISC_LIST, dt)

	player_collision_tick(dt)
	enemy_collision_tick(dt)
	
	update_debug_label(dt)

# Off we go then
game_setup()
pyglet.clock.schedule(game_update)
pyglet.app.run()
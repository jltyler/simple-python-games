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

# Help for other functions
HALF_PI = math.pi * 0.5
ONE_HALF_PI = math.pi + HALF_PI
TWO_PI = math.pi * 2

# Player settings
PLAYER_MOVE_SPEED = 250.0
PLAYER_MOVEMENT_BORDER = 24
PLAYER_DIAGONAL_MOD = 0.70710678118 # root of 2 over 2 (not used yet)
PLAYER_SLOW_MOD = 0.33
PLAYER_FIRE_RATE = 0.25
PLAYER_HIT_RADIUS = 3
PLAYER_HIT_RADIUS2 = PLAYER_HIT_RADIUS ** 2
PLAYER_HIT_X = 0
PLAYER_HIT_Y = 5
PLAYER_LIVES = 3
PLAYER_INVULNERABLE = 1.5
PLAYER_RESPAWN_TIMER = 2.0
PLAYER_SPAWN = [SCREEN_WIDTH_HALF, 150]
PLAYER_BOMBS = 1
PLAYER_SCORE = 0

BOMB_NOFIRE_TIME = 1.6
BOMB_TIMER = 0

# Weapon stuff
PLAYER_STARTING_POWER = 0
PLAYER_GUN_OFFSET_LEFT = (-8, 11)
PLAYER_GUN_OFFSET_RIGHT = (8, 11)
PLAYER_GUN_OFFSET_LEFT2 = (-14, 6)
PLAYER_GUN_OFFSET_RIGHT2 = (14, 6)

PLAYER_BULLET_SPEED = 450.0
PLAYER_BULLET_DAMAGE = 10.0
PLAYER_BULLET_RADIUS = 3
PLAYER_BULLET_RADIUS2 = PLAYER_BULLET_RADIUS**2

PLAYER_BIGBULLET_SPEED = 480.0
PLAYER_BIGBULLET_DAMAGE = 25.0
PLAYER_BIGBULLET_RADIUS = 4.5
PLAYER_BIGBULLET_RADIUS2 = PLAYER_BIGBULLET_RADIUS ** 2

PLAYER_FINALBULLET_SPEED = 510.0
PLAYER_FINALBULLET_DAMAGE = 45.0
PLAYER_FINALBULLET_RADIUS = 6
PLAYER_FINALBULLET_RADIUS2 = PLAYER_FINALBULLET_RADIUS ** 2


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
ENEMY2_SPREAD = math.radians(4)
ENEMY2_BULLETS = 4
ENEMY2_FIRE_RATE = 1.3
ENEMY2_FIRE_ANGLE = ONE_HALF_PI - (ENEMY2_SPREAD * (ENEMY2_BULLETS - 1)) / 2

ENEMY3_HEALTH = 340.0
ENEMY3_SPEED = 120.0
ENEMY3_FIRE_RATE = 1.2
Θ = math.radians(30)
ENEMY3_SPREAD = math.radians(20.0)
ENEMY3_FIRE_FUNC = lambda t, b: t*Θ + b*ENEMY3_SPREAD
ENEMY3_TARGET_Y = SCREEN_HEIGHT - 150
ENEMY3_TARGET_X = 150
ENEMY3_BULLETS = 18

ENEMY4_HEALTH = 45.0
ENEMY4_SPEED = 100.0
ENEMY4_FIRE_RATE = 0.8
ENEMY4_BULLETS = 3
ENEMY4_SPREAD = math.radians(4.0)
ENEMY4_SPREAD_OFF = (ENEMY4_SPREAD * (ENEMY4_BULLETS - 1)) / 2

# Boss settings
BOSS_INTRO_SPEED = 90 # 90
BOSS_INTRO_TIME = 4.0 # 4.0

BOSS_MAIN_RADIUS = 48
BOSS_MAIN_RADIUS2 = BOSS_MAIN_RADIUS ** 2

BOSS_MINI_OFFSET_X = 63
BOSS_MINI_OFFSET_Y = -21

BOSS_MINI_RADIUS = 10
BOSS_MINI_RADIUS2 = BOSS_MINI_RADIUS ** 2

BOSS_RAD_OFFSET_Y = -3

BOSS_HEALTH = 9000
BOSS_HEALTH_THRESHOLD = [0, BOSS_HEALTH * 0.7, BOSS_HEALTH * 0.15, 0, -10000] # Change stages at these health value

BOSS_MINI_HEALTH = 400
BOSS_MINI_LAUNCH_SPEED = 100
BOSS_MINI_LAUNCH_TIME = 1.5
BOSS_MINI_MOVE_TIMER = 0.6
BOSS_MINI_MOVE_TIMER_VARIANCE = 0.3
BOSS_MINI_MOVE_X_THRESHOLD = [SCREEN_WIDTH_HALF // 2]
BOSS_MINI_MOVE_Y_THRESHOLD = [SCREEN_HEIGHT_HALF - 100, SCREEN_HEIGHT_HALF + 300]
BOSS_MINI_MOVE_SPEED = 120
BOSS_MINI_FIRE_TIME = 0.9

BOSS_X_RANGE_S1 = 100
BOSS_WEAPON_WAIT_S1 = 1.0 # 4.0
BOSS_WEAPON_BURST_S1 = 3.5 # 3.5

BOSS_X_RANGE_S2 = 250
BOSS_WEAPON_WAIT_S2 = 0.67
BOSS_WEAPON_BURST_S2 = 3.3
BOSS_SPEED_S2 = 4.0

BOSS_X_RANGE_S3 = 300
BOSS_FADEOUT_RATE_S3 = 255
BOSS_FADEIN_RATE_S3 = 255
BOSS_WEAPON_BURST_S3 = 1.5


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
KEY_BOMB_SCREEN = pyglet.window.key.C

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
player_finalbullet_image = prepare_image("img/player_finalbullet.png")
bullet_image = prepare_image("img/bullet.png")
enemy_image = prepare_image("img/enemy.png")
enemy_shooter_image = prepare_image("img/enemy_shoot.png")
enemy_stop_image = prepare_image("img/enemy_stop.png")
enemy_aim_image = prepare_image("img/enemy_aim.png")
boss_image = prepare_image("img/boss_wip.png")
boss_mini_image = prepare_image("img/boss_mini.png")

powerup_anim, powerup_sheet = prepare_anim("img/powerup1.png", 1, 8, 0.125)
bombup_anim, bombup_sheet = prepare_anim("img/bombup.png", 1, 10, 0.125)
scoreup_anim, scoreup_sheet = prepare_anim("img/scoreup.png", 1, 10, 0.1)
explode64_anim, explode64_sheet = prepare_anim("img/explode64.png", 1, 8, 0.04)
bullet_pop_anim, bullet_pop_sheet = prepare_anim("img/bullet_pop.png", 1, 8, 0.08)



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

def fire_weapon_4(player):
	fire_weapon_3(player)
	PLAYER_BULLET_LIST.append(PlayerDiagBullet(player.x + PLAYER_GUN_OFFSET_LEFT[0], player.y + PLAYER_GUN_OFFSET_LEFT[1], True))
	PLAYER_BULLET_LIST.append(PlayerDiagBullet(player.x + PLAYER_GUN_OFFSET_RIGHT[0], player.y + PLAYER_GUN_OFFSET_RIGHT[1]))
	PLAYER_BULLET_LIST.append(PlayerFinalBullet(player.x, player.y + 12))

# Fire function array
fire_weapon = [fire_weapon_0, fire_weapon_1, fire_weapon_2, fire_weapon_3, fire_weapon_4]

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
		self.power_level = PLAYER_STARTING_POWER
		self.dead = False
		self.lives = PLAYER_LIVES
		self.invunerable = PLAYER_INVULNERABLE
		self.respawn_timer = PLAYER_RESPAWN_TIMER
		self.bombs = PLAYER_BOMBS

	def update(self, dt):
		if self.dead:
			self.respawn_timer -= dt
			if self.respawn_timer <= 0:
				self.dead = False
				self.invunerable = PLAYER_INVULNERABLE
				self.x = PLAYER_SPAWN[0]
				self.y = PLAYER_SPAWN[1]
				self.visible = True
				self.power_level = max(0, self.power_level - 2)

			return				
		self.invunerable -= dt
		# Terrible movement code
		if self.moving[0] != 0:
			self.x += self.moving[0] * PLAYER_MOVE_SPEED * self.speed_multi * dt
			if self.x < PLAYER_MOVEMENT_BORDER:
				self.x = PLAYER_MOVEMENT_BORDER
			elif self.x > SCREEN_WIDTH - PLAYER_MOVEMENT_BORDER:
				self.x = SCREEN_WIDTH - PLAYER_MOVEMENT_BORDER
		if self.moving[1] != 0:
			self.y += self.moving[1] * PLAYER_MOVE_SPEED * self.speed_multi * dt
			if self.y < PLAYER_MOVEMENT_BORDER:
				self.y = PLAYER_MOVEMENT_BORDER
			elif self.y > SCREEN_HEIGHT - PLAYER_MOVEMENT_BORDER:
				self.y = SCREEN_HEIGHT - PLAYER_MOVEMENT_BORDER

		# SHooties
		self.btimer -= dt
		if self.shooting:
			if self.btimer <= 0:
				self.btimer = PLAYER_FIRE_RATE
				fire_weapon[min(self.power_level, len(fire_weapon) - 1)](self)

	def death(self):
		self.visible = False
		MISC_LIST.append(Explode(self.x, self.y))
		self.dead = True
		if self.lives == 0:
			global GAME_OVER
			GAME_OVER = True
			return
		self.lives-= 1
		self.respawn_timer = PLAYER_RESPAWN_TIMER

	def bomb_screen(self):
		if self.bombs == 0: return
		self.bombs -= 1
		global BOMB_TIMER
		BOMB_TIMER = GAME_TIMER + BOMB_NOFIRE_TIME
		for b in ENEMY_BULLET_LIST:
			b.death()


class PlayerBullet(pyglet.sprite.Sprite):
	"""Bullet shot by player, collides with enemies"""
	def __init__(self, x, y, damage = PLAYER_BULLET_DAMAGE, image = player_bullet_image, radius = PLAYER_BULLET_RADIUS2):
		super().__init__(image, batch = BATCH)
		self.x = x
		self.y = y
		self.garbage = False
		self.damage = damage
		self.radius = radius

	def update(self, dt):
		# Go up
		self.y += PLAYER_BULLET_SPEED * dt
		if self.y > SCREEN_HEIGHT:
			self.garbage = True

class PlayerBigBullet(PlayerBullet):
	"""Big bullet does more damage and travels slightly faster"""
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_BIGBULLET_DAMAGE, player_bigbullet_image, PLAYER_BIGBULLET_RADIUS2)

	def update(self, dt):
		self.y += PLAYER_BIGBULLET_SPEED * dt
		if self.y > SCREEN_HEIGHT:
			self.garbage = True

class PlayerFinalBullet(PlayerBullet):
	"""Wave lookin bullet that devestates enemies"""
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_FINALBULLET_DAMAGE, player_finalbullet_image, PLAYER_FINALBULLET_RADIUS2)

	def update(self, dt):
		self.y += PLAYER_FINALBULLET_SPEED * dt
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
	def __init__(self, x, y, image = powerup_anim):
		super().__init__(image, batch = BATCH)
		self.x = x
		self.y = y
		self.timer = POWERUP_MOVE_TIMER
		self.new_dir()
		self.garbage = False

	def update(self, dt):
		self.x += self.speed_x * dt
		if self.x < PLAYER_MOVEMENT_BORDER or self.x > SCREEN_WIDTH - PLAYER_MOVEMENT_BORDER:
			self.speed_x *= -1
		self.y += self.speed_y * dt
		if self.y < PLAYER_MOVEMENT_BORDER or self.y > SCREEN_HEIGHT - PLAYER_MOVEMENT_BORDER:
			self.speed_y *= -1
		self.timer -= dt
		if self.timer <= 0:
			self.timer = POWERUP_MOVE_TIMER
			self.new_dir()

	def new_dir(self):
		angle = random.uniform(0, TWO_PI)
		self.speed_x = math.cos(angle) * POWERUP_MOVE_SPEED
		self.speed_y = math.sin(angle) * POWERUP_MOVE_SPEED

	def powerup(self, player):
		print("POWUH UP")
		player.power_level += 1
		self.garbage = True
		self.visible = False


class BombUp(PowerUp):
	"""Extra bomb"""
	def __init__(self, x, y):
		super().__init__(x, y, bombup_anim)

	def powerup(self, player):
		print("BOM SUP")
		player.bombs += 1
		self.garbage = True
		self.visible = False		

class ScoreUp(PowerUp):
	"""Point boost (default powerup)"""
	def __init__(self, x, y):
		super().__init__(x, y, scoreup_anim)

	def powerup(self, player):
		print("SCOr UP")
		global PLAYER_SCORE
		PLAYER_SCORE += 1000
		self.garbage = True
		self.visible = False
		


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

	def death(self):
		self.garbage = True
		MISC_LIST.append(Explode(self.x, self.y, bullet_pop_anim))
		self.delete()


class Spawner():
	"""Spawns bullets with a pattern"""
	def __init__(self, attached, base_angle = 0, fire_rate = 0.25, base_speed = ENEMY_BULLET_SPEED, bullets = 1, x_scale = 1.0, y_scale = 1.0):
		self.attached = attached
		self.base_angle = base_angle
		self.fire_rate = fire_rate
		self.base_speed = base_speed
		self.bullets = bullets
		self.x_scale = x_scale
		self.y_scale = y_scale
		self.btimer = fire_rate
		self.speed_func = lambda t, b: 0
		self.angle_func = lambda t, b: 0
		self.active = True
		self.timer = 0.0
		self.x_offset = 0
		self.y_offset = 0

	def spawn(self, timer):
		if GAME_TIMER < BOMB_TIMER: return
		for i in range(self.bullets):
			angle = self.base_angle + self.angle_func(timer, i)
			speed = self.base_speed + abs(self.speed_func(timer, i))
			i_x = math.cos(angle) * speed * self.x_scale
			i_y = math.sin(angle) * speed * self.y_scale
			ENEMY_BULLET_LIST.append(EnemyBullet(self.attached.x + self.x_offset, self.attached.y + self.y_offset, 0, 0, [i_x, i_y]))

	def update(self, dt):
		if not self.active: return
		self.btimer -= dt
		self.timer += dt
		if self.btimer <= 0:
			self.spawn(self.timer)
			self.btimer = self.fire_rate

	def copy(self):
		new_spawner = Spawner(self.attached, self.base_angle, self.fire_rate, self.base_speed, self.bullets, self.x_scale, self.y_scale)
		new_spawner.speed_func = self.speed_func
		new_spawner.angle_func = self.angle_func
		new_spawner.x_offset = self.x_offset
		new_spawner.y_offset = self.y_offset
		return new_spawner

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
		self.point_value = 50

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
		global PLAYER_SCORE
		PLAYER_SCORE += self.point_value
		MISC_LIST.append(Explode(self.x, self.y))

class EnemyWavey(Enemy):
	"""Duplicate of basic enemy moves to the center"""
	def __init__(self, x, y):
		super().__init__(x, y)
		if self.x < SCREEN_WIDTH_HALF:
			self.x_speed_func = lambda t, y: math.sin(y*0.01)*114
		else:
			self.x_speed_func = lambda t, y: math.sin(y*0.01)*-114
		self.point_value = 75

		

class EnemyShoots(Enemy):
	"""Enemy that fires triples at a fixed angle"""
	def __init__(self, x, y):
		super().__init__(x, y, enemy_shooter_image)
		self.health = ENEMY2_HEALTH
		self.weapon = Spawner(self, ENEMY2_FIRE_ANGLE, ENEMY2_FIRE_RATE, ENEMY_BULLET_SPEED, ENEMY2_BULLETS)
		self.weapon.angle_func = lambda t, b: b * ENEMY2_SPREAD
		self.point_value = 75

	def update(self, dt):
		super().update(dt)
		if self.garbage: return
		self.weapon.update(dt)

class EnemyStops(Enemy):
	"""Goes to a point on the screen then stops and starts firing"""
	def __init__(self, x, y, target_x = None, target_y = None):
		super().__init__(x, y, enemy_stop_image)
		if target_x == None:
			if x < SCREEN_WIDTH_HALF:
				target_x = ENEMY3_TARGET_X
			else:
				target_x = SCREEN_WIDTH - ENEMY3_TARGET_X
		self.target_x = target_x
		if target_y == None:
			target_y = ENEMY3_TARGET_Y
		self.target_y = target_y
		self.weapon = Spawner(self, 0, ENEMY3_FIRE_RATE, ENEMY_BULLET_SPEED, ENEMY3_BULLETS)
		self.weapon.angle_func = ENEMY3_FIRE_FUNC
		self.stopped = False
		self.health = ENEMY3_HEALTH
		self.point_value = 350

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

def get_dir_rad(x1, y1, x2, y2):
	dx = x2 - x1
	dy = y2 - y1
	# lets not divide by zero now
	if dy == 0:
		return 0.0 if dx >= 0 else math.pi
	elif dx == 0:
		return HALF_PI if dy >= 0 else ONE_HALF_PI
	raw = math.atan2(dy, dx)
	return raw if raw >= 0 else TWO_PI + raw

class EnemyAims(Enemy):
	"""Enemy that moves down like others but aims at the player when it fires it's weapon"""
	def __init__(self, x, y):
		super().__init__(x, y, enemy_aim_image)
		self.weapon = Spawner(self, 0, ENEMY4_FIRE_RATE, ENEMY_BULLET_SPEED, ENEMY4_BULLETS)
		self.health = ENEMY4_HEALTH
		self.weapon.angle_func = lambda t, b: get_dir_rad(self.x, self.y, PLAYER.x, PLAYER.y) - ENEMY4_SPREAD_OFF + b * ENEMY4_SPREAD
		self.point_value = 100
	
	def update(self, dt):
		super().update(dt)
		if self.garbage: return
		# self.weapon.base_angle = get_dir(self.x, self.y, PLAYER.x, PLAYER.y)
		self.weapon.update(dt)

class BossMinion(pyglet.sprite.Sprite):
	"""Mini flyer connected to boss n blasts shit yo"""
	def __init__(self, boss, left = False):
		super().__init__(boss_mini_image, batch = BATCH)
		self.health = BOSS_MINI_HEALTH
		self.launching = True
		self.timer = 0
		self.boss = boss
		self.left = left
		Θ = math.radians(300)
		self.launch_speed = [BOSS_MINI_LAUNCH_SPEED * math.cos(Θ), BOSS_MINI_LAUNCH_SPEED * math.sin(Θ)]
		self.boundary = [
		SCREEN_WIDTH_HALF, BOSS_MINI_MOVE_Y_THRESHOLD[0], 
		SCREEN_WIDTH, BOSS_MINI_MOVE_Y_THRESHOLD[1]]
		if self.left:
			self.launch_speed[0] *= -1
			self.boundary[0] = 0
			self.boundary[2] = SCREEN_WIDTH_HALF
		self.move_timer = 0
		self.moves_left = 3
		self.firing = False
		self.weapons = []
		self.dead = False
		self.active = False

		weapon_a = Spawner(self, 0, 0.25, ENEMY_BULLET_SPEED, 10)
		Θ = math.radians(36)
		weapon_a.angle_func = lambda t, b: t + b * Θ
		weapon_b = Spawner(self, 0, 0.25)
		weapon_b.angle_func = lambda t, b: get_dir_rad(self.x, self.y, PLAYER.x, PLAYER.y)

		self.weapons.append([weapon_a, weapon_b])


	def update(self, dt):
		if self.dead: return
		self.timer += dt
		if self.launching:
			self.x += self.launch_speed[0] * dt
			self.y += self.launch_speed[1] * dt
			if self.timer >= BOSS_MINI_LAUNCH_TIME: self.launching = False
		else:
			self.move_timer -= dt
			if self.firing:
				for w in self.active: w.update(dt)
				if self.move_timer <= 0:
					self.firing = False
					self.move_timer = random.uniform(BOSS_MINI_MOVE_TIMER, BOSS_MINI_MOVE_TIMER + BOSS_MINI_MOVE_TIMER_VARIANCE)
					self.moves_left = 3
					self.new_direction()

			if self.move_timer <= 0:
				self.move_timer = random.uniform(BOSS_MINI_MOVE_TIMER, BOSS_MINI_MOVE_TIMER + BOSS_MINI_MOVE_TIMER_VARIANCE)
				self.new_direction()
				self.moves_left -= 1
				if self.moves_left <= 0:
					self.firing = True
					self.move_timer = BOSS_MINI_FIRE_TIME
					self.active = random.choice(self.weapons)
					self.speed_x = 0
					self.speed_y = 0
			self.x += self.speed_x * dt
			self.y += self.speed_y * dt

	def impact(self, bullet):
		if self.dead: return
		if self.active:
			self.health -= bullet.damage
			if self.health <= 0:
				self.death()
		else:
			self.boss.impact(bullet)

	def death(self):
		if self.dead: return
		self.dead = True
		self.visible = False
		MISC_LIST.append(Explode(self.x, self.y))


	def new_direction(self):
		Θ = random.uniform(0, TWO_PI)
		self.speed_x = math.cos(Θ) * BOSS_MINI_MOVE_SPEED
		self.speed_y = math.sin(Θ) * BOSS_MINI_MOVE_SPEED
		if self.x < self.boundary[0]:
			self.speed_x = math.copysign(self.speed_x, 1)
		elif self.x > self.boundary[2]:
			self.speed_x = math.copysign(self.speed_x, -1)
		if self.y < self.boundary[1]:
			self.speed_y = math.copysign(self.speed_y, 1)
		elif self.y > self.boundary[3]:
			self.speed_y = math.copysign(self.speed_y, -1)


class Boss(pyglet.sprite.Sprite):
	"""Big ol blastro"""
	def __init__(self):
		super().__init__(boss_image, batch = BATCH)
		self.x = SCREEN_WIDTH_HALF
		self.y = SCREEN_HEIGHT + 200
		self.stage = 0
		self.health = BOSS_HEALTH
		self.timer = 0
		self.update_stage = [self.update_s0, self.update_s1, self.update_s2, self.update_s3, self.update_s4]
		self.weapons = [0]
		self.dead = False
		self.active = []

		# Mini flyers
		self.minion_l = BossMinion(self, True)
		self.minion_r = BossMinion(self)

		# WEAPON SET 1
		weapons_s1 = []

		# Twin spinnies
		weapon_a = Spawner(self, 0, 0.05, ENEMY_BULLET_SPEED, 2)
		weapon_a.angle_func = lambda t, b: t * 3 + b * math.pi
		weapon_a.x_offset = -BOSS_MINI_OFFSET_X
		weapon_a.y_offset = BOSS_MINI_OFFSET_Y
		weapon_b = weapon_a.copy() # Copy and mirror
		weapon_b.x_offset *= -1
		weapon_b.x_scale = -1
		weapons_s1.append([weapon_a, weapon_b])

		# Forward salvos
		weapon_a = Spawner(self, math.radians(270), 0.3, ENEMY_BULLET_SPEED, 4)
		weapon_a.angle_func = lambda t, b: 0.2 * math.sin(t * 3)
		weapon_a.speed_func = lambda t, b: b * 10
		weapon_a.x_offset = -BOSS_MINI_OFFSET_X
		weapon_a.y_offset = BOSS_MINI_OFFSET_Y
		weapon_b = weapon_a.copy()
		weapon_b.x_offset *= -1
		weapon_b.x_scale = -1
		weapons_s1.append([weapon_a, weapon_b])

		# Sun burst
		weapon_a = Spawner(self, math.radians(270), 0.2, ENEMY_BULLET_SPEED, 72)
		weapon_a.angle_func = lambda t, b: t * .2 + b * 0.349066
		weapon_a.speed_func = lambda t, b: (b+1) // 18 * 8
		weapons_s1.append([weapon_a])

		# Add to weapon array
		self.weapons.append(weapons_s1)
		# END WEAPON SET 1

		# WEAPON SET 2
		weapons_s2 = []

		# Sun burster
		weapon_a = Spawner(self, math.radians(270), 0.15, ENEMY_BULLET_SPEED, 72)
		Θ = math.radians(20)
		weapon_a.angle_func = lambda t, b: t * .15 + b * Θ
		weapon_a.speed_func = lambda t, b: (b+1) // 18 * 12
		weapons_s2.append([weapon_a])

		# Sin wave burst at player
		weapon_a = Spawner(self, 0, 0.15, ENEMY_BULLET_SPEED, 5)
		max_Θ = math.radians(20)
		weapon_a.angle_func = lambda t, b: get_dir_rad(self.x, self.y, PLAYER.x, PLAYER.y) + (b-2) * max_Θ * math.sin(t*3)
		weapons_s2.append([weapon_a])

		self.weapons.append(weapons_s2)
		# END WEAPON SET 2
		# WEAPON SET 3
		weapons_s3 = []

		# Big spinny
		weapon_a = Spawner(self, 0, 0.08, ENEMY_BULLET_SPEED, 40)
		Θ = math.radians(18)
		weapon_a.angle_func = lambda t, b: t*2 + Θ * math.sin(t*3) + b * Θ
		weapons_s3.append([weapon_a])

		# Fast burst
		weapon_a = Spawner(self, 0, 0.25, ENEMY_BULLET_SPEED, 120)
		Θ = math.radians(11.25)
		weapon_a.angle_func = lambda t, b: t//0.25*Θ + b * Θ*2
		weapon_a.speed_func = lambda t, b: 30 * b//8
		weapons_s3.append([weapon_a])

		self.weapons.append(weapons_s3)
		# END WEAPON SET 3

		self.weapon_timer = BOSS_WEAPON_WAIT_S1
		self.move_timer = 0
		self.firing = False
		self.active = None
		self.move_target_x = SCREEN_WIDTH_HALF

	def update(self, dt):
		self.timer += dt
		self.update_stage[self.stage](dt)

	def impact(self, bullet):
		if self.stage == 0: return
		self.health -= bullet.damage
		if self.health < BOSS_HEALTH_THRESHOLD[self.stage]:
			self.next_stage()

	def next_stage(self):
		self.stage += 1
		self.timer = 0
		if self.stage == 2:
			self.move_target_x = self.x
			self.weapon_timer = 0
		elif self.stage == 3:
			self.fade = 0
		elif self.stage == 4:
			self.minion_l.death()
			self.minion_r.death()
			self.move_timer = 0
			self.weapon_timer = 3.6

	def update_s0(self, dt):
		self.y -= BOSS_INTRO_SPEED * dt
		self.minion_l.set_position(self.x - BOSS_MINI_OFFSET_X, self.y + BOSS_MINI_OFFSET_Y)
		self.minion_r.set_position(self.x + BOSS_MINI_OFFSET_X, self.y + BOSS_MINI_OFFSET_Y)
		if self.timer >= BOSS_INTRO_TIME:
			self.next_stage()

	def update_s1(self, dt):
		self.x = SCREEN_WIDTH_HALF + ( BOSS_X_RANGE_S1 * math.sin(self.timer) )
		self.minion_l.set_position(self.x - BOSS_MINI_OFFSET_X, self.y + BOSS_MINI_OFFSET_Y)
		self.minion_r.set_position(self.x + BOSS_MINI_OFFSET_X, self.y + BOSS_MINI_OFFSET_Y)
		self.weapon_timer -= dt
		if self.weapon_timer <= 0:
			self.weapon_timer = BOSS_WEAPON_WAIT_S1 if self.firing else BOSS_WEAPON_BURST_S1
			self.firing = not self.firing
			self.active = random.choice(self.weapons[self.stage])
			for a in self.active: a.timer = 0
		if self.firing:
			for w in self.active:
				w.update(dt)

	def update_s2(self, dt):
		self.minion_l.update(dt)
		self.minion_r.update(dt)
		if abs(self.x - self.move_target_x) < 2:
			if self.weapon_timer <= 0:
				# Pick a new spot to move to
				self.move_target_x = random.uniform(SCREEN_WIDTH_HALF - BOSS_X_RANGE_S2, SCREEN_WIDTH_HALF + BOSS_X_RANGE_S2)
				self.move_diff = (self.move_target_x - self.x) * 0.5
				self.move_half = self.move_target_x - self.move_diff
				self.x_dir = math.copysign(1, self.move_diff)
				# print("Picking new spot: {}\n{}\n{}\n{}\n{}".format(self.x, self.move_target_x, self.move_diff, self.move_half, self.x_dir))
				self.weapon_timer = BOSS_WEAPON_BURST_S2
				self.active = random.choice(self.weapons[self.stage])
			else:
				self.weapon_timer -= dt
				for w in self.active:
					w.update(dt)
		else:
			self.x += min(50, max(5, abs(self.move_diff) - abs(self.move_half - self.x))) * BOSS_SPEED_S2 * self.x_dir * dt

	def update_s3(self, dt):
		self.minion_l.update(dt*1.5)
		self.minion_r.update(dt*1.5)
		if self.fade == 0:
			self.weapon_timer -= dt
			for w in self.active: w.update(dt)
			if self.weapon_timer <= 0:
				self.fade = 1
		elif self.fade == 1:
			self.opacity -= BOSS_FADEOUT_RATE_S3 * dt
			if self.opacity <= 0:
				self.opacity = 0
				self.x = random.randrange(SCREEN_WIDTH_HALF - BOSS_X_RANGE_S3, SCREEN_WIDTH_HALF + BOSS_X_RANGE_S3)
				self.fade = -1
		elif self.fade == -1:
			self.opacity += BOSS_FADEIN_RATE_S3 * dt
			if self.opacity >= 255:
				self.opacity = 255
				self.fade = 0
				self.active = random.choice(self.weapons[self.stage])
				self.weapon_timer = BOSS_WEAPON_BURST_S3

	def update_s4(self, dt):
		if self.dead: return
		self.weapon_timer -= dt
		if self.weapon_timer <= 0 and not self.dead:
			self.visible = False
			self.dead = True
			MISC_LIST.append(ExplodeBig(self.x, self.y))
			CENTER_LABEL.text = "Youre winner"
			return
		self.move_timer -= dt
		if self.move_timer <= 0:
			self.move_timer = random.uniform(0.15, 0.3)
			Θ = random.uniform(0, TWO_PI)
			speed = random.uniform(300, 550)
			self.x_speed = math.cos(Θ) * speed
			self.y_speed = math.sin(Θ) * speed
		self.x += self.x_speed * dt
		self.y += self.y_speed * dt
		self.x_speed *= 0.8
		self.y_speed *= 0.8
		MISC_LIST.append(
			Explode(self.x - self.image.anchor_x + random.uniform(0, self.width),
					self.y - self.image.anchor_y + random.uniform(0, self.height)))






class EnemyPattern():
	"""Spawning pattern for enemies"""
	def __init__(self, enemy_list, x_list, y_list, timer = WAVE_SPAWN_WAIT, bonus = ScoreUp):
		biggest = max(len(enemy_list), len(x_list), len(y_list))
		self.enemy_list = enemy_list # List of enemy types to spawn
		self.fill(self.enemy_list, biggest)
		self.x_list = x_list # List of x locations to spawn at
		self.fill(self.x_list, biggest)
		self.y_list = y_list # List of y locations to spawn at
		self.fill(self.y_list, biggest)
		self.timer = timer
		self.bonus = bonus

	def spawn(self):
		wave = []
		for etype, x, y in zip(self.enemy_list, self.x_list, self.y_list):
			enemy = etype(x, WAVE_SPAWN_Y + y)
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
				self.powerup.append(pattern.bonus)
				self.timer = pattern.timer
		i = 0
		if self.boss != None:
			self.boss.update(dt)
		# Jesus what a mess
		while i < len(self.waves):
			w = self.waves[i]
			if len(w) == 0:
				self.waves.pop(i)
				bonus = self.powerup.pop(i)
				if bonus != None:
					MISC_LIST.append(bonus(SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF))
				continue
			else:
				ii = 0
				while ii < len(w):
					obj = w[ii]
					if obj.garbage:
						# if enemy died from being offscreen no powerup is spawned
						if obj.offscreen:
							self.powerup[i] = None
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
		self.timer = self.image.get_duration()
		self.garbage = False
		self.color = (random.randrange(255), random.randrange(255), random.randrange(255))

	def update(self, dt):
		self.timer -= dt
		if self.timer <= 0:
			self.death()

	def death(self):
		self.garbage = True
		self.delete()
		# self.visible = False

class ExplodeBig(Explode):
	"""Growing explosion"""
	def __init__(self, x, y, image = explode64_anim):
		super().__init__(x, y, image)

	def update(self, dt):
		self.scale += 0.33
		super().update(dt)
		
		

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


tri_4_x, tri_4_y = triangle_formation(4, SCREEN_WIDTH_HALF, 0, 64, 96, True)
tri_8_x, tri_8_y = triangle_formation(8, SCREEN_WIDTH_HALF, 0, 48, 64)
rect_3x5_x, rect_3x5_y = rectangle_formation(3, 5, SCREEN_WIDTH_HALF, 0, 96, 160)
rect_3x3_x, rect_3x3_y = rectangle_formation(3, 3, SCREEN_WIDTH_HALF, 0, 96, 96)
sideline_x, sideline_y = rectangle_formation(2, 8, SCREEN_WIDTH_HALF, 0, SCREEN_WIDTH - 128, 128)

# Level 
# WAVE_MOVE_TRI = EnemyPattern([Enemy], tri_4_x, tri_4_y, [lambda t, y: 100*math.sin(y*0.02)], 1.0)
# WAVE_MOVE_RECT = EnemyPattern([Enemy], rect_4_x, rect_4_y, [lambda t, y: 100*math.sin(y*0.02)], 1.0)
WAVE_SINGLE_ENEMY = EnemyPattern([Enemy], [SCREEN_WIDTH_HALF], [0], 0.1)
# WAVE_SINGLE_ENEMY2 = EnemyPattern([Enemy], [SCREEN_WIDTH_HALF], [0], [lambda t, y: 0], 0.1, BombUp)

# ACTUAL LEVEL STUFF

WAVE_1 = EnemyPattern([Enemy], rect_3x5_x, rect_3x5_y, 12)
WAVE_2 = EnemyPattern([EnemyShoots, EnemyShoots, EnemyShoots, Enemy], rect_3x3_x, rect_3x3_y, 10, PowerUp)
WAVE_3 = EnemyPattern([EnemyStops], [SCREEN_WIDTH_HALF - 100, SCREEN_WIDTH_HALF + 100], [0], 3, BombUp)
WAVE_4 = EnemyPattern([Enemy], sideline_x, sideline_y, 12)
WAVE_5 = EnemyPattern([EnemyWavey], sideline_x, sideline_y, 12, PowerUp)
WAVE_6 = EnemyPattern([EnemyAims, EnemyShoots, EnemyShoots, EnemyAims, Enemy], tri_4_x, tri_4_y, 7)
WAVE_7 = EnemyPattern([Enemy], tri_8_x, tri_8_y, 12, PowerUp)
w8e = [EnemyAims] * 8
w8e.extend([EnemyShoots] * 7)
w8e.append(Enemy)
WAVE_8 = EnemyPattern(w8e, tri_8_x, tri_8_y, 12, PowerUp)

# WAVE_AIM = EnemyPattern([EnemyAims] * 4, [SCREEN_WIDTH // 2] * 4, [0.8] * 4
# WAVE_STOP = EnemyPattern([EnemyStops] * 2, [96, SCREEN_WIDTH - 96], [1.0, 0.0])
# WAVE_1 = EnemyPattern([Enemy] * 8, [SCREEN_WIDTH - 64] * 8, [0.8] * 8)
# WAVE_2 = EnemyPattern([Enemy] * 8, [64] * 8, [0.8] * 8)
# WAVE_3 = EnemyPattern([Enemy, EnemyShoots] * 6, [64 + i*42 for i in range(12)], [1.0] * 12)
# WAVE_4 = EnemyPattern([Enemy, EnemyShoots] * 6, [SCREEN_WIDTH - 64 - i*42 for i in range(12)], [1.0] * 12)
# WAVE_DOUBLE = EnemyPattern([Enemy, EnemyShoots, EnemyShoots, Enemy] * 4, [SCREEN_WIDTH - 64, 64] * 8, [1.5, 0] * 8)

# TEST_LEVEL = LevelPattern([WAVE_AIM, WAVE_STOP, WAVE_1, WAVE_STOP, WAVE_2, WAVE_3, WAVE_4, WAVE_DOUBLE])
TEST_LEVEL = LevelPattern([WAVE_1, WAVE_2, WAVE_3, WAVE_1, WAVE_4, WAVE_5, WAVE_6, WAVE_7, WAVE_8, WAVE_1], Boss)
# TEST_LEVEL = LevelPattern([WAVE_SINGLE_ENEMY], Boss)

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
	DEBUG_LABEL.text += "\nMisc ents: {}".format(len(MISC_LIST))
	if CURRENT_LEVEL.boss != None:
		DEBUG_LABEL.text += "\nBoss: {:.2f}, {:.2f} H: {} ({}) {}".format(CURRENT_LEVEL.boss.x, CURRENT_LEVEL.boss.y, CURRENT_LEVEL.boss.health, CURRENT_LEVEL.boss.stage, CURRENT_LEVEL.boss.weapon_timer)


def update_score_label():
	SCORE_LABEL.text = "Score: {}\nLives: {}\nBombs: {}".format(PLAYER_SCORE, PLAYER.lives, PLAYER.bombs)


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
			b.death()
			update_score_label()

	for e in MISC_LIST:
		if issubclass(e.__class__, PowerUp):
			dx = e.x - px
			dy = e.y - py
			# Check radii
			if dx**2 + dy**2 < PLAYER_HIT_RADIUS2 + POWERUP_RADIUS2:
				e.powerup(PLAYER)



def enemy_collision_tick(dt):
	for w in CURRENT_LEVEL.waves:
		for e in w:
			for b in PLAYER_BULLET_LIST:
				if b.garbage: continue
				cx = min(max(b.x, e.x - e.box[0]), e.x + e.box[0])
				cy = min(max(b.y, e.y - e.box[1]), e.y + e.box[1])
				if (cx - b.x)**2 + (cy - b.y)**2 < b.radius:
					e.impact(b)
					b.garbage = True
	if CURRENT_LEVEL.boss != None:
		boss = CURRENT_LEVEL.boss
		for b in PLAYER_BULLET_LIST:
			if b.garbage: continue
			if (boss.x - b.x)**2 + (boss.y - b.y)**2 < b.radius + BOSS_MAIN_RADIUS2:
				boss.impact(b)
				b.garbage = True
			if (boss.minion_r.x - b.x) ** 2 + (boss.minion_r.y - b.y) ** 2 < b.radius + BOSS_MINI_RADIUS2:
				boss.minion_r.impact(b)
				b.garbage = True
			if (boss.minion_l.x - b.x) ** 2 + (boss.minion_l.y - b.y) ** 2 < b.radius + BOSS_MINI_RADIUS2:
				boss.minion_l.impact(b)
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
	elif key == KEY_BOMB_SCREEN:
		PLAYER.bomb_screen()

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
	if DEBUG_PRINTOUT:
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
			e = ulist.pop(i)
			del e
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
import pyglet
import math

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 960

BATCH = pyglet.graphics.Batch()
TIMER = 0

BULLET_LIST = []
SPAWNER_LIST = []

bullet_image = pyglet.image.load('bullet.png')
bullet_image.anchor_x = bullet_image.width // 2
bullet_image.anchor_y = bullet_image.height // 2

class Bullet(pyglet.sprite.Sprite):
	"""Bullet to use in the patterns"""
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

		if self.y > SCREEN_HEIGHT or self.y < 0 or self.x > SCREEN_WIDTH or self.x < 0:
			self.garbage = True

def get_default_speed(timer):
	return 0

def get_default_angle(timer):
	return 0


class Spawner():
	"""Spawns bullets with a pattern"""
	def __init__(self, x, y, fire_angle = 270, fire_rate = 0.25, base_speed = 350, bullets = 1, angle_offset = 15):
		super(Spawner, self).__init__()
		self.x = x
		self.y = y
		self.fire_angle = fire_angle
		self.fire_rate = fire_rate
		self.base_speed = base_speed
		self.bullets = bullets
		self.angle_offset = angle_offset
		self.btimer = fire_rate
		self.speed_func = get_default_speed
		self.angle_func = get_default_angle

	def spawn(self, timer):
		speed = self.base_speed + abs(self.speed_func(timer))
		angle = self.fire_angle + self.angle_func(timer)
		for i in range(self.bullets):
			BULLET_LIST.append(Bullet(self.x, self.y, speed, angle + i * self.angle_offset))

	def update(self, dt):
		self.btimer -= dt
		if self.btimer <= 0:
			self.spawn(TIMER)
			self.btimer = self.fire_rate

def game_setup():
	print("Setup")
	spawner1 = Spawner(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 96, 240, 0.05, 100, 6, 60)
	# spawner1.angle_func = lambda t: (math.sin(4 * t) * 30) + math.sin(0.8* t) * 45
	spawner1.angle_func = lambda t: t*165
	spawner1.speed_func = lambda t: math.sin(0.4* t) * 50
	SPAWNER_LIST.append(spawner1)
	print("Setup completed")

def game_update(dt):
	global TIMER
	TIMER += dt
	i = 0
	for s in SPAWNER_LIST:
		s.update(dt)
	while i < len(BULLET_LIST):
		b = BULLET_LIST[i]
		if b.garbage:
			BULLET_LIST.pop(i)
			continue
		b.update(dt)
		i += 1

WINDOW = pyglet.window.Window(width = SCREEN_WIDTH, height = SCREEN_HEIGHT)

@WINDOW.event
def on_draw():
	WINDOW.clear()
	BATCH.draw()

game_setup()
pyglet.clock.schedule(game_update)
pyglet.app.run()
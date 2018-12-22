scale = 6
import pyglet
from Unit import Unit
import random

class EnemyUnit(Unit):
	def __init__(self, character_anims, attacksound, deathanim, x, unitType):
		rows_y = [0*scale,24*scale, 48*scale, 72*scale]
		Unit.__init__(self, character_anims, attacksound, deathanim, rows_y[random.randint(0,3)], unitType)
		self.velocity *= -1
		self.storedvelocity *= -1
		self.sprite.x = x

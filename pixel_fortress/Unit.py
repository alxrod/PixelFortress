scale = 6
import pyglet


class Unit:
	def __init__(self, character_anims, attacksound, deathanim, row, unitType):
		y=row+8*scale
		self.attacksound = attacksound
		self.type = unitType
		self.velocity = 0.75
		self.anims = character_anims[self.type]
		self.death_anim = deathanim
		self.sprite = pyglet.sprite.Sprite(self.anims["walk"], x=scale*24, y=y)
		self.attackDistance = 10*scale
		self.health = 100
		self.damage = 0.5
		self.target = None
		if self.type == 0 or self.type == 3:
			self.velocity = 0.9
		if self.type == 1 or self.type==2 or self.type==4:
			if self.type == 1:
				self.health-=50
				self.damage *= 2
			if self.type == 2:
				self.health-=50
				self.damage *= 3
			self.attackDistance *= 5
		self.storedvelocity = self.velocity

		if self.type==5:
			self.damage*=8
			self.health*3

	def update(self, target_units):
		self.sprite.x += self.velocity
		if self.target == None:
			for target in target_units:
				if abs(self.sprite.x-target.sprite.x) < self.attackDistance and target.sprite.y == self.sprite.y:
					self.target = target
					self.velocity = 0
					self.attacksound.play()
					self.sprite.image = self.anims["attack"]
					break
		elif self.target.health > 0:
			self.target.health -= self.damage
		elif self.target.health <= 0:
			self.target = None
			self.velocity = self.storedvelocity
			self.sprite.image = self.anims["walk"]
				
		if self.health <= 0:
			self.sprite.image = self.death_anim


scale = 6
import pyglet

class UnitIcon:
	def __init__(self, unitType, image, sound):
		image_seq = pyglet.image.ImageGrid(image, 36*scale, 12*scale, item_width=12*scale, item_height=12*scale)
		self.type = unitType
		self.image = pyglet.image.TextureGrid(image_seq)[unitType]
		self.sprite = pyglet.sprite.Sprite(self.image, x=scale*1, y=scale*18+24*unitType*scale)
		self.sound = sound

	def detect_click(self, x,y):
		if x >= self.sprite.x and x <= self.sprite.x+self.sprite.width:
			if y >= self.sprite.y and y <= self.sprite.y+self.sprite.height:
				self.sound.play()
				return True 

		return False


	def onclick(self, click_position):
		return self.detect_click(click_position['x'],click_position['y'])





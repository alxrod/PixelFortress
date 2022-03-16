import pyglet
from pyglet.window import key, mouse
from UnitIcon import UnitIcon
from Unit import Unit
from EnemyUnit import EnemyUnit
import random
from pyglet import font
import json
import os 

scale = 6

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()
font.add_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../resources/DisposableDroidBB.ttf"))
ddbb = font.load("DisposableDroid BB")

window = pyglet.window.Window(1152,576)


def update(dt): 
	if option_arrows[0].x > 28*scale:
		arrowMove["forward"] = False
	if option_arrows[0].x < 22*scale:
		arrowMove["forward"] = True

	if commands["assigningUnit"] == True:
		for arrow in option_arrows:
			if arrowMove["forward"] == True:
				arrow.x += 1
			else:
				arrow.x -= 1

	for unit in player_units:
		unit.update(enemy_units)
		if unit.sprite.x > window.width-36*scale:
			del player_units[player_units.index(unit)]
			commands['score'] += 1+unit.type
			print(commands['score'])
		if unit.health <= 0:
			recently_killed.append(unit)
			del player_units[player_units.index(unit)]


	for enemy in enemy_units:
		enemy.update(player_units)
		if enemy.sprite.x < 20*scale:
			del enemy_units[enemy_units.index(enemy)]
			commands['score'] -= 1+enemy.type
			print(commands['score'])
		if enemy.health <= 0:
			recently_killed.append(enemy)
			del enemy_units[enemy_units.index(enemy)]

	for unit in recently_killed:
		if unit.sprite.x > window.width-36*scale or unit.sprite.x < 20*scale:
			del recently_killed[recently_killed.index(unit)]

	if commands['score'] <= 0:
		for u in player_units:
			del player_units[player_units.index(u)]
		for u in enemy_units:
			del enemy_units[enemy_units.index(u)]
		for u in recently_killed:
			del recently_killed[recently_killed.index(u)]
		pyglet.clock.unschedule(spawn_enemy)
		commands['score'] = 0
		enemyUnitMax = 0
		if commands['saved'] == False and commands['topscore'] > commands['highscore']:
			with open("scores.txt","w") as outfile:
				json.dump(commands['topscore'], outfile)
			outfile.close()
			commands['saved'] = True

	if commands['score'] > commands['topscore']:
		commands['topscore'] = commands['score']

	enemyUnitMax = 5+(commands["topscore"]-10)//5

def spawn_enemy(dt):
	chances = [3,3,3,3,3,3,3,3,4,4,4,5]
	if len(enemy_units) < enemyUnitMax:
		unitType = chances[random.randint(0,len(chances)-1)]
		if unitType == 3:
			sound = swordHit
		elif unitType == 4:
			sound = bowHit
		elif unitType == 5:
			sound = spellHit
		enemy = EnemyUnit(character_anims, sound, death_anim, window.width-40*scale, unitType)
		enemy_units.append(enemy)


def render_character_anims(character_image, death_images):
	image_seq = pyglet.image.ImageGrid(character_image, 6, 6, item_width=(16*scale), item_height=(16*scale))
	# print "size"
	image_texture = pyglet.image.TextureGrid(image_seq)
	# print len(image_texture)
	character_anims = []
	for i in range(6):
		unitType = 5-i
		animations = {"still": image_texture[(unitType*6)],
					  "walk": pyglet.image.Animation.from_image_sequence(image_texture[(unitType*6):(unitType*6+3)],0.2, loop=True),
					  "attack": pyglet.image.Animation.from_image_sequence(image_texture[(unitType*6+3):(unitType*6+6)],0.2, loop=True)}
		character_anims.append(animations)

	image_seq_death = pyglet.image.ImageGrid(death_images, 1, 4, item_width=16*scale, item_height=16*scale)
	image_texture_death = pyglet.image.TextureGrid(image_seq_death)
	deathanim = pyglet.image.Animation.from_image_sequence(image_texture_death[0:4], .15, loop=False)
	return character_anims, deathanim



@window.event
def on_key_press(symbol, modifiers):
	if commands["assigningUnit"] == True:
		if commands["selectedUnit"] == 0:
			sound = swordHit
		elif commands["selectedUnit"] == 1:
			sound = bowHit
		elif commands["selectedUnit"] == 2:
			sound = spellHit

		if symbol == key._1:
			commands["assigningUnit"] = False
			commands["selectedRow"] = 0
			player_units.append(Unit(character_anims, sound, death_anim, rows_y[commands["selectedRow"]], commands["selectedUnit"]))
			confirm_sound.play()
		if symbol == key._2:
			commands["assigningUnit"] = False
			commands["selectedRow"] = 1
			player_units.append(Unit(character_anims, sound, death_anim, rows_y[commands["selectedRow"]], commands["selectedUnit"]))
			confirm_sound.play()
		if symbol == key._3:
			commands["assigningUnit"] = False
			commands["selectedRow"] = 2
			player_units.append(Unit(character_anims, sound, death_anim, rows_y[commands["selectedRow"]], commands["selectedUnit"]))
			confirm_sound.play()
		if symbol == key._4:
			commands["assigningUnit"] = False
			commands["selectedRow"] = 3
			player_units.append(Unit(character_anims, sound, death_anim, rows_y[commands["selectedRow"]], commands["selectedUnit"]))
			confirm_sound.play()

	if symbol == key.W:
		if commands['currency'] >= 3:
			commands["assigningUnit"] = True
			commands["selectedUnit"] = 2
			commands['currency'] -= 3
		else:
			errorSound.play()
	if symbol == key.A:
		if commands['currency'] >= 2:
			commands["assigningUnit"] = True
			commands["selectedUnit"] = 1
			commands['currency'] -= 2
		else:
			errorSound.play()
	if symbol == key.S:
		if commands['currency'] >= 1:
			commands["assigningUnit"] = True
			commands["selectedUnit"] = 0
			commands['currency'] -= 1
		else:
			errorSound.play()

@window.event
def on_key_release(symbol, modifiers):
	pass

@window.event
def on_mouse_press(x,y, button, modifiers):
	if button == mouse.LEFT:
		mouse_position['x'] = x
		mouse_position['y'] = y

	if commands["assigningUnit"] == True:
		for row in rows_y:
			if x > 22*scale:
				if y > row and y < row+24*scale:
					commands["selectedRow"] = rows_y.index(row)
					commands["assigningUnit"] = False
					confirm_sound.play()
					if commands["selectedUnit"] == 0:
						sound = swordHit
					elif commands["selectedUnit"] == 1:
						sound = bowHit
					elif commands["selectedUnit"] == 2:
						sound = spellHit
					player_units.append(Unit(character_anims, sound, death_anim, row, commands["selectedUnit"]))

	for icon in unit_icons:
		if icon.onclick(mouse_position) == True:
			if commands['currency'] >= icon.type+1:
				commands["assigningUnit"] = True
				commands["selectedUnit"] = icon.type
				commands['currency'] -= icon.type+1
			else:
				errorSound.play()

	if commands['currency'] > commands["currency_increase"]:
		if upgradeIcon.onclick(mouse_position):
			print("Upgraded mana")
			commands['currency'] -= commands['currency_increase']
			commands['currency_increase'] *= 2
			pyglet.clock.unschedule(increase_currency)
			commands["currency_gap"] *= 0.75
			pyglet.clock.schedule_interval(increase_currency, commands["currency_gap"])




@window.event
def on_draw():
	window.clear()    
	bg.blit(0,0)
	for icon in unit_icons:
		icon.sprite.draw()
		priceLabel = pyglet.text.Label(str(1+icon.type), 
                          font_name='DisposableDroid BB', 
                          font_size=32,
                          color=(176, 243, 245, 255),
                          x=icon.sprite.x+4*scale, y=icon.sprite.y-5*scale)
		priceLabel.draw()

	if commands["assigningUnit"] == True:
		for arrow in option_arrows:
			arrow.draw()

	for unit in player_units:
		unit.sprite.draw()

	for unit in enemy_units:
		unit.sprite.draw()

	for unit in recently_killed:
		unit.sprite.draw()

	pyglet.sprite.Sprite(labelBg, x=1*scale, y=window.height-14*scale).draw()
	playerLabel = pyglet.text.Label(str(commands['score']), 
                          font_name='DisposableDroid BB', 
                          font_size=48,
                          color=(241, 201, 25, 255),
                          x=6*scale, y=window.height-11*scale)
	playerLabel.draw()

	pyglet.sprite.Sprite(labelBg, x=window.width-28*scale, y=window.height-14*scale).draw()
	currencyLabel = pyglet.text.Label(str(commands['currency']), 
                          font_name='DisposableDroid BB', 
                          font_size=48,
                          color=(176, 243, 245, 255),
                          x=window.width-25*scale, y=window.height-11*scale)
	currencyLabel.draw()

	if commands['score'] <= 0:
		pyglet.text.Label("You Lost the Fortress!", 
                          font_name='DisposableDroid BB', 
                          font_size=72,
                          color=(148, 17, 0, 255),
                          x=window.width//2,
                      	  y=window.height//2,
                      	  anchor_x='center', anchor_y='center').draw()
		pyglet.text.Label("Your Top Score: " + str(commands["topscore"]) + " Highscore: " + str(commands["highscore"]), 
                          font_name='DisposableDroid BB', 
                          font_size=48,
                          color=(148, 17, 0, 255),
                          x=window.width//2,
                      	  y=window.height//2-76,
                      	  anchor_x='center', anchor_y='center').draw()

	if commands['currency'] > commands['currency_increase']:
		upgradeIcon.sprite.draw()

def increase_currency(dt):
	commands["currency"]+=1



if __name__ == '__main__':
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.txt"), 'r') as jsonFile:
		leaderboard = json.load(jsonFile)
	window.push_handlers(on_mouse_press)
	commands = dict(assigningUnit=False,selectedRow=0, selectedUnit=0, score=10, currency=3, highscore=leaderboard, topscore=1000, saved=False, currency_gap=2, time_gap=1.5, currency_increase=2)
	labelBg = pyglet.resource.image("label_bg.png")



	playerLabel = pyglet.text.Label(str(commands['score']), 
                          font_name='DisposableDroid BB', 
                          font_size=48,
                          color=(241, 201, 25, 255),
                          x=6*scale, y=window.height-11*scale)
	enemyUnitMax = 5
	time_gap = 1.5
	currency_gap = 2
	bg = pyglet.resource.image("bg.png")

	player_units = []
	enemy_units = []
	recently_killed = []
	unit_icons = []
	icon_images = pyglet.resource.image("unit_icons.png")
	select_sound = pyglet.resource.media('select.wav', streaming=False)
	confirm_sound = pyglet.resource.media('confirm.wav', streaming=False)

	upgradeArrow = pyglet.resource.image("upgrade_arrow.png")
	upgradeIcon = UnitIcon(100, upgradeArrow, select_sound)
	upgradeIcon.sprite.image = upgradeArrow 
	upgradeIcon.sprite.x = window.width-42*scale
	upgradeIcon.sprite.y = window.height-14*scale


	swordHit = pyglet.resource.media('blade.wav', streaming=False)
	bowHit = pyglet.resource.media('bow.wav', streaming=False)
	spellHit = pyglet.resource.media('fire.wav', streaming=False)
	errorSound = pyglet.resource.media('error.wav', streaming=False)

	unit_images = pyglet.resource.image("characters.png")
	death_images = pyglet.resource.image("death_anim.png")
	character_anims, death_anim = render_character_anims(unit_images, death_images)

	for i in range(3):
		unit_icons.append(UnitIcon(i,icon_images, select_sound))

	rows_y = [0*scale,24*scale, 48*scale, 72*scale]


	option_arrows = []
	arrowUpper = 26*scale
	arrowLower = 22*scale


	arrow_image = pyglet.resource.image("arrow.png")
	for i in range(4):
		option_arrows.append(pyglet.sprite.Sprite(arrow_image, x=22*scale, y=rows_y[i]+8*scale))

	mouse_position = dict(x=0,y=0)
	arrowMove = dict(forward=True)
		
	pyglet.clock.schedule(update)
	pyglet.clock.schedule_interval(spawn_enemy, commands["time_gap"])
	pyglet.clock.schedule_interval(increase_currency, commands["currency_gap"])
	pyglet.app.run()
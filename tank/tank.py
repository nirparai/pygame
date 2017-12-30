import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0,.5)
red = (255,0,0)
light_red = (200,0,0)
green = (0,155,0)
light_green = (0,255,0)
yellow = (200,200,0)
light_yellow = (255,255,0)

display_width = 800
display_height = 600

groundHeight = 35
FPS = 15

gameDisplay = pygame.display.set_mode((display_width,display_height), pygame.RESIZABLE)
pygame.display.set_caption('Tank')

# pygame.display.set_icon(img)

clock = pygame.time.Clock()

tankWidth = 40
tankHeight = 20
turretWidth = 5
wheelWidth = 5



smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def pause():
	paused = True
	message_to_screen("Paused",black,-100,size="large")
	message_to_screen("Press C to continue or Q to quit",black,-25)
	pygame.display.update()

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				aquit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()	
					quit()
		clock.tick(5)


def score(score):
	text =  smallfont.render("Score : "+str(score),True, black)
	gameDisplay.blit(text,[0,0])

def text_objects(text,color,size):
	if size == "small":
		textSurface =  smallfont.render(text, True, color)
	elif size == "medium":
		textSurface =  medfont.render(text, True, color)
	elif size == "large":
		textSurface =  largefont.render(text, True, color)		
	return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size='small'):
	textSurf, textRect = text_objects(msg,color,size)
	textRect.center = buttonX+(buttonWidth/2),buttonY+(buttonHeight/2)
	gameDisplay.blit(textSurf, textRect)


def message_to_screen(msg,color,y_displace=0,size = "small"):
	textSurface, textRect = text_objects(msg,color,size)
	textRect.center =  (display_width/2) , (display_height/2)+y_displace
	gameDisplay.blit(textSurface, textRect)


def tank(x,y,turPos):
	x = int(x)
	y = int(y)
	possibleTurrets = [
						(x-27, y-2),
						(x-26, y-5),
						(x-25, y-8),
						(x-23, y-12),
						(x-20, y-14),
						(x-18, y-15),
						(x-15, y-17),
						(x-13, y-19),
						(x-11, y-21),
						]

	pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))
	pygame.draw.rect(gameDisplay, black,(x - tankHeight, y, tankWidth, tankHeight ))
	pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)

	startX = 15
	for _ in range(7):
		pygame.draw.circle(gameDisplay, black, (x- startX , y+20), wheelWidth)
		startX -= 5

	return possibleTurrets[turPos]

def enemy_tank(x,y,turPos):
	x = int(x)
	y = int(y)
	possibleTurrets = [
						(x+7, y-2),
						(x+26, y-5),
						(x+25, y-8),
						(x+23, y-12),
						(x+20, y-14),
						(x+18, y-15),
						(x+15, y-17),
						(x+13, y-19),
						(x+11, y-21),
						]

	pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))
	pygame.draw.rect(gameDisplay, black,(x - tankHeight, y, tankWidth, tankHeight ))
	pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)

	startX = 15
	for _ in range(7):
		pygame.draw.circle(gameDisplay, black, (x- startX , y+20), wheelWidth)
		startX -= 5

	return possibleTurrets[turPos]		

def game_controls():
	gCont = True

	while gCont:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(white)
		message_to_screen("Controls", green, -100, "large")
		message_to_screen("Fire: Spacebar",black,-30,"small")
		message_to_screen("Move Turret : Up and Down arrow",black,0,"small")
		message_to_screen("Move Tank : Left and Right arrow",black,30,"small")
		message_to_screen("Pause P",black,60,"small")

		button("play", 100,500,100,50, green, light_green, action="play")
		button("main", 300,500,100,50, yellow, light_yellow,action="main")
		button("quit", 500,500,100,50, red , light_red,action="quit")

		pygame.display.update()
		clock.tick(15)	


def button(text, x, y, width, heigth,inactive_color, active_color,action=None):
	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()	

	if x+width > cur[0] > x and y+heigth > cur[1] > y :
		pygame.draw.rect(gameDisplay, active_color, (x,y,width,heigth))
		if click[0] == 1 and action != None:
			if action == "quit" :
				pygame.quit()
				quit()
			elif action == "controls"	:
				game_controls()
			elif action == "play"	:
				gameLoop()
			elif action == "main"	:
				game_intro()

	else :
		pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,heigth))	

	text_to_button(text, black, x,y, width,heigth)	

def gameLoop():
	gameExit = False
	gameOver = False

	mainTankX = display_width * 0.9
	mainTankY = display_height * 0.9

	enemyTankX = display_width * 0.1
	enemyTankY = display_height * 0.9

	playerHealth = 100
	enemyHealth = 100
	tankMove = 0
	currentTurPos = 0
	changeTur = 0

	firePower = 50
	powerChange = 0

	xlocation = (display_width/2) + random.randint(-0.2*display_width, 0.2*display_width)
	randomHeight = random.randrange(display_height*0.1, display_height*0.6) 
	barrier_width = 50



	while not gameExit:

		if gameOver == True:
			message_to_screen("Game Over",red,-50,size="large")
			message_to_screen("C to continue, Q to quit",black)
			pygame.display.update()
		while gameOver == True:			
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False

					if event.key == pygame.K_c:
						gameLoop()	


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True

			if  event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					tankMove = -5

				elif event.key == pygame.K_RIGHT:
					tankMove = 5

				elif event.key == pygame.K_UP:
					changeTur = 1

				elif event.key == pygame.K_DOWN:
					changeTur = -1

				elif event.key == pygame.K_a:
					powerChange = -1

				elif event.key == pygame.K_d:
					powerChange = 1

				elif event.key == pygame.K_p:
					pause()	

				elif event.key == pygame.K_SPACE:
					damage = fireShell(gun, mainTankX, mainTankY, currentTurPos, firePower, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY)
					enemyHealth -= damage
					damage = enemyFireShell(enemyGun, enemyTankX, enemyTankY, currentTurPos, xlocation, barrier_width, randomHeight, mainTankX, mainTankY)
					playerHealth -= damage

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					tankMove = 0

				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					changeTur = 0	

				elif event.key == pygame.K_a or event.key == pygame.K_d:					
					powerChange = 0

		mainTankX += tankMove

		currentTurPos += changeTur

		if currentTurPos > 8:
			currentTurPos = 8
		elif currentTurPos < 0:
			currentTurPos = 0

		if mainTankX - (tankWidth/2) < xlocation + barrier_width	:
			mainTankX += 5

		gameDisplay.fill(white)
		healthBars(playerHealth, enemyHealth)
		gun =tank(mainTankX,mainTankY,currentTurPos)
		enemyGun =enemy_tank(enemyTankX,enemyTankY,currentTurPos)								

		firePower += powerChange
		power(firePower)	
		barrier(xlocation, randomHeight, barrier_width)		
		gameDisplay.fill(green, rect = [0, display_height - groundHeight, display_width, groundHeight])
		pygame.display.update()
		clock.tick(FPS)		

	pygame.quit()
	quit()


def barrier(xlocation, randomHeight, barrier_width):
	pygame.draw.rect(gameDisplay, black, [xlocation, display_height - randomHeight, barrier_width, randomHeight])

def explosion(x, y, size=50):
	explode = True

	while explode:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		startPoint = x, y
		colorChoices = [red, light_red, yellow, light_yellow]		
		magnitude = 1

		while magnitude < size:
			exploding_bit_x = x+random.randrange(-1*magnitude, magnitude)
			exploding_bit_y = y+random.randrange(-1*magnitude, magnitude)

			pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)],(exploding_bit_x, exploding_bit_y),random.randrange(1,5))
			magnitude += 1

			pygame.display.update()
			clock.tick(100)
		explode = False	


def fireShell(xy, tankx, tanky, turPos, gunPower, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY):
	damage = 0
	fire = True
	startingShell =  list(xy)

	while fire:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)			

		
		startingShell[0] -= (12 - turPos)*2
		startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015/(gunPower/50))**2)- (turPos +  turPos/(12 - turPos)))

		if startingShell[1] > display_height - groundHeight:
			hit_x = int((startingShell[0]*display_height - groundHeight)/startingShell[1])
			hit_y = int(display_height - groundHeight)

			explosion(hit_x, hit_y)

			fire = False

			if enemyTankX + 15 > hit_x >enemyTankX - 15 :
				damage += 25

		check_x_1 = startingShell[0] <= xlocation+barrier_width
		check_x_2 = startingShell[0] >= xlocation

		check_y_1 = startingShell[1] <= display_height
		check_y_2 = startingShell[1] >= display_height - randomHeight

		if check_x_1 and check_x_2 and check_y_1 and check_y_2:
			hit_x = int(startingShell[0])
			hit_y = int(startingShell[1])

			explosion(hit_x, hit_y)

			fire = False

		pygame.display.update()
		clock.tick(60)		
	return damage	

def enemyFireShell(xy, tankx, tanky, turPos, xlocation, barrier_width, randomHeight, pTankX, pTankY):
	damage = 0
	currentPower = 1
	powerFound = False

	while not powerFound:
		currentPower += 1

		if currentPower > 100:
			powerFound = True
		fire = True

		startingShell =  list(xy)

		while fire:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			
			startingShell[0] += (12 - turPos)*2
			startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015/(currentPower/50))**2)- (turPos +  turPos/(12 - turPos)))

			if startingShell[1] > display_height - groundHeight:
				hit_x = int((startingShell[0]*display_height - groundHeight)/startingShell[1])
				hit_y = int(display_height - groundHeight)

				if pTankX + 15 > hit_x >pTankX - 15 :
					powerFound = True
					damage += 25
				
				fire = False

			check_x_1 = startingShell[0] <= xlocation+barrier_width
			check_x_2 = startingShell[0] >= xlocation

			check_y_1 = startingShell[1] <= display_height
			check_y_2 = startingShell[1] >= display_height - randomHeight

			if check_x_1 and check_x_2 and check_y_1 and check_y_2:
				hit_x = int(startingShell[0])
				hit_y = int(startingShell[1])

				fire = False


		
	fire = True
	startingShell =  list(xy)

	while fire:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)			

		
		startingShell[0] += (12 - turPos)*2
		startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015/(currentPower/50))**2)- (turPos +  turPos/(12 - turPos)))

		if startingShell[1] > display_height - groundHeight:
			hit_x = int((startingShell[0]*display_height - groundHeight)/startingShell[1])
			hit_y = int(display_height - groundHeight)

			explosion(hit_x, hit_y)

			fire = False

		check_x_1 = startingShell[0] <= xlocation+barrier_width
		check_x_2 = startingShell[0] >= xlocation

		check_y_1 = startingShell[1] <= display_height
		check_y_2 = startingShell[1] >= display_height - randomHeight

		if check_x_1 and check_x_2 and check_y_1 and check_y_2:
			hit_x = int(startingShell[0])
			hit_y = int(startingShell[1])

			explosion(hit_x, hit_y)

			fire = False

		pygame.display.update()
		clock.tick(60)

	return damage			


def healthBars(playerHealth, enemyHealth):
	if playerHealth > 75:
		playerHealthColor = green
	elif playerHealth > 50:
		playerHealthColor = yellow
	else:
		playerHealthColor = red

	if enemyHealth > 75:
		enemyHealthColor = green
	elif enemyHealth > 50:
		enemyHealthColor = yellow
	else:
		enemyHealthColor = red			

	pygame.draw.rect(gameDisplay, playerHealthColor, (680, 25, playerHealth, 25))	
	pygame.draw.rect(gameDisplay, enemyHealthColor, (20, 25, enemyHealth, 25))	


def power(level):
	text = smallfont.render("Power : "+str(level)+" %", True, black)
	gameDisplay.blit(text,[display_width/2, 0])


def game_intro():
	intro = True

	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_s:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()		
					quit()

		gameDisplay.fill(white)
		message_to_screen("Tank it up", green, -100, "large")
		message_to_screen("Seek and destroy",black,-30,"small")
		message_to_screen("Shoot as many as you can",black,20,"small")

		button("play", 100,500,100,50, green, light_green, action="play")
		button("controls", 300,500,100,50, yellow, light_yellow,action="controls")
		button("quit", 500,500,100,50, red , light_red,action="quit")

		pygame.display.update()
		clock.tick(15)	

game_intro()
gameLoop()


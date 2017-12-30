import pygame
import time
import random

pygame.init()
white = (255,255,255)
black = (0,0,0,.5)
red = (255,0,0)
green = (0,155,0)
display_width = 800
display_height = 600
block_size = 20
appleThickness = 30
FPS = 15
direction = "right"


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slyther')

img = pygame.image.load('snakehead.png')
appleimg = pygame.image.load('apple.png')
pygame.display.set_icon(img)

clock = pygame.time.Clock()
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
				quit()

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


def randAppleGen():
	randAppleX = round(random.randrange(0, display_width- appleThickness )/10)*10
	randAppleY = round(random.randrange(0, display_height-appleThickness)/10)*10
	return randAppleX, randAppleY

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
		message_to_screen("Snake and the Apple", green, -100, "large")
		message_to_screen("God condem the devil to chase the fruit for eternity",black,-30,"small")
		message_to_screen("the more you eat the nearer to your own destruction, again and again",black,20,"small")
		message_to_screen("Press S to start or Q to quit",black)

		pygame.display.update()
		clock.tick(15)

def snake(block_size,snakelist):
	if direction ==  "right":
		head = pygame.transform.rotate(img,270)

	elif direction ==  "left":
		head = pygame.transform.rotate(img,90)
	
	elif direction ==  "up":
		head = img

	elif direction ==  "down":
		head = pygame.transform.rotate(img,180)
	
		
	gameDisplay.blit(head,(snakelist[-1][0],snakelist[-1][1]))
	for XnY in snakelist[:-1]:
		pygame.draw.rect(gameDisplay,green,[XnY[0],XnY[1],block_size,block_size])

def text_objects(text,color,size):
	if size == "small":
		textSurface =  smallfont.render(text, True, color)
	elif size == "medium":
		textSurface =  medfont.render(text, True, color)
	elif size == "large":
		textSurface =  largefont.render(text, True, color)		
	return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size = "small"):
	textSurface, textRect = text_objects(msg,color,size)
	textRect.center =  (display_width/2) , (display_height/2)+y_displace
	gameDisplay.blit(textSurface, textRect)

def gameLoop():
	gameExit = False
	gameOver = False
	global direction

	direction = "right"

	lead_x = display_width/2
	lead_y = display_height/2
	lead_x_change = 10
	lead_y_change = 0


	snakeList = []
	snakeLength = 1

	randAppleX, randAppleY = randAppleGen()

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
					direction =  "left"
					lead_x_change = -10
					lead_y_change = 0

				elif event.key == pygame.K_RIGHT:
					direction =  "right"
					lead_x_change = 10
					lead_y_change = 0

				elif event.key == pygame.K_UP:
					direction =  "up"
					lead_y_change = -10	
					lead_x_change = 0		

				elif event.key == pygame.K_DOWN:
					direction =  "down"
					lead_y_change = 10
					lead_x_change = 0	

				elif event.key == pygame.K_p:
					pause()			

		if lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0:
			gameOver = True

		lead_x += lead_x_change
		lead_y += lead_y_change
					
		gameDisplay.fill(white)
		
		gameDisplay.blit(appleimg,[randAppleX,randAppleY])
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)

		snakeList.append(snakeHead)
		if len(snakeList) > snakeLength:
			del snakeList[0]

		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead :
				gameOver = True

		
		snake(block_size,snakeList)
		score((snakeLength-1)*100)
		pygame.display.update()

		if lead_x > randAppleX and lead_x < randAppleX + appleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + appleThickness :
			if lead_y >  randAppleY and lead_y < randAppleY + appleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness :
				randAppleX, randAppleY = randAppleGen()
				snakeLength += 1

		clock.tick(FPS)		

	pygame.quit()
	quit()

game_intro()
gameLoop()
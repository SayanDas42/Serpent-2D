import pygame
import time
import random

pygame.init()
pygame.display.set_caption("Serpent 2D")
wd=1200
ht=800
gameScreen=pygame.display.set_mode((wd,ht))

icon=pygame.image.load('images/Serpent.jpg')
pygame.display.set_icon(icon)
img=pygame.image.load('images/snakehead.jpg')
appleimg=pygame.image.load('images/Apple.jpg')
snake_body=pygame.image.load('images/Snake_skin.jpg')
eat_sound=pygame.mixer.music.load('sounds/eat_apple.mp3')

white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
green=(0,100,0)
blue=(0,0,255)
clock=pygame.time.Clock()
block_size=30
gameDisplay = pygame.display.set_mode((wd,ht))

def intro_msg(msg,type,f_siz,x_displace,y_displace):
	font=pygame.font.SysFont(None,f_siz)
	screen_text=font.render(msg,True,type)
	gameScreen.blit(screen_text,[ht/2+x_displace,ht/2+y_displace])
	
def message_to_screen(msg,type):
	font=pygame.font.SysFont(None,30)
	screen_text=font.render(msg,True,type)
	gameScreen.blit(screen_text,[ht/2,ht/2])

def score_to_screen(msg,type):
	font=pygame.font.SysFont(None,30)
	screen_text=font.render(msg,True,type)
	gameScreen.blit(screen_text,[ht/2+60,ht/2+30])

def score(scr):
	smallfont=pygame.font.SysFont(None,30)
	text=smallfont.render("Score = "+str(scr),True,blue)
	gameDisplay.blit(text,(0,0))

def serpent(block_size,snakelist):
	if direc=="right":
		head=pygame.transform.rotate(img,90)
	if direc=="left":
		head=pygame.transform.rotate(img,270)
	if direc=="up":
		head=pygame.transform.rotate(img,180)
	if direc=="down":
		head=img
	gameDisplay.blit(head,(snakelist[-1][0],snakelist[-1][1]))
	for xy in snakelist[:-1]:
		#pygame.draw.rect(gameScreen,green,[xy[0],xy[1],block_size,block_size])
		gameDisplay.blit(snake_body,(xy[0],xy[1]))
		

def gameIntro():
	intro=True
	while intro==True:
		gameScreen.fill(white)
		intro_msg("Welcome",red,100,0,-250)
		intro_msg("Use Arrow Keys to move the Snake.",blue,50,-100,-160)
		intro_msg("Eat Apples to earn points.",blue,50,-50,-100)
		intro_msg("Avoid colliding with the borders and with yourself.",blue,50,-180,-30)
		intro_msg("Press Enter to start the game.",black,40,-30,40)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
					intro=False
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_RETURN:
					gameLoop()
					intro=False
	

def gameLoop():
	global direc
	direc="down"
	snakelist=[]
	snakelen=1
	lead_x=wd/2
	lead_y=ht/2
	lead_x_change=0
	lead_y_change=0
	randAppleX=random.randrange(0,wd-block_size,block_size)
	randAppleY=random.randrange(0,ht-block_size,block_size)
	gameClose=False
	gameOver=False
	gameScreen.fill(white)
	pygame.draw.rect(gameScreen,green,(lead_x,lead_y,block_size,block_size))
	pygame.display.update()
	while not gameClose:
		while gameOver==True:
			gameScreen.fill(white)
			message_to_screen("Game Over. Press Enter to restart",red)
			score_to_screen("Final Score = "+str((snakelen-1)*10),blue)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					gameClose=True
					gameOver=False
				elif event.type==pygame.KEYDOWN:
					if event.key==pygame.K_RETURN:
						direc="down"
						snakelist=[]
						snakelen=1
						lead_x=wd/2
						lead_y=ht/2
						lead_x_change=0
						lead_y_change=0
						randAppleX=random.randrange(0,wd-block_size,block_size)
						randAppleY=random.randrange(0,ht-block_size,block_size)
						gameClose=False
						gameOver=False
						gameScreen.fill(white)
						pygame.draw.rect(gameScreen,green,(lead_x,lead_y,block_size,block_size))
						pygame.display.update()
						
		if gameClose==True:
			break
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameClose=True
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					direc="left"
					lead_x_change=-block_size
					lead_y_change=0
				if event.key==pygame.K_RIGHT:
					direc="right"
					lead_x_change=block_size
					lead_y_change=0
				if event.key==pygame.K_UP:
					direc="up"
					lead_y_change=-block_size
					lead_x_change=0
				if event.key==pygame.K_DOWN:
					direc="down"
					lead_y_change=block_size
					lead_x_change=0
			"""if event.type==pygame.KEYUP:
				lead_x_change=0
				lead_y_change=0"""
				
		lead_x+=lead_x_change
		lead_y+=lead_y_change
		gameScreen.fill(white)
		gameDisplay.blit(appleimg,(randAppleX,randAppleY))
		if lead_x>=wd-block_size or lead_x<=0 or lead_y>=ht-block_size or lead_y<=0:
			gameOver=True
		
		snakehead=[]
		snakehead.append(lead_x)
		snakehead.append(lead_y)
		snakelist.append(snakehead)
		if len(snakelist)>snakelen:
			del snakelist[0]
		for eachseg in snakelist[:-1]:
			if eachseg==snakehead:
				gameOver=True
				continue
				
		serpent(block_size,snakelist)
		score((snakelen-1)*10)
		pygame.display.update()
		
		if lead_x>=randAppleX-10 and lead_x<=randAppleX+block_size:
			if lead_y>=randAppleY-10 and lead_y<=randAppleY+block_size:
				pygame.mixer.music.play()
				randAppleX=random.randrange(0,wd-block_size,block_size)
				randAppleY=random.randrange(0,ht-block_size,block_size)
				snakelen+=1
		clock.tick(8)

gameIntro()		
pygame.quit()

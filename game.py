import pygame
from pygame.locals import *
import serial
import math
import time
from random import randint
import sys

#PORT=1; #COM Port No(Change it according to your PC)

PORT="/dev/ttyUSB0";
ser=serial.Serial(PORT,9600,timeout=None);
ch='n';
while(ch!='y'):
	ch=input("Press y after connecting \n")

x=0
y=0

tmp = pygame.image.load('bg.jpg')
bg = pygame.transform.scale(tmp,(800,600))

pygame.init()
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("Don\'t Shoot Jack Sparrow!")
gameover=False
clock=pygame.time.Clock();

birds=[1,1,1,1]
jack=[1,1,1]

locbird=[ [randint(100,700),100] , [randint(100,700),200] , [randint(100,700),400] , [randint(100,700),500] ]
locjack=[ [randint(200,500),randint(300,500)] , [600,15] , [randint(200,500),randint(300,500)] ] 
direcbird=[0,0,0,0]
for i in range(4):
    direcbird[i]=randint(1,8)
direcjack=[randint(1,2),True,randint(1,8)]


loc2bird=[[0,0],[0,0],[0,0],[0,0]]
loc2jack=[[0,0],[0,0],[0,0]]
t0=time.time()
score=0
shots=0
count=0
ser.write('y')
time.sleep(1)
while not gameover:
	for i in range(8):
		img1 = pygame.image.load('C__fakepath_bird-'+str(i)+'.png')
		img1 = pygame.transform.scale(img1,(100,80))
		img2 = pygame.image.load('C__fakepath_p1-'+str(i)+'.png')
		img2 = pygame.transform.scale(img2,(80,200))

		img4 = pygame.image.load('C__fakepath_p3-'+str(i)+'.png')
		img4 = pygame.transform.scale(img4,(80,200))
		seconds=math.floor(time.time()-t0)
		if(seconds==120):
			gameover=True
		if(birds[0]==0 and birds[1]==0 and birds[2]==0 and birds[3]==0):
			gameover=True
		if(jack[0]==0 or jack[1]==0 or jack[2]==0):
			gameover=True
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				gameover=True
		screen.fill([255,255,255])
		font=pygame.font.SysFont(None,40)
		screen.blit(bg,(0,0))
		text=font.render("X :"+str(x),True,[0,100,255])
		screen.blit(text,[10,20])
		text=font.render("Y :"+str(y),True,[0,100,255])
		screen.blit(text,[10,80])
		pygame.draw.circle(screen,[0,0,0],[int((800/2)+(x*-5)),int((600/2)+(y*5))],5)
		pygame.draw.circle(screen,[255,0,0],[int((800/2)+(x*-5)),int((600/2)+(y*5))],30,2)


		time.sleep(0.07)
		if(ser.inWaiting()>0):
			#ch=b'/'
			# while(ch.decode('UTF-8')!=':' and ser.inWaiting()>0):
			# 	ch=ser.read(1)
			# 	print(ch)
			

			# while(ch.decode('UTF-8')!='.' and ser.inWaiting()>0):
			# 	ch=ser.read(1)
			#if(ser.inWaiting()>0):
			line=ser.readline()
			ch = line.split('\t')
			if(len(ch)==3 and str(ch[0])!='' and str(ch[1])!=''):
				x = int(str(ch[0]))
				y = int(str(ch[1]))
				if(ch[2]=='1\r\n'):
					print("Gun Fired")
					pygame.draw.circle(screen,[255,255,0],[int((800/2)+(x*-5)),int((600/2)+(y*5))],5)
					loop=1
					X = int((800/2)+(x*-5))
					Y = int((600/2)+(y*-5))
					shots = shots+1
					for j in range(4):
						if(birds[j]==1):
							x1 = loc2bird[j][0]
							y1 = loc2bird[j][1]
							if(X>x1-50 and X<x1+50 and Y>y1-50 and Y<y1+50):
								birds[j]=0
								score = score +500*loop
								loop = loop+1

			
				
		ser.flushInput()


		for j in range(4):
			img = img1
			if(birds[j]==1):
				x1=locbird[j][0]
				y1=locbird[j][1]
				if(direcbird[j]==1):
					new=pygame.transform.rotate(img,90)
					x1=x1
					y1=y1-5
				elif(direcbird[j]==2):
					new=pygame.transform.rotate(img,45)
					x1=x1+5
					y1=y1-5
				elif(direcbird[j]==4):
					new=pygame.transform.rotate(img,-45)
					x1=x1+5
					y1=y1+5
				elif(direcbird[j]==5):
					new=pygame.transform.rotate(img,-90)
					x1=x1
					y1=y1+5
				elif(direcbird[j]==6):
					new=pygame.transform.rotate(img,-45)
					new=pygame.transform.flip(new,1,0)
					x1=x1-5
					y1=y1+5
				elif(direcbird[j]==7):
					new=pygame.transform.flip(img,1,0)
					x1=x1-5
					y1=y1
				elif(direcbird[j]==8):
					new=pygame.transform.rotate(img,45)
					new=pygame.transform.flip(new,1,0)
					x1=x1-5
					y1=y1-5
				elif(direcbird[j]==3):
					new=img
					x1=x1+5
					y1=y1
				locbird[j][0]=x1
				locbird[j][1]=y1
				#checking for boundry location and reflecting the bird accordingly
				if(y1-20<0):
					direcbird[j]=randint(4,6)
				elif(y1+20>500):
					direcbird[j]=randint(8,10)
					if(direcbird[j]>8):
						direcbird[j]=direcbird[j]-8
				elif(x1+20>700):
					direcbird[j]=randint(6,8)
				elif(x1-20<0):
					direcbird[j]=randint(2,4)
				w,h=new.get_size()
				screen.blit(new,(locbird[j][0],locbird[j][1]))
				loc2bird[j][0]=int(x1+w/2)
				loc2bird[j][1]=int(y1+h/2)

			#pygame.display.flip()
		img = img2
		if(jack[0]==1):
			x2=locjack[0][0]
			y2=locjack[0][1]
			w,h=img.get_size()
			if(direcjack[0]==1):
				new2=pygame.transform.scale(img,(w-5,h-10))
				x2=x2
				y2=y2-5
			elif(direcjack[0]==2):
				new2=pygame.transform.scale(img,(w+5,h+10))
				x2=x2
				y2=y2+5

			if(y2-350<0):
				direcjack[0]=2
				x2=randint(200,500)
			elif(y2>500):
				direcjack[0]=1
				x2=randint(200,500)
			locjack[0][0]=x2
			locjack[0][1]=y2
			w2,h2=new.get_size()
			screen.blit(new2,(locjack[0][0],locjack[0][1]))
			loc2jack[0][0]=int(x2+w2/2)
			loc2jack[0][1]=int(y2+h2/2)

		img3 = pygame.image.load('C__fakepath_p2-'+str(i)+'.png')
		img3 = pygame.transform.scale(img3,(80,200))
		if(jack[1]==1):
			x3=locjack[1][0]
			y3=locjack[1][1]
			if(direcjack[1]):
				x3=x3
				y3=15
			elif(not direcjack[1]):
				x3=x3
				y3=250
			locjack[1][0]=x3
			locjack[1][1]=y3
			if(count%40 == 0):
				direcjack[1]= not direcjack[1]
			w3,h3=img3.get_size()
			screen.blit(img3,(locjack[1][0],locjack[1][1]))
			loc2jack[1][0]=int(x3+w3/2)
			loc2jack[1][1]=int(y3+h3/2)
			count=count+1

			
		pygame.time.wait(15)
		pygame.display.flip()


#show stats of your play 
print score, shots          
#pygame.quit()





			

import pygame, math, random

pygame.init()

screenWidth, screenHeight = (1000,600)

screen = pygame.display.set_mode((screenWidth, screenHeight))

clock = pygame.time.Clock()

isGameOn = True

walls = []



rectSize = 40
rectsInRow = 5

wallSize3D = 50
map = [
	  [1,1,1,1,1,1,1,1],
	  [1,1,0,0,0,0,0,1],
	  [1,0,0,0,1,1,0,1],
	  [1,0,1,0,0,1,0,1,1,1,1],
	  [1,0,1,1,1,1,0,0,0,0,1],
	  [1,0,0,0,1,0,0,1,0,0,1],
	  [1,1,1,1,1,1,1,1,1,1,1]
]

class Wall():
	def __init__(self, x2D, y2D):
		self.x2D = x2D
		self.y2D = y2D
		self.rect = pygame.Rect(self.x2D,self.y2D,rectSize,rectSize)
		self.isEnemy = False

	def draw(self):
		self.rect = pygame.Rect(self.x2D,self.y2D,rectSize,rectSize)
		pygame.draw.rect(screen,(200,10,10),(self.x2D,self.y2D,rectSize,rectSize))
		#pygame.draw.rect(screen,(255,255,200),(self.x2D,self.y2D,rectSize,rectSize),1)

class Enemy():
	def __init__(self,x2D,y2D):
		self.rectSize =5 
		self.x2D = x2D
		self.y2D = y2D
		self.rect = pygame.Rect(self.x2D,self.y2D,self.rectSize,self.rectSize)
		self.isEnemy = True
		self.color2 = 0
	def draw(self):
		self.rect = pygame.Rect(self.x2D,self.y2D,self.rectSize,self.rectSize)
		pygame.draw.rect(screen,(100,20,40),(self.x2D,self.y2D,self.rectSize,self.rectSize))


class Player():
	def __init__(self):
		self.mouse_x_last = 0
		self.x2D = rectSize*rectsInRow/2
		self.y2D = rectSize*rectsInRow/2
		self.rad2D = 5
		self.direction = 300
		self.FOV = 90
		self.rayXEnd = 0
		self.rayYEnd = 0
		self.rayMaxLen = 5
		self.hasHitWall = False
		self.rectCheck = pygame.Rect(0,0,0,0)
		self.vector = (0,0)
		self.color2 = 0
		self.isThrowingBall = False

		self.rays = []

		self.enemyRays = []

	

	def calculate2DRay(self):
		#self.direction += 0.5
		
		
		self.rays = []

		
		for dire in range(self.direction-int(self.FOV/2),self.direction+int(self.FOV/2),1):
			self.rayMaxLen = 0
			self.hasHitWall = False
			while self.hasHitWall == False:
				if self.rayMaxLen>300:
					self.hasHitWall = True
				self.rayMaxLen+=2
				self.rayXEnd = self.x2D + math.cos(math.radians(dire))*self.rayMaxLen
				self.rayYEnd = self.y2D - math.sin(math.radians(dire))*self.rayMaxLen


				self.rectCheck = pygame.Rect(self.rayXEnd,self.rayYEnd,1,1)

				
				for wall in walls:
					if self.rectCheck.colliderect(wall):
						if wall.isEnemy:
							self.enemyRays.append(self.rayMaxLen)
							


						#print(self.FOV)
						self.hasHitWall = True
						pygame.draw.line(screen,(200,50,0),(self.x2D,self.y2D),(self.rayXEnd,self.rayYEnd))
						self.rays.append(self.rayMaxLen)
						if dire == self.direction:
							self.vector = (self.rayXEnd,self.rayYEnd)
							if wall.isEnemy and self.isThrowingBall:
								walls.remove(wall)

							
							#print(int(math.tan(math.radians(self.FOV/2))*self.rayMaxLen*(5)))
							pygame.draw.line(screen,(0,50,200),(self.x2D,self.y2D),(self.rayXEnd,self.rayYEnd))


	def draw2DRay(self):
		self.calculate2DRay()
		self.handle3D()
		


		#pygame.draw.line(screen,(200,50,0),(self.x2D,self.y2D),(self.rayXEnd,self.rayYEnd))


	def handle3D(self):
		#print(len(self.rays))
		step = 11
		x = screenWidth-step

		for ray in self.rays:
			self.hasHitEnemy = False
			h2 = math.tan(math.radians(self.FOV/2))*ray*(3)
			ratio = 1/h2
			h2 = ratio*10000
			print(ratio)
			self.color = ratio*2000
			if self.color>250:
				self.color = 250
			for enemyRay in self.enemyRays:
				if ray == enemyRay:
					self.hasHitEnemy = True
			
			if self.hasHitEnemy:
				pygame.draw.rect(screen,(self.color2,self.color,255),(x,screenHeight/2-h2/2,11,h2))
			else:
				pygame.draw.rect(screen,(random.randint(0,10),self.color,255),(x,screenHeight/2-h2/2,11,h2))
			x-=step
		self.enemyRays = []



	def keysHandler(self):
		self.realVectorX =self.vector[0]- self.x2D 
		self.realVectorY =self.vector[1]- self.y2D  

		self.bigVector = math.fabs(self.realVectorY)+math.fabs(self.realVectorX)
		self.realVectorX2 = math.fabs(self.realVectorX)/self.bigVector
		self.realVectorY2 = math.fabs(self.realVectorY)/self.bigVector

		print(self.realVectorX)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			if self.x2D<self.vector[0]:
				self.x2D += 2*self.realVectorX2
			if self.x2D>self.vector[0]:
				self.x2D -= 2*self.realVectorX2
			if self.y2D<self.vector[1]:
				self.y2D += 2*self.realVectorY2
			if self.y2D>self.vector[1]:
				self.y2D -= 2*self.realVectorY2
		if keys[pygame.K_s]:
			if self.x2D<self.vector[0]:
				self.x2D -= 2*self.realVectorX2
			if self.x2D>self.vector[0]:
				self.x2D += 2*self.realVectorX2
			if self.y2D<self.vector[1]:
				self.y2D -= 2*self.realVectorY2
			if self.y2D>self.vector[1]:
				self.y2D += 2*self.realVectorY2
		if keys[pygame.K_e]:
			self.isThrowingBall = True
		else:
			self.isThrowingBall = False


		if keys[pygame.K_RIGHT]:
			self.direction-=4
		if keys[pygame.K_LEFT]:
			self.direction+=4
		


	def draw(self):
		pygame.draw.circle(screen,(0,100,0),(self.x2D,self.y2D),self.rad2D)
		self.draw2DRay()
		pygame.draw.rect(screen,(0,0,200),self.rectCheck)
		self.keysHandler()
		





Player = Player()

def calculate2D():
	x = 0
	y = 0
	
	for row in map:
		for box in row:
			if box != 0:
				walls.append(Wall(x,y))
			#pygame.draw.rect(screen,(255,255,200),(x,y,rectSize,rectSize),1)
			x += rectSize
		x = 0
		y += rectSize
	walls.append(Enemy(100,50))
	walls.append(Enemy(120,100))
	walls.append(Enemy(250,100))

calculate2D()
def draw2D():
	
	x = 0
	y = 0
	
	for row in map:
		for box in row:
			
			#pygame.draw.rect(screen,(255,255,200),(x,y,rectSize,rectSize),1)
			x += rectSize
		x = 0
		y += rectSize
	

	for wall in walls:
		wall.draw()

	Player.draw()








while isGameOn:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
				isGameOn = False


	screen.fill((0,0,0))
	draw2D()






	pygame.display.update()
	clock.tick(60)
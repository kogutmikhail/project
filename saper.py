import pygame, sys
from ctypes import windll
from random import randrange
from pygame.locals import *

'''Возвращает Windows-окно'''
def MessageBox(title, text, style):
    return windll.user32.MessageBoxW(0, text, title, style) # Функция MessageBox заимствована из интернет-источника

pygame.init()
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
timecount = pygame.time.Clock()
gamespace = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Сапер")
deftile = pygame.image.load("tile.png")
MouseBlock = pygame.image.load("MouseTile.png")
emptyblock = pygame.image.load("ztile.png")
bomnum1 = pygame.image.load("tile1.png")
bomnum2 = pygame.image.load("tile2.png")
bomnum3 = pygame.image.load("tile3.png")
bomnum4 = pygame.image.load("tile4.png")
bomnum5 = pygame.image.load("tile5.png")
bomnum6 = pygame.image.load("tile6.png")
bomnum7 = pygame.image.load("tile7.png")
bomnum8 = pygame.image.load("tile8.png")

tiles = []
boxcount = 0

class tile():
	'''Клетка поля 9х9'''
	x = 0
	y = 0
	bombtest = False
	def __init__(self, position):
		'''Координаты клетки'''
		self.loc = position 
		'''Значение клетки
		0-8 - кол-во бомб рядом
		9 - бомба'''
		self.flag = -3

sample = tile(Rect(-15,-15,0,0))
sample.x = -10
sample.y = -10
MouseTile = sample


def drawtilesInit():
	'''Создает матрицу незаполненных клеток'''
	for x in range(0, 9):
		for y in range(0, 9):
			t = tile(Rect(x*17+10, y*17+10, 17, 17))
			t.index = len(tiles)
			t.x = x
			t.y = y
			tiles.append(t)
			gamespace.blit(deftile, (x*17 + 10, y*17 + 10))

drawtilesInit()

def newbombs():
	'''Случайным образом расставляет 10 бомб'''
	boxcount = 0
	arr = []
	while boxcount <10:
		num = randrange(len(tiles))
		if num not in arr:
			arr.append(num)
			tiles[num].bombtest = True
			boxcount += 1

newbombs()
emptytiles = []
remains = 0
def drawtiles():
	'''Рисует главный экран'''
	global remains
	for a in tiles:
		if a.flag == -3:
			gamespace.blit(deftile, a.loc)
			remains +=1
		elif a.flag == 0:
			if not a in emptytiles:
				getzeros(a)
			gamespace.blit(emptyblock, a.loc)
		elif a.flag == 9:
			lose()
		elif a.flag == 1: gamespace.blit(bomnum1, a.loc)
		elif a.flag == 2: gamespace.blit(bomnum2, a.loc)
		elif a.flag == 3: gamespace.blit(bomnum3, a.loc)
		elif a.flag == 4: gamespace.blit(bomnum4, a.loc)
		elif a.flag == 5: gamespace.blit(bomnum5, a.loc)
		elif a.flag == 6: gamespace.blit(bomnum6, a.loc)
		elif a.flag == 7: gamespace.blit(bomnum7, a.loc)
	'''Выигрыш, если осталось 10 некликнутых клеток'''
	if remains == 10: win()


def inside():
	return Rect(10, 10, 153, 153).collidepoint(event.pos)

def cursortile():
	'''Возвращает клетку, над которой находится курсор'''
	for tile in tiles:
		if tile.loc.collidepoint(event.pos):
			return tile

def gettile(x, y):
	'''Возвращает клетку с координатами х,y'''
	for tile in tiles:
		if tile.x == x and tile.y == y:
			return tile

def getneighbors(a):
	'''Возращает соседей клетки'''
	try:
		if a.x < 9 and a.x > 0 and a.y > 0 and a.y < 9:
			return (gettile(a.x - 1, a.y), gettile(a.x + 1, a.y), gettile(a.x, a.y - 1), gettile(a.x, a.y + 1), gettile(a.x - 1, a.y - 1), gettile(a.x + 1, a.y +1), gettile(a.x + 1, a.y - 1), gettile(a.x - 1, a.y + 1))
		elif a.x ==9 and a.y > 0 and a.y < 9:
			return (gettile(a.x - 1, a.y - 1), gettile(a.x - 1, a.y), gettile(a.x - 1, a.y + 1), gettile(a.x,a.y+1), gettile(a.x, a.y -1))
		elif a.x ==0 and a.y > 0 and a.y < 9:
			return (gettile(a.x + 1, a.y), gettile(a.x + 1, a.y - 1), gettile(a.x + 1, a.y + 1), gettile(a.x, a.y+1), gettile(a.x, a.y-1))
		elif a.y ==0 and a.x > 0 and a.x < 9:
			return (gettile(a.x, a.y + 1), gettile(a.x + 1, a.y + 1), gettile(a.x-1, a.y), gettile(a.x+1, a.y), gettile(a.x-1, a.y+1))
		elif a.y == 0 and a.x == 0:
			return (gettile(1, 0), gettile(1, 1), gettile(0, 1))
	except Exception: return None

def getbombs(a):
	'''Возвращает число бомб рядом'''
	bomnum = 0
	neighbors = getneighbors(a)
	if not neighbors: return 0
	for a in neighbors:
		if a and a.bombtest: bomnum = bomnum + 1
	return bomnum

tiles_in_queue = []


def win():
	'''Окно выигрыша'''
	MessageBox("Вы выиграли", "Победа", 0)
	newgame()

def lose():
	'''Окно проигрыша'''
	MessageBox("Вы проиграли", "Поражение", 0)
	newgame()

def cross(a):
	'''Крестом находит пустые клетки рядом с пустыми клетками'''
	if a.x == 0 and a.y == 0:
		return (gettile(0, 1), gettile(1, 0))
	elif a.x == 0 and a.y == 9:
		return (gettile(0, 8), gettile(1, 9))
	elif a.x == 9 and a.y == 0:
		return (gettile(8, 0), gettile(9, 1))
	elif a.x == 9 and a.y == 9:
		return (gettile(8, 9), gettile(9, 8))
	elif a.x > 0  and a.x < 9 and a.y > 0:
		return (gettile(a.x, a.y-1), gettile(a.x-1, a.y), gettile(a.x+1, a.y), gettile(a.x, a.y+1))
	elif a.x == 0 and a.y > 0 and a.y < 9:
		return (gettile(a.x, a.y-1), gettile(a.x, a.y+1), gettile(a.x+1, a.y))
	elif a.x == 9 and a.y > 0 and a.y < 9:
		return (gettile(a.x-1, a.y), gettile(a.x, a.y-1), gettile(a.x, a.y+1)) 
	elif a.y == 0 and a.x > 0 and a.x < 9:
		return (gettile(a.x - 1, a.y), gettile(a.x+1, a.y), gettile(a.x, a.y+1))
	elif a.y == 9 and a.x > 0 and a.x < 9:
		return (gettile(a.x - 1, a.y), gettile(a.x+1, a.y), gettile(a.x, a.y-1))

def getzeros(a):
	'''Добавляет клетки с флагом 0 в массив'''
	for t in cross(a):
		if t and getbombs(t) == 0:
			t.flag = 0
	for tt in getneighbors(a):
		w = getbombs(tt)
		if w > 0 and w < 9:
			tt.flag = w
	emptytiles.append(a)


def newgame():
	'''Новая игра'''
	global timecount
	global tiles
	timecount = pygame.time.Clock()
	tiles[:] = []
	drawtilesInit()
	newbombs()
	
if __name__ == "__main__":	
	while True:
		gamespace.fill(white)
		drawtiles()
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				MouseTile = cursortile()
				if not inside():
		
					MouseTile = sample
			elif event.type == MOUSEBUTTONUP:
				if inside():
					if event.button == 1:
						MouseTile.flag = getbombs(MouseTile)
						if MouseTile.flag == 0:
							tiles_in_queue.append(MouseTile)
							getzeros(MouseTile)
						if MouseTile.bombtest: MouseTile.flag = 9
		if MouseTile.flag == -3: gamespace.blit(MouseBlock, MouseTile.loc)    
		pygame.display.update()
		timecount.tick(50)
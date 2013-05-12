__author__ = 'pragungoyal'

from sketch import *
import math
from numpy import *
from cardboard_cup import *
upperSide = 60
lowerSide = 45
slantHeight = 20
unitSideLength = 100
num_sides = 4
num_cups_x = 4
num_cups_y = 3
thickness=0.5
outerCutsCenterDistance = slantHeight + (lowerSide/2)
inf = float('inf')
dash_length = [2,2]

class Platform(Sketch):
	def __init__(self,upperSide,lowerSide,unitSideLength,num_sides,thickness,*args,**kwargs):
		self.Cups = SketchList()
		for j in range(num_cups_y):
			for i in range(num_cups_x):
				offsetX = unitSideLength*(i+1)
				offsetY = unitSideLength*(j+1)
				self.Cups.append(CardBoardCup(offsetX,offsetY,upperSide,lowerSide,unitSideLength,num_sides,thickness))
		height = unitSideLength*num_cups_y
		width = unitSideLength*num_cups_x
		offsetX = unitSideLength/2
		offsetY = unitSideLength/2
		BoundaryLine = MetaLine('TwoPoints',(SimpleLine,),{'operation':'cut'})
		self.line1 = BoundaryLine().set(startX=offsetX,startY=offsetX,endX=offsetX,endY=offsetY+height)
		self.line2 = BoundaryLine().set(startX=offsetX+width,startY=offsetY,endX=offsetX+width,endY=offsetY+height)
		self.line3 = BoundaryLine().set(startX=offsetX,startY=offsetY+height,endX=offsetX+width,endY=offsetY+height)
		self.line4 = BoundaryLine().set(startX=offsetX,startY=offsetY,endX=offsetX+width,endY=offsetY)


if __name__ == '__main__':
	a = Platform(upperSide,lowerSide,unitSideLength,num_sides,thickness)
	a.render('platform.svg',root=True)


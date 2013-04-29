import svgwrite
from svgwrite import cm, mm
import inspect

corelDrawX4Ratio = float(40)/125
ratio = corelDrawX4Ratio

dash_length = [6,2]

class MetaLine(type):
	def __new__(cls,name,parents,dct):
		#print cls,name,parents,dct
		return super(MetaLine,cls).__new__(cls,name,parents,dct)


class SimpleLine(object):
	__metaclass__ = MetaLine
	def set(self,**kwargs):
		for (key,value) in kwargs.items():
			setattr(self,key,value)
		return self
	def getEndPoints(self):
		if self.slope==0.0:
			startPt = (self.startX,self.Y)
			endPt = (self.endX,self.Y)
			return (startPt,endPt)

		if self.slope==float('inf'):
			startPt = (self.X,self.startY)
			endPt = (self.X,self.endY)
			return (startPt,endPt)


class MetaSketch(type):
	def __new__(cls,name,parents,dct):
		return super(MetaSketch,cls).__new__(cls,name,parents,dct)


class SketchList(list):
	pass


class SimpleLineList(list):
	pass


class Sketch(object):
	__metaclass__ = MetaSketch
	def displace(self,X,Y):
		self.X = X
		self.Y = Y
		return self

	def __init__(self,X=None,Y=None):
		self.X = 0.0
		self.Y = 0.0

	def render(self,fileName=None,root=False):
		base = None
		if root:
			base = svgwrite.Drawing(filename=fileName, debug=True)
		else:
			#base = svgwrite.container.SVG(insert=(self.X*mm,self.Y*mm))
			base = svgwrite.container.Group()
			#base = svgwrite.container.SVG()

		for (a,b) in inspect.getmembers(self):
			if isinstance(b,Sketch):
				#print 'Sketch found,',a
				base.add(b.render())
			if isinstance(b,SketchList):
				#print 'Sketchlist Found'
				for i in b:
					#print 'Sketch found in list,',a,i
					base.add(i.render())
			if isinstance(b,SimpleLine):
				#print 'LineFound,',a
				addLine(base,b)

			if isinstance(b,SimpleLineList):
				for i in b:
					addLine(base,i)

		if root:
			base.save()
		else:
			return base


def convLen(a):
	return a*ratio*mm

def addLine(base,line):
	((startX,startY),(endX,endY)) = line.getEndPoints()
	if line.operation == 'cut':
		base.add(svgwrite.shapes.Line(start=(convLen(startX),convLen(startY)), end=(convLen(endX),convLen(endY)), stroke='black'),)
	if line.operation == 'score':
		base.add(svgwrite.shapes.Line(start=(convLen(startX),convLen(startY)), end=(convLen(endX),convLen(endY)), stroke='red'))
	if line.operation == 'dash':
		base.add(svgwrite.shapes.Line(start=(convLen(startX),convLen(startY)), end=(convLen(endX),convLen(endY)), stroke='black').dasharray(dash_length))

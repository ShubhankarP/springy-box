import svgwrite
from svgwrite import cm, mm
import inspect

corelDrawX4Ratio = float(40)/125
ratio = corelDrawX4Ratio

dash_length = [0.9,1.5]

class MetaLine(type):
	def __new__(cls,name,parents,dct):
		#print cls,name,parents,dct
		return super(MetaLine,cls).__new__(cls,name,parents,dct)


class SimpleLine(object):
	__metaclass__ = MetaLine
	def set(self,**kwargs):
		for (key,value) in kwargs.items():
			if key=='start':
				setattr(self,'startX',value[0])
				setattr(self,'startY',value[1])
			elif key=='end':
				setattr(self,'endX',value[0])
				setattr(self,'endY',value[1])
			else:
				setattr(self,key,value)
		return self
	def getEndPoints(self):
		if not hasattr(self,'slope'):
			return ((self.startX,self.startY),(self.endX,self.endY))

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
	def addLinesFromXYLists(self,Line,XList,YList):
		a = min(len(XList),len(YList))
		for i in range(a):
			if i < a-1:
				#Read: sI: starting Index, eI:endingIndex
				sI = i
				eI = i+1
			else:
				sI = i
				eI = 0
			self.append(Line().set(startX=XList[sI],startY=YList[sI],endX=XList[eI],endY=YList[eI]))

	def addLinesFromXXYYTuples(self,Line,XXYYTuples):
		for i in range(len(XXYYTuples)):
			self.append(Line().set(startX=XXYYTuples[i][0],startY=XXYYTuples[i][2],endX=XXYYTuples[i][1],endY=XXYYTuples[i][3]))


	def addLinesFromXYXYTuples(self,Line,XYXYTuples):
		for i in range(len(XYXYTuples)):
			self.append(Line().set(startX=XYXYTuples[i][0],startY=XYXYTuples[i][1],endX=XYXYTuples[i][2],endY=XYXYTuples[i][3]))



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

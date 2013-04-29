__author__ = 'pragungoyal'

from sketch import *

side = 50
num_sides = 4
num_panels = 6
thickness=0.5

length = side*num_panels + (4*thickness)
num_cuts = 20
cut_width = 0.6
cut_ratio = 0.2
spring_width = side*cut_ratio/2
dash_length = [6,2]

dwg = svgwrite.Drawing(filename='twin_box.svg', debug=True)
cuts = dwg.g(id='cuts', stroke='black')
scores = dwg.g(id='scores', stroke='red')
dwg.add(cuts)
dwg.add(scores)

total_width = (4.5)*side
print 'Total width',total_width


class NormalSide(Sketch):
	def __init__(self,referenceHeight,startX,count,*args,**kwargs):
		HorzLine = MetaLine('HorzLine',(SimpleLine,),{'startX':startX, 'endX':(startX+side), 'slope':0.0})
		VertLine = MetaLine('VertLine',(SimpleLine,),{'X':startX, 'slope':float('inf')})

		elasticity_control_cutout_left = startX + spring_width
		elasticity_control_cutout_right = startX + side - spring_width
		ElasticVertLine1 = MetaLine('ElasticVertLine',(SimpleLine,),{'X':elasticity_control_cutout_left , 'slope':float('inf')})
		ElasticVertLine2 = MetaLine('ElasticVertLine',(SimpleLine,),{'X':elasticity_control_cutout_right , 'slope':float('inf')})
		ElasticHorzLine = MetaLine('ElasticHorzLine',(SimpleLine,),{'startX':elasticity_control_cutout_right ,'endX':elasticity_control_cutout_left , 'slope':0.0})

		#Top Top Hinge
		self.topTopHinge = SimpleLineList()
		for i in range(num_cuts):
			topTopHingeBottom  = referenceHeight + (i*cut_width)
			self.topTopHinge.append(HorzLine().set(operation='score', Y=topTopHingeBottom ))

		self.topEV1 = ElasticVertLine1().set(operation='cut',startY=referenceHeight,endY=topTopHingeBottom)
		self.topEV2 = ElasticVertLine2().set(operation='cut',startY=referenceHeight,endY=topTopHingeBottom)
		self.topEH1 = ElasticHorzLine().set(operation='cut',Y=topTopHingeBottom)
		self.topEH2 = ElasticHorzLine().set(operation='cut',Y=referenceHeight)

		topHingesTop = referenceHeight
		topFold= topHingesTop - side - (thickness*count)
		self.topFold = HorzLine().set(operation='dash', Y=topFold)

		self.topVFold = VertLine().set(operation='dash',startY=topHingesTop,endY=topFold)

		topCut = topFold- side
		self.topCut = HorzLine().set(operation='cut', Y=topCut)

		self.topVCut = VertLine().set(operation='cut',startY=topFold,endY=topCut)

		#Top Mid Hinge
		topMidHinge = topTopHingeBottom + side
		self.topMidHinge = HorzLine().set(operation='dash', Y=topMidHinge)

		#Top Bottom Hinge
		self.topBottomHinges = SimpleLineList()
		topBottomHingeTop = topMidHinge + side
		for i in range(num_cuts):
			topBottomHingeBottom  = topBottomHingeTop  + (i*cut_width)
			self.topBottomHinges.append(HorzLine().set(operation='score', Y=topBottomHingeBottom))

		self.top1EV1 = ElasticVertLine1().set(operation='cut',startY=topBottomHingeTop,endY=topBottomHingeBottom)
		self.top1EV2 = ElasticVertLine2().set(operation='cut',startY=topBottomHingeTop,endY=topBottomHingeBottom)
		self.top1EH1 = ElasticHorzLine().set(operation='cut',Y=topBottomHingeTop)
		self.top1EH2 = ElasticHorzLine().set(operation='cut',Y=topBottomHingeBottom)


		self.topHingeVCut = VertLine().set(operation='cut',startY=topHingesTop,endY=topBottomHingeBottom)

		#Bottom Top Hinge
		self.bottomTopHinges = SimpleLineList()
		bottomTopHingeTop  = topBottomHingeBottom + side
		for i in range(num_cuts):
			bottomTopHingeBottom  = bottomTopHingeTop  + (i*cut_width)
			self.bottomTopHinges.append(HorzLine().set(operation='score', Y=bottomTopHingeBottom))

		self.top2EV1 = ElasticVertLine1().set(operation='cut',startY=bottomTopHingeTop,endY=bottomTopHingeBottom)
		self.top2EV2 = ElasticVertLine2().set(operation='cut',startY=bottomTopHingeTop,endY=bottomTopHingeBottom)
		self.top2EH1 = ElasticHorzLine().set(operation='cut',Y=bottomTopHingeTop)
		self.top2EH2 = ElasticHorzLine().set(operation='cut',Y=bottomTopHingeBottom)


		self.midVFold = VertLine().set(operation='dash',startY=topBottomHingeBottom,endY=bottomTopHingeTop)

		#Bottom Mid Hinge
		bottomMidHinge = bottomTopHingeBottom + side
		self.bottomMidHinge = HorzLine().set(operation='dash', Y=bottomMidHinge)

		#Bottom bottom Hinge
		self.bottomBottomHinges = SimpleLineList()
		bottomBottomHingeTop  = bottomMidHinge + side
		for i in range(num_cuts):
			bottomBottomHingeBottom = bottomBottomHingeTop  + (i*cut_width)
			self.bottomBottomHinges.append(HorzLine().set(operation='score', Y=bottomBottomHingeBottom))

		self.bottomEV1 = ElasticVertLine1().set(operation='cut',startY=bottomBottomHingeTop,endY=bottomBottomHingeBottom)
		self.bottomEV2 = ElasticVertLine2().set(operation='cut',startY=bottomBottomHingeTop,endY=bottomBottomHingeBottom)
		self.bottomEH1 = ElasticHorzLine().set(operation='cut',Y=bottomBottomHingeTop)
		self.bottomEH2 = ElasticHorzLine().set(operation='cut',Y=bottomBottomHingeBottom)

		self.bottomHingeVCut = VertLine().set(operation='cut',startY=bottomTopHingeTop,endY=bottomBottomHingeBottom)

		bottomFold = bottomBottomHingeBottom + side + (count*thickness)
		self.bottomFold = HorzLine().set(operation='dash', Y=bottomFold)

		self.bottomVFold = VertLine().set(operation='dash',startY=bottomBottomHingeBottom,endY=bottomFold)

		bottomCut = bottomFold + side
		self.bottomCut = HorzLine().set(operation='cut', Y=bottomCut)

		self.bottomVCut = VertLine().set(operation='cut',startY=bottomCut,endY=bottomFold)


class FirstSide(NormalSide):
	def __init__(self,referenceHeight,startX,count,*args,**kwargs):
		super(FirstSide,self).__init__(referenceHeight,startX,count,*args,**kwargs)
		HorzLine = MetaLine('HorzLine',(SimpleLine,),{'startX':startX, 'endX':(startX+side), 'slope':0.0})
		VertLine = MetaLine('HorzLine',(SimpleLine,),{'X':startX, 'slope':float('inf')})

		self.topVFold.operation = 'cut'
		self.midVFold.operation = 'cut'
		self.bottomVFold.operation = 'cut'


class LastSide(NormalSide):
	def __init__(self,referenceHeight,startX,count,*args,**kwargs):
		super(LastSide,self).__init__(referenceHeight,startX,count,*args,**kwargs)
		endX = (startX + side)
		HorzLine = MetaLine('HorzLine',(SimpleLine,),{'startX':endX, 'endX':(endX+side/2+thickness), 'slope':0.0})
		VertLine1 = MetaLine('VertLine1',(SimpleLine,),{'X':endX, 'slope':float('inf')})
		VertLine1Fold = MetaLine('VertLine1',(SimpleLine,),{'X':endX-thickness, 'slope':float('inf')})
		VertLine2 = MetaLine('VertLine2',(SimpleLine,),{'X':(endX + side/2 + thickness), 'slope':float('inf')})

		topFlapBottom = referenceHeight
		self.topFlapBottom = HorzLine().set(operation='cut', Y=topFlapBottom )

		topFlapTop = topFlapBottom - side
		self.topFlapTop = HorzLine().set(operation='cut', Y=topFlapTop )

		self.topVFlapCut = VertLine2().set(operation='cut',startY=topFlapTop,endY=topFlapBottom)
		self.topVFlapFold = VertLine1Fold().set(operation='dash',startY=topFlapTop,endY=topFlapBottom)
		self.topVCut2 = VertLine1().set(operation='cut',startY=self.topCut.Y,endY=topFlapTop)

		midFlapTop = self.topBottomHinges[-1].Y
		self.midFlapTop = HorzLine().set(operation='cut', Y=midFlapTop )
		midFlapBottom = self.bottomTopHinges[0].Y
		self.midFlapBottom = HorzLine().set(operation='cut', Y=midFlapBottom )
		self.midFlapVFold = VertLine1Fold().set(operation='dash',startY=midFlapTop,endY=midFlapBottom)
		self.midFlapVCut = VertLine2().set(operation='cut',startY=midFlapTop,endY=midFlapBottom)

		self.midTopVCut = VertLine1().set(operation='cut',startY=topFlapBottom,endY=midFlapTop)

		bottomFlapTop = self.bottomBottomHinges[-1].Y
		self.bottomFlapTop = HorzLine().set(operation='cut', Y=bottomFlapTop )
		bottomFlapBottom = bottomFlapTop + side
		self.bottomFlapBottom = HorzLine().set(operation='cut', Y=bottomFlapBottom )
		self.bottomVFlapFold = VertLine1Fold().set(operation='dash',startY=bottomFlapTop,endY=bottomFlapBottom)
		self.bottomVFlapCut = VertLine2().set(operation='cut',startY=bottomFlapTop,endY=bottomFlapBottom)

		self.bottomVCut2 = VertLine1().set(operation='cut',startY=bottomFlapBottom,endY=self.bottomCut.Y)

		self.midBottomVCut = VertLine1().set(operation='cut',startY=midFlapBottom,endY=bottomFlapTop)


class TwinBox(Sketch):
	def __init__(self):
		start_x = 10
		end_x = 0
		top_cut = 0
		bottom_cut = 0
		reference_height = 3*side+thickness
		self.sides = SketchList()
		for i in range(4):
			if i == 0:
				cls = FirstSide
			elif i == 3:
				cls = LastSide
			else:
				cls = NormalSide
			self.sides.append(cls(reference_height,start_x+(i*side),i))


if __name__ == '__main__':
	a = TwinBox()
	a.render('twin.svg',root=True)

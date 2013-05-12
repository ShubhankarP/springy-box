__author__ = 'pragungoyal'
from sketch import *
import math
from numpy import *

upperSide = 70
lowerSide = 50
slantHeight = 20
num_sides = 4
thickness=0.5
outerCutsCenterDistance = slantHeight + (lowerSide/2)
inf = float('inf')
dash_length = [2,2]


class CardBoardCup(Sketch):
	def __init__(self,offsetX,offsetY,topSide,lowerSide,unitSideLength,num_sides,thickness,*args,**kwargs):
		internalAngle = (2*math.pi)/num_sides
		halfInternalAngle = internalAngle/2

		self.lineList = SimpleLineList()

		CornerCutsLine = MetaLine('TwoPoints',(SimpleLine,),{'operation':'cut'})
		InnerSquareLine = MetaLine('TwoPoints',(SimpleLine,),{'operation':'dash'})
		OuterSquareLine = MetaLine('TwoPoints',(SimpleLine,),{'operation':'dash'})
		CornerFoldsLine = MetaLine('TwoPoints',(SimpleLine,),{'operation':'dash'})
		SideFoldsLine = MetaLine('TwoPoints',(SimpleLine,),{'operation':'dash'})

		halfOuterSquareSideLength = lowerSide/2 + slantHeight
		offsetArray = array([offsetX,offsetY])

		for i in range(num_sides):
			#This defines the rotation
			angle = internalAngle*i
			rotMat= array([[math.cos(angle),-1*math.sin(angle)],[math.sin(angle),math.cos(angle)]])

			#This defines the inner square
			height = ((lowerSide/2)/math.tan(halfInternalAngle))
			innerC1 = array([-lowerSide/2,height])
			innerC2 = array([lowerSide/2,height])
			rotInnerC1 = dot(innerC1,rotMat) + offsetArray
			rotInnerC2 = dot(innerC2,rotMat) + offsetArray
			self.lineList.append(InnerSquareLine().set(start=rotInnerC1,end=rotInnerC2))

			#This defines the outer square
			height = ((lowerSide/2)/math.tan(halfInternalAngle)) + slantHeight
			outerC1 = array([-upperSide/2,height])
			outerC2 = array([upperSide/2,height])
			rotOuterC1 = dot(outerC1,rotMat) + offsetArray
			rotOuterC2 = dot(outerC2,rotMat) + offsetArray
			self.lineList.append(OuterSquareLine().set(start=rotOuterC1,end=rotOuterC2))

			#This defines the cut-out corners
			endCorner1 = array([-halfOuterSquareSideLength,height])
			endCorner2 = array([halfOuterSquareSideLength,height])
			rotEndCorner1 = dot(endCorner1 ,rotMat) + offsetArray
			rotEndCorner2 = dot(endCorner2 ,rotMat) + offsetArray
			self.lineList.append(CornerCutsLine().set(start=rotOuterC2, end=rotEndCorner2))
			self.lineList.append(CornerCutsLine().set(start=rotOuterC1, end=rotEndCorner1))

			#This defines the corner-side-folds
			self.lineList.append(CornerFoldsLine().set(start=rotOuterC1, end=rotInnerC1))
			self.lineList.append(CornerFoldsLine().set(start=rotOuterC2, end=rotInnerC2))
			#This defines the corner-center-folds
			self.lineList.append(CornerFoldsLine().set(start=rotEndCorner1, end=rotInnerC1))

			#This defines extreme outer side folds
			sideFoldEnd1 = array([-unitSideLength/2,endCorner1[1]])
			rotSideFoldEndCorner1 = dot(sideFoldEnd1 ,rotMat) + offsetArray
			self.lineList.append(SideFoldsLine().set(start=rotEndCorner1, end=rotSideFoldEndCorner1))

			sideFoldEnd2 = array([unitSideLength/2,endCorner2[1]])
			rotSideFoldEndCorner2 = dot(sideFoldEnd2 ,rotMat) + offsetArray
			self.lineList.append(SideFoldsLine().set(start=rotEndCorner2, end=rotSideFoldEndCorner2))

			#This defines extreme inner side folds
			sideFoldEnd3 = array([outerC1[0],unitSideLength/2])
			rotSideFoldEndCorner3 = dot(sideFoldEnd3 ,rotMat) + offsetArray
			self.lineList.append(SideFoldsLine().set(start=rotOuterC1, end=rotSideFoldEndCorner3))

			sideFoldEnd4 = array([outerC2[0],unitSideLength/2])
			rotSideFoldEndCorner4 = dot(sideFoldEnd4 ,rotMat) + offsetArray
			self.lineList.append(SideFoldsLine().set(start=rotOuterC2, end=rotSideFoldEndCorner4))

			#This defines middle side fold
			sideFoldEnd5 = array([(outerC1[0]+endCorner1[0])/2,unitSideLength/2])
			sideFoldEnd51 = array([(outerC1[0]+endCorner1[0])/2,outerC1[1]])
			rotSideFoldEndCorner5 = dot(sideFoldEnd5 ,rotMat) + offsetArray
			rotSideFoldEndCorner51 = dot(sideFoldEnd51 ,rotMat) + offsetArray
			self.lineList.append(SideFoldsLine().set(start=rotSideFoldEndCorner5, end=rotSideFoldEndCorner51))

			sideFoldEnd6 = array([(outerC2[0]+endCorner2[0])/2,unitSideLength/2])
			sideFoldEnd61 = array([(outerC2[0]+endCorner2[0])/2,outerC2[1]])
			rotSideFoldEndCorner6 = dot(sideFoldEnd6 ,rotMat) + offsetArray
			rotSideFoldEndCorner61 = dot(sideFoldEnd61 ,rotMat) + offsetArray
			self.lineList.append(SideFoldsLine().set(start=rotSideFoldEndCorner6, end=rotSideFoldEndCorner61))


if __name__ == '__main__':
	a = CardBoardCup(200,100,upperSide,lowerSide,num_sides,thickness)
	a.render('cardboard_cup.svg',root=True)

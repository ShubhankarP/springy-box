import svgwrite
from svgwrite import cm, mm

side = 40
num_sides = 4
num_panels = 6
thickness=0.5
length = side*num_panels + (4*thickness)
num_cuts = 10
cut_width = 0.6
cut_ratio = 1/10

dwg = svgwrite.Drawing(filename='basic_box.svg', debug=True)
cuts = dwg.g(id='cuts', stroke='black')
scores = dwg.g(id='scores', stroke='red')
dwg.add(cuts)
dwg.add(scores)

def basic_box():
	start_x = 0
	end_x = 0
	top_cut = 0
	bottom_cut = 0
	reference_height = 2*side
	for i in range(num_sides):
		end_x = start_x + side
		(top_cut,bottom_cut) = addSide(dwg,start_x,end_x,i,reference_height)
		start_x = start_x + side
	lastSide(dwg,start_x,top_cut,bottom_cut,reference_height)
	dwg.save()


def addSide(dwg,start_x,end_x,count,reference_height):
	"""I add horizontal cuts for each side to each panel
	"""
	#Leave for thickness
	#All sides meet at the hinges, so we take the top hinge as the reference
	top_hinges = []
	top_hinges_bottom = 0
	top_hinges_top = reference_height
	for i in range(num_cuts):
		top_hinges_bottom = reference_height + (i*cut_width)
		top_hinges.append(top_hinges_bottom)
	top_fold = top_hinges_top - side + (thickness*count)
	top_cut = top_fold - side
	mid_hinge = top_hinges_bottom + side
	bottom_hinges = []
	bottom_hinge_top = mid_hinge + side
	for i in range(num_cuts):
		bottom_hinge_bottom = bottom_hinge_top + (i*cut_width)
		bottom_hinges.append(bottom_hinge_bottom)
	bottom_fold = bottom_hinge_bottom + side + (count) * thickness
	bottom_cut = bottom_fold + side

	cuts_arr = [top_cut,bottom_cut]
	scores_arr = [top_fold,mid_hinge,bottom_fold]+top_hinges+bottom_hinges
	for y in cuts_arr:
		cuts.add(dwg.line(start=(start_x*mm,y*mm), end=(end_x*mm,y*mm)))
	for y in scores_arr:
		scores.add(dwg.line(start=(start_x*mm,y*mm), end=(end_x*mm,y*mm)))

	#If this is the first side, then cut otherwise score
	if count == 0:
		cuts.add(dwg.line(start=(start_x*mm,top_cut*mm), end=(start_x*mm,bottom_cut*mm)))
	else:
		scores.add(dwg.line(start=(start_x*mm,top_fold*mm), end=(start_x*mm,top_hinges_top*mm)))
		cuts.add(dwg.line(start=(start_x*mm,top_hinges_top*mm), end=(start_x*mm,bottom_hinge_bottom*mm)))
		scores.add(dwg.line(start=(start_x*mm,bottom_hinge_bottom*mm), end=(start_x*mm,bottom_fold*mm)))
		cuts.add(dwg.line(start=(start_x*mm,top_cut*mm), end=(start_x*mm,top_fold*mm)))
		cuts.add(dwg.line(start=(start_x*mm,bottom_fold*mm), end=(start_x*mm,bottom_cut*mm)))
	return (top_cut,bottom_cut)


def lastSide(dwg,start_x,top_cut,bottom_cut,reference_height):
	#Add tabs
	tab_length = side - (thickness*num_sides)
	end_x = start_x + tab_length

	top_hinge = reference_height
	top_tab_bottom = top_hinge
	top_tab_top = top_tab_bottom - tab_length
	bottom_tab_top = top_hinge + side + side + (num_cuts*cut_width*2)
	bottom_tab_bottom = bottom_tab_top + tab_length

	arr = [top_tab_top,top_tab_bottom,bottom_tab_top,bottom_tab_bottom]
	for y in arr:
		cuts.add(dwg.line(start=(start_x*mm,y*mm), end=((end_x*mm,y*mm))))

	cuts.add(dwg.line(start=(end_x*mm,top_tab_top*mm), end=((end_x*mm,top_tab_bottom*mm))))
	cuts.add(dwg.line(start=(end_x*mm,bottom_tab_top*mm), end=((end_x*mm,bottom_tab_bottom*mm))))
	scores.add(dwg.line(start=(start_x*mm,top_tab_top*mm), end=((start_x*mm,top_tab_bottom*mm))))
	scores.add(dwg.line(start=(start_x*mm,bottom_tab_top*mm), end=((start_x*mm,bottom_tab_bottom*mm))))

	cuts.add(dwg.line(start=(start_x*mm,top_cut*mm), end=((start_x*mm,top_tab_top*mm))))
	cuts.add(dwg.line(start=(start_x*mm,bottom_cut*mm), end=((start_x*mm,bottom_tab_bottom*mm))))
	cuts.add(dwg.line(start=(start_x*mm,top_tab_bottom*mm), end=((start_x*mm,bottom_tab_top*mm))))


def addLineCut(dwg,a,b):
	pass

def addLineScore(dwg,a,b):
	pass

if __name__ == '__main__':
	basic_box()

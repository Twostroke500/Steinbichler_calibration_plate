# Generate a Steinbichler/Zeiss calibration plate, suitable for "Comet" 3D-Scanners. Save the pattern as a *.svg
# Everything to this script was "reversed" trough the calibration file of the smallest CP_P100 calibration plate.
# 
# Steinbichler calib-plates are a 100*100 grid pattern with 3 reference points in the middle
# The different sizes of plates should be a subset of this 100*100 grid.
#
# Plates are photogrammetricly checked and actual point coordinates are written to a calibration file, which 
# contains only visible points. Invisible points are left out.
# Example: the CP_P_100 plate-file starts at point-ID 3131 and ends at ID 6970 in this structure:
#  ID       X        ;  Y        ;  Z       ;
#  6970	=	99.991337;	95.008696;	0.063444;
#
import drawsvg as draw
# 
d_punkte = 2 # diameter of the points in the grid. 2 mm, measured from a photo
d_nullpunkte = 3.5 # diameter of the 3 reference points in the grids center. Roughly 4 mm, measured from a photo
n_punkte = 100 # number of points in x and y. Must be 100 for the reference points in the middle to be placed correctly
abstand = 5 # distance between the points
randabstand = 2 # border margin of the plate
n_punkte_x = n_punkte_y = n_punkte # number of points is equal in x and y direction
#
#x = y = -b/2 + randabstand*2 # initialize xy-point coordinates with the plates border margin
start=x=y= -(((n_punkte*abstand)+(randabstand))/2)+0.5*abstand+0.5*randabstand
#
# plate size
#b = h = (n_punkte*abstand)+(2*randabstand) # calculate the plates overall full size 
#
b = (37*abstand)+d_punkte+randabstand # CP 100
h = (36*abstand)+d_punkte+randabstand # CP 100
#
# b = (37*abstand)+d_punkte+randabstand # CP xxx
# h = (36*abstand)+d_punkte+randabstand # CP xxx
#
#
point_color = 'black'
background_color = 'white'
#
# define Drawing
d = draw.Drawing(h, b, origin=(-b/2-abstand, -h/2-d_punkte-d_punkte*0.25))
d.append(draw.Rectangle(-b, -h, 2*b, 2*h, fill=background_color)) # box to apply background color if needed
# d.append(draw.Circle(0, 0, d_punkte/2, fill='red')) # SVG origin
n=i_x=i_y=0 # initialize some variables
#
while i_y < n_punkte_y: # loop for the pattern in y-direction
    while i_x < n_punkte_x: # loop for the pattern in x-direction
        d.append(draw.Circle(x, y, d_punkte/2, fill=point_color)) # draw point 
        #d.append(draw.Text(str((n_punkte*n_punkte)-1-n), 1.5, x-2, y-2, fill=point_color)) # print point numbers in svg for "debugging" :)
        #
        # draw a thicker reference point over the smaller one, if point ID is either 5050, 5053 or 5250
        # Steinbichler plate numbering starts from the bottom right. Since this pattern starts from top left, me must check from the other side
        # so reference points are "x*y - point number" 
        if n == (n_punkte*n_punkte-1-5050): # This is point (0, 0, 0)
            d.append(draw.Circle(x, y, d_nullpunkte/2, fill=point_color))
        if n == (n_punkte*n_punkte-1-5053): # This is point (x, 0, 0)
            d.append(draw.Circle(x, y, d_nullpunkte/2, fill=point_color))
        if n == (n_punkte*n_punkte-1-5250): # This is point (x, y, 0)
            d.append(draw.Circle(x, y, d_nullpunkte/2, fill=point_color))
        x = x + abstand # increment point position in x
        i_x = i_x + 1
        n = n + 1 # increment for point number
    else:
        i_x = 0
        x = start # border margin
    i_y = i_y + 1
    y = y + abstand # increment y point position
#
#
d.set_render_size(3*b, 3*h)  # render scale
d.save_svg('calibration_plate_cp100.svg')
d.save_png('calibration_plate_cp100.png') # uncomment to also save as png
#
# Display in Jupyter notebook
d  # Display as svg
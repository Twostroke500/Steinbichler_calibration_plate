# This script takes points from a GOM Tritop Photogrammetry file, filters the points and writes them in the correct order for a steinbichler *.lst file
# This is still untested and i provide no warranty in any way.
#
# (0,0,0), point ID 5050 must be at the thick center point of the plate
# (x,0,0), point ID 5053 must be at the thick point to the left of the center
# (x,y,0), point ID 5250 must be at the thick point over the center point 
# => 3-2-1 alignment
#
import xml.etree.ElementTree as ET
import datetime
#
# export points from GOM into a refxml file and parse the file name here:
tree = ET.parse('your_gom_photogrammetry_file.refxml')
root = tree.getroot()
output = 'your_output_file.lst' # name your output file here
#
# Data that will be written to the file after the points
year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day
calib_interval = 12
#
# point to point pitch of the plate
coordinate_pitch = 5.0 #5.0 for cp100, 10.0 for cp300
coordinate_tolerance = 1.0
#
x_min_coordinate = -95.0 - coordinate_tolerance # plate s/n 1004 has -90 in x negative. Plate s/n 880 has -95
x_max_coordinate = 100.0 + coordinate_tolerance # plate s/n 1004 has +100 in x positive. Plate s/n 880 has +95  
y_abs_coordinate = 95.0 + coordinate_tolerance # this ranges between +-95 for plates s/n 880 and s/n 1004 
z_tolerance = 2.0 # to filter out outlier points in front or behind the plate
#
# GOM Photogrammetry point numbering is random. Steinbichler needs the points named after their position on the plate
# Steinbichler plates are numbert after a 100*100 grid pattern
def calc_point_id(x, y, coordinate_pitch):
    # most negative point on 100*100 grid
    min = 100*coordinate_pitch/2
    # offset plate point coordinates to move origin to bottom right
    # there should not be any more negative plate coordinates after this
    x_trans = min + x
    y_trans = min + y
    # divide coordinate by pitch to get line and row position of each point
    x_pos = int(round(x_trans / coordinate_pitch, 0))
    y_pos = int(round(y_trans / coordinate_pitch, 0))
    # calculate point ID
    # multiply 100 points * y-row position and add the x-position
    point_id = int((y_pos*100)+x_pos)
    return point_id
#
# create a list to store id, x, y, z
point_list = []
# Read points from the GOM Photogrammetry XML-file
for point in root:
    # ignore coded reference points and points which are no photogrammetry-type
    if point.get('coded_point') == 'false' and point.get('type') == 'photogrammetry':
        # get point coordinates
        for coordinates in point.findall('coordinates'):
            # read point coordinates from XML as a float value
            x = float(coordinates.find('x').text)
            y = float(coordinates.find('y').text)
            z = float(coordinates.find('z').text)
            # filtering out points which are not on the plate
            if -z_tolerance < z < z_tolerance: 
                if x_min_coordinate < x < x_max_coordinate:
                    if -y_abs_coordinate < y < y_abs_coordinate:
                        # take coordinates and calculate steinbichler point id
                        point_id = calc_point_id(x, y, coordinate_pitch)
                        # append points with steinbichler-ID to the list
                        point_list.append([point_id, x, y, z])
#
# take the List and sort items for their ID
sorted_list = sorted(point_list)
# write the calibration file of the plate...
# generate file and write first line to the calibration file
with open(output, 'w') as f:
    f.write('[Points]\n')
#
# iterate thorugh the list and write the information to the file in the correct format
i = 0
with open(output, 'a') as f:
    for x in sorted_list:
        # print content from sorted list into file with in correct format
        print('%i\t%s\t%f%s\t%f%s\t%f%s' % (sorted_list[i][0],"=",float(sorted_list[i][1]),";",float(sorted_list[i][2]),";",float(sorted_list[i][3]),";"), file=f)
        i = i + 1
#
# add Information appendix to the calibration file
with open(output, "a") as f:
    print("", file=f)
    print("[Information]", file=f)
    print('Calibration_Year = %i' % (year), file=f)
    print('Calibration_Month = %i' % (month), file=f)
    print('Calibration_Day = %i' % (day), file=f)
    print('Calibration_MonthIntervall = %i' % (calib_interval), file=f)
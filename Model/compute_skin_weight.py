import math
from read_airfoil_coordinates import read_airfoil_coordinates
from read_inputFile import read_inputFile

def main(half_span, front_spar_XC, aft_spar_XC, spar_TC, torque):
    parameters = read_inputFile()
    airfoilCoordinates = read_airfoil_coordinates("C:\\Users\\tyann\\OneDrive\\Documents\\Concordia University\\2024 - 08 [Winter]\\AERO 290\\Model\\airfoil_coordinates.txt")
    chord_length = parameters["Wing_Root_Chord"]
    skin_thickness = parameters["Wing_Skin_Thickness"]
    density = parameters["Materials_Aluminum_Density"]
    shear_strength = parameters["Materials_Aluminum_Shear_Strength"]
    safety_factor = 2
    shear_strength *= safety_factor

    wingbox_width = chord_length * (aft_spar_XC-front_spar_XC)
    wingbox_height = chord_length * spar_TC
    wingbox_area = wingbox_width * wingbox_height
    
    #skin_thickness = torque / (2*shear_strength*wingbox_area)
    #print(f"skin thickness = {skin_thickness}")
    airfoilPerimeter = 0
    for i in range(1,len(airfoilCoordinates)):
        currentStation = [x*chord_length for x in airfoilCoordinates[i]]
        lastStation = [x*chord_length for x in airfoilCoordinates[i-1]]
        airfoilPerimeter += math.dist(currentStation, lastStation)

    skin_weight = skin_thickness * airfoilPerimeter * density * half_span
    #print(skin_weight)
    return skin_weight
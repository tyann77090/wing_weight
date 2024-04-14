import math
from read_inputFile import read_inputFile

def main(Lift, y_strut):
    parameters = read_inputFile()
    fuselage_height = parameters["Fuselage_Height"]
    strength = parameters["Materials_Aluminum_Tensile_Strength"]
    density = parameters["Materials_Aluminum_Density"]
    safety_factor = 3

    l_strut = math.sqrt(fuselage_height**2 + y_strut**2)
    strut_angle = math.atan(fuselage_height/y_strut)
    strut_load = Lift * safety_factor
    strut_min_area = strut_load / strength
    weight = strut_min_area * l_strut * density
    print(math.degrees(strut_angle))
    return weight, strut_angle
#main(45236.716195564644, 0.25*16.92)
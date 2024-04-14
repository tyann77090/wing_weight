import math
import matplotlib.pyplot as plt
import numpy as np
from read_airfoil_coordinates import read_airfoil_coordinates

#chordwise location of spars as fraction of airfoil chord, starting from LE
def compute(front_spar_XC, aft_spar_XC):
    airfoilFilePath = "C:\\Users\\tyann\\OneDrive\\Documents\\Concordia University\\2024 - 08 [Winter]\\AERO 290\\Model\\airfoil_coordinates.txt"
    airfoilCoordinates = read_airfoil_coordinates(airfoilFilePath)

    n_chordwise_sections = math.floor(len(airfoilCoordinates)/2)
    #print(n_chordwise_sections)
    upper_XC_station = []
    wingbox_height = []
    for i in range(n_chordwise_sections):
        upper_station = airfoilCoordinates[i][1]
        lower_station = airfoilCoordinates[-i-1][1]
        upper_XC_station.append(airfoilCoordinates[i][0])
        wingbox_height.append(round(upper_station-lower_station,6))
    upper_XC_station.reverse()
    wingbox_height.reverse()

    found = False
    for i in range(n_chordwise_sections):
        if found == False:
            xp = [upper_XC_station[i-1], upper_XC_station[i]]
            yp = [wingbox_height[i-1], wingbox_height[i]]
            if upper_XC_station[i] >= front_spar_XC:
                front_spar_TC = np.interp(front_spar_XC, xp, yp)
                found = True
        else:
            xp = [upper_XC_station[i], upper_XC_station[i-1]]
            yp = [wingbox_height[i], wingbox_height[i-1]]
            if wingbox_height[i] <= front_spar_TC and found == True:
                rear_spar_aftest_XC = np.interp(front_spar_TC, yp, xp) #aftest position of the rear spar to have a rectangular wingbox
                if rear_spar_aftest_XC < aft_spar_XC:
                    print("Input rear spar XC (%8.6f) too large. Set to %8.6f"%(rear_spar_aftest_XC, aft_spar_XC))
                    aft_spar_XC = rear_spar_aftest_XC
                break

    elastic_axis = front_spar_XC + (front_spar_XC + aft_spar_XC)/2

    return elastic_axis, front_spar_TC
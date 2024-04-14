import random
import numpy as np
from read_inputFile import read_inputFile
from scipy.optimize import minimize

def inertia_rect(b,h, A, d): #where h is normal to the moment arrow
    return (1/12) * b * h**3 + A * d**2

def compute_inertia(input_parameters):
    wingbox_height = globals()["wingbox_height"]
    target_inertia = globals()["target_inertia"]
    spar_web_thickness = input_parameters[0]
    spar_flange_thickness = input_parameters[1]
    spar_flange_width = input_parameters[2]

    spar_web_height = wingbox_height - 2*spar_flange_thickness

    A_flange = spar_flange_thickness * spar_flange_width
    A_web = spar_web_thickness * spar_web_height
    
    d_flange = wingbox_height/2 - spar_flange_thickness/2
    d_web = 0

    inertia_flange = inertia_rect(spar_flange_width, spar_flange_thickness, A_flange, d_flange)
    inertia_web = inertia_rect(spar_web_thickness, spar_web_height, A_web, d_web)

    totalInertia = 2*inertia_flange + inertia_web
    delta_from_target = totalInertia - target_inertia
    #print(delta_from_target)
    return delta_from_target

def compute_web_area(input_parameters):
    wingbox_height = globals()["wingbox_height"]
    target_web_area = globals()["target_web_area"]
    spar_web_thickness = input_parameters[0]
    spar_flange_thickness = input_parameters[1]
    spar_web_height = wingbox_height - 2*spar_flange_thickness
    A_web = spar_web_thickness * spar_web_height
    delta_from_target_area = A_web - target_web_area
    #print(delta_from_target_area)
    return delta_from_target_area

def compute_weight(input_parameters):
    wingbox_height = globals()["wingbox_height"]
    spar_web_thickness = input_parameters[0]
    spar_flange_thickness = input_parameters[1]
    spar_flange_width = input_parameters[2]

    spar_web_height = wingbox_height - 2*spar_flange_thickness
    A_flange = spar_flange_thickness * spar_flange_width
    A_web = spar_web_thickness * spar_web_height
    weight = 2*A_flange + A_web
    return weight


def main(shear, bending_moment):
    global wingbox_height
    global target_inertia
    global target_web_area
    #print(f"shear = {shear}")
    parameters = read_inputFile()
    chord_length = parameters["Wing_Root_Chord"]
    front_spar_XC = parameters["Structure_Front_Spar_XC"]
    aft_spar_XC = parameters["Structure_Aft_Spar_XC"]
    front_spar_TC = 0.11100783462224867#0.10
    strength = parameters["Materials_Aluminum_Tensile_Strength"]
    density = parameters["Materials_Aluminum_Density"]
    safety_factor = 2

    wingbox_width = chord_length * (aft_spar_XC-front_spar_XC)
    wingbox_height = chord_length * front_spar_TC
    #print(wingbox_width)
    
    
    shear = shear * safety_factor
    bending_moment = bending_moment * safety_factor

    globals()["target_web_area"] = shear / strength
    globals()["target_inertia"] = bending_moment * (wingbox_height/2) / strength
    #print(f"target web area = {globals()["target_web_area"]}")
#input_parameters = [spar_web_thickness, spar_flange_thickness, spar_flange_width]
    x0 = np.array([0.001, 0.001, 0.001])
    methods = ["SLSQP", "trust-constr", "COBYLA"]
    bnds = ((0.001, 0.1), (0.01, wingbox_height/2), (0.001, wingbox_width))
    cons = ({'type': 'ineq', 'fun': compute_inertia},
            {'type': 'ineq', 'fun': compute_web_area},
            {'type': 'ineq', 'fun': lambda x: x[1]-(x[0]/2)},
            {'type': 'ineq', 'fun': lambda x: (2*x[0])-x[1]},
            #{'type': 'ineq', 'fun': lambda x: (wingbox_height - 2*x[1])-x[2]},
            )
    
    res = minimize(compute_weight, x0, method=methods[0], bounds=bnds,constraints=cons)
    if res["success"] == True:
        solution = res["x"].tolist()
        #print("ok")
        return density*compute_weight(solution)
    else:
        print("error")
    #print(res["success"])
    
    #print(solution)

    #print(compute_inertia(solution))
    #print(compute_web_area(solution))
    #print(res)
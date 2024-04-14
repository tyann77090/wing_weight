import math
import warnings
import numpy as np
import matplotlib.pyplot as plt
import compute_lifting_line
import compute_elastic_axis
import compute_spar_weight
import compute_skin_weight
import compute_strut_weight
from read_inputFile import read_inputFile

warnings.filterwarnings("ignore")
airfoilPropPath = "C:\\Users\\tyann\\OneDrive\\Documents\\Concordia University\\2024 - 08 [Winter]\\AERO 290\\Model\\airfoil_properties.txt"

parameters = read_inputFile()

N = 1000
air_density = parameters["Environment_Air_Density"]
Sref = parameters["Wing_Area"]
AR = parameters["Wing_AR"]
v_ft = parameters["Performance_Speed"]
i_w = parameters["Aerodynamics_Incidence_Angle"]
front_spar_XC = parameters["Structure_Front_Spar_XC"]
aft_spar_XC = parameters["Structure_Aft_Spar_XC"]
aerodynamic_center = parameters["Airfoil_Aerodynamic_Center"]
root_chord = parameters["Wing_Root_Chord"]
taper_ratio = parameters["Wing_Taper_Ratio"]

b = math.sqrt(AR*Sref)
half_span = b/2
q = 0.5 * air_density * v_ft**2

yield_strength = 276 * 10**6
safety_factor = 2.5
allowable_yield_strength = yield_strength / safety_factor

MTOM = parameters["Weight_MTOM"]
load_factor = parameters["Weight_Load_Factor"]
g = 9.81
MTOW = MTOM*g
max_load = MTOW * load_factor

eta_engine = 0.3
eta_strut = 0.5
def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]


mass_engine = 200
weight_engine = mass_engine * g

avg_wing_loading = max_load / Sref
print(f"MTOW = {avg_wing_loading}")
print(f"maximum load = {max_load}")

airfoil_alpha = []
airfoil_Cm = []
with open(airfoilPropPath) as airfoilPropFile:
    for i in range(3): airfoilPropFile.readline()
    while True:
        line = airfoilPropFile.readline()
        if len(line) > 1:
            if line != "End_of_File":
                split = line.split()
                airfoil_alpha.append(float(split[0]))
                airfoil_Cm.append(float(split[4]))
            else:
                break
for i in range(len(airfoil_alpha)):
    xp = [airfoil_alpha[i-1], airfoil_alpha[i]]
    yp = [airfoil_Cm[i-1], airfoil_Cm[i]]
    if i_w <= airfoil_alpha[i]:
        Cm = np.interp(i_w, xp, yp)
        break

CL, spanwise_station, spanwise_Lift, spanwise_CL, c_vector = compute_lifting_line.compute_CL(N)
elastic_axis, spar_TC = compute_elastic_axis.compute(front_spar_XC, aft_spar_XC)

lift = q * (Sref/2) * CL #lift of halfspan

lift_int2 = -np.trapz([spanwise_Lift[i] * spanwise_station[i] for i in range(len(spanwise_station))], spanwise_station)
lift_conc_y = lift_int2/lift #point where distributed lift is concentrated

print(lift)
print("\n")

     
y_engine = closest(spanwise_station, half_span*eta_engine)
y_strut = closest(spanwise_station, half_span*eta_strut)
print(y_strut)

strut_weight, strut_angle = compute_strut_weight.main(lift, y_strut)

chord_length_dist = list(map(lambda x: (root_chord - (x*root_chord*(1-taper_ratio)/half_span) ), spanwise_station))
print(spanwise_station)
print(chord_length_dist)

shear_total_dist = []
shear_aero_dist = []
shear_engine_dist = []
shear_strut_dist = []

bending_moment_aero_dist = []
bending_moment_engine_dist = []
bending_moment_strut_dist = []
bending_moment_total_dist = []

twisting_moment_dist = []
wingbox_weight_canti = []
wingbox_weight_strut = []
skin_weight = []
for i in range(N):

    shear_aero_dist.append( np.trapz(spanwise_Lift[:i], spanwise_station[:i]) )
    bending_moment_aero_dist.append( np.trapz(shear_aero_dist[:i], spanwise_station[:i]) )
    if y_engine >= spanwise_station[i]:
        shear_engine_dist.append(weight_engine)
        bending_moment_engine_dist.append(-weight_engine * (y_engine-spanwise_station[i]))
    else:
        shear_engine_dist.append(0)
        bending_moment_engine_dist.append(0)

    if y_strut >= spanwise_station[i]:
        shear_strut_dist.append(0.7*lift*math.sin(strut_angle))
        bending_moment_strut_dist.append(np.trapz(shear_strut_dist[:i], spanwise_station[:i]))
    else:
        shear_strut_dist.append(0)
        bending_moment_strut_dist.append(0)
        
    shear_total_dist.append(shear_aero_dist[i]+shear_engine_dist[i]+shear_strut_dist[i])
    bending_moment_total_dist.append(bending_moment_aero_dist[i]+bending_moment_engine_dist[i]+bending_moment_strut_dist[i])
    wingbox_weight_canti.append(compute_spar_weight.main(shear_aero_dist[i], bending_moment_aero_dist[i]))
    wingbox_weight_strut.append(compute_spar_weight.main(shear_total_dist[i], bending_moment_total_dist[i]))


for i in range(N):
    distance_EA_from_AC = abs(elastic_axis-aerodynamic_center)
    localTwist = q * (spanwise_CL[i]*c_vector[i]*distance_EA_from_AC + Cm*c_vector[i]**2)
    twisting_moment_dist.append(localTwist)
print(f"max torque = {max(twisting_moment_dist)}")
total_skin_weight = compute_skin_weight.main(half_span, front_spar_XC, aft_spar_XC, spar_TC, max(twisting_moment_dist))

total_spar_weight_canti = np.trapz(spanwise_station, wingbox_weight_canti)
total_spar_weight_strut = np.trapz(spanwise_station, wingbox_weight_strut)

totalWingWeight_canti = total_skin_weight + total_spar_weight_canti
totalWingWeight_strut = total_skin_weight + total_spar_weight_strut + strut_weight
print(f"Cantilever Wing Weight = {2*totalWingWeight_canti}")
print(f"Strut Braced Wing Weight = {2*totalWingWeight_strut}")

norm_spanwise_station = list(map(lambda y: (2*y/b), spanwise_station ))
plt.figure()
plt.plot(norm_spanwise_station, bending_moment_aero_dist, color="green")
plt.plot(norm_spanwise_station, bending_moment_strut_dist, color="blue")
plt.plot(norm_spanwise_station, bending_moment_engine_dist, color="red")
plt.plot(norm_spanwise_station, bending_moment_total_dist, color="black")
plt.xlabel("Spanwise station (2y/b)")
plt.ylabel("Bending moment (Nm)")
plt.legend(['Cantilever', 'Strut', 'Engine', 'Total'])
plt.grid(True)
plt.show()
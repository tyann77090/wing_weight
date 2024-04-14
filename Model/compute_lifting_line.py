import math
import numpy
import matplotlib.pyplot as plt
from read_inputFile import read_inputFile
def compute_CL(N):
    parameters = read_inputFile()

    air_density = parameters["Environment_Air_Density"]
    v = parameters["Performance_Speed"]
    incidence_angle = math.radians(parameters["Aerodynamics_Incidence_Angle"])
    twist_angle = math.radians(parameters["Wing_Twist_Angle"])
    Sref = parameters["Wing_Area"]
    AR = parameters["Wing_AR"]
    taper_ratio = parameters["Wing_Taper_Ratio"]
    chord_root = parameters["Wing_Root_Chord"]

    liftCurveSlope_2D = parameters["Aerodynamics_2D_Lift_Curve_Slope"]
    ZeroLift_Alpha = math.radians(parameters["Aerodynamics_ZeroLift_Alpha"])
    AOA_dist = []
    for i in range(N):
        AOA_dist.append(incidence_angle + (twist_angle/N)*i)
    AOA_dist.reverse()
    b = math.sqrt(AR*Sref)
    chord_tip = chord_root*taper_ratio

    phi_vector = []
    c_vector = []
    mu_vector = []
    LHS_matrix = [[0 for i in range(N)] for j in range(N)]
    RHS_matrix = [0 for i in range(N)]
    for i in range(N):
        phi_vector.append((i+1)*(math.pi/2)/N)
        c_vector.append(chord_tip*math.cos(phi_vector[i]) + chord_root*(1-math.cos(phi_vector[i])))
        mu_vector.append(c_vector[i] * (liftCurveSlope_2D/(4*b)))

        for j in range(N):
            odd_col = 2*j+1
            LHS_matrix[i][j] = math.sin(odd_col*phi_vector[i]) * (odd_col*mu_vector[i] + math.sin(phi_vector[i]))
        RHS_matrix[i] = (mu_vector[i]*(AOA_dist[i]-ZeroLift_Alpha)*math.sin(phi_vector[i]))
    A_vector = numpy.linalg.solve(LHS_matrix, RHS_matrix)

    CL = math.pi*AR*A_vector[0]

    spanwise_station = []
    spanwise_Lift = []
    spanwise_CL = []
    for i in range(N):
        vortexStrength = 0
        for n in range(N):
            odd = 2*n+1
            vortexStrength = vortexStrength + 2*b*v*A_vector[n]*math.sin(odd*phi_vector[i])
        
        spanwise_station.append((b/2)*math.cos(phi_vector[i]))
        spanwise_Lift.append(air_density*v*vortexStrength)
        spanwise_CL.append((2*vortexStrength) / (v*c_vector[i]))
    
    #plt.figure()
    ##plt.plot(spanwise_station, twisting_moment_dist)
    #plt.plot(spanwise_station, spanwise_Lift)
    #plt.grid(True)
    #plt.show()
    return CL, spanwise_station, spanwise_Lift, spanwise_CL, c_vector

import math
import numpy
import matplotlib.pyplot as plt

air_density = 0.736
v = 128.61
incidence_angle = math.radians(1.2)
twist_angle = 0
Sref = 26.03
AR = 11
taper_ratio = 0.7
chord_root = 1.538
liftCurveSlope_2D = 5.63
ZeroLift_Alpha = math.radians(-3.40)
N=1000

AOA_dist = []
for i in range(N):
    AOA_dist.append(incidence_angle + (twist_angle/N)*i)
AOA_dist.reverse()
b = math.sqrt(AR*Sref)
chord_tip = chord_root*taper_ratio
q = 0.5 * air_density * v**2

phi_vector = []
c_vector = []
mu_vector = []
LHS_matrix = [[0 for _ in range(N)] for _ in range(N)]
RHS_matrix = [0 for _ in range(N)]
for i in range(N):
    phi_vector.append((i+1)*(math.pi/2)/N)
    c_vector.append(chord_tip*math.cos(phi_vector[i]) + chord_root*(1-math.cos(phi_vector[i])))
    mu_vector.append(c_vector[i] * (liftCurveSlope_2D/(4*b)))

    for j in range(N):
        odd_col = 2*j+1
        LHS_matrix[i][j] = math.sin(odd_col*phi_vector[i]) * (odd_col*mu_vector[i] + math.sin(phi_vector[i]))
    RHS_matrix[i] = (mu_vector[i]*(AOA_dist[i]-ZeroLift_Alpha)*math.sin(phi_vector[i]))
A_vector = numpy.linalg.solve(LHS_matrix, RHS_matrix)

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

norm_spanwise_station = list(map(lambda y: (2*y/b), spanwise_station ))
ellip_lift = list(map(lambda y: air_density*v*vortexStrength*math.sqrt(1-y**2), norm_spanwise_station))

CL = math.pi*AR*A_vector[0]
lift = q * (Sref) * CL
print(lift)

plt.figure()
plt.plot(norm_spanwise_station, spanwise_Lift)
plt.plot(norm_spanwise_station, ellip_lift)
plt.xlabel("Spanwise station (2y/b)")
plt.ylabel("Lift (N)")
plt.grid(True)
plt.show()


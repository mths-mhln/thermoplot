import os
import sys
from src.coolprop_interface_thermoplot import CoolPropAbstractState
cwd = os.getcwd()
sys.path.append(f'{cwd}/src/')


import matplotlib.pyplot as plt
import numpy as np
from src.thermoplot import thermoplot


input_file_path = "config/R1234ze(E).ini"
fig = thermoplot(input_file_path)
axes = fig.get_axes()
print(f"axes: {axes}")


# plot whatever you want on it
AS = CoolPropAbstractState("HEOS", "R1234ze(E)")

T = AS.PropsSI('T', "P", 6833552.881809819, "D", 1126.1086961042747)

S = AS.PropsSI('S', "P", 6833552.881809819, "D", 1126.1086961042747)

axes[0].plot(S, T, marker='o', color='red', markersize=5, label='Test Point')


def _computeSoundSpeed_p_rho_single(p, rho, AS):
    """Core scalar function - no self, pure computation"""
    # check if the state is single phase or two phase
    T = AS.PropsSI("T", "P", p, "D", rho)
    S_sat_V = AS.PropsSI("S", "T", T, "Q", 1)
    S_sat_L = AS.PropsSI("S", "T", T, "Q", 0)
    S = AS.PropsSI("S", "T", T, "D", rho)

    
    if S <= S_sat_L or S >= S_sat_V:
        # single phase
        a = AS.PropsSI("A", "P", p, "D", rho)
        return a
    else:
        # two-phase (HEM model from Cioffi et al.)
        alpha_V = AS.PropsSI("Q", "P", p, "D", rho)
        alpha_L = 1 - alpha_V

        soundSpeed_L = AS.PropsSI("A", "P", p, "Q", 0)
        soundSpeed_V = AS.PropsSI("A", "P", p, "Q", 1)
        rho_L = AS.PropsSI("D", "P", p, "Q", 0)
        rho_V = AS.PropsSI("D", "P", p, "Q", 1)
        c_p_L = AS.PropsSI("Cpmass", "P", p, "Q", 0)
        c_p_V = AS.PropsSI("Cpmass", "P", p, "Q", 1)
        
        # Finite difference for ds/dp at constant Q
        ds_dp_cQ_L = (AS.PropsSI("S", "P", p + 1e3, "Q", 0) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 0)) / (2 * 1e3)
        ds_dp_cQ_V = (AS.PropsSI("S", "P", p + 1e3, "Q", 1) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 1)) / (2 * 1e3)
        
        # Sound speed according to Eq. 29 (Cioffi et al.)
        a = (rho * (
                alpha_L / (rho_L * soundSpeed_L**2) +
                alpha_V / (rho_V * soundSpeed_V**2) +
                T * ((alpha_L * rho_L / c_p_L) * ds_dp_cQ_L +
                        (alpha_V * rho_V / c_p_V) * ds_dp_cQ_V)
                ))**(-0.5)
        
        return a


D = AS.PropsSI("D", "P", 0.1e6, "Q", 0.7)
print(_computeSoundSpeed_p_rho_single(0.1e6, D, AS))

plt.show()




def _computeSoundSpeed_p_rho_single_lorenzo(p, rho, AS):
    """Core scalar function - no self, pure computation"""
    # check if the state is single phase or two phase
    T = AS.PropsSI("T", "P", p, "D", rho)
    S_sat_V = AS.PropsSI("S", "T", T, "Q", 1)
    S_sat_L = AS.PropsSI("S", "T", T, "Q", 0)
    S = AS.PropsSI("S", "T", T, "D", rho)

    
    if S <= S_sat_L or S >= S_sat_V:
        # single phase
        a = AS.PropsSI("A", "P", p, "D", rho)
        return a
    else:
        # two-phase (HEM model from Cioffi et al.)
        alpha_V = AS.PropsSI("Q", "P", p, "D", rho)
        alpha_L = 1 - alpha_V

        soundSpeed_L = AS.PropsSI("A", "P", p, "Q", 0)
        soundSpeed_V = AS.PropsSI("A", "P", p, "Q", 1)
        rho_L = AS.PropsSI("D", "P", p, "Q", 0)
        rho_V = AS.PropsSI("D", "P", p, "Q", 1)
        c_p_L = AS.PropsSI("Cpmass", "P", p, "Q", 0)
        c_p_V = AS.PropsSI("Cpmass", "P", p, "Q", 1)
        
        # Finite difference for ds/dp at constant Q
        ds_dp_cQ_L = (AS.PropsSI("S", "P", p + 1e3, "Q", 0) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 0)) / (2 * 1e3)
        ds_dp_cQ_V = (AS.PropsSI("S", "P", p + 1e3, "Q", 1) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 1)) / (2 * 1e3)
        
        # Sound speed according


# isentropic expansion: starting from "P", 6833552.881809819, "D", 1126.1086961042747, going to P = 136671
P_1 = 6833552.881809819
rho_1 = 1126.1086961042747
S_1 = AS.PropsSI("S", "P", P_1, "D", rho_1)
P_2 = 136671

S = np.ones(100) * S_1
P = np.linspace(P_1, P_2, 100)

rho = AS.PropsSI("D", "P", P, "S", S)
internal_energy = AS.PropsSI("U", "P", P, "S", S)
T = AS.PropsSI("T", "P", P, "S", S)
soundSpeed = np.array([_computeSoundSpeed_p_rho_single(p, r, AS) for p, r in zip(P, rho)])
Q = AS.PropsSI("Q", "P", P, "S", S)
Cp_mass = AS.PropsSI("Cpmass", "P", P, "S", S)



plt.plot(P, soundSpeed)
plt.xlabel("Pressure (Pa)")
plt.ylabel("Sound Speed (m/s)")
plt.show()

plt.plot(P, rho)
plt.xlabel("Pressure (Pa)")
plt.ylabel("Density (kg/m³)")
plt.show()

plt.plot(P, T)
plt.xlabel("Pressure (Pa)")
plt.ylabel("Temperature (K)")
plt.show()

plt.plot(P, Q)
plt.xlabel("Pressure (Pa)")
plt.ylabel("Quality")
plt.show()

plt.plot(P, Cp_mass)
plt.xlabel("Pressure (Pa)")
plt.ylabel("Specific Heat Capacity at Constant Pressure (J/kg/K)")
plt.show()

plt.plot(P, internal_energy)
plt.xlabel("Pressure (Pa)")
plt.ylabel("Specific Internal Energy (J/kg)")
plt.show()
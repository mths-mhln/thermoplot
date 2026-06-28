import os
import sys
from src.coolprop_interface_thermoplot import CoolPropAbstractState
cwd = os.getcwd()
sys.path.append(f'{cwd}/src/')


import matplotlib.pyplot as plt
import numpy as np
from src.thermoplot import thermoplot_cached


# input_file_path = "config/R1234ze(E).ini"
# fig = thermoplot(input_file_path)
# axes = fig.get_axes()
# # plot whatever you want on it
# AS = CoolPropAbstractState("HEOS", "R1234ze(E)")
# T = AS.PropsSI('T', "P", 6833552.881809819, "D", 1126.1086961042747)
# S = AS.PropsSI('S', "P", 6833552.881809819, "D", 1126.1086961042747)
# axes[0].plot(S, T, marker='o', color='red', markersize=5, label='Test Point')


def _computeSoundSpeed_p_rho_single(p, rho, AS):
    """Core scalar function - no self, pure computation"""
    # check if the state is single phase or two phase
    T = AS.PropsSI("T", "P", p, "D", rho)
    S_sat_V = AS.PropsSI("S", "T", T, "Q", 1)
    S_sat_L = AS.PropsSI("S", "T", T, "Q", 0)
    S = AS.PropsSI("S", "T", T, "D", rho)
    # print("T: ", T)
    # print("S_sat_V: ", S_sat_V)
    # print("S_sat_L: ", S_sat_L)
    # print("S: ", S)

    
    if S <= S_sat_L or S >= S_sat_V:
        # single phase
        a = AS.PropsSI("A", "P", p, "D", rho)
        return a
    else:
        # two-phase (HEM model from Cioffi et al.)
        x_V = AS.PropsSI("Q", "P", p, "D", rho)
        x_L = 1 - x_V

        soundSpeed_L = AS.PropsSI("A", "P", p, "Q", 0)
        soundSpeed_V = AS.PropsSI("A", "P", p, "Q", 1)
        rho_L = AS.PropsSI("D", "P", p, "Q", 0)
        rho_V = AS.PropsSI("D", "P", p, "Q", 1)
        c_p_L = AS.PropsSI("Cpmass", "P", p, "Q", 0)
        c_p_V = AS.PropsSI("Cpmass", "P", p, "Q", 1)

        
        alpha_V = x_V*(rho/rho_V)
        alpha_L = x_L*(rho/rho_L)

        # Finite difference for ds/dp at constant Q
        ds_dp_cQ_L = (AS.PropsSI("S", "P", p + 1e3, "Q", 0) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 0)) / (2 * 1e3)
        ds_dp_cQ_V = (AS.PropsSI("S", "P", p + 1e3, "Q", 1) -
                        AS.PropsSI("S", "P", p - 1e3, "Q", 1)) / (2 * 1e3)
        
        # print("x_V: ", x_V)
        # print("x_L: ", x_L)
        # print("soundSpeed_L: ", soundSpeed_L)
        # print("soundSpeed_V: ", soundSpeed_V)
        # print("rho_L: ", rho_L)
        # print("rho_V: ", rho_V)
        # print("c_p_L: ", c_p_L)
        # print("c_p_V: ", c_p_V)
        # print("ds_dp_cQ_L: ", ds_dp_cQ_L)
        # print("ds_dp_cQ_V: ", ds_dp_cQ_V)
        # print("rho: ", rho)
        # print("T: ", T)
        
        # Sound speed according to Eq. 29 (Cioffi et al.)

        a = np.sqrt(1/(
            rho * (
                alpha_L / (rho_L * soundSpeed_L**2) +
                alpha_V / (rho_V * soundSpeed_V**2) +
                T * ((alpha_L * rho_L / c_p_L) * ds_dp_cQ_L**2 +
                        (alpha_V * rho_V / c_p_V) * ds_dp_cQ_V**2
                )
            )
        ))
        
        return a

AS = CoolPropAbstractState("REFPROP", "R1234ze(E)")
D = AS.PropsSI("D", "P", 0.1e6, "Q", 0.7)
# print(_computeSoundSpeed_p_rho_single(0.1e6, D, AS))




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

# print("=============================================")
# print("=============================================")
# print("=============================================")
# print("=============================================")
# print("=============================================")
# P_1 = 6833552.881809819
# rho_1 = 1126.1086961042747
# S_1 = AS.PropsSI("S", "P", P_1, "D", rho_1)
# P_2 = 136671

# S = np.ones(100) * S_1
# P = np.linspace(P_1, P_2, 100)
# T = AS.PropsSI("T", "P", P, "S", S)

# input_file_path = "config/R1234ze(E).ini"
# fig = thermoplot_cached(input_file_path)
# axes = fig.get_axes()
# axes[0].plot(S, T, marker='o', color='green', markersize=5, label='Isentropic Expansion Path')
# plt.show()

# rho_v = AS.PropsSI("D", "P", T, "Q", 1)
# rho_l = AS.PropsSI("D", "P", T, "Q", 0)
# x_V = AS.PropsSI("Q", "P", P, "S", S)
# x_L = 1 - x_V
# print("x_V: ", x_V)
# print("x_L: ", x_L)
# rho_cp = AS.PropsSI("D", "P", P, "S", S)
# alpha_V = x_V * (rho_cp / rho_v)
# alpha_L = x_L * (rho_cp / rho_l)
# rho = alpha_V * rho_v + alpha_L * rho_l
# rho_cp = AS.PropsSI("D", "P", P, "S", S)
# # rho = AS.PropsSI("D", "P", P, "S", S)
# internal_energy = AS.PropsSI("U", "P", P, "S", S)
# T = AS.PropsSI("T", "P", P, "S", S)
# soundSpeed = np.array([_computeSoundSpeed_p_rho_single(p, r, AS) for p, r in zip(P, rho_cp)])
# Q = AS.PropsSI("Q", "P", P, "S", S)
# Cp_mass = AS.PropsSI("Cpmass", "P", P, "S", S)



# plt.plot(P, soundSpeed)
# plt.xlabel("Pressure (Pa)")
# plt.ylabel("Sound Speed (m/s)")
# plt.show()

# plt.plot(P, rho)
# plt.xlabel("Pressure (Pa)")
# plt.ylabel("Density (kg/m³)")
# plt.show()

# plt.plot(P, T)
# plt.xlabel("Pressure (Pa)")
# plt.ylabel("Temperature (K)")
# plt.show()

# plt.plot(P, Q)
# plt.xlabel("Pressure (Pa)")
# plt.ylabel("Quality")
# plt.show()

# plt.plot(P, Cp_mass)
# plt.xlabel("Pressure (Pa)")
# plt.ylabel("Specific Heat Capacity at Constant Pressure (J/kg/K)")
# plt.show()

# plt.plot(P, internal_energy)
# plt.xlabel("Pressure (Pa)")
# plt.ylabel("Specific Internal Energy (J/kg)")
# plt.show()

# # decrease metrics
# print("Sound speed decrease: ", (soundSpeed[0] - soundSpeed[-1]) / soundSpeed[0] * 100, "%")
# print("soundspeed", soundSpeed)
# print("Density decrease: ", (rho[0] - rho[-1]) / rho[0] * 100, "%")
# print("Temperature decrease: ", (T[0] - T[-1]) / T[0] * 100, "%")
# print("Quality increase: ", (Q[-1] - Q[0]) / (Q[-1] + 1e-6) * 100, "%") # add small number to avoid division by zero
# print("Specific heat capacity decrease: ", (Cp_mass[0] - Cp_mass[-1]) / Cp_mass[0] * 100, "%")
# print("Specific internal energy decrease: ", (internal_energy[0] - internal_energy[-1]) / internal_energy[0] * 100, "%")


# print(AS.PropsSI("D", "P", P[-1], "Q", 0))
# print(AS.PropsSI("D", "P", P[-1], "Q", 1))
# print(AS.PropsSI("D", "P", P[-1], "S", S[-1]))



# create a plot showing variation of HEM sound speed for p = 0.1 MPa and quality varying from 0-1
# p = 0.1e6  # 0.1 MPa
# Q = np.linspace(0,1, 10000)
# # convert quality into void fraction 
# rho = AS.PropsSI("D", "P", p, "Q", Q)
# rho_v = AS.PropsSI("D", "P", p, "Q", 1)
# alpha_V = Q * (rho / rho_v)
# soundSpeed_HEM = np.array([_computeSoundSpeed_p_rho_single(p, AS.PropsSI("D", "P", p, "Q", Q_input), AS) for Q_input in Q])
# print(soundSpeed_HEM)
# plt.plot(alpha_V, soundSpeed_HEM)
# plt.xlabel("Quality")
# plt.ylim(0,120)
# plt.ylabel("HEM Sound Speed (m/s)")
# plt.title("HEM Sound Speed vs Quality at 0.1 MPa")
# plt.show()



input_file_path = "config/CO2.ini"
fig = thermoplot_cached(input_file_path)
axes = fig.get_axes()
AS = CoolPropAbstractState("REFPROP", "CO2")
T = AS.PropsSI("T", "P", 5132184.458519519, "D", 127.92696343816884)
S = AS.PropsSI("S", "P", 5132184.458519519, "D", 127.92696343816884)
axes[0].plot(S, T, marker='o', color='green', markersize=5, label='Isentropic Expansion Path')
plt.show()



print(AS.PropsSI("S", "T", 304.128, "Q", 1))







import utils.fluid_properties.fluid_properties as FP
from utils.fluid_properties.fluid_properties import AbstractState_v2
from CoolProp.CoolProp import AbstractState
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI
import numpy as np

AS = AbstractState_v2("CoolProp", "R1234ze(E)")

fluid_propssi = FP.fluid('CoolProp', 'R1234ze(E)')
fluid_abstractstate = FP.AbstractState_v2('CoolProp', 'R1234ze(E)')

# Try and compare similar expansions using fluid and abstractstate

# t_lst = np.array([300, 310, 320, 330, 340])
# p_lst = np.array([100000, 200000, 300000, 400000, 500000])

AS = AbstractState_v2("REFPROP", "R1234ze(E)")
# # AS.update(CP.QSmass_INPUTS, 0, 1000)
# # print(AS)

# # print(PropsSI('Dmass', 'T', 1000, 'Q', 0, "REFPROP::R1234ze(E)"))


# for t in t_lst:
#     print(f"PropsSI: {FP.PropsSI('Dmass', 'T', t, 'Q', 0, fluid_propssi)}")
    

# print(f"PropsSAS: {FP.PropsSI('Dmass', 'p', 159000, 'Q', 0, fluid_abstractstate)}")
# print(f"PropsSAS: {FP.PropsSI('Dmass', 'h', 327000, 'Q', 0, fluid_abstractstate)}")
# print(f"PropsSAS: {FP.PropsSI('Dmass', 'T', 300, 'Q', 0, fluid_abstractstate)}")


# print(FP.PropsSI("Tcrit", fluid_object=fluid_abstractstate))

# print(PropsSI('H', 'S', 232.54848753170145, 'T', 169.16899999999998, "REFPROP::R1234ze(E)"))
print(AS.PropsSI("P", "H", 423308.27067669, "T", 382.513))
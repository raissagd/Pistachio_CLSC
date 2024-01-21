import decode as dc
import numpy as np
import read

# Flow from pistachio factories K to pistachio customers N1
chromo_KN1 = [2, 5, 3, 6, 4, 1]
sources_K= [0, 1, 2]
depots_N1 = [0, 1, 2]
production_capacity_K = read.Cpw
demand_N1 = read.Dp
shipment_cost_KN1 = read.Cp
dc.decode(sources_K, depots_N1, demand_N1, production_capacity_K, shipment_cost_KN1, chromo_KN1)

# Flow from cosmetic factories S to cosmetic consumers N3
chromo_SN3 = [2, 3, 1, 4]
sources_S = [0, 1]
depots_N3 = [0, 1]
production_capacity_S = read.Cpv
demand_N3 = read.Ds
shipment_cost_SN3 = read.Cl
dc.decode(sources_S, depots_N3, demand_N3, production_capacity_S, shipment_cost_SN3, chromo_SN3)

# Flow from composting centers Q to compost consumers M
chromo_QM = [2, 3, 1, 4]
sources_Q = [0, 1]
depots_M = [0, 1]
production_capacity_Q = read.Cpy
demand_M = read.Dc
shipment_cost_QM = read.Cd
dc.decode(sources_Q, depots_M, demand_M, production_capacity_Q, shipment_cost_QM, chromo_QM)

# ---------------------------------------------------------
# Flow from oil extraction centers (E -> N2 & S + Q)
chromo_ESN2 = [2, 3, 5, 7, 1, 4, 6, 8, 9]
sources_E = [0, 1, 2, 3]
depots_SN2 = [0, 1, 2, 3, 4]
production_capacity_E = read.Cpr
demand_N2 = read.Du
total_demand_E = np.hstack((demand_N2, production_capacity_S))
total_shipment_cost_E= np.hstack((read.CN, read.CS)) # shipment cost E -> N2 + shipment cost E -> S

dc.decode(sources_E, depots_SN2, total_demand_E, production_capacity_E, total_shipment_cost_E, chromo_ESN2)

total_demand_E = production_capacity_E / (1 - read.lambd) # lambda = waste percentage of oil extracting process
amount_to_send_to_compost = total_demand_E * read.lambd

# ---------------------------------------------------------
# Flow from processing center (J -> K & E + Q)
chromo_JKE = [3, 9, 4, 8, 1, 10, 2, 5, 6, 7]
sources_J = [0, 1, 2]
depots_KE = [0, 1, 2, 3, 4, 5, 6]
production_capacity_J = read.Cpu
total_demand_J = np.hstack((production_capacity_K, total_demand_E))
total_shipment_cost_J = np.hstack((read.CK, read.CE)) # shipment cost J -> K + shipment cost J -> E

dc.decode(sources_J, depots_KE, total_demand_J, production_capacity_J, total_shipment_cost_J, chromo_JKE)
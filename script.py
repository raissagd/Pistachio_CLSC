import decode as dc
import numpy as np
import read

# Flow from pistachio factories K to pistachio customers N1
chromo_KN1 = [2, 5, 3, 6, 4, 1]
production_capacity_K = read.Cpw
demand_N1 = read.Dp
shipment_cost_KN1 = read.Cp  # Shipping cost pistachio factory k -> pistachio customer N1
dc.decoding(chromo_KN1, production_capacity_K, demand_N1, shipment_cost_KN1)

# Flow from cosmetic factories S to cosmetic consumers N3
chromo_SN3 = [2, 3, 1, 4]
production_capacity_S = read.Cpv
demand_N3 = read.Ds
shipment_cost_SN3 = read.Cl # Shipping cost cosmetic factory s -> customer N3
dc.decoding(chromo_SN3, production_capacity_S, demand_N3, shipment_cost_SN3)

# Flow from composting centers Q to compost consumers M
chromo_QM = [2, 3, 1, 4]
production_capacity_Q = read.Cpy
demand_M = read.Dc
shipment_cost_QM = read.Cd # Shipping cost composting center q -> compost customer m
dc.decoding(chromo_QM, production_capacity_Q, demand_M, shipment_cost_QM)

# ---------------------------------------------------------
# Flow from oil extraction centers (E -> N2 & S + Q)
chromo_ESN2 = [2, 3, 5, 7, 1, 4, 6, 8, 9]
production_capacity_E = read.Cpr
demand_N2S = np.hstack((read.Du, production_capacity_S))  # amount N2 demands + production capacity of S
total_shipment_cost_E = np.hstack((read.CN, read.CS)) # shipment cost E -> N2 + shipment cost E -> S

dc.decoding(chromo_ESN2, production_capacity_E, demand_N2S, total_shipment_cost_E)

amount_e_demands = production_capacity_E / (1 - read.lambd) # lambda = waste percentage of oil extracting process
amount_to_send_from_e_to_compost = amount_e_demands * read.lambd

# ---------------------------------------------------------
# Flow from processing center (J -> K & E + Q)
chromo_JKE = [3, 9, 4, 8, 1, 10, 2, 5, 6, 7]
production_capacity_J = read.Cpu
demand_KE = np.hstack((production_capacity_K, amount_e_demands)) # producion capacity of K + total amount E demands
total_shipment_cost_J = np.hstack((read.CK, read.CE)) # shipment cost J -> K + shipment cost J -> E

dc.decoding(chromo_JKE, production_capacity_J, demand_KE, total_shipment_cost_J)

amount_j_demands = production_capacity_J / (1 - read.Beta) / (read.Theta[0] + read.Theta[1]) # Theta = Waste percentage of product type b from processing center j
amount_to_send_from_j_to_compost_ = amount_j_demands * read.Theta[2]

# ---------------------------------------------------------
# Flow from producers to processing center (I -> J)
chromo_JI = [6,3,4,2,1,5]
production_capacity_I = read.Cpa
total_shipment_cost_I = read.CX

dc.decoding(chromo_JI, production_capacity_I, amount_j_demands, total_shipment_cost_I)
import decode as dc
import numpy as np
import read

# fluxo fábricas de pistache -> clientes de pistache
chromo = [2,5,3,6,4,1]
K = [0, 1, 2] # set of sources
J = [0, 1, 2] # set of depots
a = read.Cpw # Production capacity for pistachio factory k
b = read.Dp  # The demand of open-mouth pistachio by pistachio customer N1
c = read.Cp # Shipping cost pistachio factory k -> pistachio customer N1
dc.decode(K, J, b, a, c, chromo)

# fluxo fábricas de cosmético -> consumidores de cosmético
chromo2 =  [2, 3, 1, 4]
K2 = [0, 1]
J2 = [0, 1] 
a2 = read.Cpv # Production capacity for cosmetic factory s
b2 = read.Ds # The demand of cosmetic by cosmetic customer N3
c2 = read.Cl # Shipping cost cosmetic factory s -> customer N3
dc.decode(K2, J2, b2, a2, c2, chromo2)

# fluxo centros de compostagem -> consumidores de compostagem
chromo3 =  [2, 3, 1, 4]
a3 = read.Cpy# Production capacity for composting center q
b3 = read.Dc # The demand for compost by customer M
c3 = read.Cd # Shipping cost composting center q -> compost customer m
dc.decode(K2, J2, b3, a3, c3, chromo3)

# ---------------------------------------------------------
# fluxo centros de extração de óleo

K3 = [0, 1, 2, 3]
J3 = [0, 1, 2, 3, 4]
chromo4 = [2, 3, 5, 7, 1, 4, 6, 8, 9]

a4 = read.Cpr # Production capacity for oil extraction center e
bn2 = read.Du  # The demand for oil by oil customer N2
cen2 = read.CN # Shipping cost oil extraction center e -> oil customer N2
ces = read.CS # Shipping cost oil extraction center e -> cosmetic factory s

b4 = np.hstack((bn2, a2)) # demanda N2 + capacidade de produção S
c4 = np.hstack((cen2, ces)) # custo N2 + custo S

dc.decode(K3, J3, b4, a4, c4, chromo4)

o_tanto_que_e_precisa_receber = a4/(1-read.lambd) # lambda = waste percentage of oil extracting process
o_tanto_que_e_pode_enviar_para_q = o_tanto_que_e_precisa_receber * read.lambd

# ---------------------------------------------------------
# fluxo centro de processamento
chromo5 = [ 3, 9, 4, 8, 1, 10, 2, 5, 6, 7]
K5 = [0, 1, 2]
J5 = [0, 1, 2, 3, 4, 5, 6]
a5 = read.Cpu # Production capacity for processing centers j
b5 = np.hstack((a, o_tanto_que_e_precisa_receber)) # capacidade de produção de J + quanto E precisa receber
c5 = np.hstack((read.CK, read.CE))  # Shipping cost processing center j -> pistachio factory k + Shipping cost processing center j -> oil extraction center e
dc.decode(K5, J5, b5, a5, c5, chromo5)
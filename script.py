import decode as dc
import numpy as np
import read

# Fluxo 1: fábricas de pistache -> consumidores de pistache
S1 = np.array([2,3,1]) 

# Capacidade da fonte
a1 = read.gammak * read.Cpw # quantidade que chega do centro de processamento * taxa de produção da fábrica

# Demanda de cada depósito
b1 = read.Dp

# Custo total = custo de transporte + custo de produção
c1 = read.Cp + read.Cw[:, None] 

# Calculando o custo e a matriz de transporte
totalcost, P = dc.decoding(S1, a1, b1, c1)

# -------------------------------------------------------------
# Fluxo 2: fábricas de cosméticos -> consumidores de cosméticos
S2 = np.array([1,2])
a2 = read.gammas * read.Cpv
b2 = read.Ds
c2 = read.Cl + read.Cv[:, None]
cost2, L = dc.decoding(S2, a2, b2, c2) # L = quanto de cosmético foi enviado para cada consumidor 
totalcost += cost2

# -------------------------------------------------------------
# Fluxo 3: centros de extração de óleo -> consumidores de óleo + fábricas de cosméticos
S3 = np.array([3,1,2,4])
a3 = (1 - read.lamb) * read.Cpr # capacidade de produção do centro de extração de óleo x 1 - porcentagem de perda de óleo no processo de extração
b3 = np.hstack((read.Du, np.sum(L, axis=1)/read.gammas)) # demanda dos consumidores de óleo + quantidade de óleo que deve ser enviado para as fábricas de cosméticos (quantidade calculada no fluxo anterior / taxa de produção das fábricas)
c3 = np.hstack((read.CN + read.Cr[:, None], read.CS + read.Cr[:, None])) # custo de transporte do centro de extração de óleo para o consumidor de óleo + custo de transporte do centro de extração de óleo para a fábrica de cosméticos
cost3, OOc = dc.decoding(S3, a3, b3, c3) # OOC é um array com a quantidade de produto que deve ser enviado para cada um dos 2 consumidores de óleo e para a única fábrica de cosméticos (matriz 1x3, por isso tem que ser dividida)
totalcost += cost3

# Separa as variáveis
O = OOc[:, :read.N2] # 1x2
Oc = OOc[:, read.N2:] # 1x1

# -------------------------------------------------------------
# Fluxo 4: centro de processamento -> fábricas de pistache + centros de extração de óleo

# Etapa: Centro de processamento -> fábricas de pistache
S4_1 = np.array([3, 1, 2]) 
a4_1 = read.Cpu
b4_1 = np.sum(P, axis=1)/read.gammak
_, Go = dc.decoding(S4_1, a4_1, b4_1, read.CK + read.Cu1[:, None]) 

# Etapa: Centro de processamento -> centro de extração de óleo 
S4_2 = np.array([3, 1, 2])
a4_2 = read.Cpu
b4_2 = (np.sum(O, axis=1) + np.sum(Oc, axis=1))/(1-read.lamb)
_, Gr = dc.decoding(S4_2, a4_2, b4_2, read.CE + read.Cu2[:, None])

# Etapa: forçando as restrições de igualdade 
# Demanda do centro de processamento compatível com o transporte para as fábricas de pistache
bX1 = np.sum(Go, axis=1)/(1-read.beta)/read.theta[0]

# Demanda do centro de processamento compatível com o transporte para o centro de extração de óleo
bX2 = np.sum(Gr, axis=1)/(1-read.beta)/read.theta[1]

# Demanda final do centro de processamento
b = np.zeros(read.J)

# Para cada centro de processamento
for j in range(read.J):
    
    # Se a demanda relacionada às fabricas de pistache é maior
    if bX1[j] > bX2[j]:
        
        # A demanda final do centro de processamento é a demanda relacionada às fabricas de pistache
        b[j] = bX1[j]
        
        # Encontro qual centro de extração de óleo tem o menor custo
        e = np.argmin(read.CE[j, :] + read.Cu2[j])
        
        # Calculo quanto de caroço deveria sair do centro de processamento
        amount = b[j]*read.theta[1]*(1-read.beta)
        
        # Atribuo a aquele trecho a quantidade de caroço que falta para completar a demanda final
        Gr[j, e] = Gr[j, e] + amount - np.sum(Gr[j, :])
    
    # Caso contrário
    else:
        # A demanda final do centro de processamento é a demanda relacionada ao centro de extração de óleo
        b[j] = bX2[j]
        
        # Encontro qual fabrica de pistache tem o menor custo
        k = np.argmin(read.CK[j, :] + read.Cu1[j])
        
        # Calculo quanto de pistache deveria sair do centro de processamento
        amount = b[j]*read.theta[0]*(1-read.beta)
        
        # Atribuo a aquele trecho a quantidade de pistache que falta para completar a demanda final
        Go[j, k] = Go[j, k] + amount - np.sum(Go[j, :])

# Calcula o custo
totalcost += np.sum((read.CK + read.Cu1[:, None])*Go) + np.sum((read.CE + read.Cu2[:, None])*Gr)

# -------------------------------------------------------------
# Fluxo 5: produtores de pistache -> centros de processamento
S5 = np.array([3, 5, 1, 4, 2])
a5 = read.Cpa
b5 = np.sum(Go, axis=1)/(1-read.beta)/read.theta[0]
c5 = read.CX + read.CI[:, None]
cost5, X = dc.decoding(S5, a5, b5, c5)
totalcost += cost5

# -------------------------------------------------------------
# Fluxo 6: centros de compostagem -> consumidores de compostagem
S6 = np.array([1,2,3])
a6 = read.gammaq * read.Cpy
b6 = read.Dc
c6 = read.Cd + read.Cy[:, None]
cost6, D = dc.decoding(S6, a6, b6, c6)
totalcost += cost6

# -------------------------------------------------------------
# Fluxo 7: centros de processamento/ extração de óleo -> centros de compostagem

# Define a matriz de fluxo entre os centros de processamento e os centros de compostagem
Gw = np.zeros((read.J, read.Q))

# A quantidade de resíduo a ser enviada pelos centros de processamento
a = np.sum(X, axis=0)* read.theta[2]

# A quantidade mínima de resíduo necessária pelos centros de compostagem
b = np.sum(D, axis=1)/ read.gammaq

# Para cada centro de processamento
for j in range(read.J):
    # Identifica o centro de compostagem com o menor custo
    q = np.argmin(read.CJ[j, :])
    
    # Atribui todo o resíduo para esse trecho
    Gw[j, q] = a[j]

# Para cada centro de compostagem
for q in range(read.Q):
    # Se a quantidade de resíduo já enviada é menor que a quantidade necessária
    if b[q] > Gw[:, q].sum():
        # Atualiza a demanda do centro de compostagem diminuido a quantidade
        b[q] = b[q] - np.sum(Gw[:, q])
    
    # Se a quantidade de resíduo já enviada é maior que a quantidade necessária
    else:
        # Nenhum resíduo a mais é necessário
        b[q] = 0

# Se ainda há algum centro de compostagem que necessita de resíduo
if np.sum(b) > 0:
    # Exemplo de cromossomo para a etapa considerada
    S7 = np.array([1])
    
    # Definindo a capacidade de cada fonte
    a = read.lamb*np.sum(Gr, axis=0)
    
    # Calculando o custo e a matriz de transporte
    _, Ow = dc.decoding(S7, a, b, read.CQ)

# Caso contrário, não é necessário enviar nenhum resíduo do centro de extração de óleo para os centros de compostagem
else:
    Ow = np.zeros((read.E, read.Q))
    
# Atualiza os custos
totalcost += np.sum(read.CJ*Gw) + np.sum(read.CQ*Ow)

# Imprime os dados da etapa
a = np.hstack((np.sum(X, axis=0)*read.theta[2], read.lamb*np.sum(Gr, axis=0)))
b = np.sum(D, axis=1)/read.gammaq
GwOw = np.vstack((Gw, Ow))
print(f"a={a} | Gw+Ow={GwOw} | b={b}")

# -------------------------------------------------------------
# Somando os custos de abertura à função objetivo

# Abertura dos centros de processamento
U = np.sum(X, axis=0) != 0
U = U.astype(int)

# Abertura dos centros de compostagem
Y = (Gw.sum(axis=0) + Ow.sum(axis=0)) != 0
Y = Y.astype(int)

# Abertura das fábricas de pistache
W = np.sum(Go, axis=0) != 0
W = W.astype(int)

# Abertura dos centros de extração de óleo
R = np.sum(Gr, axis=0) != 0
R = R.astype(int)

# Abertura das fábricas de cosméticos
V = np.sum(Oc, axis=0) != 0
V = V.astype(int)

totalcost += (np.sum(read.Fu*U) + np.sum(read.Fy*Y) + np.sum(read.Fw*W) + np.sum(read.Fr*R) 
              + np.sum(read.Fv*V))

print(f"A avaliação da solução pela função-objetivo: F1 = {totalcost}")
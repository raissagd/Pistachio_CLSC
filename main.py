import decode as dc
import numpy as np
import read

def generate_random_chromosome(size):
    numbers = np.arange(1, size + 1)
    np.random.shuffle(numbers)
    return np.array(numbers.tolist())

def calculate_flux():
    # -------------------------------------------------------------
    # Fluxo 1: fábricas de pistache -> consumidores de pistache
    S1 = generate_random_chromosome(read.K + read.N1)
    a1 = read.gammak * read.Cpw
    b1 = read.Dp
    c1 = read.Cp + read.Cw[:, None]
    totalcost, P = dc.decoding(S1, a1, b1, c1)

    # -------------------------------------------------------------
    # Fluxo 2: fábricas de cosméticos -> consumidores de cosméticos
    S2 = generate_random_chromosome(read.S + read.N3)
    a2 = read.gammas * read.Cpv
    b2 = read.Ds
    c2 = read.Cl + read.Cv[:, None]
    cost2, L = dc.decoding(S2, a2, b2, c2)
    totalcost += cost2

    # -------------------------------------------------------------
    # Fluxo 3: centros de extração de óleo -> consumidores de óleo + fábricas de cosméticos
    S3 = generate_random_chromosome(read.E + read.N2 + read.S)
    a3 = (1 - read.lamb) * read.Cpr
    b3 = np.hstack((read.Du, np.sum(L, axis=1)/read.gammas))
    c3 = np.hstack((read.CN + read.Cr[:, None], read.CS + read.Cr[:, None]))
    cost3, OOc = dc.decoding(S3, a3, b3, c3)
    totalcost += cost3

    O = OOc[:, :read.N2]
    Oc = OOc[:, read.N2:]

    # -------------------------------------------------------------
    # Fluxo 4: centro de processamento -> fábricas de pistache + centros de extração de óleo

    # Etapa: Centro de processamento -> fábricas de pistache
    S4_1 = generate_random_chromosome(read.J + read.K)
    a4_1 = read.Cpu
    b4_1 = np.sum(P, axis=1)/read.gammak
    _, Go = dc.decoding(S4_1, a4_1, b4_1, read.CK + read.Cu1[:, None])

    # Etapa: Centro de processamento -> centro de extração de óleo 
    S4_2 = generate_random_chromosome(read.J + read.E)
    a4_2 = read.Cpu
    b4_2 = (np.sum(O, axis=1) + np.sum(Oc, axis=1))/(1-read.lamb)
    _, Gr = dc.decoding(S4_2, a4_2, b4_2, read.CE + read.Cu2[:, None])
    
    # Etapa: forçando as restrições de igualdade 
    # Demanda do centro de processamento compatível com o transporte para as fábricas de pistache
    bX1 = np.sum(Go, axis=1)/(1-read.beta)/read.theta[0]

    # Demanda do centro de processamento compatível com o transporte para o centro de extração de óleo
    bX2 = np.sum(Gr, axis=1)/(1-read.beta)/read.theta[1]

    # Demanda final do centro de processamento
    b4 = np.zeros(read.J)

    # Para cada centro de processamento
    for j in range(read.J):
        
        # Se a demanda relacionada às fabricas de pistache é maior
        if bX1[j] > bX2[j]:
            
            # A demanda final do centro de processamento é a demanda relacionada às fabricas de pistache
            b4[j] = bX1[j]
            
            # Encontro qual centro de extração de óleo tem o menor custo
            e = np.argmin(read.CE[j, :] + read.Cu2[j])
            
            # Calculo quanto de caroço deveria sair do centro de processamento
            amount = b4[j]*read.theta[1]*(1-read.beta)
            
            # Atribuo a aquele trecho a quantidade de caroço que falta para completar a demanda final
            Gr[j, e] = Gr[j, e] + amount - np.sum(Gr[j, :])
        
        # Caso contrário
        else:
            # A demanda final do centro de processamento é a demanda relacionada ao centro de extração de óleo
            b4[j] = bX2[j]
            
            # Encontro qual fabrica de pistache tem o menor custo
            k = np.argmin(read.CK[j, :] + read.Cu1[j])
            
            # Calculo quanto de pistache deveria sair do centro de processamento
            amount = b4[j]*read.theta[0]*(1-read.beta)
            
            # Atribuo a aquele trecho a quantidade de pistache que falta para completar a demanda final
            Go[j, k] = Go[j, k] + amount - np.sum(Go[j, :])

    # Calcula o custo
    totalcost += np.sum((read.CK + read.Cu1[:, None])*Go) + np.sum((read.CE + read.Cu2[:, None])*Gr)
 
    # -------------------------------------------------------------
    # Fluxo 5: produtores de pistache -> centros de processamento
    S5 = generate_random_chromosome(read.I + read.J)
    a5 = read.Cpa
    b5 = np.sum(Go, axis=1)/(1-read.beta)/read.theta[0]
    c5 = read.CX + read.CI[:, None]
    cost5, X = dc.decoding(S5, a5, b5, c5)
    totalcost += cost5

    # -------------------------------------------------------------
    # Fluxo 6: centros de compostagem -> consumidores de compostagem
    S6 = generate_random_chromosome(read.Q + read.M)
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
    a7 = np.sum(X, axis=0)* read.theta[2]

    # A quantidade mínima de resíduo necessária pelos centros de compostagem
    b7 = np.sum(D, axis=1)/ read.gammaq

    # Para cada centro de processamento
    for j in range(read.J):
        # Identifica o centro de compostagem com o menor custo
        q = np.argmin(read.CJ[j, :])
        
        # Atribui todo o resíduo para esse trecho
        Gw[j, q] = a7[j]

    # Para cada centro de compostagem
    for q in range(read.Q):
        # Se a quantidade de resíduo já enviada é menor que a quantidade necessária
        if b7[q] > Gw[:, q].sum():
            # Atualiza a demanda do centro de compostagem diminuido a quantidade
            b7[q] = b7[q] - np.sum(Gw[:, q])
        
        # Se a quantidade de resíduo já enviada é maior que a quantidade necessária
        else:
            # Nenhum resíduo a mais é necessário
            b7[q] = 0

    # Se ainda há algum centro de compostagem que necessita de resíduo
    if np.sum(b7) > 0:
        # Exemplo de cromossomo para a etapa considerada
        S7 = np.array([1])
        
        # Definindo a capacidade de cada fonte
        a = read.lamb*np.sum(Gr, axis=0)
        
        # Calculando o custo e a matriz de transporte
        _, Ow = dc.decoding(S7, a, b7, read.CQ)

    # Caso contrário, não é necessário enviar nenhum resíduo do centro de extração de óleo para os centros de compostagem
    else:
        Ow = np.zeros((read.E, read.Q))
        
    # Atualiza os custos
    totalcost += np.sum(read.CJ*Gw) + np.sum(read.CQ*Ow)

    # Imprime os dados da etapa
    a = np.hstack((np.sum(X, axis=0)*read.theta[2], read.lamb*np.sum(Gr, axis=0)))
    b = np.sum(D, axis=1)/read.gammaq
    GwOw = np.vstack((Gw, Ow))

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

    print(f"A avaliacao da solucao pela funcao-objetivo: F1 = {totalcost}")

calculate_flux()
K = [0, 1, 2] # Índices das fontes
J = [0, 1, 2, 3] # Índices dos depósitos
a = [550, 300, 450] # Capacidade de cada fonte
b = [300, 350, 300, 350] # Demanda de cada depósito
c = [[11, 19, 17, 18], [16, 14, 18, 15], [15, 16, 19, 13]] # Matriz de custo de transporte da fonte para o depósito
chromosome = [2, 5, 3, 7, 4, 1, 6] # Cromossomo representando as prioridades

def decode_step(K, J, b, a, c, chromosome):
    # Passo 1: Inicializar g com zero
    g = 0
    
    # Passo 2: Encontrar o índice 'l' com a maior prioridade no cromossomo que não seja zero.
    non_zero_priorities = [i for i, v in enumerate(chromosome) if v != 0]
    if not non_zero_priorities:
        # Se todas as prioridades forem zero, o algoritmo deve terminar.
        return None, None, None
    
    l = max(non_zero_priorities, key=lambda x: chromosome[x])

    # Passo 3: Selecionar a fonte ou depósito baseado em 'l'
    if l < len(K):  # l é um índice de fonte
        k_star = K[l]
        # Encontrar depósito com o menor custo que ainda não foi esgotado
        j_star = min((j for j in range(len(J)) if chromosome[len(K) + j] != 0),
                     key=lambda j: c[k_star][j])
    else:  # l é um índice de depósito
        j_star = J[l - len(K)]
        # Encontrar fonte com o menor custo que ainda não foi esgotado
        k_star = min((k for k in range(len(K)) if chromosome[k] != 0),
                     key=lambda k: c[k][j_star])
    
    # Passo 4: Atribuir a quantidade disponível mínima da fonte para o depósito
    g = min(a[k_star], b[j_star])
    # Atualizar as disponibilidades na fonte e no depósito
    a[k_star] -= g
    b[j_star] -= g

    # Invalidar a fonte ou depósito esgotado no cromossomo
    if a[k_star] == 0:
        chromosome[k_star] = 0
    if b[j_star] == 0:
        chromosome[len(K) + j_star] = 0

    return g, k_star, j_star

def transport_allocation(K, J, b, a, c, chromosome):
    # Lista para manter a quantidade transportada de cada fonte para cada depósito
    shipments = [[0 for _ in J] for _ in K]
    
    # Continuar decodificando o cromossomo até que todas as prioridades sejam zero
    while any(v != 0 for v in chromosome):
        # Obter a quantidade transportada e os índices no passo atual
        g, k_star, j_star = decode_step(K, J, b, a, c, chromosome)
        
        # Se não puder ser feito nenhum transporte, interromper o loop
        if g is None:
            brea
        
        # Registrar o transporte na matriz de transportes
        shipments[k_star][j_star] += g

    return shipments

def print_shipment_info(k_star, j_star, g, chromosome, a, b):
    print(f"Da fonte {k_star} para o depósito {j_star}, a quantidade enviada foi {g}.")
    print("Cromossomo atualizado:", chromosome)
    print("Capacidades das fontes atualizadas (a):", a)
    print("Demandas dos depósitos atualizadas (b):", b)
    print("-----------------------------------------------------------")

# Chamar a função principal e imprimir após cada alocação
def main(K, J, b, a, c, chromosome):
    # Continuar decodificando o cromossomo até que todas as prioridades sejam zero
    while any(v != 0 for v in chromosome):
        g, k_star, j_star = decode_step(K, J, b, a, c, chromosome)
        
        if g is None:
            print("Todas as demandas foram atendidas ou as fontes esgotadas.")
            brea

        print_shipment_info(k_star, j_star, g, chromosome, a, b)

main(K, J, b, a, c, chromosome)
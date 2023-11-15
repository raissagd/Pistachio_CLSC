sources = [0, 1, 2] # Índices das fontes
depots = [0, 1, 2, 3] # Índices dos depósitos
ak = [550, 300, 450] # Capacidade de cada fonte
bj = [300, 350, 300, 350] # Demanda de cada depósito
ckj = [[11, 19, 17, 18], [16, 14, 18, 15], [15, 16, 19, 13]] # Matriz de custo de transporte da fonte para o depósito
chromosome = [2, 5, 3, 7, 4, 1, 6] # Cromossomo representando as prioridades

def decode_step(sources, depots, bj, ak, ckj, chromosome):
    # Passo 1: Inicializar gkj com zero
    gkj = 0
    
    # Passo 2: Encontrar o índice 'l' com a maior prioridade no cromossomo que não seja zero.
    non_zero_priorities = [i for i, v in enumerate(chromosome) if v != 0]
    if not non_zero_priorities:
        # Se todas as prioridades forem zero, o algoritmo deve terminar.
        return None, None, None
    
    l = max(non_zero_priorities, key=lambda x: chromosome[x])

    # Passo 3: Selecionar a fonte ou depósito baseado em 'l'
    if l < len(sources):  # l é um índice de fonte
        k_star = sources[l]
        # Encontrar depósito com o menor custo que ainda não foi esgotado
        j_star = min((j for j in range(len(depots)) if chromosome[len(sources) + j] != 0),
                     key=lambda j: ckj[k_star][j])
    else:  # l é um índice de depósito
        j_star = depots[l - len(sources)]
        # Encontrar fonte com o menor custo que ainda não foi esgotado
        k_star = min((k for k in range(len(sources)) if chromosome[k] != 0),
                     key=lambda k: ckj[k][j_star])
    
    # Passo 4: Atribuir a quantidade disponível mínima da fonte para o depósito
    gkj = min(ak[k_star], bj[j_star])
    # Atualizar as disponibilidades na fonte e no depósito
    ak[k_star] -= gkj
    bj[j_star] -= gkj

    # Invalidar a fonte ou depósito esgotado no cromossomo
    if ak[k_star] == 0:
        chromosome[k_star] = 0
    if bj[j_star] == 0:
        chromosome[len(sources) + j_star] = 0

    return gkj, k_star, j_star

def print_shipment_info(k_star, j_star, gkj, chromosome, ak, bj):
    print(f"Da fonte {k_star} para o depósito {j_star}, a quantidade enviada foi {gkj}.")
    print("Cromossomo atualizado:", chromosome)
    print("Capacidades das fontes atualizadas (ak):", ak)
    print("Demandas dos depósitos atualizadas (bj):", bj)
    print("-----------------------------------------------------------")

# Chamar a função principal e imprimir após cada alocação
def main(sources, depots, bj, ak, ckj, chromosome):
    # Continuar decodificando o cromossomo até que todas as prioridades sejam zero
    while any(v != 0 for v in chromosome):
        gkj, k_star, j_star = decode_step(sources, depots, bj, ak, ckj, chromosome)
        
        if gkj is None:
            print("Todas as demandas foram atendidas ou as fontes esgotadas.")
            break

        print_shipment_info(k_star, j_star, gkj, chromosome, ak, bj)

main(sources, depots, bj, ak, ckj, chromosome)
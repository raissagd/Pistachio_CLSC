#!/usr/bin/env python3
"""
Teste do operador InactiveActiveSwap
"""

import sys
import os
import numpy as np

# Simulando um exemplo simples
class MockSolution:
    def __init__(self):
        # Simular cromossomos S1-S8 com prioridades
        self.S1 = np.array([5, 2, 8, 1, 6, 3, 7, 4])  # 8 nós: 4 fontes + 4 depósitos
        self.S2 = np.array([3, 1, 4, 2, 5, 6])        # 6 nós: 3 fontes + 3 depósitos
        self.S3 = np.array([2, 4, 1, 3, 5])           # 5 nós: 2 fontes + 3 depósitos
        self.S4 = np.array([1, 3, 2, 4])              # 4 nós: 2 fontes + 2 depósitos
        self.S5 = np.array([2, 1, 3, 4])              # 4 nós: 2 fontes + 2 depósitos
        self.S6 = np.array([1, 2, 3, 4, 5])           # 5 nós: 3 fontes + 2 depósitos
        self.S7 = np.array([3, 1, 2, 4])              # 4 nós: 2 fontes + 2 depósitos
        self.S8 = np.array([1, 2, 3, 4])              # 4 nós: 2 fontes + 2 depósitos
        
        # Simular nós ativos/inativos correspondentes
        # 1 = ativo, 0 = inativo
        self.A1 = np.array([1, 0, 1, 1, 0, 1, 0, 1])  # 5 ativos, 3 inativos
        self.A2 = np.array([1, 1, 0, 0, 1, 0])        # 3 ativos, 3 inativos  
        self.A3 = np.array([0, 1, 1, 0, 1])           # 3 ativos, 2 inativos
        self.A4 = np.array([1, 0, 1, 0])              # 2 ativos, 2 inativos
        self.A5 = np.array([0, 1, 0, 1])              # 2 ativos, 2 inativos
        self.A6 = np.array([1, 0, 1, 1, 0])           # 3 ativos, 2 inativos
        self.A7 = np.array([0, 1, 1, 0])              # 2 ativos, 2 inativos
        self.A8 = np.array([1, 0, 0, 1])              # 2 ativos, 2 inativos

class MockNeighborhood:
    """Simulação simplificada do operador InactiveActiveSwap"""
    
    def __init__(self, N=1):
        self.N = N
        
    def selectRandomChromosome(self, solution):
        chromosomes = [f"S{i}" for i in range(1, 9)]
        attr = np.random.choice(chromosomes)
        chromosome = getattr(solution, attr)
        return attr, chromosome
        
    def applyChange(self, solution):
        import copy
        solution_copy = copy.deepcopy(solution)

        for _ in range(self.N):
            # Select a random chromosome
            chromosome_attr, chromosome = self.selectRandomChromosome(solution_copy)
            
            # Get the corresponding active nodes array
            active_attr = chromosome_attr.replace('S', 'A')  # S1 -> A1, S2 -> A2, etc.
            active_nodes = getattr(solution_copy, active_attr)
            
            # Skip if active_nodes is None
            if active_nodes is None:
                continue
                
            # Find active and inactive nodes
            active_indices = np.where(active_nodes == 1)[0]
            inactive_indices = np.where(active_nodes == 0)[0]
            
            # Skip if there are no active or inactive nodes
            if len(active_indices) == 0 or len(inactive_indices) == 0:
                print(f"Skipping {chromosome_attr}: No active ({len(active_indices)}) or inactive ({len(inactive_indices)}) nodes")
                continue
            
            # Randomly select one active and one inactive node
            i = np.random.choice(active_indices)  # Active node index
            j = np.random.choice(inactive_indices)  # Inactive node index
            
            print(f"\n{chromosome_attr}:")
            print(f"  Cromossomo antes: {chromosome}")
            print(f"  Nós ativos: {active_nodes}")
            print(f"  Trocando nó ativo {i} (prioridade {chromosome[i]}) com nó inativo {j} (prioridade {chromosome[j]})")
            
            # Swap the priorities between active and inactive nodes
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
            
            print(f"  Cromossomo depois: {chromosome}")
            
            # Update the solution with the modified chromosome
            setattr(solution_copy, chromosome_attr, chromosome)

        return solution_copy

def main():
    print("=== TESTE DO OPERADOR InactiveActiveSwap ===\n")
    
    # Criar solução mock
    solution = MockSolution()
    
    # Mostrar estado inicial
    print("ESTADO INICIAL:")
    for i in range(1, 9):
        s_attr = f"S{i}"
        a_attr = f"A{i}"
        chromosome = getattr(solution, s_attr)
        active = getattr(solution, a_attr)
        active_count = np.sum(active)
        inactive_count = len(active) - active_count
        print(f"  {s_attr}: {chromosome}")
        print(f"  {a_attr}: {active} ({active_count} ativos, {inactive_count} inativos)")
        print()
    
    # Criar e aplicar operador
    operator = MockNeighborhood(N=3)  # Aplicar 3 vezes
    
    print("APLICANDO OPERADOR (3 iterações):")
    print("="*50)
    
    new_solution = operator.applyChange(solution)
    
    print("\n" + "="*50)
    print("RESULTADO FINAL:")
    for i in range(1, 9):
        s_attr = f"S{i}"
        chromosome = getattr(new_solution, s_attr)
        print(f"  {s_attr}: {chromosome}")
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    main()
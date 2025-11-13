"""
Fluxo:
1. Solução inicial → gera cromossomos S1-S8
2. Decode → transforma cromossomos em matrizes de fluxo → calcula FX1
3. Encode → transforma essas matrizes de volta em cromossomos
4. Decode novamente → transforma os novos cromossomos em matrizes → calcula FX2
5. Se FX1 == FX2: O encoding está correto!
"""

import sys
sys.path.insert(0, '../Classes/')

from Problem import loadInstance
from Solution import Solution
import numpy as np

def test_encode_decode_cycle():
    print("=" * 70)
    print("TESTE: Encode ↔ Decode Cycle")
    print("=" * 70)
    
    # 1. Carregar instância
    print("\n[1] Carregando instância data_100...")
    problem = loadInstance("data_10", quiet=True)
    print(f"    ✓ Carregado (num_var_priority = {problem.num_var_priority})")
    
    # 2. Criar solução inicial com cromossomos determinísticos
    print("\n[2] Gerando solução inicial (determinística)...")
    solution1 = Solution()
    solution1.generateChromosomeDeterministic(problem)
    print(f"    ✓ Cromossomos gerados:")
    print(f"      S1: {solution1.S1[:5]}... (tamanho {len(solution1.S1)})")
    print(f"      S2: {solution1.S2[:5]}... (tamanho {len(solution1.S2)})")
    
    # 3. Primeiro DECODE → calcula FX1
    print("\n[3] Aplicando DECODE (primeira vez)...")
    FX1 = solution1.evaluate(problem)
    print(f"    ✓ FX1 = {FX1:,.2f}")
    
    # 5. ENCODE → transforma matrizes de volta em cromossomos
    print("\n[4] Aplicando ENCODE (matrizes → cromossomos)...")
    solution1.encode(problem)
    print(f"    ✓ Novos cromossomos gerados:")
    print(f"      S1: {solution1.S1[:5]}... (tamanho {len(solution1.S1)})")
    print(f"      S2: {solution1.S2[:5]}... (tamanho {len(solution1.S2)})")
    
    # 7. Segundo DECODE → calcula FX2
    print("\n[6] Aplicando DECODE (segunda vez)...")
    FX2 = solution1.evaluate(problem)
    print(f"    ✓ FX2 = {FX2:,.2f}")
    
    # 8. RESULTADO FINAL
    print("\n" + "=" * 70)
    print("RESULTADO DO TESTE")
    print("=" * 70)
    
    print(f"\nFX1 (original):        {FX1:,.6f}")
    print(f"FX2 (após encode):     {FX2:,.6f}")
    print(f"Diferença absoluta:    {abs(FX1 - FX2):,.10f}")
    
    if abs(FX1 - FX2) < 1e-6:
        print(f"Diferença relativa:    {abs(FX1 - FX2) / FX1 * 100:.10e}%")
    
    tolerance = 1e-6
    print(f"\n{'='*70}")
    
    if abs(FX1 - FX2) < tolerance:
        print(f"✅ TESTE PASSOU!")
        print(f"   O encode está funcionando corretamente.")
        print(f"   FX1 == FX2 (diferença < {tolerance})")
    else:
        print(f"❌ TESTE FALHOU!")
        print(f"   FX1 ≠ FX2 (diferença = {abs(FX1 - FX2):.10e})")
    
    print(f"{'='*70}\n")
    
    return abs(FX1 - FX2) < tolerance

def test_encode_step():
    """
    Testa apenas o método encode_step com dados sintéticos.
    """
    print("\n" + "=" * 70)
    print("TESTE ISOLADO: encode_step")
    print("=" * 70)
    
    # Matrizes de exemplo: 3 fontes, 4 depósitos
    g = np.array([
        [300.0,   0.0, 250.0,   0.0],  # Fonte 0 envia para depósitos 0 e 2
        [  0.0, 300.0,   0.0,   0.0],  # Fonte 1 envia para depósito 1
        [  0.0,  50.0,  50.0, 350.0]   # Fonte 2 envia para depósitos 1, 2 e 3
    ])
    
    c = np.array([
        [11, 19, 17, 18],  # Custos da fonte 0
        [16, 14, 18, 15],  # Custos da fonte 1
        [15, 16, 19, 13]   # Custos da fonte 2
    ])
    
    a = np.array([550.0, 300.0, 450.0])  # Capacidades das fontes
    b = np.array([300.0, 350.0, 300.0, 350.0])  # Demandas dos depósitos
    
    print("\nMatriz de fluxo (g):")
    print(g)
    print("\nMatriz de custos (c):")
    print(c)
    print(f"\nCapacidades (a): {a}")
    print(f"Demandas (b): {b}")
    
    # Criar um objeto Solution para usar o método encode_step
    solution = Solution()
    v = solution.encode_step(g, c, a, b)
    
    print(f"\n✓ Cromossomo gerado (v): {v}")
    print(f"  Tamanho: {len(v)}")
    print(f"  Fontes (0-2): {v[0:3]}")
    print(f"  Depósitos (0-3): {v[3:7]}")

if __name__ == "__main__":
    print("\n🔬 TESTES DE VALIDAÇÃO\n")
    
    # Escolha qual teste executar:
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--encode_step-only":
        # Testa apenas o encode_step
        test_encode_step()
    else:
        # Testa o ciclo completo encode/decode
        success = test_encode_decode_cycle()
        exit(0 if success else 1)
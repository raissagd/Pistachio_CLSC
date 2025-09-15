import gurobipy as grb
import numpy as np
from Solution import Solution
from Convergence import Convergence
from abc import ABC, abstractmethod
from time import time
from Log import Neighborhood_op_log
import random
import math
import copy

class Algorithm(ABC):
    def __init__(self):
        pass

    def solve(self, data, quiet=False):
        return Solution()


class VariableNeighborhoodSearch(Algorithm):
    """
    Function VNS (x, kmax)
        1:    k ← 1
        2:    repeat
        3:       x' ← Shake(x, k)                     // Perturbation of the solution
        4:       x'' ← BestImprovement(x')           // Local search
        5:       x ← NeighbourhoodChange(x, x'', k) // If x'' is better, change the neighborhood. Repeat the process
        6:    until k = kmax
    """

    def __init__(self, operator, max_eval, initialization, name="VNS", init_temp=100, cooling_rate=0.995):
        self.operator = operator  # operator for generating neighbors
        self.max_eval = max_eval  # Maximum number of iterations
        self.n_eval = 1  # Number of evaluations
        self.initialization = initialization  # Initialization method
        self.log = None # Log for storing neighborhood operations
        self.name = name # Name of the algorithm
        self.T = init_temp
        self.cooling_rate = cooling_rate

    def best_improvement(self, solution, data, operator_index, number_of_neighbors, log):
        failure_counter = 0
        initial_FX = solution.FX

        while True:
            neighbors = []  # List to store the neighbor solutions
            Fx_neighbors = []  # List to store the fitness values of the neighbor solutions

            for _ in range(number_of_neighbors):
                # Generate a neighbor solution (apply an operator to the current solution)
                neighbor = self.operator[operator_index].applyChange(solution)
                neighbor.evaluate(data)  # Evaluate the neighbor solution
                self.n_eval += 1
                neighbors.append(neighbor)  # Store it
                Fx_neighbors.append(neighbor.FX)  # Store its fitness value

            best_neighbor_index = np.argmin(Fx_neighbors)
            best_neighbor = neighbors[best_neighbor_index] # Select the best neighbor    

            # Update the current solution if the best neighbor is better
            if Fx_neighbors[best_neighbor_index] < solution.FX:
                solution = best_neighbor
                failure_counter = 0
                success = 1
            else:
                failure_counter += 1
                success = 0
                if failure_counter == 5:  # If 5 consecutive failures occur, break the loop
                    break

            if log is not None:
                log.log(data.instance, self.name, self.operator[operator_index].name, self.n_eval, success, (initial_FX - solution.FX) / initial_FX * 100 if success else 0, solution.FX  ) # Log the neighborhood operation
        
        return solution

    def shake(self, solution, data, operator_index):
        operator = self.operator[operator_index] # Select the operator for shake
        
        # Calculate number of perturbations based on problem size
        # Total variables = sum of all chromosome segments
        total_variables = (data.K + data.N1) + (data.S + data.N3) + (data.E + data.N2 + data.S) + \
                         (data.J + data.K) + (data.J + data.E) + (data.I + data.J) + \
                         (data.Q + data.M) + (data.E + data.Q)
        
        # Number of perturbations proportional to problem size (e.g., 5-10% of total variables)
        num_perturbations = max(10, int(0.07 * total_variables))  # At least 10 perturbations

        perturbed_solution = copy.deepcopy(solution)
        
        # Apply multiple perturbations with the same operator
        for _ in range(num_perturbations):
            perturbed_solution = operator.applyChange(perturbed_solution)

        perturbed_solution.evaluate(data)  # Evaluate the perturbed solution
        self.n_eval += 1
        return perturbed_solution
    
    def accept(self, old_fx, new_fx):
        delta = new_fx - old_fx
        if delta < 0:
            # always accepts better solutions
            return True
        elif delta == 0:
            # rejects equal solutions
            return False
        else:
            # accepts worse solutions with a probability of exp(−Δ/T)
            return random.random() < math.exp(-delta / self.T)
        
    def solve(self, data, quiet=False, log=None):
        solution = super().solve(data)
        convergence = Convergence()
        tic = time()
        
        if (self.initialization == 0):
            solution.generateChromosomeDeterministic(data)
        else:
            solution.generateChromosomeStochastic(data)

        solution.evaluate(data)
        self.n_eval = 1  # Prevent early stopping in case of reusing the object
        convergence.add(solution, self.n_eval) # Add FX e numero de avaliações

        best_overall = copy.deepcopy(solution)  # Keep track of the best overall solution

        if not quiet:
            print(f"Initial FX: {solution.FX}")

        operator_index = 0
        number_of_neighbors = 15

        # Neighborhood change
        while True:
            perturbed_solution = self.shake(solution, data, operator_index)  # Shake the current solution

            new_solution = self.best_improvement(perturbed_solution, data, operator_index, number_of_neighbors, log) # Local search on the perturbed solution

            old_fx = solution.FX
            new_fx = new_solution.FX

            """ if new_solution.FX < solution.FX:
                # If the new solution is better, update the current solution and repeat the process
                solution = new_solution
                operator_index = 0
            elif self.n_eval >= self.max_eval:
                # If the maximum number of evaluations is reached,
                break
            elif operator_index == len(self.operator) - 1:
                # If all operator have been tested,
                break
            else:
                # If the new solution is not better, try the next operator
                operator_index += 1
            convergence.add(solution, self.n_eval)  """

            if self.accept(old_fx, new_fx):
                solution = new_solution
                if new_solution.FX < best_overall.FX:
                    best_overall = copy.deepcopy(new_solution)
                if new_fx < old_fx:
                    operator_index = 0
                self.T *= self.cooling_rate

            elif self.n_eval >= self.max_eval:
                break

            else:
                # Tries next operator (or ends if all operator have been tested)
                operator_index += 1
                if operator_index >= len(self.operator):
                    operator_index = 0

            if not quiet:
                print(f"Current FX: {solution.FX} | Best FX: {best_overall.FX}"
                      f" | Evaluations: {self.n_eval}")

            convergence.add(solution, self.n_eval)

        if not quiet:
            print(f"Final solution: {best_overall.FX}")
            print(f"Number of evaluations: {self.n_eval}")
        solution.execution_time = time()-tic
        solution.convergence = convergence
        
        solution.log = log
        # log_data = self.log.get()
        # log_data.to_csv(f'./tests/run_parallel/{data.instance}_{self.name}.csv', index=False)
        
        best_overall.n_eval = self.n_eval  
        best_overall.log = log
        return best_overall

class VariableNeighborhoodSearch2(Algorithm):
    """
    VNS2 - Modified Variable Neighborhood Search
    
    Nova abordagem baseada na orientação:
    1. FASE 1: Intensificação na base atual (sem perturbação) - testa todos operadores
    2. FASE 2: Perturbação + Intensificação - testa todos operadores na base perturbada  
    3. FASE 3: Comparação estratégica entre os dois mínimos locais
    4. SA para aceitar solução pior quando "pode ir mais longe"
    """

    def __init__(self, operator, max_eval, initialization, name="VNS2", init_temp=100, cooling_rate=0.995):
        self.operator = operator  # operator for generating neighbors
        self.max_eval = max_eval  # Maximum number of iterations
        self.n_eval = 1  # Number of evaluations
        self.initialization = initialization  # Initialization method
        self.log = None # Log for storing neighborhood operations
        self.name = name # Name of the algorithm
        self.T = init_temp
        self.cooling_rate = cooling_rate

    def best_improvement(self, solution, data, operator_index, 
                         number_of_neighbors, log):
        """
        Busca local que aplica best improvement usando um operador específico
        """
        initial_FX = solution.FX
        current_solution = copy.deepcopy(solution)

        neighbors = []  # List to store the neighbor solutions
        Fx_neighbors = []  # List to store the fitness values of the neighbor solutions

        for _ in range(number_of_neighbors):
            # Generate a neighbor solution (apply an operator to the current solution)
            neighbor = self.operator[operator_index].applyChange(current_solution)
            neighbor.evaluate(data)  # Evaluate the neighbor solution
            self.n_eval += 1
            neighbors.append(neighbor)  # Store it
            Fx_neighbors.append(neighbor.FX)  # Store its fitness value

        best_neighbor_index = np.argmin(Fx_neighbors)
        best_neighbor = neighbors[best_neighbor_index] # Select the best neighbor    

        # Update the current solution if the best neighbor is better
        if Fx_neighbors[best_neighbor_index] < current_solution.FX:
            success = 1
        else:
            success = 0

        if log is not None:
            log.log(data.instance, self.name,
                    self.operator[operator_index].name, 
                    self.n_eval, success, 
                    (initial_FX - best_neighbor.FX) / initial_FX * 100 if success else 0, 
                    best_neighbor.FX) # Log the neighborhood operation
        
        return best_neighbor

    def local_search(self, base_solution, data, number_of_neighbors, log):
        """
        Aplica busca local com TODOS os operadores na mesma base e retorna o melhor resultado
        """
        best_result = copy.deepcopy(base_solution)

        operator_index = 0
        while operator_index < len(self.operator) and self.n_eval < self.max_eval:

            best_neighbor = self.best_improvement(best_result, data,
                                                  operator_index,
                                                  number_of_neighbors, log)

            if best_neighbor.FX < best_result.FX:
                best_result = copy.deepcopy(best_neighbor)
                operator_index = 0  # Restart with the first operator if improvement found
            else:
                operator_index += 1
        
        return best_result

    def shake(self, solution, data, operator_index):
        """
        Perturbação da solução usando um operador específico
        """
        operator = self.operator[operator_index] # Select the operator for shake
        
        # Calculate number of perturbations based on problem size
        # Total variables = sum of all chromosome segments
        total_variables = data.num_var_priority
        
        # Number of perturbations proportional to problem size (e.g., 5-10% of total variables)
        num_perturbations = max(10, int(0.07 * total_variables))  # At least 10 perturbations

        perturbed_solution = copy.deepcopy(solution)
        
        # Apply multiple perturbations with the same operator
        for _ in range(num_perturbations):
            perturbed_solution = operator.applyChange(perturbed_solution)
        
        perturbed_solution.evaluate(data)  # Evaluate the perturbed solution
        self.n_eval += 1
        return perturbed_solution
    
    def accept_worse_solution(self, better_fx, worse_fx):
        """
        Critério de aceitação para soluções piores (Simulated Annealing)
        Usado para aceitar solução perturbada quando pode "ir mais longe"
        """
        delta = worse_fx - better_fx
        return random.random() < math.exp(-delta / self.T)

    def neighborhood_change(self, new_fx, current_fx):
        """
        Muda para o próximo operador (ou reinicia se todos já foram testados)
        """
        if new_fx <= current_fx:
            return True
        else:
            self.accept_worse_solution(current_fx, new_fx)
        
    def solve(self, data, quiet=False, log=None):
        current_solution = super().solve(data)
        tic = time()
        convergence = Convergence()  # Create a new convergence object

        if (self.initialization == 0):
            current_solution.generateChromosomeDeterministic(data)
        else:
            current_solution.generateChromosomeStochastic(data)

        current_solution.evaluate(data)
        self.n_eval = 1  # Prevent early stopping in case of reusing the object
        convergence.add(current_solution, self.n_eval) # Add FX e numero de avaliações

        best_overall = copy.deepcopy(current_solution)  # Keep track of the best overall solution

        if not quiet:
            print(f"Initial FX: {current_solution.FX}")

        number_of_neighbors = 15
        operator_index = 0

        # Loop principal do VNS2 Novo
        while self.n_eval < self.max_eval:
            
            new_solution = self.local_search(current_solution, data, 
                                             number_of_neighbors, log)
            
            if self.n_eval >= self.max_eval:
                break

            if new_solution.FX < best_overall.FX:
                best_overall = copy.deepcopy(new_solution)

            if self.neighborhood_change(new_solution.FX, current_solution.FX):
                current_solution = new_solution
                operator_index = 0
            else:
                operator_index += 1
                if operator_index >= len(self.operator):
                    operator_index = 0

            if not quiet:
                print(f"Current FX: {current_solution.FX} "
                      f"| Best FX: {best_overall.FX}"
                      f" | Evaluations: {self.n_eval}")
            
            # Atualiza temperatura
            self.T *= self.cooling_rate
            
            # Registra convergência
            convergence.add(best_overall, self.n_eval)
            
        if not quiet:
            print(f"Final solution: {best_overall.FX}")
            print(f"Number of evaluations: {self.n_eval}")
        
        best_overall.execution_time = time() - tic
        best_overall.convergence = convergence
        best_overall.log = log
        best_overall.n_eval = self.n_eval  
        
        return best_overall

class ExactAlgorithm(Algorithm):
    def __init__(self, time_limit=None):
        self.time_limit = time_limit

    def extract_solution_from_model(self, modelo, data, X, Go, Gr, Gw, O, Oc, 
                                    Ow, L, P, D, U, Y, W, R, V):
        """
        Extrai as variáveis de decisão do modelo Gurobi e cria um objeto Solution.
        """
        solution = Solution()
        
        # Extrair valores das variáveis de decisão do Gurobi
        # Variáveis de fluxo
        solution.X = np.array([[X[i, j].X for j in range(int(data.J))] for i in range(int(data.I))])
        solution.Go = np.array([[Go[j, k].X for k in range(int(data.K))] for j in range(int(data.J))])
        solution.Gr = np.array([[Gr[j, e].X for e in range(int(data.E))] for j in range(int(data.J))])
        solution.Gw = np.array([[Gw[j, q].X for q in range(int(data.Q))] for j in range(int(data.J))])
        solution.O = np.array([[O[e, n2].X for n2 in range(int(data.N2))] for e in range(int(data.E))])
        solution.Oc = np.array([[Oc[e, s].X for s in range(int(data.S))] for e in range(int(data.E))])
        solution.Ow = np.array([[Ow[e, q].X for q in range(int(data.Q))] for e in range(int(data.E))])
        solution.L = np.array([[L[s, n3].X for n3 in range(int(data.N3))] for s in range(int(data.S))])
        solution.P = np.array([[P[k, n1].X for n1 in range(int(data.N1))] for k in range(int(data.K))])
        solution.D = np.array([[D[q, m].X for m in range(int(data.M))] for q in range(int(data.Q))])
        
        # Variáveis binárias (converter para inteiros)
        solution.U = np.array([int(round(U[j].X)) for j in range(int(data.J))])
        solution.Y = np.array([int(round(Y[q].X)) for q in range(int(data.Q))])
        solution.W = np.array([int(round(W[k].X)) for k in range(int(data.K))])
        solution.R = np.array([int(round(R[e].X)) for e in range(int(data.E))])
        solution.V = np.array([int(round(V[s].X)) for s in range(int(data.S))])
        
        # Valor da função objetivo
        solution.FX = modelo.objVal
        
        # Gerar cromossomos baseados na solução ótima (para compatibilidade)
        solution.generateChromosomeDeterministic(data)
        
        # Converter para matrizes esparsas
        solution.convert2sparse()
        
        return solution

    def solve(self, data, quiet=False):
        # Configurar ambiente para suprimir mensagens de licença

        if quiet:
            env = grb.Env(empty=True)
            env.setParam('OutputFlag', 0)
            env.start()
        else:
            env = grb.Env()
            env.start()
        
        # Criação do modelo
        modelo = grb.Model(
            """Otimização de rede de cadeia de abastecimento de pistache com "
            "realimentação""",
            env=env
        )

        # Variáveis de decisão positivas: fluxos de produtos
        X = modelo.addVars(int(data.I), int(data.J),
                           vtype=grb.GRB.CONTINUOUS, name="X", lb=0.)
        Go = modelo.addVars(int(data.J), int(data.K),
                            vtype=grb.GRB.CONTINUOUS, name="Go", lb=0.)
        Gr = modelo.addVars(int(data.J), int(data.E),
                            vtype=grb.GRB.CONTINUOUS, name="Gr", lb=0.)
        Gw = modelo.addVars(int(data.J), int(data.Q),
                            vtype=grb.GRB.CONTINUOUS, name="Gw", lb=0.)
        O = modelo.addVars(int(data.E), int(data.N2),
                           vtype=grb.GRB.CONTINUOUS, name="O", lb=0.)
        Oc = modelo.addVars(int(data.E), int(data.S),
                            vtype=grb.GRB.CONTINUOUS, name="Oc", lb=0.)
        Ow = modelo.addVars(int(data.E), int(data.Q),
                            vtype=grb.GRB.CONTINUOUS, name="Ow", lb=0.)
        L = modelo.addVars(int(data.S), int(data.N3),
                           vtype=grb.GRB.CONTINUOUS, name="L", lb=0.)
        P = modelo.addVars(int(data.K), int(data.N1),
                           vtype=grb.GRB.CONTINUOUS, name="P", lb=0.)
        D = modelo.addVars(int(data.Q), int(data.M),
                           vtype=grb.GRB.CONTINUOUS, name="D", lb=0.)

        # Variáveis binárias: indicadores de ativação
        U = modelo.addVars(int(data.J), vtype=grb.GRB.BINARY, name="U")
        Y = modelo.addVars(int(data.Q), vtype=grb.GRB.BINARY, name="Y")
        W = modelo.addVars(int(data.K), vtype=grb.GRB.BINARY, name="W")
        R = modelo.addVars(int(data.E), vtype=grb.GRB.BINARY, name="R")
        V = modelo.addVars(int(data.S), vtype=grb.GRB.BINARY, name="V")

        # Custo de abertura de instalações
        z1 = (grb.quicksum(data.Fu[j] * U[j] for j in range(int(data.J)))
              + grb.quicksum(data.Fy[q] * Y[q] for q in range(int(data.Q)))
              + grb.quicksum(data.Fw[k] * W[k] for k in range(int(data.K)))
              + grb.quicksum(data.Fr[e] * R[e] for e in range(int(data.E)))
              + grb.quicksum(data.Fv[s] * V[s] for s in range(int(data.S))))

        # Custo de produção
        z2 = (grb.quicksum(data.CI[i] * X[i, j] for i in range(int(data.I)) for j in range(int(data.J)))
              + grb.quicksum(data.Cu1[j] * Go[j, k]
                             for j in range(int(data.J)) for k in range(int(data.K)))
              + grb.quicksum(data.Cu2[j] * Gr[j, e]
                             for j in range(int(data.J)) for e in range(int(data.E)))
              + grb.quicksum(data.Cy[q] * D[q, m]
                             for q in range(int(data.Q)) for m in range(int(data.M)))
              + grb.quicksum(data.Cw[k] * P[k, n1]
                             for k in range(int(data.K)) for n1 in range(int(data.N1)))
              + grb.quicksum(data.Cr[e] * O[e, n2]
                             for e in range(int(data.E)) for n2 in range(int(data.N2)))
              + grb.quicksum(data.Cr[e] * Oc[e, s]
                             for e in range(int(data.E)) for s in range(int(data.S)))
              + grb.quicksum(data.Cv[s] * L[s, n3] for s in range(int(data.S)) for n3 in range(int(data.N3))))

        # Custos de transporte
        z3 = (grb.quicksum(data.CX[i, j] * X[i, j] for i in range(int(data.I)) for j in range(int(data.J)))
              + grb.quicksum(data.CK[j, k] * Go[j, k]
                             for j in range(int(data.J)) for k in range(int(data.K)))
              + grb.quicksum(data.CE[j, e] * Gr[j, e]
                             for j in range(int(data.J)) for e in range(int(data.E)))
              + grb.quicksum(data.CJ[j, q] * Gw[j, q]
                             for j in range(int(data.J)) for q in range(int(data.Q)))
              + grb.quicksum(data.CS[e, s] * Oc[e, s]
                             for e in range(int(data.E)) for s in range(int(data.S)))
              + grb.quicksum(data.CN[e, n2] * O[e, n2]
                             for e in range(int(data.E)) for n2 in range(int(data.N2)))
              + grb.quicksum(data.CQ[e, q] * Ow[e, q]
                             for e in range(int(data.E)) for q in range(int(data.Q)))
              + grb.quicksum(data.Cl[s, n3] * L[s, n3]
                             for s in range(int(data.S)) for n3 in range(int(data.N3)))
              + grb.quicksum(data.Cp[k, n1] * P[k, n1]
                             for k in range(int(data.K)) for n1 in range(int(data.N1)))
              + grb.quicksum(data.Cd[q, m] * D[q, m] for q in range(int(data.Q)) for m in range(int(data.M))))

        # Definindo a função objetivo
        modelo.setObjective(z1 + z2 + z3, grb.GRB.MINIMIZE)

        # Restrição de capacidade
        modelo.addConstrs(
            (grb.quicksum(X[i, j] for j in range(int(data.J)))
             <= data.Cpa[i] for i in range(int(data.I))),
            name="Eq.(4)"
        )

        modelo.addConstrs(
            (grb.quicksum(X[i, j] for i in range(int(data.I)))
             <= data.Cpu[j] * U[j] for j in range(int(data.J))),
            name="Eq.(5)"
        )

        modelo.addConstrs(
            (grb.quicksum(Ow[e, q] for e in range(int(data.E))) + grb.quicksum(Gw[j, q] for j in range(int(data.J)))
             <= data.Cpy[q] * Y[q] for q in range(int(data.Q))), name="Eq.(6)"
        )

        modelo.addConstrs(
            (grb.quicksum(Go[j, k] for j in range(int(data.J)))
             <= data.Cpw[k] * W[k] for k in range(int(data.K))),
            name="Eq.(7)"
        )

        modelo.addConstrs(
            (grb.quicksum(Gr[j, e] for j in range(int(data.J)))
             <= data.Cpr[e] * R[e] for e in range(int(data.E))),
            name="Eq.(8)"
        )

        modelo.addConstrs(
            (grb.quicksum(Oc[e, s] for e in range(int(data.E)))
             <= data.Cpv[s] * V[s] for s in range(int(data.S))),
            name="Eq.(9)"
        )

        modelo.addConstrs(
            (grb.quicksum(Go[j, k] for k in range(int(data.K))) + grb.quicksum(Gr[j, e] for e in range(int(data.E))) + grb.quicksum(Gw[j, q] for q in range(int(data.Q)))
             <= grb.quicksum(X[i, j] for i in range(int(data.I))) for j in range(int(data.J))),
            name="Eq.(10)"
        )

        modelo.addConstrs(
            (grb.quicksum(Go[j, k] for k in range(int(data.K)))
             == (1 - data.beta) * data.theta[0] * grb.quicksum(X[i, j] for i in range(int(data.I))) for j in range(int(data.J))),
            name="Eq.(11)"
        )

        modelo.addConstrs(
            (grb.quicksum(Gr[j, e] for e in range(int(data.E)))
             == (1 - data.beta) * data.theta[1] * grb.quicksum(X[i, j] for i in range(int(data.I))) for j in range(int(data.J))),
            name="Eq.(12)"
        )

        modelo.addConstrs(
            (grb.quicksum(Gw[j, q] for q in range(int(data.Q)))
             == data.theta[2] * grb.quicksum(X[i, j] for i in range(int(data.I))) for j in range(int(data.J))),
            name="Eq.(13)"
        )

        modelo.addConstrs(
            (grb.quicksum(P[k, n1] for n1 in range(int(data.N1)))
             <= data.gammak * grb.quicksum(Go[j, k] for j in range(int(data.J))) for k in range(int(data.K))),
            name="Eq.(14)"
        )

        modelo.addConstrs(
            (grb.quicksum(O[e, n2] for n2 in range(int(data.N2))) + grb.quicksum(Oc[e, s] for s in range(int(data.S)))
             <= (1 - data.lamb) * grb.quicksum(Gr[j, e] for j in range(int(data.J))) for e in range(int(data.E))),
            name="Eq.(15)"
        )

        modelo.addConstrs(
            (grb.quicksum(Ow[e, q] for q in range(int(data.Q)))
             <= data.lamb * grb.quicksum(Gr[j, e] for j in range(int(data.J))) for e in range(int(data.E))),
            name="Eq.(16)"
        )

        modelo.addConstrs(
            (grb.quicksum(L[s, n3] for n3 in range(int(data.N3)))
             <= data.gammas * grb.quicksum(Oc[e, s] for e in range(int(data.E))) for s in range(int(data.S))),
            name="Eq.(17)"
        )

        modelo.addConstrs(
            (grb.quicksum(D[q, m] for m in range(int(data.M)))
             <= data.gammaq*(grb.quicksum(Gw[j, q] for j in range(int(data.J))) + grb.quicksum(Ow[e, q] for e in range(int(data.E)))) for q in range(int(data.Q))),
            name="Eq.(18)"
        )

        modelo.addConstrs(
            (grb.quicksum(P[k, n1] for k in range(int(data.K)))
             >= data.Dp[n1] for n1 in range(int(data.N1))),
            name="Eq.(19)"
        )

        modelo.addConstrs(
            (grb.quicksum(O[e, n2] for e in range(int(data.E)))
             >= data.Du[n2] for n2 in range(int(data.N2))),
            name="Eq.(20)"
        )

        modelo.addConstrs(
            (grb.quicksum(L[s, n3] for s in range(int(data.S)))
             >= data.Ds[n3] for n3 in range(int(data.N3))),
            name="Eq.(21)"
        )

        modelo.addConstrs(
            (grb.quicksum(D[q, m] for q in range(int(data.Q)))
             >= data.Dc[m] for m in range(int(data.M))),
            name="Eq.(22)"
        )

        if self.time_limit is not None:
            modelo.setParam('TimeLimit', self.time_limit)

        # Resolvendo o modelo (OutputFlag já configurado no ambiente)
        try:
            tic = time()
            modelo.optimize()
        except:
            time_limit = time() - tic
            modelo.setParam('TimeLimit', .8*time_limit)
            modelo.optimize()


        # Verificar se uma solução ótima foi encontrada
        if modelo.status == grb.GRB.OPTIMAL:
            # Extrair solução do modelo usando método auxiliar
            solution = self.extract_solution_from_model(modelo, data, X, Go, 
                                                        Gr, Gw, O, Oc, Ow, L, 
                                                        P, D, U, Y, W, R, V)
            solution.n_eval = modelo.IterCount + modelo.NodeCount  # Aproximação
            if not quiet:
                print(f"Solução ótima encontrada: FX = {solution.FX}")
            
        else:
            # Se não encontrou solução ótima, criar solução vazia
            solution = Solution()
            solution.FX = float('inf')
            
            # Informar o status
            if not quiet:
                print(f"Gurobi status: {modelo.status}")
            if modelo.status == grb.GRB.INFEASIBLE:
                if not quiet:
                    print("Modelo infeasível")
            elif modelo.status == grb.GRB.UNBOUNDED:
                if not quiet:
                    print("Modelo não limitado")
            elif modelo.status == grb.GRB.TIME_LIMIT:
                if not quiet:
                    print("Limite de tempo atingido")
                # Se chegou no limite de tempo, pode ter uma solução sub-ótima
                if modelo.solCount > 0:
                    solution = self.extract_solution_from_model(modelo, data, 
                                                                X, Go, Gr, Gw, 
                                                                O, Oc, Ow, L, 
                                                                P, D, U, Y, W,
                                                                R, V)
                    solution.n_eval = modelo.IterCount + modelo.NodeCount  # Aproximação
                    if not quiet:
                        print(f"Melhor solução encontrada no limite de tempo: FX = {solution.FX}")
            else:
                if not quiet:
                    print(f"Outro status de terminação: {modelo.status}")

        # Fechar ambiente
        env.close()
        
        return solution

class IteratedLocalSearch(Algorithm):
    def __init__(self, operator, max_eval=100000):
        self.operator = operator  # operator for generating neighbors
        self.max_eval = max_eval  # Maximum number of evaluations
        self.n_eval = 0  # Number of evaluations

    def localSearch(self, solution, data, number_of_neighbors=15):

        failure_counter = 0
        while True:

            neighbors = []
            Fx_neighbors = []

            for n in range(number_of_neighbors):
                # Generate a neighbor solution (apply an operator to the current solution)
                neighbor = self.operator.applyChange(solution)
                neighbor.evaluate(data)  # Evaluate the neighbor solution
                self.n_eval += 1
                neighbors.append(neighbor)  # Store the neighbor solution
                # Store the fitness value of the neighbor solution
                Fx_neighbors.append(neighbor.FX)

            best_neighbor_index = np.argmin(Fx_neighbors)
            best_neighbor = neighbors[best_neighbor_index]

            # Update current solution if the best neighbor is better
            if Fx_neighbors[best_neighbor_index] < solution.FX:
                solution = best_neighbor
                failure_counter = 0
            else:
                failure_counter += 1
                if failure_counter == 5:  # If 5 consecutive failures occur, break the loop
                    break

        return solution

    def shake(self, solution, data, num_shakes=10):
        for _ in range(num_shakes):
            solution = self.operator.applyChange(solution)
        solution.evaluate(data)
        self.n_eval += 1
        return solution

    def solve(self, data, quiet=False):
        """
        Algoritmo Pesquisa Local Iterativa
            s <- Gera()
            s2 <- PesquisaLocal(s)

            repita
                s <- Perturba(s2, memória)
                s3 <- PesquisaLocal(s)
                s2 <- Aceita (s2, s3, memória)
            até condição de paragem ser verdadeira
        """
        current_solution = super().solve(data)
        current_solution.generateChromosomeStochastic(data)
        current_solution.evaluate(data)
        self.n_eval = 1  # Prevent early stopping in case of reusing the object
        convergence = Convergence()
        convergence.add(current_solution, self.n_eval)

        num_shakes = max(10, int(0.07 * data.num_var_priority))  # Number of shakes proportional to problem size

        if not quiet:
            print(f"Initial FX: {current_solution.FX}")

        # Local search on the initial solution
        current_solution = self.localSearch(current_solution, data)

        while self.n_eval < self.max_eval:
            # Perturbation of previous local search solution
            new_solution = self.shake(current_solution, data, num_shakes)
            # Local search on the perturbed solution
            new_solution = self.localSearch(new_solution, data)

            if new_solution.FX < current_solution.FX:
                current_solution = new_solution

            convergence.add(current_solution, self.n_eval)

            if not quiet:
                print(f"Current FX: {current_solution.FX} "
                      f"| Evaluations: {self.n_eval}")

        if not quiet:
            print(f"Final solution: {current_solution.FX}")
        current_solution.convergence = convergence
        return current_solution

class GeneticAlgorithm(Algorithm):
    def __init__(self, population_size, crossover_rate=0.9, mutation_rate=0.1,
                 max_eval=100000, initialization=0, crossover_type="hybrid"):
        self.population_size = population_size  # Size of the population
        self.crossover_rate = crossover_rate  # Crossover rate
        self.mutation_rate = mutation_rate  # Mutation rate
        self.initialization = initialization  # Initialization method for the population
        self.max_eval = max_eval  # Maximum number of evaluations
        self.n_eval = 0  # Number of evaluations
        self.crossover_type = crossover_type  # Type of crossover: "segment", "intra_segment", or "hybrid"

    def initialize_population(self, data):
        # Initialize the population with random solutions
        population = []
        for _ in range(self.population_size):
            solution = Solution()
            if self.initialization == 0:
                # Generate chromosome deterministically
                solution.generateChromosomeDeterministic(data)
            else:
                # Generate chromosome stochastically
                solution.generateChromosomeStochastic(data)
            # Evaluate the solution
            solution.evaluate(data)
            self.n_eval += 1
            # Add the solution to the population
            population.append(solution)
        return population

    def select_parents(self, population):
        # Select two parents randomly from the population
        parent1, parent2 = np.random.choice(population, size=2, replace=False)
        return parent1, parent2

    def crossover(self, parent1, parent2):
        # Perform crossover between two parents to produce two children
        child1, child2 = Solution(), Solution()
        crossover_point = np.random.randint(1, 8)  # Crossover point

        for i in range(1, 9):
            if i <= crossover_point:
                # Assign segments from parents to children
                setattr(child1, f"S{i}", getattr(parent1, f"S{i}").copy())
                setattr(child2, f"S{i}", getattr(parent2, f"S{i}").copy())
            else:
                setattr(child1, f"S{i}", getattr(parent2, f"S{i}").copy())
                setattr(child2, f"S{i}", getattr(parent1, f"S{i}").copy())

        return child1, child2

    def crossover_intra_segment(self, parent1, parent2):
        """
        Perform intra-segment crossover: applies crossover within each segment
        instead of swapping entire segments between parents.
        """
        child1, child2 = Solution(), Solution()

        # Apply crossover within each segment S1 to S8
        for i in range(1, 9):
            segment1 = getattr(parent1, f"S{i}").copy()
            segment2 = getattr(parent2, f"S{i}").copy()
            
            # Only perform crossover if segment has more than 1 element
            if len(segment1) > 1:
                # Single point crossover within the segment
                crossover_point = np.random.randint(1, len(segment1))
                
                # Create children segments using list concatenation
                child_segment1 = np.concatenate((segment1[:crossover_point], [x for x in segment2 if x not in list(segment1[:crossover_point])]))
                child_segment2 = np.concatenate((segment2[:crossover_point], [x for x in segment1 if x not in list(segment2[:crossover_point])]))

                # Assign the crossed segments to children
                setattr(child1, f"S{i}", child_segment1)
                setattr(child2, f"S{i}", child_segment2)
            else:
                # If segment has only 1 element, just copy from parents
                setattr(child1, f"S{i}", segment1)
                setattr(child2, f"S{i}", segment2)

        return child1, child2

    def crossover_hybrid(self, parent1, parent2, intra_segment_prob=0.5):
        """
        Hybrid crossover: randomly chooses between segment-level crossover 
        and intra-segment crossover based on probability.
        
        Args:
            parent1, parent2: Parent solutions
            intra_segment_prob: Probability of using intra-segment crossover (default 0.5)
        """
        if np.random.rand() < intra_segment_prob:
            return self.crossover_intra_segment(parent1, parent2)
        else:
            return self.crossover(parent1, parent2)

    def mutate(self, solution, max_mutations=3):
        # Perform mutation on a segment of the solution's chromosome
        for _ in range(max_mutations):
            segment = np.random.randint(1, 9)  # Select a random segment
            chromosome = getattr(solution, f"S{segment}").copy()
            # Select two random positions in the segment to swap
            i, j = np.random.randint(0, len(chromosome), size=2)
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
            # Update the solution's segment with the mutated chromosome
            setattr(solution, f"S{segment}", chromosome)

    def tournament_selection(self, population):
        # Perform binary tournament selection to retain only the best individuals
        selected = []
        pairs = np.random.permutation(len(population))
        for i in range(0, len(pairs), 2):
            if population[pairs[i]].FX < population[pairs[i+1]].FX:
                selected.append(population[pairs[i]])
            else:
                selected.append(population[pairs[i+1]])
        return selected

    def solve(self, data, log=None, quiet=False):
        _ = super().solve(data)
        convergence = Convergence()  # Create a new convergence object
        # Prevent early stopping in case of reusing the object
        self.n_eval = 0

        tic = time()
        
        # Solve the problem using the genetic algorithm
        population = self.initialize_population(data)
        best_solution = min(population, key=lambda sol: sol.FX)
        convergence.add(best_solution, self.n_eval)

        if not quiet:
            print(f"Initial best FX = {best_solution.FX}")

        while self.n_eval < self.max_eval:
            new_population = []

            # Since each pair of parents generate two children, the number of pairs is half the population size
            num_pairs = self.population_size // 2

            for _ in range(num_pairs):
                if self.n_eval >= self.max_eval:
                    break

                # Select two parents from the current population randomly
                parent1, parent2 = self.select_parents(population)

                # Perform crossover based on the crossover rate and type
                if np.random.rand() < self.crossover_rate:
                    if self.crossover_type == "intra_segment":
                        child1, child2 = self.crossover_intra_segment(parent1, parent2)
                    elif self.crossover_type == "hybrid":
                        child1, child2 = self.crossover_hybrid(parent1, parent2)
                    else:  # default "segment"
                        child1, child2 = self.crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                # Perform mutation based on the mutation rate
                if np.random.rand() < self.mutation_rate:
                    self.mutate(child1)
                if np.random.rand() < self.mutation_rate:
                    self.mutate(child2)

                # Evaluate the new solutions
                child1.evaluate(data)
                child2.evaluate(data)
                self.n_eval += 2
                if self.n_eval >= self.max_eval:
                    break

                # Add the new solutions to the new population
                new_population.extend([child1, child2])

            # Update the population using tournament selection
            new_population.extend(population)
            if self.n_eval <= self.max_eval:
                population = self.tournament_selection(new_population)
                best_solution = min(population, key=lambda sol: sol.FX)
            else:
                best_solution = min(new_population, key=lambda sol: sol.FX)
            convergence.add(best_solution, self.n_eval)

            if not quiet:
                print(f"Current best FX = {best_solution.FX} "
                      f"| Evaluations: {self.n_eval}")
        
        if not quiet:
            print(f"Best FX = {best_solution.FX}")
        best_solution.execution_time = time()-tic
        best_solution.convergence = convergence
        return best_solution
    
if __name__ == "__main__":

    from Problem import loadInstance
    from Log import Neighborhood_op_log
    from Neighborhood import Swap, Reversion, Insertion, Slide, InactiveActiveSwap 

    # Example usage
    problem = loadInstance("data_10", quiet=True)

    # Test Exact Algorithm
    print("\n=== Exact Algorithm (Gurobi) ===")
    exact = ExactAlgorithm(time_limit=None)  # Sem limite de tempo
    exact_solution = exact.solve(problem)

    # Test VNS with InactiveActiveSwap
    operator = [InactiveActiveSwap(1)]
    vns = VariableNeighborhoodSearch2(operator, max_eval=1000,  # Reduced for testing
                                      initialization=1, init_temp=100,
                                      cooling_rate=0.995)
    log = Neighborhood_op_log()
    print("=== VNS with InactiveActiveSwap ===")
    best_solution_vns = vns.solve(problem, log=log)

    # Hybrid crossover
    ga_hybrid = GeneticAlgorithm(population_size=20, crossover_rate=0.9, 
                                mutation_rate=0.1, max_eval=1000, 
                                initialization=1, crossover_type="hybrid")
    print("\n=== GA with Hybrid Crossover ===")
    best_ga_hybrid = ga_hybrid.solve(problem)        
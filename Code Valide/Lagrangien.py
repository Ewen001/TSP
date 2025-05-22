import numpy as np 
from scipy.optimize import linear_sum_assignment


# Définir la matrice des distances entre 6 grandes villes françaises (en km)
matrice = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

n = matrice.shape[0]
lambdas = np.zeros((n,n))

def gen_solution_faisable(matrice, lambdas):
    
    #on génère une solution du TSP réspéctant les contraintes d'entrée et de sortie
    #unique mais on ignore la contrainte excluant les sous tours, donc la solution peut 
    #être formée d'un cycle incomplet( pour le moment )
    
    matrice_mod = matrice + lambdas             #matrice de coût impactée par les mult°
    
    np.fill_diagonal(matrice_mod, np.inf)       #on accepte pas ville i -> ville i
    
    lin, col = linear_sum_assignment(matrice_mod) #fonction de résolution du module spicy.optimize
                                                    #permet de résoudre l'affectation 
                                                        #avec un coût minimal
    #donc lin forme une liste de ville de départ, et col une liste de ville d'arrivé
    #correspondantes respectivement à lin
    
    # zip nous permet d'associer chaque i correspondant de lin a chaque i correspondant 
    # de j, on a donc une formation d'arrètes. Par soucis de complexité de traitement
    #et de compréhension de la solution on inscrit ce résultat sous forme binaire.
    sol = np.zeros((n,n))
    for i,j in zip(lin, col):
        sol[i, j] = 1
    
    return sol                             
        


def calcul_lagrangien(matrice, lambdas, sol):
    
    #on calcul la valeur du lagrangien selon la formulation mathématique indiquée 
    #dans le rapport 
    
    cout_solution = np.sum(matrice*sol)
    penalite = np.sum(lambdas*(sol-1))
    L = cout_solution + penalite
    return L


sol = gen_solution_faisable(matrice, lambdas)
lagrangien = calcul_lagrangien(matrice, lambdas, sol)

print("Solution faisable du problème relaxé:\n", sol)
print("Valeur du Lagrangien (borne inférieur du problème):\n", lagrangien)




    

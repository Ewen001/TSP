import numpy as np
from scipy.optimize import linear_sum_assignment

# Matrice des distances (en km) entre 6 grandes villes françaises
matrice = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

n = matrice.shape[0]
lambdas = np.zeros((n, n))  # Matrice des multiplicateurs de Lagrange

def gen_solution_faisable(matrice, lambdas):
    """
    Génère une solution faisable du problème relaxé (problème d’affectation).
    """
    matrice_mod = matrice + lambdas
    np.fill_diagonal(matrice_mod, np.inf)  # Interdit les boucles i → i

    lin, col = linear_sum_assignment(matrice_mod)
    sol = np.zeros((n, n))
    for i, j in zip(lin, col):
        sol[i, j] = 1

    return sol

def calcul_lagrangien(matrice, lambdas, sol):
    """
    Calcule la valeur du Lagrangien :
    L(x, λ) = ∑ (c_ij + λ_ij) * x_ij - ∑ λ_ij
    """
    lagrangien = np.sum((matrice + lambdas) * sol) - np.sum(lambdas)
    return lagrangien

# Exécution
sol = gen_solution_faisable(matrice, lambdas)
lagrangien = calcul_lagrangien(matrice, lambdas, sol)

# Affichage
print("Solution faisable du problème relaxé :\n", sol)
print("Valeur du Lagrangien (borne inférieure du problème) :\n", lagrangien)

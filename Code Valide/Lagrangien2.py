# -*- coding: utf-8 -*-
"""
Created on Thu May 22 17:40:02 2025

@author: Cytech

@filename: Lagrangien.py

adaptée (pour data structure) pour sous gradient

"""

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
lambdas = np.zeros((n, n))  # Initialisation des multiplicateurs de Lagrange à zéro


def gen_solution_faisable(matrice_mod):
    # Génère une solution faisable du TSP respectant contraintes d'entrée et sortie uniques
    # Ignore la contrainte d'exclusion des sous-tours, la solution peut contenir plusieurs cycles
    
    n = matrice_mod.shape[0]  # taille de la matrice (nombre de villes)
    
    np.fill_diagonal(matrice_mod, np.inf)  # interdit les transitions de type ville i -> i
    
    lin, col = linear_sum_assignment(matrice_mod)  # résout le problème d'affectation pour minimiser le coût total
    
    sol = np.zeros((n, n))  # initialisation matrice solution binaire
    
    for i, j in zip(lin, col):
        sol[i, j] = 1  # marque la présence d'un arc i -> j dans la solution
    
    return sol



def calcul_lagrangien(matrice, lambdas_st, sol):

    n = matrice.shape[0]
    cout_solution = np.sum(matrice * sol)  # somme des arcs sélectionnés dans la solution
    penalite = 0

    for S, lambda_S in lambdas_st.items():  # pour chaque sous-tour détecté précédemment
        S = list(S)
        arcs_dans_S = 0
        for i in S:
            for j in S:
                if i != j:  # on ne compte pas les boucles (i -> i)
                    arcs_dans_S += sol[i, j]
        g_S = arcs_dans_S - (len(S) - 1)  # mesure de violation de la contrainte de sous-tour
        penalite += lambda_S * g_S       # pénalité pondérée par le lambda associé

    L = cout_solution + penalite
    return L


# Test local 
if __name__ == "__main__":
    sol = gen_solution_faisable(matrice, lambdas)
    lagrangien = calcul_lagrangien(matrice, {}, sol)

    print("Solution faisable du problème relaxé:\n", sol)
    print("Valeur du Lagrangien (borne inférieure du problème):\n", lagrangien)

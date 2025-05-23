import numpy as np
from scipy.optimize import linear_sum_assignment  # Algorithme de résolution du problème d’affectation (méthode de Kuhn-Munkres)

# Liste des villes dans l'ordre utilisé dans la matrice
villes = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Matrice des distances symétriques entre les 6 villes (en kilomètres)
matrice = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]
])

n = len(villes)  # Nombre de villes

# Génère une solution faisable en respectant uniquement les contraintes d’entrée/sortie uniques (pas de contrainte de sous-tour)
def solution_relaxee(matrice):
    matrice_mod = matrice.copy()  # Copie de la matrice de distances
    np.fill_diagonal(matrice_mod, np.inf)  # On interdit les boucles : i → i (coût infini)
    
    # Résout le problème d'affectation minimale (entrée/sortie unique)
    row, col = linear_sum_assignment(matrice_mod)
    
    # Création de la matrice binaire xij : 1 si on va de i à j, 0 sinon
    sol = np.zeros((n, n))
    for i, j in zip(row, col):
        sol[i, j] = 1
    return sol  # Matrice binaire de la solution relaxée

# Calcule la valeur de la fonction lagrangienne pour un sous-ensemble S
def lagrangien(matrice, sol, S, lambda_S):
    # Coût total de la solution relaxée
    cout = np.sum(matrice * sol)
    
    # Nombre d’arcs dans le sous-ensemble S (i ≠ j)
    x_soustour = sum(sol[i, j] for i in S for j in S if i != j)
    
    # Pénalité appliquée si ce sous-ensemble forme un sous-tour
    penalite = lambda_S * (x_soustour - (len(S) - 1))
    
    # Valeur totale de la fonction lagrangienne
    return cout + penalite

# Exemple : on relâche une contrainte de sous-tour sur le sous-ensemble S = {Lille, Strasbourg, Lyon}
S = [1, 2, 3]       # Indices des villes concernées
lambda_S = 50       # Valeur du multiplicateur de Lagrange associé à S

# Exécution du calcul
sol = solution_relaxee(matrice)        # Génère la solution relaxée (matrice binaire)
L = lagrangien(matrice, sol, S, lambda_S)  # Calcule la valeur du lagrangien avec pénalité

# Affichage des résultats
print("Matrice binaire de la solution (x_{ij}) :")
print(sol.astype(int))  # Affiche la matrice binaire en 0 et 1 (au lieu de 0.0 et 1.0)
print(f"\nValeur du lagrangien (avec pénalité sur S) : {round(L, 2)} km")

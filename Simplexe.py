import numpy as np
from scipy.optimize import linprog

# Liste des villes
Liste_ville = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Matrice symétrique des distances (en km)
distance_matrice = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]
])

n = len(Liste_ville)

# Construction de la liste des chemins possibles (i < j)
chemin_valide = [(i, j) for i in range(n) for j in range(i + 1, n)]
m = len(chemin_valide)

# PHASE 1 : Ajout des variables artificielles pour trouver une solution faisable
A_eq = []
b_eq = []

for ville in range(n):
    ligne = []
    for (i, j) in chemin_valide:
        ligne.append(1 if ville == i or ville == j else 0)
    A_eq.append(ligne)
    b_eq.append(2)

# Étend A_eq avec des variables artificielles (une par contrainte)
A_eq_phase1 = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(A_eq)]
c_phase1 = [0] * m + [1] * n  # objectif : minimiser la somme des variables artificielles
borne_phase1 = [(0, 1)] * m + [(0, None)] * n  # bornes des x_ij et des variables artificielles

res_phase1 = linprog(c=c_phase1, A_eq=A_eq_phase1, b_eq=b_eq, bounds=borne_phase1, method="highs")

# PHASE 2 : Résolution du problème original si faisable
if res_phase1.success and res_phase1.fun < 1e-5:
    # Construire le vrai problème avec les bonnes bornes et fonction objectif
    c_phase2 = [distance_matrice[i][j] for (i, j) in chemin_valide]
    A_eq_phase2 = A_eq
    bounds_phase2 = [(0, 1)] * m

    res_phase2 = linprog(c=c_phase2, A_eq=A_eq_phase2, b_eq=b_eq, bounds=bounds_phase2, method="highs")

    if res_phase2.success:
        print("Résolution réussie avec la méthode des 2 phases.")
        print("Borne inférieure du TSP :", round(res_phase2.fun, 1), "km")
    else:
        print("Phase 2 : Échec de la résolution -", res_phase2.message)
else:
    print("Phase 1 : Aucune solution réalisable trouvée (système infaisable).")

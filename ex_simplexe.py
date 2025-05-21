import numpy as np
from scipy.optimize import linprog

# Liste des 6 grandes villes françaises
cities = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Matrice des distances entre les villes (en km), symétrique
distance_matrix = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

n = len(cities)  # Nombre de villes

# Variables x_ij pour i ≠ j (pas de boucle vers soi-même)
# On stocke tous les couples (i, j) valides
valid_arcs = [(i, j) for i in range(n) for j in range(n) if i != j]

# Fonction objectif : minimiser la somme des c_ij * x_ij
# c = vecteur des coûts associés aux arcs valides
c = [distance_matrix[i][j] for (i, j) in valid_arcs]

A_eq = []   # Matrice des contraintes
b_eq = []   # Vecteur second membre

# Chaque ville doit avoir exactement **une sortie**
for i in range(n):
    row = [1 if arc[0] == i else 0 for arc in valid_arcs]
    A_eq.append(row)
    b_eq.append(1)

# Chaque ville doit avoir exactement **une entrée**
for j in range(n):
    row = [1 if arc[1] == j else 0 for arc in valid_arcs]
    A_eq.append(row)
    b_eq.append(1)

# x_ij ∈ [0, 1] (relaxation continue, donc pas binaire)
bounds = [(0, 1) for _ in valid_arcs]

# On utilise la méthode 'highs' (plus rapide et robuste)
result = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# Affichage des résultats
if result.success:
    print("Résolution simplexe réussie (relaxation linéaire)")
    print("Borne inférieure du TSP :", round(result.fun, 1), "km")
else:
    print("Échec de la résolution :", result.message)

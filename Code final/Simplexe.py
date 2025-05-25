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

# Construction de la liste des chemins possibles (i, j) avec i < j 
chemin_valide = [(i, j) for i in range(n) for j in range(i + 1, n)]

# Construction du vecteur des coûts associés à chaque chemin valide
c = [distance_matrice[i][j] for (i, j) in chemin_valide]    # c[i] correspond au coût (distance) pour le chemin chemin_valide[i]

A_eq = []   # Matrice des contraintes
b_eq = []   # Vecteur second membre

for ville in range(n):  # Parcourt chaque ville
    ligne = []  # Initialisation d'une ville vide (correspond aux coeff de la contrainte)
    for (i, j) in chemin_valide:    # Parcourt tous les chemins non orientés
        if ville == i or ville == j:    # Vérifie s'il y a un lien entre cette ville et une autre
            ligne.append(1) # Si oui on ajoute une contrainte à 1 pour dire que cette ville est ok
        else:
            ligne.append(0) # Si non on ajoute une contrainte à 0 pour dire que cette ville n'est pas concernée
    A_eq.append(ligne)  # On ajoute cette ligne à la matrice des contraintes
    b_eq.append(2)  # On ajoute le 2nd membre (chaque ville à 2 contraintes)

# Borne de x_ij ∈ [0, 1] (relaxation continue, donc pas binaire)
borne = [(0, 1) for _ in chemin_valide]

# On utilise la méthode 'highs' (plus rapide et robuste)
res = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=borne, method="highs")

# Affichage des résultats
if res.success:
    print("Résolution simplexe réussie (relaxation linéaire)")
    print("Borne inférieure du TSP :", round(res.fun, 1), "km")
else:
    print("Échec de la résolution :", res.message)
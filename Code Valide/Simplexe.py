import numpy as np
from scipy.optimize import linprog # Fonction du module optimze de la bibliotheque scipy destinée à résoudre des problèmes de programmation linéaire

# Liste des 6 grandes villes françaises
Liste_ville  = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Matrice des distances entre les villes (en km), symétrique
distance_matrice = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

n = len(Liste_ville)  # Nombre de villes

# Construction de la liste des chemins possibles (i, j) avec i ≠ j 
chemin_valide = [(i, j) for i in range(n) for j in range(n) if i != j]

# Construction du vecteur des coûts associés à chaque chemin valide
c = [distance_matrice[i][j] for (i, j) in chemin_valide]                 # c[i] correspond au coût (distance) pour le chemin chemin_valide[i]

A_eq = []   # Matrice des contraintes
b_eq = []   # Vecteur second membre

# Contrainte 1 : chaque ville doit avoir exactement une sortie
for i in range(n):
    ligne = [1 if chemin[0] == i else 0 for chemin in chemin_valide]     # liste row qui correspond à une ligne et qui vaut 1 si le chemin part de la ville i, sinon 0
    A_eq.append(ligne)                                                   # Ajoute la ligne dans la matrice qui représente les contraintes d'égalité
    b_eq.append(1)                                                       # Ajoute 1 dans le second membre correspondant à la contrainte.

# Contrainte 2 : chaque ville doit avoir exactement une entrée
for j in range(n):
    ligne = [1 if chemin[1] == j else 0 for chemin in chemin_valide]     # liste row qui correspond à une ligne et qui vaut 1 si le chemin arrive de la ville j, sinon 0
    A_eq.append(ligne)
    b_eq.append(1)

# Borne de x_ij ∈ [0, 1] (relaxation continue, donc pas binaire)
borne = [(0, 1) for _ in chemin_valide] 

# On utilise la méthode 'highs' (plus rapide et robuste)
Resultat = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=borne, method='highs')

# Affichage des résultats
if Resultat.success:
    print("Résolution simplexe réussie (relaxation linéaire)")
    print("Borne inférieure du TSP :", round(Resultat.fun, 1), "km")
else:
    print("Échec de la résolution :", Resultat.message)

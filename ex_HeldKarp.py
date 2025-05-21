# Importation des modules nécessaires
import numpy as np                          # Pour manipuler des tableaux/matrices numériques
from itertools import permutations          # Pour générer toutes les permutations possibles

# Définition de la matrice des distances entre 6 villes françaises
# Chaque case [i][j] représente la distance (en km) entre la ville i et la ville j
# Cette matrice est symétrique (distance aller = distance retour)
distance_matrix = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

# Liste des noms des villes dans le même ordre que dans la matrice
cities = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Définition de la fonction Held-Karp
def held_karp_brute_force(cost_matrix):
    """
    Résout le problème du voyageur de commerce (TSP) pour un petit nombre de villes.
    Cette version teste toutes les permutations possibles pour trouver la tournée la moins coûteuse.

    Paramètre :
    - cost_matrix : la matrice des distances entre les villes

    Retourne :
    - best_path : l'ordre des villes qui donne le plus petit coût total
    - min_cost : la distance totale de ce chemin optimal
    """
    n = len(cost_matrix)           # Nombre de villes
    min_cost = float('inf')        # On initialise le coût minimum à l'infini
    best_path = None               # Pour stocker le meilleur chemin trouvé

    # On génère toutes les permutations possibles des villes sauf la première (ville de départ fixe)
    for perm in permutations(range(1, n)):
        path = [0] + list(perm) + [0]  # Le chemin commence et se termine à la ville 0 (Paris ici)
        cost = sum(cost_matrix[path[i], path[i+1]] for i in range(n))  # On calcule le coût du chemin
        if cost < min_cost:            # Si on trouve un chemin moins cher, on le garde
            min_cost = cost
            best_path = path

    return best_path, min_cost         # On retourne le chemin optimal et son coût

# Exécution de l’algorithme sur notre matrice de distances
best_path, total_cost = held_karp_brute_force(distance_matrix)

# On convertit les indices des villes en noms pour un affichage plus lisible
best_path_named = [cities[i] for i in best_path]

# Affichage final du résultat
print("Tournée optimale :", " → ".join(best_path_named))
print("Distance totale :", round(total_cost, 1), "km")
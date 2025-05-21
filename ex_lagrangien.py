import numpy as np
from itertools import permutations

# Liste des 6 villes françaises
city_list = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Matrice des distances entre les villes (en kilomètres)
distance_matrix = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

n = len(city_list)  # Nombre de villes

# On attribue arbitrairement une pénalité à chaque ville pour tester l’effet
lambda_vals = np.array([0.5, -0.2, 0.1, -0.3, 0.4, -0.1])  # Un lambda par ville

# Relaxation lagrangienne : fonction à minimiser

def lagrangian_relaxation(matrix, lambdas):
    """
    Calcule le coût total d’un circuit + pénalité selon le nombre de visites par ville.
    Renvoie le chemin de plus faible coût lagrangien.
    """
    best_cost = float('inf')
    best_path = None

    for perm in permutations(range(1, n)):  # on fixe Paris comme ville de départ (indice 0)
        path = [0] + list(perm) + [0]       # circuit complet
        cost = sum(matrix[path[i], path[i+1]] for i in range(n))  # distance réelle

        # Ajout d'une pénalité sur les violations (visites supplémentaires)
        penalty = sum(lambdas[i] * (path.count(i) - 1) for i in range(n))
        lagrangian_cost = cost + penalty

        if lagrangian_cost < best_cost:
            best_cost = lagrangian_cost
            best_path = path

    return best_path, best_cost

# Exécution

best_path_indices, lagrangian_value = lagrangian_relaxation(distance_matrix, lambda_vals)
best_path_named = [city_list[i] for i in best_path_indices]

# Résultat

print("Tournée choisie (relaxation lagrangienne) :", " → ".join(best_path_named))
print("Valeur de la fonction lagrangienne :", round(lagrangian_value, 1), "km")

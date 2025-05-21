import numpy as np

# Définir la matrice des distances entre 6 grandes villes françaises (en km)
distance_matrix = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

# Liste des villes dans le même ordre que dans la matrice
cities = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

def path_cost(path, matrix):
    """
    Calcule la distance totale du chemin donné.
    On additionne les distances entre chaque paire de villes consécutives.
    """
    return sum(matrix[path[i], path[i+1]] for i in range(len(path) - 1))

def two_opt(path, matrix):
    """
    Implémente l'algorithme 2-opt pour optimiser un circuit TSP.
    Inverse des segments du chemin tant que cela permet de réduire la distance totale.
    """
    best_path = path.copy()
    best_cost = path_cost(best_path, matrix)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path) - 1):
                # Inversion du segment entre i et j
                new_path = best_path[:i] + best_path[i:j+1][::-1] + best_path[j+1:]
                new_cost = path_cost(new_path, matrix)
                if new_cost < best_cost:
                    best_path = new_path
                    best_cost = new_cost
                    improved = True
    return best_path, best_cost

# Chemin initial : on suit l’ordre des villes et on revient au départ
initial_path = list(range(len(cities))) + [0]

# Exécution de l’algorithme 2-opt
best_path_indices, total_cost = two_opt(initial_path, distance_matrix)

# Traduction des indices en noms de villes
best_path_named = [cities[i] for i in best_path_indices]

# Affichage du résultat
print("Tournée trouvée :", " → ".join(best_path_named))
print("Distance totale :", round(total_cost, 1), "km")

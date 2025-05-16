import itertools
import numpy as np

def held_karp(distance_matrix):
    """
    Implémente l'algorithme Held-Karp pour résoudre le TSP de manière exacte.
    :param distance_matrix: matrice carrée des distances [n x n]
    :return: (coût minimal, chemin optimal)
    """
    n = len(distance_matrix)
    C = {}

    # Étape 1 : Initialisation pour les chemins partant de 0
    for k in range(1, n):
        C[(1 << k, k)] = (distance_matrix[0][k], [0, k])

    # Étape 2 : Remplissage récursif de la table
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = sum([1 << x for x in subset])
            for k in subset:
                prev_bits = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == k:
                        continue
                    if (prev_bits, m) in C:
                        prev_cost, prev_path = C[(prev_bits, m)]
                        cost = prev_cost + distance_matrix[m][k]
                        res.append((cost, prev_path + [k]))
                C[(bits, k)] = min(res)

    # Étape 3 : Retour à la ville de départ
    bits = (2 ** n - 1) - 1  # tous les sommets sauf 0
    res = []
    for k in range(1, n):
        if (bits, k) in C:
            cost, path = C[(bits, k)]
            res.append((cost + distance_matrix[k][0], path + [0]))
    min_cost, optimal_path = min(res)
    return min_cost, optimal_path

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple avec 4 villes (matrice symétrique)
    distance_matrix = np.array([
        [np.inf, 10, 15, 20],
        [10, np.inf, 35, 25],
        [15, 35, np.inf, 30],
        [20, 25, 30, np.inf]
    ])
    
    cost, path = held_karp(distance_matrix)
    print("Coût minimal :", cost)
    print("Chemin optimal :", path)

import numpy as np
import random
import matplotlib.pyplot as plt

def gen_tour(n):
    
    #génère une liste "indices" d'indices de villes, puis la mélange afin de randomiser la liste (tour)
    
    indices = list(range(n))
    random_indices = []
    while indices:
        i = random.randrange(len(indices))
        random_indices.append(indices.pop(i))
    return random_indices

def comp_distance(tour, matrix):
    
    #calcul la distance parcourue par le tour pris en paramètre
    
    dist = 0
    for i in range(len(tour)):
        dist += matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return dist

def swap(tour, i, k): # i < k ! 
    
    #on prend la séquence d'indices de i à k inclus, on l'inverse tout en conservant l'avant et l'après de cette séquence spécifique.
    
    prev = tour[:i]
    rev = []
    for r in range(i, k+1):
        rev.insert(0, tour[r])
    nex = tour[k+1:]
    return prev + rev + nex

def two_opt(matrix, init=None):

   # Améliore une tournée initiale ou aléatoire avec l’algorithme 2-opt.
    #L’algorithme essaie d’inverser toutes les sous-séquences possibles
    #pour réduire la distance totale jusqu’à ce qu’aucune amélioration ne soit trouvée.

    n = len(matrix)
    tour = init[:] if init else gen_tour(n)
    best_distance = comp_distance(tour, matrix)
    improvement = True

    while improvement:
        improvement = False
        new_best = tour[:]

        for i in range(1, n - 2):
            for k in range(i + 1, n):
                candidate = swap(tour, i, k)
                candidate_distance = comp_distance(candidate, matrix)

                if candidate_distance < best_distance:
                    new_best = candidate
                    best_distance = candidate_distance
                    improvement = True
                    break
            if improvement:
                break

        tour = new_best

    return tour, best_distance

def plot_tour(tour, coords):
    """Affiche graphiquement une tournée"""
    x = [coords[i][0] for i in tour + [tour[0]]]
    y = [coords[i][1] for i in tour + [tour[0]]]
    plt.plot(x, y, 'o-')
    plt.title("Tournée optimisée (2-opt)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":

    n = 10
    coords = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

    # Création de la matrice de distances aléatoire, on peut aussi implémenter un exemple statique
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                xi, yi = coords[i]
                xj, yj = coords[j]
                matrix[i][j] = np.hypot(xi - xj, yi - yj)

    tour, distance = two_opt(matrix)
    print("Tournée optimisée :", tour)
    print("Distance totale :", round(distance, 2))

    plot_tour(tour, coords)

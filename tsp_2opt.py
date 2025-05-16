import random
import numpy as np
import matplotlib.pyplot as plt

def calculate_total_distance(tour, distance_matrix):
    """Calcule la longueur totale d'un circuit donné"""
    total = 0
    for i in range(len(tour)):
        total += distance_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return total

def generate_random_tour(n):
    """Génère une tournée aléatoire de n villes"""
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def two_opt_swap(tour, i, k):
    """Effectue un échange 2-opt entre les indices i et k"""
    new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
    return new_tour

def two_opt(distance_matrix, initial_tour=None):
    """Algorithme 2-opt pour améliorer une tournée"""
    n = len(distance_matrix)
    if initial_tour is None:
        tour = generate_random_tour(n)
    else:
        tour = initial_tour[:]
    
    best_distance = calculate_total_distance(tour, distance_matrix)
    improved = True
    
    while improved:
        improved = False
        for i in range(1, n - 2):
            for k in range(i + 1, n):
                new_tour = two_opt_swap(tour, i, k)
                new_distance = calculate_total_distance(new_tour, distance_matrix)
                if new_distance < best_distance:
                    tour = new_tour
                    best_distance = new_distance
                    improved = True
                    break  # on redémarre à chaque amélioration
            if improved:
                break
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

# Exemple d'utilisation
if __name__ == "__main__":
    n = 10  # nombre de villes
    coords = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
    distance_matrix = np.zeros((n, n))
    
    # Calcul des distances euclidiennes entre les villes
    for i in range(n):
        for j in range(n):
            if i != j:
                xi, yi = coords[i]
                xj, yj = coords[j]
                distance_matrix[i][j] = np.hypot(xi - xj, yi - yj)
    
    # Exécution de l'algorithme
    tour, distance = two_opt(distance_matrix)
    print("Tournée optimisée :", tour)
    print("Distance totale :", round(distance, 2))
    
    # Affichage
    plot_tour(tour, coords)

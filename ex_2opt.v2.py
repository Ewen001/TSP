# -*- coding: utf-8 -*- ajouter preuve de complexité pour n e [5,20]
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import random
import matplotlib.pyplot as plt

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
    
    # Affiche du parcours optimisé avec représentation graphique des villes.
    
    x = [coords[i][0] for i in tour + [tour[0]]]
    y = [coords[i][1] for i in tour + [tour[0]]]
    
    plt.plot(x, y, 'o-')

    # Affichage des noms des villes a coté de chaque point
    
    for idx in range(len(tour)):
        city_index = tour[idx]
        plt.text(coords[city_index][0] + 1, coords[city_index][1] + 1, cities[city_index], fontsize=9)

    plt.title("Parcours optimal (2-opt)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


# Coordonnées fictives des villes pour l'affichage graphique (indépendantes des vraies distances mais correspondance géographique)
coords = [
    (50, 50),   # Paris
    (70, 80),   # Lille
    (90, 60),   # Strasbourg
    (60, 30),   # Lyon
    (80, 10),   # Marseille
    (40, 10)    # Toulouse
]

initial_path = list(range(len(cities))) + [0]

best_path, distance = two_opt(distance_matrix)
print("Chemin optimisé :", [cities[i] for i in best_path])
print("Distance totale :", round(distance, 2))

plot_tour(best_path, coords)



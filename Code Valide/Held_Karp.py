import itertools
import random
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np


def held_karp(dists):
    """
    Paramètres :
        dists : matrice des distances

    Retourne :
        Un tuple (coût, chemin).
        coût  : distance totale du chemin optimal
        chemin : chemin optimal à travers les villes
    """
    n = len(dists)

    # Dictionnaire avec comme clé (ensemble_de_ville_visité, ville_courante)
    # et comme valeur (coût_min, ville_précédente)
    # Les sous-ensembles sont représentés par des bits à 1.
    C = {}

    # Initialiser les coûts de transition depuis l’état initial (ville 0)
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Itérer sur les sous-ensembles de taille croissante et stocker les résultats
    # intermédiaires à la manière classique de la programmation dynamique
    for taille_ss_ens in range(2, n):
        for ss_ens in itertools.combinations(range(1, n), taille_ss_ens):
            # Mettre à 1 les bits correspondant aux villes dans ce sous-ensemble
            bits = 0
            for bit in ss_ens:
                bits |= 1 << bit

            # Trouver le plus petit coût pour atteindre ce sous-ensemble
            for k in ss_ens:
                prec = bits & ~(1 << k)  # Sous-ensemble sans le sommet k

                res = []
                for m in ss_ens:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prec, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # On considère tous les bits sauf le bit de départ (ville 0)
    bits = (2**n - 1) - 1

    # Calcul du coût optimal pour revenir à la ville de départ
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Remonter le chemin optimal (backtracking)
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Ajouter la ville de départ (implicite)
    path.append(0)

    return list(reversed(path)), opt

# On génére l'exemple avec des distances entre des villes françaises

distance_matrix = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])


# On charge les résultats de l'algorithme de Held-Karp
best_path, total_cost = held_karp(distance_matrix)

# On écrit le chemin de ville en ville avec ke nom des villes
cities = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]
best_path_named = [cities[i] for i in best_path]

# Affichage final du résultat
print("Tournée optimale :", " → ".join(best_path_named))
print("Distance totale :", round(total_cost, 1), "km")


# Dans cette section on cherche à illustrer la complexité de l'algorithme

# Cette fonction génére une matrice de distance aléatoire de taille n, symétrique
def generate_distances(n):
    dists = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dists[i][j] = dists[j][i] = random.randint(1, 99)

    return dists

# On créé notre liste des temps d'éxécution, ainsi que les tailles n que l'on souhaite testé
l_time = []
sizes = range(4, 15)

for n in sizes:
    dists = generate_distances(n)
    start = perf_counter()

    print(held_karp(dists))

    end = perf_counter()
    l_time.append(end - start) # Mesure du temps d'éxécution

    print(f"n={n}: {l_time[-1]:.4f}s")

# Afiichage graphique
plt.plot(sizes, l_time, 'o-')
plt.xlabel('Nombre de villes')
plt.ylabel('Temps (s)')
plt.title('Complexité de Held-Karp')
plt.show()
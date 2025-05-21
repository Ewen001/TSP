import numpy as np
from itertools import permutations

# Liste des villes (doit correspondre à l’ordre de la matrice)
city_list = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Matrice des distances entre les villes (symétrique, en km)
distance_matrix = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]
])

n = len(city_list)  # Nombre de villes

np.random.seed(0)  # Pour reproductibilité
lambda_vals = np.random.uniform(-1, 1, size=n)  # Initialisation aléatoire des multiplicateurs
alpha = 1.0       # Pas initial
max_iter = 50     # Nombre maximal d’itérations

# Fonction lagrangienne

def lagrangian_relaxation(matrix, lambdas):
    """
    Évalue tous les chemins possibles et renvoie celui avec le plus faible coût lagrangien :
    coût réel + pénalités en fonction des violations de visites.
    """
    best_cost = float('inf')
    best_path = None

    for perm in permutations(range(1, n)):
        path = [0] + list(perm) + [0]  # Circuit complet
        cost = sum(matrix[path[i], path[i+1]] for i in range(n))  # Coût réel

        # Pénalité pour chaque ville si elle est visitée plus d’une fois
        penalty = sum(lambdas[i] * (path.count(i) - 1) for i in range(n))
        lagrangian_cost = cost + penalty

        if lagrangian_cost < best_cost:
            best_cost = lagrangian_cost
            best_path = path

    return best_path, best_cost

# Itérations du sous-gradient

history = []  # Historique des valeurs de la fonction duale

for k in range(max_iter):
    # Résolution du problème relaxé avec les multiplicateurs actuels
    path, lag_cost = lagrangian_relaxation(distance_matrix, lambda_vals)
    history.append(lag_cost)

    # Calcul du sous-gradient : on veut que chaque ville soit visitée une seule fois
    g = np.array([path.count(i) - 1 for i in range(n)])  # 0 si respecté, ≠0 sinon

    # Norme du sous-gradient : si nulle, on arrête
    norm_g = np.linalg.norm(g)
    if norm_g == 0:
        break

    # Mise à jour des multiplicateurs : λ := λ + pas * sous-gradient
    step = alpha / (k + 1)  # Pas décroissant
    lambda_vals = lambda_vals + step * g

# Résultat final

final_path = [city_list[i] for i in path]
final_cost = round(history[-1], 1)

print("Tournée finale associée :", " → ".join(final_path))
print("Borne inférieure finale (duale) :", final_cost, "km")

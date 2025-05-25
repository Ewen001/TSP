import numpy as np
from scipy.optimize import linear_sum_assignment

# Matrice des distances (en km) entre 6 grandes villes françaises.
# Chaque case [i][j] contient la distance de la ville i à la ville j.
matrice = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

# Noms des villes correspondants aux indices de la matrice
noms_villes = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Nombre de villes (taille de la matrice)
n = matrice.shape[0]

# Initialisation de la matrice des pénalités (même taille que la matrice de distances)
# Utilisée pour "pousser" l'algorithme à éviter certains arcs lors de la détection de sous-tours
penalite_arcs = np.zeros((n, n))

def gen_solution_faisable(matrice, penalites):
    # Combine les distances avec les pénalités pour obtenir une matrice modifiée
    matrice_mod = matrice + penalites

    # On empêche les boucles triviales (rester dans la même ville) en mettant l'infini sur la diagonale
    np.fill_diagonal(matrice_mod, np.inf)

    # On applique l'algorithme pour résoudre le problème d’affectation de coût minimal
    lin, col = linear_sum_assignment(matrice_mod)

    # Création d'une matrice binaire représentant la solution (1 si l’arc est choisi)
    sol = np.zeros((n, n))
    for i, j in zip(lin, col):
        sol[i, j] = 1

    # Retourne une matrice de décision (solution)
    return sol

def detecter_sous_tours(sol):
    # Nombre de villes
    n = sol.shape[0]

    # Ensemble des indices de villes non encore visitées
    non_visites = set(range(n))

    # Liste de tous les sous-tours détectés
    sous_tours = []

    # On explore tous les cycles jusqu'à ce que toutes les villes soient visitées
    while non_visites:
        courant = non_visites.pop()  # On commence un cycle avec une ville non encore visitée
        tour = [courant]

        # Trouve la ville suivante (celle vers laquelle part le seul arc actif)
        suivant = int(np.argmax(sol[courant]))

        # On suit les arcs jusqu'à revenir au point de départ du cycle
        while suivant != tour[0]:
            if suivant in tour:
                break  # Cycle déjà rencontré (sécurité)
            tour.append(suivant)
            non_visites.discard(suivant)
            suivant = int(np.argmax(sol[suivant]))

        # On ajoute le sous-tour trouvé à la liste
        sous_tours.append(tour)

    return sous_tours

def casser_un_arc_par_sous_tour(penalites, sous_tours, bonus=1000):
    # Pour chaque sous-tour identifié
    for tour in sous_tours:
        if len(tour) == n:
            continue  # C'est une tournée complète, on ne veut pas la casser
        a = tour[0]
        b = tour[1]
        # On augmente artificiellement le coût de l'arc (a, b) pour le forcer à ne pas être repris
        penalites[a, b] += bonus
    return penalites

def calcul_distance_totale(matrice, tour):
    distance = 0
    # On additionne les distances de chaque ville à la suivante, en bouclant à la fin
    for i in range(len(tour)):
        a = tour[i]
        b = tour[(i + 1) % len(tour)]  # %len permet de revenir à la première ville
        distance += matrice[a, b]
    return distance

# Nombre maximal d'itérations pour tenter de construire une tournée complète
nb_iterations = 200

# Variable pour stocker la meilleure solution trouvée (si elle existe)
meilleure_solution = None

# Lancement des itérations
for k in range(nb_iterations):
    # Génération d'une solution faisable avec les pénalités actuelles
    sol = gen_solution_faisable(matrice, penalite_arcs)

    # Détection des cycles (sous-tours)
    sous_tours = detecter_sous_tours(sol)

    # Nombre de sous-tours identifiés
    nb_sous_tours = len(sous_tours)

    print(f"Itération {k+1}: nombre de sous-tours = {nb_sous_tours}")

    # Si on a réussi à obtenir une seule tournée couvrant toutes les villes
    if nb_sous_tours == 1:
        meilleure_solution = sol.copy()  # On garde cette solution
        print(f"\nTournée complète trouvée à l’itération {k+1}.")
        break  # Arrêt de la boucle : objectif atteint

    # Sinon, on ajoute des pénalités pour casser les sous-tours et on retente
    penalite_arcs = casser_un_arc_par_sous_tour(penalite_arcs, sous_tours)

if meilleure_solution is not None:
    # Récupération du chemin (liste d'indices de villes) à partir de la matrice finale
    tour = detecter_sous_tours(meilleure_solution)[0]

    # Traduction en noms de villes pour affichage lisible
    tour_noms = [noms_villes[i] for i in tour]

    # Affichage du parcours complet (boucle fermée)
    print("Tournée :", " → ".join(tour_noms + [tour_noms[0]]))

    # Calcul de la distance totale réelle
    distance = calcul_distance_totale(matrice, tour)
    print(f"Distance totale réelle de la tournée : {distance:.2f} km")

else:
    print("\nAucune tournée complète trouvée.")

import numpy as np
import random
import matplotlib.pyplot as plt
from time import perf_counter # TEST COMPLEXITE

# Liste des villes dans le même ordre que dans la matrice
Liste_ville = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Définir la matrice des distances entre 6 grandes villes françaises (en km)
distance_matrice = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

# Fonction qui génère une permutation aléatoire des indices de villes de 0 à n-1.
def gen_tour(n):
    indices = list(range(n))          # Crée une liste ordonnée des indices [0, 1, 2, ..., n-1]
    random.shuffle(indices)           # Algorithme standard pour mélanger une liste de manière uniforme (Fisher-Yates, O(n))
    return indices                    # Retourne la liste melangée

def gen_tour2(n):                       # Crée une liste ordonnée commencant par Paris
    indices = list(range(1, n))         # Exclut Paris
    random.shuffle(indices)             # Mélange les autres villes
    return [0] + indices                # Ajoute Paris en tête


# Fonction pour calculer la distance parcourue par le tour pris en paramètre
def distance(tour, matrice):
    dist = 0
    n = len(tour)

    for i in range(n):
        ville_depart = tour[i]                         # Initialise la première ville
        ville_arrivee = tour[(i + 1) % n]              # Gère le retour à la première ville
        dist += matrice[ville_depart][ville_arrivee]   # Accède dans la matrice à la ville de départ et à la ville d'arrivée puis calcul la distance entre elles
   
    return dist


# Inverse une sous-séquence du tour entre les indices i et k
def changement(tour, i, k):
     
    avant_changement = tour[:i]        # Avant la sous-séquence (éléments 0 à i-1)  
    changement = tour[i:k+1][::-1]     # Inverse la sous-séquence (éléments i à k)
    nouveau = tour[k+1:]               # Après la sous-séquence (éléments k+1 à fin)
   
    return avant_changement + changement + nouveau


# Optimise un tour pour le problème du voyageur de commerce en utilisant l'algorithme 2-opt
def two_opt(matrice, tour_initial=None, max_iterations = 1000):
   
    n = len(matrice)                                                           # Nombre de villes
    tour = tour_initial.copy() if tour_initial is not None else gen_tour(n)    # Copie du tour initial ou génération aléatoire
    meilleur_distance = distance(tour, matrice)                                # Distance initiale
    ameliorable = True
    iterations = 0                                                             # Compteur

    # Tant que c'est améliorable et qu'on n'a pas atteint le max d'itération
    while ameliorable and iterations < max_iterations:
        ameliorable = False
        iterations += 1   # Incrémente le compteur
       
        # Parcourt toutes les paires de villes possibles
        for i in range(1, n - 1):              # La première ville est fixé
            for k in range(i + 1, n):          # k doit être > i                        
               
                # Évite les changements inutiles entre villes qui ont la meme distance
                if k == i + 1:
                    continue
                   
                # Génère un nouveau tour candidat
                candidat = changement(tour, i, k)                  # Applique le 2-opt changement entre i et k
                distance_candidat = distance(candidat, matrice)    # On regarde s'il est meilleur
               
                # S'il est meilleur, met à jour la meilleure solution
                if distance_candidat < meilleur_distance:
                    tour = candidat
                    meilleur_distance = distance_candidat
                    ameliorable = True
                    break      # Passe à l'itération suivante immédiatement
           
            if ameliorable:    # Si amélioration trouvée, on repart du nouveau tour immédiatement
                break
               
    return tour, meilleur_distance

# Exécution
initial_tour = gen_tour2(len(Liste_ville))
meilleur_chemin, distance_totale = two_opt(distance_matrice, initial_tour)

print("Tournée optimale:", " → ".join([Liste_ville[i] for i in meilleur_chemin] + [Liste_ville[meilleur_chemin[0]]]))
print(f"Distance totale: {distance_totale:.2f} km")

# Dans cette section on cherche à illustrer la complexité de l'algorithme

# Cette fonction génére une matrice de distance aléatoire de taille n, symétrique
def generate_distances(n):
    matrice = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            matrice[i][j] = matrice[j][i] = random.randint(1, 99)

    return matrice

# On créé notre liste des temps d'éxécution, ainsi que les tailles n que l'on souhaite testé
l_time = []
sizes = range(4, 15)

for n in sizes:
    matrice = generate_distances(n)
    start = perf_counter()

    print(two_opt(matrice))

    end = perf_counter()
    l_time.append(end - start) # Mesure du temps d'éxécution

    print(f"n={n}: {l_time[-1]:.4f}s")

# Afiichage graphique
plt.plot(sizes, l_time, 'o-')
plt.xlabel('Nombre de villes')
plt.ylabel('Temps (s)')
plt.title('Complexité de 2opt')
plt.show()
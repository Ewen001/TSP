import numpy as np
import matplotlib.pyplot as plt
from math import factorial
from itertools import permutations           # Pour générer toutes les permutations possibles

Liste_ville = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

distance_matrice = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]
])


# Algorithme Held-Karp
def Held_Karp(matrice_des_couts):
    n = len(matrice_des_couts)           # Nombre de villes
    Couts_min = float('inf')             # On initialise le coût minimum à l'infini
    Meilleur_chemin = None               # Pour stocker le meilleur chemin trouvé

    # On génère toutes les permutations possibles des villes sauf la première (ville de départ fixe)
    for perm in permutations(range(1, n)):
        chemin = [0] + list(perm) + [0]                                            # Le chemin commence et se termine à la ville 0 (Paris ici)
        Cout = sum(matrice_des_couts[chemin[i], chemin[i+1]] for i in range(n))    # On calcule le coût du chemin
        if Cout < Couts_min:                                                       # Si on trouve un chemin moins cher, on le garde
            Couts_min = Cout
            Meilleur_chemin = chemin
            
    return Meilleur_chemin, Couts_min         # On retourne le chemin optimal et son coût                   

# Exécution de l’algorithme sur notre matrice exemple
Meilleur_chemin, Cout_total = Held_Karp(distance_matrice)

 On convertit les indices des villes en noms pour l'affichage
Nouv_Meilleur_chemin = [Liste_ville[i] for i in Meilleur_chemin]

print("Tournée optimale :", " → ".join(Nouv_Meilleur_chemin))
print("Distance totale :", round(Cout_total, 1), "km")


# Graphique de complexité
n_values = np.arange(2, 12)  # Nombre de villes de 2 à 11

Complexite_Herld_Karp = [n**2 * 2**n for n in n_values]  
Complexite_factoriel = [factorial(n) for n in n_values]  

plt.figure(figsize=(10, 6))
plt.plot(n_values, Complexite_Herld_Karp, label="Held-Karp (O(n²·2ⁿ))", marker='o', color='blue')
plt.plot(n_values, Complexite_factoriel, label=" Factoriel (O(n!))", marker='s', color='red')
plt.yscale('log')  # Échelle logarithmique pour mieux visualiser
plt.xlabel("Nombre de villes (n)")
plt.ylabel("Complexité (opérations)")
plt.title("Comparaison de la complexité algorithmique")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

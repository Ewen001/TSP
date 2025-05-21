import numpy as np
from itertools import permutations # Fonction de itertools qui permet de générer toutes les permutations possibles 
from time import perf_counter
import random

# Liste des villes de notre exemple 
Liste_ville = ["Paris", "Lille", "Strasbourg", "Lyon", "Marseille", "Toulouse"]

# Matrice des distances entre les villes (symétrique, en km)
matrice_distances = np.array([
    [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
    [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
    [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
    [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
    [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
    [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
])

n = len(Liste_ville)  # Nombre de villes

np.random.seed(0)                                 # Permet de fixer la même séquence de nombres aléatoires pour chaque essais
Val_Lambda = np.random.uniform(-1, 1, size=n)     # Initialisation aléatoire des multiplicateurs entre -1 et 1 
taille_pas = 1.0                                  # Pas initial pour améliorer petit à petit les multiplicateurs
max_Iteration = 50 

# Fonction de relaxation lagrangienne
def RelaxationLagrangien(matrice_distances, multiplicateurs):
    meilleur_cout = float('inf')
    meilleur_chemin = None

    # On parcourt toutes les permutations possible parmis les 6 villes
    for perm in permutations(range(1, n)):
        chemin = [0] + list(perm) + [0]                                            # On part de la ville 0, on visite les villes dans l'ordre donné par perm, en revenant à la ville 0
        cout = sum(matrice_distances[chemin[i], chemin[i+1]] for i in range(n))    # Coût réel du trajet

        # Pénalité liée aux violations de la contrainte "visiter une ville une seule fois"
        penalite = sum(multiplicateurs[i] * (chemin.count(i) - 1) for i in range(n))    # Somme du multiplicateur de Lagrange multiplié par le nombre de foix que la ville i a été visité en trop
        cout_lagrangien = cout + penalite                                               # Coût réel 

        if cout_lagrangien < meilleur_cout: # On prend la meilleur solution 
            meilleur_cout = cout_lagrangien
            meilleur_chemin = chemin

    return meilleur_chemin, meilleur_cout


# Méthode du sous-gradient itérative
historique = []  # Pour stocker l'évolution de la fonction duale

# Boucle qui sauvegarde le meillieur chemin courant et son cout dans l'historique, se répète 50 fois
for iteration_Actuelle in range(max_Iteration):
    chemin_courant, cout_lagrangien = RelaxationLagrangien(matrice_distances, Val_Lambda)
    historique.append(cout_lagrangien)

    # On place les valeurs du sous-gradient dans une matrice : on veut que chaque ville soit visitée exactement une fois
    sous_gradient = np.array([chemin_courant.count(i) - 1 for i in range(n)])  
    
    # Norme du vecteur sous_gradient qui mesure à quel point les contraintes sont violées.
    norme_sg = np.linalg.norm(sous_gradient) # Si 0, la solution est faisable, on peut arrêter
    if norme_sg == 0:
        break

    # Mise à jour des multiplicateurs de Lagrange 
    pas = taille_pas / (iteration_Actuelle + 1)              # Pas décroissant avec le nombre d'itérationspour précision
    Val_Lambda = Val_Lambda + pas * sous_gradient            # Nouveau lambda, on avance dans la direction du sous gradient multplié par la taille du pas

# Affichage du résultat final
chemin_final = [Liste_ville[i] for i in chemin_courant]
cout_final = round(historique[-1], 1)

print("Tournée finale associée :", " → ".join(chemin_final))
print("Borne inférieure finale (duale) :", cout_final, "km")

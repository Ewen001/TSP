# -*- coding: utf-8 -*-
"""
Created on Thu May 22 17:40:02 2025

@author: Cytech

@filename: Sous_gradient.py

@desc: on reprend les résultats du problème relaxé (simplifié) et on maj les lambdas

"""

import numpy as np
from Lagrangien2 import gen_solution_faisable, calcul_lagrangien



def detecter_sous_tours(sol):
    
    #on a la matrice n*n sol recuperée depuis Lagrangien.py
    # cette solution est une solution au TSP relaxée, donc elle peut toujours contenir des sous tours
    #Cette fonction va detecter et extraire ces sous tours
    
    n = sol.shape[0] 
    ind_non_visite = set(range(n))#on crée un set (liste) de toutes les villes qui n'ont pas encore été visitées
    sous_tours = [] #set pour stocker les sous tours
    
    while ind_non_visite: #on cherche les villes non visitées, donc tant qu'il en reste on continue la recherche
        act = ind_non_visite.pop() #on suppr la ville non visité de la liste d'indices, et on la prend comme ville actuelle
        tour = [act] # car ici, on commence une nouvelle tournée en débutant par cette ville actuelle
        next = np.where(sol[act] == 1)[0][0]
        while next !=tour[0]: #tant qu'on ne reboucle pas a la ville de départ on a pas un cycle complet
            tour.append(next) #on avance a la meme ville qu'on ajoute au cycle
            ind_non_visite.remove(next)# on la retire des villes non visitées par conséquent
            next = np.where(sol[next] == 1)[0][0]#on avance, on cherche la prochaine ville du cycle
        sous_tours.append(tour) #une fois qu'on reviens a la ville de départ, et on peut ajouter ce cycle au set des sous tours
    return sous_tours

def maj_lambdas(lambdas_st, sous_tours, sol, tx):
    for T in sous_tours: #on itère a travers tout les sous tours 
        T_trie = tuple(sorted(T)) #on formalise les sous tours afin d'éviter les doublons, et on les places dans une liste immuable
        arcs_dans_T = 0 #(|-> pour pouvoir lutiliser en clef (necessite dimmuabilité) du dictionnaire lambdas_st)
        for i in T: # de cette ligne à ".. += sol[i,j], on compte le nombre d'arcs vaides dans notre sous tours
            for j in T:     #par respect de la formulation mathématique, cela signfie pour tout i différent de j, sol[i, j] = 1
                if(i != j):     #la matrice sol étant binaire on ++ le compteur via sa valeur
                    arcs_dans_T += sol[i,j]
        g_T = arcs_dans_T -(len(T) -1) # g_T = 0 => le cycle est complet, si diff° de 0 alors on souhaite pénaliser ce sous tour
        anc_lambda = lambdas_st.get(T_trie, 0) # on récup la valeur du lambda précédant cet pénalisation, ou 0 si on est à l'initialisation (la matrice des mult ° Lagrangiens est alors nulle)
        lambdas_st[T_trie] = max(0, anc_lambda + tx*g_T) #augmentation du lambda associé au cycle actuel si on a dt° que ce cycle est un sous tour
    return lambdas_st                              #on pondère par le LR et on garde les lambdas > 0 (max(0, ...))
    
    
def matrice_modd(matrice, lambdas_st):
    matrice_mod = matrice.copy()
    for S, lambda_S in lambdas_st.items():
        for i in S:
            for j in S:
                if i != j:
                    matrice_mod[i,j] += lambda_S
    return matrice_mod


def boucle_sous_gradient(matrice, it=100, alpha_base=2.0, alpha_dec=0.95):
    n = matrice.shape[0]
    lambdas_st = dict() # on crée une collection pour stocker les multiplicateurs
    alpha = alpha_base #pariel on initialise la meilleur solution, et la borne inf° du cout
    best_cout = float('inf')
    best_sol = None

    for k in range(it): #pour chaque itération, 
        matrice_mod = matrice_modd(matrice, lambdas_st) #   maj avec les lambdas sur la matrice 
        sol = gen_solution_faisable(matrice_mod)    #solution du pb relaxé (lag°.py)
        cout = calcul_lagrangien(matrice, lambdas_st, sol) # calcul le cout du lagrangien pour sol avec les lmabdas(lag°.py)
        sous_tours = detecter_sous_tours(sol)   # |-> calculé comme cout original + penalité sous tours
                                #utilise la fct de detection des sous tours precedemment implementée
        if cout < best_cout: #stockage de la meilleur borne inférieur trouvée 
            best_cout = cout
            best_sol = sol
        
        print(f"Iteration {k+1}: cout={cout:.2f}, nb sous-tours={len(sous_tours)}, alpha={alpha:.4f}")
        
        if len(sous_tours) == 1: #len st == 1 => on est sur un seul cycle complet => pas de sous tours => solution optimale 
            print("Solution optimale (cycle unique) trouvée.")
            break
        
        lambdas_st = maj_lambdas(lambdas_st, sous_tours, sol, alpha) # maj des multiplicateurs via la fct implémentée précédemment
        alpha *= alpha_dec  #(on pénalise chaque sous tours via son lambda proportionellement à la violation(via le sous gradient))
    
    return best_cout, best_sol, lambdas_st

if __name__ == "__main__":
    # Exemple matrice distances
    matrice = np.array([
        [0, 203.6, 398.5, 391.7, 660.5, 588.0],     # Paris
        [203.6, 0, 409.1, 556.9, 833.8, 790.4],     # Lille
        [398.5, 409.1, 0, 382.6, 614.9, 736.4],     # Strasbourg
        [391.7, 556.9, 382.6, 0, 277.5, 360.3],     # Lyon
        [660.5, 833.8, 614.9, 277.5, 0, 319.6],     # Marseille
        [588.0, 790.4, 736.4, 360.3, 319.6, 0]      # Toulouse
        ])

    cout, sol, lambdas = boucle_sous_gradient(matrice)
    print("\nMeilleur coût trouvé :", cout)
    print("Solution finale (matrice binaire des chemins) :\n", sol)
    print("Multiplicateurs λ par sous-tour :\n", lambdas)
    

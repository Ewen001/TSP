# -*- coding: utf-8 -*-
"""
Created on Thu May 22 17:40:02 2025

@author: Cytech

@filename: Sous_gradient.py

@desc: on reprend les résultats du problème relaxé (simplifié) et on maj les lambdas

"""

import numpy as np
from Lagrangien import gen_solution_faisable, calcul_lagrangien



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
    

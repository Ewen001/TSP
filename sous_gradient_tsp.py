import numpy as np
def lagrangian_relaxation(c, lambda_val, penalty_factor=1):
    n = len(c)
    x = np.zeros((n, n))  # Matrice des variables binaires x_ij
    # Appliquer la relaxation lagrangienne
    for i in range(n):
        for j in range(i + 1, n):
            # Comparaison élément par élément
            if c[i, j] + lambda_val[i, j] > 0:
                x[i, j] = 1
            else:
                x[i, j] = 0
    # Calcul de la fonction objectif lagrangienne
    lagrangian_obj = np.sum(c * x) + penalty_factor * np.sum(lambda_val)
    return lagrangian_obj, x

def compute_subgradient(c, x, lambda_val):
#Calcul du sous-gradient pour la relaxation lagrangienne du pb du voyageur, c : Matrice des coûts, x : #Solution approximée (matrice des variables binaires), lambda_val : Multiplicateurs de Lagrange.
#Retourne le sous-gradient pour la mise à jour des multiplicateurs de Lagrange.
    n = len(c)
    subgradient = np.zeros_like(lambda_val)
    # Calcul du sous-gradient pour chaque sous-ensemble de villes
    for i in range(n):
        for j in range(i + 1, n):
            if x[i, j] == 1:  # Si l'arête est incluse dans le cycle
                subgradient[i, j] = c[i, j]  # Coefficient de la fonction objectif
            else:
                subgradient[i, j] = -c[i, j]
    return subgradient

def update_lambda(lambda_val, subgradient, step_size):
#Mise à jour des multiplicateurs de Lagrange avec la méthode du sous-gradient, Lambda_val : #Multiplicateurs de Lagrange actuels, subgradient : Sous-gradient calculé, step_size : Taille du pas pour #la mise à jour.
#Retourne les nouveaux multiplicateurs de Lagrange.
    return lambda_val + step_size * subgradient

def subgradient_method(c, x, max_iter=100, initial_lambda=0.1, step_size=0.01):
#Méthode du sous-gradient pour maximiser la relaxation lagrangienne du TSP, c : Matrice des coûts, x #: Solution approximée, max_iter : Nombre d'itérations, initial_lambda : Valeur initiale des multiplicateurs #de Lagrange, step_size : Taille du pas pour la mise à jour
#Retourne les multiplicateurs de Lagrange optimisés et la fonction objectif.
    n = len(c)
    lambda_val = np.full((n, n), initial_lambda)  # Initialisation des multiplicateurs de Lagrange
    for iter_num in range(max_iter):
        # Calcul du sous-gradient
        subgradient = compute_subgradient(c, x, lambda_val)
        # Mise à jour des multiplicateurs de Lagrange
        lambda_val = update_lambda(lambda_val, subgradient, step_size)
        # Afficher étape par étape 
        if iter_num % 10 == 0:
            print(f"Iteration {iter_num}, Lambda : {lambda_val}")
    # Calcul de la fonction objectif après mise à jour des lambda
    lagrangian_obj, _ = lagrangian_relaxation(c, lambda_val)  # Utilise la fonction de relaxation lagrangienne 
    return lambda_val, lagrangian_obj

# Exemple d'utilisation avec une matrice de coûts aléatoire
n = 5
c = np.random.rand(n, n)  # Matrice des coûts aléatoires
x = np.random.rand(n, n) > 0.5  # Solution approximée aléatoire (matrice binaire)

lambda_optimized, lagrangian_obj = subgradient_method(c, x)

print("Multiplicateurs de Lagrange optimisés :")
print(lambda_optimized)
print("Valeur de la fonction objective après optimisation :")
print(lagrangian_obj)

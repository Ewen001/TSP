import numpy as np 

# Fonction pour le problème relaxé du lagrangien
def RelaxationLagrangien(c, Val_Lambda, penalite=1):
    n = len(c)  # Nombre de villes
    x = np.zeros((n, n))  # Matrice x de taille n x n 
    
    for i in range(n): 
        for j in range(i + 1, n):  # Toutes les paires de villes
            if c[i, j] + Val_Lambda[i, j] > 0:  # Choisir l’arête si somme positive
                x[i, j] = 1 
            else:
                x[i, j] = 0
                
    lagrangien = np.sum(c * x) + penalite * np.sum(Val_Lambda)  # Fonction objectif lagrangienne
    return lagrangien, x
    

# Fonction pour calculer le sous-gradient    
def SousGradient(c, x, Val_Lambda):
    n = len(c)
    sous_gradient = np.zeros_like(Val_Lambda)  # Initialisation
    
    for i in range(n):
        for j in range(i + 1, n):
            if x[i, j] == 1:
                sous_gradient[i, j] = c[i, j]
            else:
                sous_gradient[i, j] = -c[i, j]
    return sous_gradient
    
    
# Fonction qui met à jour les multiplicateurs lambda    
def Majlambda(Val_Lambda, sous_gradient, taille_pas):
    return Val_Lambda + taille_pas * sous_gradient
    
    
def Methode_SousGradient(c, x, maxIteration=100, Val_Lambda_init=0.1, taille_pas=0.01):
    n = len(c)
    Val_Lambda = np.full((n, n), Val_Lambda_init)  # Initialisation
    
    for iterationActuelle in range(maxIteration):
        sg = SousGradient(c, x, Val_Lambda)  # Calcul sous-gradient
        Val_Lambda = Majlambda(Val_Lambda, sg, taille_pas)  # Mise à jour lambda
        
        if iterationActuelle % 10 == 0:
            print(f"Iteration {iterationActuelle}, Lambda : {Val_Lambda}")
            
    lagrangian_obj, _ = RelaxationLagrangien(c, Val_Lambda)  # Calcul fonction objectif finale
    return Val_Lambda, lagrangian_obj


# Exemple d’utilisation
n = 5
c = np.random.rand(n, n)  # Matrice des coûts aléatoires
x = np.random.rand(n, n) > 0.5  # Solution approximée binaire aléatoire

Meilleur_lambda, lagrangian = Methode_SousGradient(c, x)

print("Multiplicateurs de Lagrange optimisés :")
print(Meilleur_lambda)
print("Valeur de la fonction objective après optimisation :")
print(lagrangian)

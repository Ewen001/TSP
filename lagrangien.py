import numpy as np

def lagrangian_relaxation_best_arcs(c, lambda_val, penalty_factor=1, verbose=True):
    """
    Applique une relaxation lagrangienne améliorée au TSP.
    
    Sélectionne les n arêtes les plus prometteuses selon le score : c_ij + λ_ij.
    
    Paramètres :
    - c : matrice des coûts (n x n)
    - lambda_val : multiplicateurs de Lagrange (n x n)
    - penalty_factor : facteur de pondération (par défaut 1)
    - verbose : True pour affichage terminal
    """
    n = len(c)
    x = np.zeros((n, n))

    if verbose:
        print("=== Relaxation lagrangienne améliorée ===")
        print("Matrice des coûts c :\n", np.round(c, 2))
        print("Multiplicateurs de Lagrange λ :\n", np.round(lambda_val, 2))

    # Calcul des scores lagrangiens pour chaque arête
    scores = []
    for i in range(n):
        for j in range(n):
            if i != j:
                score = c[i, j] + penalty_factor * lambda_val[i, j]
                scores.append((i, j, score))

    # Tri des arêtes par score croissant (meilleures d'abord)
    scores.sort(key=lambda x: x[2])

    # Sélection des n arêtes avec une seule entrée/sortie par ville
    used_i = set()
    used_j = set()
    count = 0
    for i, j, _ in scores:
        if i not in used_i and j not in used_j:
            x[i, j] = 1
            used_i.add(i)
            used_j.add(j)
            count += 1
        if count == n:
            break

    # Calcul de la valeur de la fonction objectif lagrangienne
    masked_c = np.where(np.isfinite(c), c, 0)
    lagrangian_obj = np.sum(masked_c * x) + penalty_factor * np.sum(lambda_val)

    if verbose:
        print("Solution x_ij :\n", x)
        print("Valeur de la fonction objectif lagrangienne :", round(lagrangian_obj, 2))

    return lagrangian_obj, x

# === Exemple d'utilisation ===
if __name__ == "__main__":
    np.random.seed(0)
    n = 5
    c = np.random.randint(10, 100, size=(n, n)).astype(float)
    np.fill_diagonal(c, np.inf)  # interdire les boucles (i → i)
    lambda_val = np.zeros((n, n))

    lagrangian_relaxation_best_arcs(c, lambda_val, verbose=True)

import numpy as np
# Utilisation de numpy pour manipuler les matrices

def pivot(tableau, row, col):
    # Effectue un pivot sur la ligne 'row' et la colonne 'col' du tableau
    tableau[row, :] /= tableau[row, col]
    for i in range(tableau.shape[0]):
        if i != row:
            tableau[i, :] -= tableau[i, col] * tableau[row, :]

def simplex(c, A, b):
    
    # Maximise c^T x avec les contraintes  Ax <= b, x >= 0
    
    m, n = A.shape

    # Construction du tableau : contraintes + variables artificielles + second membre
    tableau = np.zeros((m + 1, n + m + 1))
    tableau[:m, :n] = A
    tableau[:m, n:n + m] = np.eye(m)
    tableau[:m, -1] = b
    tableau[-1, :n] = c  

    base = list(range(n, n + m))
    while True:
        # On cherche la variable entrante
        pivot_col = np.argmin(tableau[-1, :-1])
        if tableau[-1, pivot_col] >= 0:
            break

        # On cherche la variable sortante
        ratios = []
        for i in range(m):
            if tableau[i, pivot_col] > 0:
                ratios.append(tableau[i, -1] / tableau[i, pivot_col])
            else:
                ratios.append(np.inf)
        pivot_row = np.argmin(ratios)
        if ratios[pivot_row] == np.inf:
            raise Exception("Problème non borné")
        # Pivotage
        pivot(tableau, pivot_row, pivot_col)
        base[pivot_row] = pivot_col

    # On extrait la solution
    solution = np.zeros(n)
    for i in range(m):
        if base[i] < n:
            solution[base[i]] = tableau[i, -1]

    valeur = tableau[-1, -1]
    return solution, valeur

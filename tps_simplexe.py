import numpy as np

def pivot(tableau, row, col):
    """Effectue un pivot sur la ligne 'row' et la colonne 'col' du tableau."""
    tableau[row, :] /= tableau[row, col]
    for i in range(tableau.shape[0]):
        if i != row:
            tableau[i, :] -= tableau[i, col] * tableau[row, :]

def simplex(c, A, b):
    """
    Résout un problème linéaire de type max c^T x
    sous les contraintes : Ax <= b, x >= 0
    """
    m, n = A.shape

    # Construction du tableau : contraintes + variables artificielles + second membre
    tableau = np.zeros((m + 1, n + m + 1))
    tableau[:m, :n] = A
    tableau[:m, n:n + m] = np.eye(m)       # variables artificielles (slack)
    tableau[:m, -1] = b                    # colonne des constantes (second membre)
    tableau[-1, :n] = -c                   # fonction objectif (à maximiser)

    base = list(range(n, n + m))  # variables de base initiales (slack variables)

    iteration = 0
    while True:
        print(f"\n🔄 Itération {iteration}")
        print("Tableau actuel :")
        print(np.round(tableau, 2))

        # Recherche de la variable entrante (plus petit coef négatif de la dernière ligne)
        pivot_col = np.argmin(tableau[-1, :-1])
        if tableau[-1, pivot_col] >= 0:
            print("\n✅ Optimum atteint !")
            break

        # Recherche de la variable sortante
        ratios = []
        for i in range(m):
            if tableau[i, pivot_col] > 0:
                ratios.append(tableau[i, -1] / tableau[i, pivot_col])
            else:
                ratios.append(np.inf)
        pivot_row = np.argmin(ratios)

        if ratios[pivot_row] == np.inf:
            raise Exception("❌ Problème non borné : aucune contrainte ne limite la variable entrante.")

        print(f"➡️  Variable entrante : x{pivot_col + 1}")
        print(f"↪️  Variable sortante  : x{base[pivot_row] + 1}")

        # Mise à jour
        pivot(tableau, pivot_row, pivot_col)
        base[pivot_row] = pivot_col
        iteration += 1

    # Extraction de la solution
    solution = np.zeros(n)
    for i in range(m):
        if base[i] < n:
            solution[base[i]] = tableau[i, -1]

    valeur = tableau[-1, -1]
    print("\n📦 Solution optimale trouvée :")
    print("x =", np.round(solution, 2))
    print("Valeur optimale =", round(valeur, 2))

    return solution, valeur

# Exemple d'utilisation
if __name__ == "__main__":
    c = np.array([3, 2])  # maximise 3x1 + 2x2
    A = np.array([
        [2, 1],
        [1, 2],
        [1, -1]
    ])
    b = np.array([18, 14, 2])

    simplex(c, A, b)

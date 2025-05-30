Ce projet Python compare plusieurs méthodes d'optimisation appliquées au problème du voyageur de commerce (TSP) sur un ensemble de 6 grandes villes françaises.

Objectif : Trouver une tournée de coût minimal visitant chaque ville une seule fois et revenant au point de départ.

Méthodes implémentées :
- `HeldKarp.py` : Méthode exacte pour résoudre le TSP. Complexité exponentielle.
- `2opt.py` : Heuristique d'amélioration locale. Rapide mais non optimale.
- `Simplexe.py` : Fournit une borne inférieure en relâchant les contraintes d'intégralité.
- `Lagrangien.py` : Fournit une borne inférieure du TSP via une résolution du problème d'affectation.
- `SousGradient.py` : Approche itérative corrigeant les sous-tours pour approcher une solution admissible.

Données utilisées : Toutes les méthodes utilisent la même*matrice de distances entre : Paris, Lille, Strasbourg, Lyon, Marseille, Toulouse

Exécution en console :
```bash
python HeldKarp.py
python 2opt.py
python Simplexe.py
python Lagrangien.py
python SousGradient.py
```

Analyse de complexité : Certain script affiche également les temps d'exécution selon le nombre de villes (aléatoires), avec un graphique de performance.

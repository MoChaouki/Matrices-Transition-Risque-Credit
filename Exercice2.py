import math
import numpy as np
import matplotlib.pyplot as plt

# Partie A : Calcul des probabilités marginales de défaut
# Les probabilités marginales de défaut représentent la probabilité qu'une entreprise fasse défaut
# à une période donnée, sachant qu'elle n'a pas fait défaut avant cette période.

# Probabilités cumulatives de défaut
# Ce sont les probabilités qu'une entreprise ait fait défaut jusqu'à une certaine période.
P_cumulatives = [0.02, 0.045, 0.078, 0.112]
n = len(P_cumulatives)

# Ajouter une probabilité initiale P(0) = 0 pour simplifier les calculs des différences
P_cumulatives = [0] + P_cumulatives

# Calcul des probabilités marginales
# Probabilité marginale = différence entre deux probabilités cumulatives successives
prob_marginales = [P_cumulatives[i] - P_cumulatives[i-1] for i in range(1, n+1)]

# Afficher les probabilités marginales pour chaque année
print("Partie a : Probabilités marginales de défaut")
for t, p in enumerate(prob_marginales, 1):
    print(f"Année {t} : {p:.4f}")

# Partie B : Calcul des intensités de défaut (hazard rates)
# Les intensités de défaut (hazard rates, λ_t) mesurent la probabilité instantanée de défaut
# conditionnelle à la survie jusqu'à la période précédente.

# Probabilité de survie initiale S(0) = 1
S = [1]  # Liste pour stocker les probabilités de survie
for p in prob_marginales:
    # Probabilité de survie à la période t = probabilité de survie précédente × (1 - probabilité marginale)
    S.append(S[-1] * (1 - p))

# Calcul des intensités de défaut à partir des probabilités marginales et de survie
lambda_t = [-math.log(1 - (prob_marginales[t] / S[t])) for t in range(n)]

# Afficher les intensités de défaut pour chaque année
print("\nPartie b : Intensités de défaut (hazard rates)")
for t, l in enumerate(lambda_t, 1):
    print(f"Année {t} : {l:.4f}")

# Partie C : Construction des matrices de transition
# Les matrices de transition définissent les probabilités de passer d'un état à un autre
# pour chaque année. Ces matrices sont construites en fonction des intensités de défaut.

# Construction des matrices de transition pour chaque année
matrices_transition = []
for t, l in enumerate(lambda_t):
    # Matrice de transition pour l'année t
    # Ligne 0 : [Probabilité de survie, Probabilité de défaut]
    # Ligne 1 : [0, 1] (Défaut est un état absorbant)
    P = np.array([[1 - l, l], [0, 1]])
    matrices_transition.append(P)

# Afficher les matrices de transition pour chaque année
print("\nPartie c : Matrices de transition compatibles avec les intensités de défaut")
for t, P in enumerate(matrices_transition, 1):
    print(f"\nMatrice pour l'année {t} :\n{P}")

# Visualisation des probabilités marginales et des intensités de défaut
# Graphique pour montrer l'évolution des probabilités marginales et des intensités de défaut
plt.figure(figsize=(10, 5))

# Graphique des probabilités marginales
plt.subplot(1, 2, 1)
plt.plot(range(1, len(prob_marginales) + 1), prob_marginales, marker='o', label="Probabilités marginales")
plt.title("Probabilités marginales de défaut")
plt.xlabel("Année")
plt.ylabel("Probabilité marginale")
plt.grid(True)
plt.legend()

# Graphique des intensités de défaut (hazard rates)
plt.subplot(1, 2, 2)
plt.plot(range(1, len(lambda_t) + 1), lambda_t, marker='o', label="Intensités de défaut (hazard rates)")
plt.title("Intensités de défaut")
plt.xlabel("Année")
plt.ylabel("Intensité de défaut")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Vérification des matrices de transition
# Vérifier que la somme des probabilités dans chaque ligne des matrices de transition est proche de 1
print("\nSommes des lignes des matrices de transition (doivent être proches de 1) :")
for t, P in enumerate(matrices_transition, 1):
    print(f"Année {t} : {np.sum(P, axis=1)}")  # Afficher la somme des lignes pour chaque année

# Vérification des matrices de transition (détail ligne par ligne)
print("\nVérification des matrices de transition : Somme des lignes (doit être proche de 1)")
for t, P in enumerate(matrices_transition, 1):  # Parcourir chaque matrice de transition
    somme_lignes = np.sum(P, axis=1)  # Calculer la somme des éléments de chaque ligne
    print(f"Année {t} : Sommes des lignes = {somme_lignes}")


################## Code pour export de données a Excel #################
import pandas as pd

# Probabilités marginales
df_prob_marginales = pd.DataFrame({'Année': list(range(1, len(prob_marginales) + 1)),
                                   'Probabilités marginales': prob_marginales})
df_prob_marginales.to_csv('prob_marginales.csv', index=False)

# Intensités de défaut
df_intensites = pd.DataFrame({'Année': list(range(1, len(lambda_t) + 1)),
                              'Intensités de défaut': lambda_t})
df_intensites.to_csv('intensites.csv', index=False)

# Matrices de transition pour chaque année
for t, P in enumerate(matrices_transition, 1):
    df_matrix = pd.DataFrame(P, columns=['Investment Grade', 'Default'])
    df_matrix.to_csv(f'matrix_transition_year_{t}.csv', index=False)

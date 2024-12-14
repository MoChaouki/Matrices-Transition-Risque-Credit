import numpy as np

# 1.1 Probabilité qu’une entreprise notée BB soit en défaut dans 3 ans
# Matrice de transition : 
# Chaque ligne représente un état initial, et chaque colonne représente un état futur.
# Les valeurs dans chaque ligne indiquent les probabilités de transition entre les états.
P = np.array([
    [0.90, 0.08, 0.02, 0.00],  # De Investment Grade (0) vers les autres états
    [0.06, 0.85, 0.07, 0.02],  # De BB (1) vers les autres états
    [0.00, 0.08, 0.84, 0.08],  # De B (2) vers les autres états
    [0.00, 0.00, 0.00, 1.00]   # Défaut (3) est un état absorbant
])

# Calcul de la matrice de transition sur 3 périodes (P^3)
# Cela correspond à élever la matrice à la puissance 3 pour obtenir les probabilités cumulées de transition
# après 3 étapes (3 ans dans ce cas).
P3 = np.linalg.matrix_power(P, 3)

# Probabilité qu'une entreprise notée BB (état 1) soit en défaut (état 3) après 3 ans
prob_BB_to_D_in_3_years = P3[1, 3]  # Ligne 1, colonne 3 : Probabilité de BB → Défaut
print(f"Probabilité que BB soit en défaut dans 3 ans : {prob_BB_to_D_in_3_years:.4f}")

# 1.2 Distribution stationnaire
# La distribution stationnaire est atteinte lorsque les probabilités de transition ne changent plus.
# Cela signifie que toutes les lignes de la matrice sont identiques après un grand nombre d'itérations.

# Calcul des valeurs propres et vecteurs propres de la transposée de P
# Les vecteurs propres donnent les distributions stationnaires possibles.
valeurs_propres, vecteurs_propres = np.linalg.eig(P.T)

# Identification de la valeur propre égale à 1
# La distribution stationnaire correspond au vecteur propre associé à la valeur propre égale à 1.
index_valeur_propre_1 = np.argmax(np.isclose(valeurs_propres, 1))  # Localisation de λ=1
vecteur_stationnaire = vecteurs_propres[:, index_valeur_propre_1]  # Récupération du vecteur propre associé

# Normalisation pour que la somme des probabilités soit égale à 1
distribution_stationnaire = vecteur_stationnaire / np.sum(vecteur_stationnaire)
print("Distribution stationnaire :")
print(distribution_stationnaire.real)  # Affichage uniquement des valeurs réelles (en cas de très petites parties imaginaires dues à des arrondis)

# 1.3 Propriété de convergence (Calcul de P^20)
# Calcul de la matrice P^20 pour vérifier si la matrice converge (stabilisation des probabilités).
P20 = np.linalg.matrix_power(P, 20)

print("Matrice P^20 :")
print(P20)

# Vérification de la convergence : Si toutes les lignes de P^20 sont proches, la matrice a convergé.
# Cette vérification compare les lignes 0, 1 et 2 entre elles.
convergence_verifiee = np.allclose(P20[0], P20[1]) and np.allclose(P20[1], P20[2])
print(f"Convergence vérifiée : {convergence_verifiee}")

import numpy as np
import random

# Partie a : Annualiser la matrice de transition
# Matrice de transition trimestrielle
# P_trim est une matrice représentant les probabilités de transition entre états (Investment Grade et Default) chaque trimestre.
P_trim = np.array([[0.95, 0.05],  # Ligne 0 : Probabilités pour Investment Grade (survivre ou passer en défaut)
                   [0.10, 0.90]]) # Ligne 1 : Probabilités pour Default (restant en défaut ou revenant à un autre état)

# Annualiser en élevant la matrice trimestrielle à la puissance 4
# Cela représente les transitions cumulées sur une année (4 trimestres).
P_annuelle = np.linalg.matrix_power(P_trim, 4)

# Afficher la matrice annualisée
print("Partie a : Matrice annualisée de transition")
print(P_annuelle)

# Partie b : Simuler 1000 trajectoires sur 5 ans
n_simulations = 1000  # Nombre de trajectoires à simuler
n_periods = 20        # Nombre total de périodes (5 ans x 4 trimestres)
initial_state = 0     # Investment Grade est l'état initial (0)

# Fonction pour simuler une trajectoire
# Cette fonction simule une seule trajectoire en fonction de la matrice de transition trimestrielle P_trim.
def simulate_trajectory(P, n_periods, initial_state):
    state = initial_state  # Débuter à l'état initial
    trajectory = [state]  # Enregistrer l'état initial
    for _ in range(n_periods):  # Simuler sur chaque période
        # Transition vers le prochain état en fonction des probabilités de la matrice de transition
        state = np.random.choice([0, 1], p=P[state])  # Transition en fonction de la ligne correspondante dans P
        trajectory.append(state)  # Ajouter l'état courant à la trajectoire
    return trajectory

# Simuler 1000 trajectoires
# Chaque trajectoire est générée à partir de la fonction simulate_trajectory.
trajectories = [simulate_trajectory(P_trim, n_periods, initial_state) for _ in range(n_simulations)]

# Afficher quelques trajectoires pour vérifier
print("\nPartie b : Exemple de trajectoires simulées")
for i in range(5):  # Afficher seulement les 5 premières trajectoires
    print(f"Trajectoire {i+1} : {trajectories[i]}")

# Partie c : Estimer les probabilités de défaut à 5 ans
# Nombre de trajectoires qui se terminent dans l'état "Default" (1) après 5 ans
defauts = sum(trajectory[-1] == 1 for trajectory in trajectories)

# Probabilité de défaut estimée à 5 ans (proportion des trajectoires en défaut)
probabilite_defaut_5_ans = defauts / n_simulations

# Afficher la probabilité estimée
print("\nPartie c : Probabilité de défaut estimée à 5 ans par simulation")
print(f"Probabilité de défaut : {probabilite_defaut_5_ans:.4f}")

# Calcul de l'évolution moyenne des états
# Calculer la proportion moyenne des entreprises dans l'état Investment Grade (0) à chaque trimestre.
# np.mean(trajectories, axis=0) calcule la moyenne pour chaque période sur les trajectoires simulées.
average_states = np.mean(trajectories, axis=0)

# Visualisation de l'évolution moyenne des états
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(range(n_periods + 1), average_states, label="État moyen (Investment Grade)")
plt.title("Évolution moyenne des états simulés sur 5 ans")
plt.xlabel("Période (trimestres)")  # Chaque période correspond à un trimestre
plt.ylabel("Proportion en Investment Grade")  # Proportion moyenne dans l'état 0
plt.grid(True)  # Ajouter une grille pour plus de lisibilité
plt.legend()  # Ajouter une légende
plt.show()




################## Code pour export de données a Excel #################

import pandas as pd
# Résumé des trajectoires simulées
df_trajectories = pd.DataFrame({'Période': list(range(n_periods + 1)),
                                'Proportion moyenne Investment Grade': average_states})
df_trajectories.to_csv('trajectories.csv', index=False)

# Probabilité estimée de défaut à 5 ans
with open('prob_defaut_simule.csv', 'w') as f:
    f.write(f'Probabilité estimée de défaut à 5 ans : {probabilite_defaut_5_ans:.4f}')
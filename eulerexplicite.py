import numpy as np

def calcul_euler(C0, k, h, t_max=24):
    """
    Calcule la solution numérique par la méthode d'Euler explicite.
    C(n+1) = C(n) + h * (-k * C(n))

    Paramètres
    ----------
    C0 : concentration initiale (mg/L)
    k  : constante d'élimination (h^-1)
    h  : pas de temps (h)
    t_max : durée de simulation (h)

    Retourne
    --------
    t : array des instants
    C : array des concentrations
    """
    n_points = int(t_max / h) + 1
    t = np.zeros(n_points)
    C = np.zeros(n_points)
    C[0] = C0

    for n in range(n_points - 1):
        t[n + 1] = t[n] + h
        C[n + 1] = C[n] + h * (-k * C[n])

    return t, C
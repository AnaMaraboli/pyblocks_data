# estadistica_inferencial.py

import streamlit as st
import numpy as np
from scipy import stats
from typing import Dict
import matplotlib.pyplot as plt

# -----------------------------------
# Funciones auxiliares (tu código ya existente)
# -----------------------------------
def test_una_media(sample_mean, pop_mean, sample_std, n, alpha, side, use_z):
    se = sample_std / np.sqrt(n)
    stat = (sample_mean - pop_mean) / se
    dist = stats.norm(0, 1) if use_z else stats.t(df=n-1)

    if side == "Bilateral":
        p_value = 2 * (1 - dist.cdf(abs(stat)))
        crit = dist.ppf(1 - alpha/2)
        reject = abs(stat) > crit
    elif side == "Unilateral (mayor)":
        p_value = 1 - dist.cdf(stat)
        crit = dist.ppf(1 - alpha)
        reject = stat > crit
    else:
        p_value = dist.cdf(stat)
        crit = dist.ppf(alpha)
        reject = stat < crit

    return stat, p_value, crit, reject, dist

# -----------------------------------
# Función principal que retorna resultados
# -----------------------------------
def estadistica_inferencial() -> Dict:
    st.subheader("📊 Estadística Inferencial Completa")
    # ... resto de tu código ...
    resultados = {}
    # (Aquí va exactamente tu código que ya enviaste)
    return resultados

# -----------------------------------
# Alias para app.py
# -----------------------------------
def render():
    return estadistica_inferencial()

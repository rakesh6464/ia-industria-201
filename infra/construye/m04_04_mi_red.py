"""Constrúyelo tú (M04-04): tu propia red neuronal, vuelta a vuelta.

Lo construyes paso a paso: en cada PASO del lab te dan un bloque de código.
Pégalo debajo del comentario de ese paso, guarda y ejecuta desde infra/:

    docker compose --profile lab run --rm --no-deps --entrypoint python lab -W ignore /construye/m04_04_mi_red.py
"""
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.neural_network import MLPClassifier

# --- Decisiones tuyas (las cambiarás en los pasos finales) -------------------
NEURONAS = 64          # neuronas de la capa oculta
VUELTAS = 300          # cuántas pasadas por las fotos de entrenamiento
PARTE = 1.0            # qué parte de las fotos de entrenamiento se usa (1.0 = todas)

# --- PASO 1: las fotos en números y el corte de siempre (ya está hecho) ------
fotos = pd.read_csv("/data/imagenes/manifiesto.csv")
X = np.stack([np.asarray(Image.open(r).convert("L").resize((16, 16)), dtype=np.float32).reshape(-1) / 255.0
              for r in fotos["ruta"]])
y = fotos["defecto"].to_numpy()
buenas, malas = np.where(y == 0)[0], np.where(y == 1)[0]
k = max(1, round(28 * PARTE))                                         # fotos de cada clase para aprender
ent = np.concatenate([buenas[:k], malas[:k]])
exa = np.concatenate([buenas[28:], malas[28:]])                       # el examen del M04-01
print(f"fotos para aprender={len(ent)}  fotos de examen={len(exa)}  números por foto={X.shape[1]}")

# --- PASO 2: crear la red y darle una sola vuelta ------------------------------
# (pega aquí el bloque del paso 2)
red = MLPClassifier(hidden_layer_sizes=(NEURONAS,), random_state=0)
red.partial_fit(X[ent], y[ent], classes=[0, 1])                   # una sola pasada por las fotos

def acierto(filas):
    return (red.predict(X[filas]) == y[filas]).mean()

pesos = sum(c.size for c in red.coefs_) + sum(b.size for b in red.intercepts_)
print(f"pesos de la red: {pesos}")
print(f"tras 1 vuelta: pérdida={red.loss_:.3f}  acierto entrenamiento={acierto(ent):.2f}  examen={acierto(exa):.2f}")

# --- PASO 3: entrenar vuelta a vuelta ------------------------------------------
# (pega aquí el bloque del paso 3)
print("vuelta  pérdida  acierto_entrenamiento  acierto_examen")
for vuelta in range(2, VUELTAS + 1):
    red.partial_fit(X[ent], y[ent])                                # una pasada más
    if vuelta % (VUELTAS // 10) == 0:                              # diez filas, sean cuantas sean las vueltas
        print(f"{vuelta:6d}  {red.loss_:7.3f}  {acierto(ent):21.2f}  {acierto(exa):14.2f}")

# Reto 1: las mismas fotos de examen, con otras condiciones
def acierto_con(X_cambiadas):
    return (red.predict(X_cambiadas[exa]) == y[exa]).mean()

print(f"examen normal:            {acierto_con(X):.2f}")
print(f"con +0,15 de luz:         {acierto_con(np.clip(X + 0.15, 0, 1)):.2f}")
desplazadas = np.stack([np.roll(f.reshape(16, 16), 2, axis=1).reshape(-1) for f in X])   # carcasa 2 puntos a la derecha
print(f"carcasa movida 2 puntos:  {acierto_con(desplazadas):.2f}")

# Reto 2: lo que cuesta cada modelo
import time
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(max_iter=400).fit(X[ent], y[ent])
for nombre, m in (("regresión logística", logreg), ("red", red)):
    t = time.perf_counter()
    for _ in range(100):
        m.predict(X[exa])
    ms = (time.perf_counter() - t) / (100 * len(exa)) * 1000
    pesos_m = logreg.coef_.size + 1 if m is logreg else pesos
    print(f"{nombre:20s} acierto={(m.predict(X[exa]) == y[exa]).mean():.2f}  pesos={pesos_m:6d}  ms_por_foto={ms:.3f}")

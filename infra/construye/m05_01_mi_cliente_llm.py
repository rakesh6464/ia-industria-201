"""Constrúyelo tú (M05-01): tu propio cliente del modelo local.

Lo construyes paso a paso: en cada PASO del lab te dan un bloque de código.
Pégalo debajo del comentario de ese paso, guarda y ejecuta desde infra/:

    docker compose --profile lab run --rm --no-deps --entrypoint python lab -W ignore /construye/m05_01_mi_cliente_llm.py
"""
import time

import httpx

LLM = "http://llm:8088"        # el contenedor llm, por su nombre en la red de Docker

# --- Decisiones tuyas (las cambiarás en los pasos finales) -------------------
PREGUNTA = "¿A qué par se aprieta el tornillo de la brida de EST-01? Si no lo sabes, di: no lo sé."
LONGITUDES = (20, 80, 200)     # máximos de tokens que se prueban en el paso 4

# --- PASO 1: ¿está vivo el servicio? (ya está hecho) -------------------------
print("salud:", httpx.get(f"{LLM}/salud", timeout=10).json())

# --- PASO 2: hacer una pregunta ------------------------------------------------
# (pega aquí el bloque del paso 2)
def preguntar(texto, max_tokens=80):
    peticion = {"messages": [{"role": "user", "content": texto}], "max_tokens": max_tokens}
    inicio = time.time()
    respuesta = httpx.post(f"{LLM}/v1/chat/completions", json=peticion, timeout=180).json()
    return respuesta, time.time() - inicio

respuesta, segundos = preguntar(PREGUNTA)
print(f"respuesta ({segundos:.1f} s): {respuesta['choices'][0]['message']['content']}")

# --- PASO 3: contar los tokens -------------------------------------------------
# (pega aquí el bloque del paso 3)
uso = respuesta["usage"]
print(f"tokens: pregunta={uso['prompt_tokens']} respuesta={uso['completion_tokens']}  "
      f"velocidad={uso['completion_tokens'] / segundos:.0f} tokens/s")

# --- PASO 4: cómo crece el tiempo con la longitud ------------------------------
# (pega aquí el bloque del paso 4)
print("max_tokens  escritos  segundos")
for maximo in LONGITUDES:
    r, s = preguntar("Escribe un párrafo largo sobre el mantenimiento de un husillo.", maximo)
    print(f"{maximo:10d}  {r['usage']['completion_tokens']:8d}  {s:8.1f}")

# Reto 1: estimar otros tamaños con la velocidad medida
velocidad = uso["completion_tokens"] / segundos
print("modelo  tokens/s  segundos_para_200  memoria_aprox")
for tamano in (0.5, 1.5, 7):
    veces = tamano / 0.5
    print(f"{tamano:4.1f} B  {velocidad / veces:8.1f}  {200 / (velocidad / veces):17.0f}  {470 * veces / 1000:10.1f} GB")

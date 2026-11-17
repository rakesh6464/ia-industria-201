"""Constrúyelo tú (M05-03): tu propio asistente con el procedimiento (RAG).

Lo construyes paso a paso: en cada PASO del lab te dan un bloque de código.
Pégalo debajo del comentario de ese paso, guarda y ejecuta desde infra/:

    docker compose --profile lab run --rm --no-deps --entrypoint python lab -W ignore /construye/m05_03_mi_asistente.py
"""
import re

import httpx

# --- Decisiones tuyas (las cambiarás en los pasos finales) -------------------
PREGUNTA = "¿A qué par se aprieta el tornillo de la brida?"
VACIAS = {"a", "al", "de", "del", "el", "la", "las", "los", "lo", "un", "una", "y", "o", "en", "se", "que",
          "qué", "es", "por", "para", "con", "hay", "cómo", "cuánto", "cuál", "si", "no", "su", "sus"}
MINIMO_PALABRAS = 1      # palabras en común que tiene que tener un párrafo para usarlo

# --- PASO 1: el procedimiento, en párrafos (ya está hecho) -------------------
documento = open("/opt/linea/docs/procedimiento-est01.md", encoding="utf-8").read()   # infra/linea/docs/
parrafos = [p.strip() for p in documento.split("\n\n") if p.strip() and not p.startswith("#")]
print(f"el procedimiento tiene {len(parrafos)} párrafos (sin contar los títulos)")

# --- PASO 2: las palabras que importan -----------------------------------------
# (pega aquí el bloque del paso 2)
def palabras(texto):
    todas = set(re.findall(r"[a-záéíóúñ0-9]+", texto.lower()))    # solo letras y números
    return todas - VACIAS

print("palabras de la pregunta:", sorted(palabras(PREGUNTA)))

# --- PASO 3: elegir el párrafo -------------------------------------------------
# (pega aquí el bloque del paso 3)
def puntos(parrafo, pregunta):
    return len(palabras(parrafo) & palabras(pregunta))      # palabras en común

def elegir(pregunta):
    mejor = max(parrafos, key=lambda p: puntos(p, pregunta))
    return mejor, puntos(mejor, pregunta)

parrafo, en_comun = elegir(PREGUNTA)
print(f"párrafo elegido ({en_comun} palabras en común): {parrafo}")

# --- PASO 4: preguntar con el párrafo delante ----------------------------------
# (pega aquí el bloque del paso 4)
def generar(pregunta, parrafo):
    mensajes = [{"role": "system", "content": "Responde solo con el texto que se te da. Copia los números tal cual."},
                {"role": "user", "content": f"Texto: {parrafo}\n\nPregunta: {pregunta}"}]
    r = httpx.post("http://llm:8088/v1/chat/completions", json={"messages": mensajes, "max_tokens": 40}, timeout=60)
    return r.json()["choices"][0]["message"]["content"].strip()

respuesta = generar(PREGUNTA, parrafo)
print("respuesta:", respuesta)

# --- PASO 5: comprobar que no se ha inventado nada -----------------------------
# (pega aquí el bloque del paso 5)
numeros_respuesta = set(re.findall(r"\d+", respuesta))
numeros_parrafo = set(re.findall(r"\d+", parrafo))
inventados = numeros_respuesta - numeros_parrafo
print("comprobación:", "OK, todos los números salen del procedimiento" if not inventados else f"NO: inventa {inventados}")

# Reto 1: un párrafo nuevo en el procedimiento, sin tocar el modelo
parrafos.append("El husillo se lubrica cada 500 horas de trabajo con grasa G-2. Anotar la fecha en la hoja de la estación.")
pregunta = "¿Cada cuántas horas se lubrica el husillo?"
nuevo, comun = elegir(pregunta)
r = generar(pregunta, nuevo)
print(f"párrafo elegido ({comun} en común): {nuevo}")
print("respuesta:", r)

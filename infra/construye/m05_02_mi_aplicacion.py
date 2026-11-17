"""Constrúyelo tú (M05-02): tu propia aplicación que sabe fallar.

Lo construyes paso a paso: en cada PASO del lab te dan un bloque de código.
Pégalo debajo del comentario de ese paso, guarda y ejecuta desde infra/:

    docker compose --profile lab run --rm --no-deps --entrypoint python lab -W ignore /construye/m05_02_mi_aplicacion.py
"""
import httpx

# --- Decisiones tuyas (las cambiarás en los pasos finales) -------------------
SERVICIO = "http://llm:8088"     # dónde está el modelo
MAX_TOKENS = 60                  # longitud máxima de la respuesta
TIEMPO_MAX_S = 20                # cuánto espera la aplicación antes de rendirse

# --- PASO 1: la petición que manda la aplicación (ya está hecho) -------------
def peticion(pregunta):
    return {"messages": [{"role": "system", "content": "Responde en español, en una o dos frases."},
                         {"role": "user", "content": pregunta}],
            "max_tokens": MAX_TOKENS}

print("la aplicación preguntará a", SERVICIO, "con un máximo de", MAX_TOKENS, "tokens y", TIEMPO_MAX_S, "s de espera")

# --- PASO 2: preguntar y leer por qué terminó ----------------------------------
# (pega aquí el bloque del paso 2)
def consultar(pregunta):
    r = httpx.post(f"{SERVICIO}/v1/chat/completions", json=peticion(pregunta), timeout=TIEMPO_MAX_S)
    r.raise_for_status()                                  # un error del servicio se convierte en excepción
    eleccion = r.json()["choices"][0]
    return eleccion["message"]["content"].strip(), eleccion["finish_reason"]

texto, motivo = consultar("¿Qué es un PLC?")
print(f"motivo={motivo}  respuesta={texto}")

# --- PASO 3: un mensaje claro para cada caso -----------------------------------
# (pega aquí el bloque del paso 3)
def responder(pregunta):
    try:
        texto, motivo = consultar(pregunta)
    except httpx.ConnectError:
        return "AVISO: el asistente no está disponible. Usa el procedimiento en papel."
    except httpx.TimeoutException:
        return f"AVISO: el asistente no ha respondido en {TIEMPO_MAX_S} s. Inténtalo más tarde."
    except httpx.HTTPStatusError as error:
        return f"AVISO: el asistente ha dado un error ({error.response.status_code})."
    if motivo == "length":
        return texto + "  [respuesta incompleta: pide una pregunta más concreta]"
    return texto

print("pantalla:", responder("¿Qué es un PLC?"))

# Reto 1: medir cuánto tarda de verdad antes de fijar el tiempo máximo
import time
preguntas = ["¿Qué es un PLC?", "¿Para qué sirve un husillo?", "¿Qué es el OEE?", "¿Qué es una microparada?",
             "¿Qué mide un sensor de vibración?", "¿Qué es MQTT?", "¿Qué es una consigna?", "¿Qué es un SCADA?"]
tiempos = []
for p in preguntas:
    inicio = time.time()
    consultar(p)
    tiempos.append(time.time() - inicio)
tiempos.sort()
print(f"tiempos: mínimo={tiempos[0]:.1f} s  mediana={tiempos[len(tiempos) // 2]:.1f} s  máximo={tiempos[-1]:.1f} s")
print(f"tiempo máximo propuesto (el doble del peor): {2 * tiempos[-1]:.0f} s")

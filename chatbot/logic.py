import re
import json
import random

# Importamos la función que, aunque no usemos, es parte de la estructura.
# Si alguna vez arreglamos la conexión, solo debemos cambiar esta línea.
# from .internet_search import get_generative_response

# --- Cargar todas las respuestas desde el archivo JSON ---
def load_responses():
    try:
        # 'responses.json' está en la carpeta principal
        with open('responses.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: El archivo 'responses.json' no se encontró.")
        return {} 
    except json.JSONDecodeError:
        print("Error: El archivo 'responses.json' tiene un formato incorrecto.")
        return {}

# Cargamos las respuestas en una variable global
RESPONSES = load_responses()
# ---------------------------------------------------------


def get_dreamate_response(user_input):
    """
    Procesa la entrada del usuario y devuelve una respuesta de la base de datos JSON.
    """
    
    if not RESPONSES:
        return "Error interno: No pude cargar mis respuestas. Revisa la consola."

    low_input = user_input.lower()

    # --- REGIONAL DE SALUDOS ---
    if any(saludo in low_input for saludo in ["hola", "buenos días", "buenas noches"]):
        return random.choice(RESPONSES["greetings"])

    # --- REGLA DE DESPEDIDA ---
    if any(despedida in low_input for despedida in ["adiós", "bye", "hasta luego"]):
        return random.choice(RESPONSES["farewell"])

    # --- REGLA PARA DETECTAR HORAS DE SUEÑO (MEJORADA) ---
    match = re.search(r'\d+', low_input)
    if match:
        horas = int(match.group(0))
        feedback = RESPONSES["hours_feedback"]
        
        if horas <= 3:
            return feedback["extreme_low"].format(horas=horas)
        elif 4 <= horas <= 5:
            return feedback["low"].format(horas=horas)
        elif 6 == horas:
            return feedback["medium"].format(horas=horas)
        elif 7 <= horas <= 9:
            return feedback["good"].format(horas=horas)
        elif 10 <= horas <= 11:
            return feedback["high"].format(horas=horas)
        else: # 12+ horas
            return feedback["extreme_high"].format(horas=horas)

    # --- REGLA PARA PEDIR CONSEJOS (AHORA USA LA LISTA GRANDE) ---
    if any(palabra in low_input for palabra in ["consejo", "tip", "ayuda", "higiene", "mejorar"]):
        return random.choice(RESPONSES["sleep_hygiene_tips"])

    # --- SECCIÓN DE TEMAS ESPECÍFICOS (¡LA MONSTRUOSIDAD!) ---

    # Temas del JSON original
    if "cafeína" in low_input or "café" in low_input:
        return random.choice(RESPONSES["topics"]["caffeine"])
    
    if "ejercicio" in low_input or "gimnasio" in low_input:
        return random.choice(RESPONSES["topics"]["exercise"])
    
    if "siesta" in low_input:
        return random.choice(RESPONSES["topics"]["naps"])
    
    # Nuevos temas (Melatonina)
    if "melatonina" in low_input:
        return random.choice(RESPONSES["topics"]["melatonin"])
    
    # Nuevos temas (REM)
    if "rem" in low_input or "movimiento ocular" in low_input:
        return random.choice(RESPONSES["topics"]["rem"])
        
    # Nuevos temas (Ciclos de sueño)
    if "ciclo" in low_input or "fases del sueño" in low_input:
        return random.choice(RESPONSES["topics"]["sleep_cycles"])

    # Nuevos temas (Ritmo Circadiano)
    if "ritmo circadiano" in low_input or "reloj biológico" in low_input:
        return random.choice(RESPONSES["topics"]["circadian_rhythm"])

    # Nuevos temas (Insomnio)
    if "insomnio" in low_input or "no puedo dormir" in low_input:
        return random.choice(RESPONSES["topics"]["insomnia"])
    
    # Nuevos temas (Despertar cansado)
    if "cansado" in low_input or "despierto cansado" in low_input:
        return random.choice(RESPONSES["topics"]["waking_up_tired"])

    # Nuevos temas (Parálisis del sueño)
    if "parálisis" in low_input or "no me puedo mover" in low_input:
        return random.choice(RESPONSES["topics"]["sleep_paralysis"])

    # Nuevos temas (Roncar / Apnea)
    if "roncar" in low_input or "ronquidos" in low_input or "apnea" in low_input:
        return random.choice(RESPONSES["topics"]["snoring"])

    # Nuevos temas (Luz azul / Pantallas)
    if "luz azul" in low_input or "pantalla" in low_input or "móvil" in low_input or "celular" in low_input:
        return random.choice(RESPONSES["topics"]["blue_light"])
        
    # Nuevos temas (Soñar)
    if "sueños" in low_input or "soñar" in low_input or "pesadillas" in low_input:
        return random.choice(RESPONSES["topics"]["insomnia"]) # (Podemos apuntar a insomnio o crear uno nuevo)

    # --- REGLA DE BÚSQUEDA (FINAL: DESHABILITADA) ---
    # La dejamos al final por si no encuentra un tema específico.
    if "busca" in low_input or "noticias" in low_input or "investiga" in low_input or "qué es" in low_input:
        return "Lo siento, la función de búsqueda de internet está deshabilitada. Sin embargo, pregúntame directamente por temas como 'REM', 'melatonina', 'insomnio' o 'luz azul'."

    # --- RESPUESTA POR DEFECTO ---
    return random.choice(RESPONSES["default"])
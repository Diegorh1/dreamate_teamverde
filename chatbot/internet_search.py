import os
import requests
import json
import random

# Importamos el modelo de Google
import google.generativeai as genai 

# --- CONFIGURACIÓN DE LAS LLAVES (VERSIÓN "HARDCODED") ---
# Usamos la llave 1 que SÍ funcionó en el Playground
BRAVE_API_KEY = "BSAKrI2zrvu7gPTLgJLrMZR7p8lBHIl" 
GEMINI_API_KEY = "AIzaSyCka5SkxOAKJwGVd-m-okGiWazsc7Ywv7A" 
# ---------------------------------------------------------

# Configura el modelo de Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.0-pro')
except Exception as e:
    print(f"Error al configurar Gemini (revisa tu API key): {e}")
    exit()

def search_brave(query):
    """
    Usa Brave Search API para buscar resultados en la web.
    """
    url = "https://api.search.brave.com/res/v2/web/search"
    
    # --- ¡LOS ENCABEZADOS CORRECTOS Y COMPLETOS! ---
    # Esto imita perfectamente al Playground
    headers = {
        "X-Subscription-Token": BRAVE_API_KEY,
        "Accept": "application/json",  # <-- ¡EL QUE FALTABA! Le dice al servidor que queremos JSON.
        "Accept-Encoding": "gzip",     # <-- El que pide la compresión
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" # El disfraz
    }
    # -----------------------------------------------
    
    params = {"q": query, "count": 3, "country": "MX", "search_lang": "es"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() 
        
        try:
            search_results = response.json()
        except json.JSONDecodeError:
            print(f"ERROR INTERNO: El servidor devolvió texto no JSON. Contenido: {response.text[:100]}...")
            return f"Error: Brave devolvió un mensaje de error no esperado. La llave es incorrecta o la suscripción falló."

        snippets = []
        if search_results.get("web") and search_results["web"].get("results"):
            for result in search_results["web"]["results"]:
                snippets.append(f"Fuente: {result.get('title')}\nSnippet: {result.get('snippet')}")

        if not snippets:
            return "No se encontraron resultados en Brave Search."

        return "\n\n".join(snippets)

    except requests.exceptions.RequestException as e:
        print(f"Error al buscar en Brave: {e}")
        return f"Error de conexión externa: {e}"

def get_generative_response(user_query):
    """
    Función RAG final: Integra la búsqueda (ojos) con la IA (cerebro).
    """
    
    # 1. Buscar en Internet (Ojos)
    print(f"Dreamate (Búsqueda): Buscando '{user_query}'...")
    context = search_brave(user_query) # Llama a la función de Brave

    if context.startswith("Error"):
        return f"Lo siento, la búsqueda falló. Motivo: {context}"
        
    # 2. Construir el Prompt para Gemini
    prompt = f"""
    Eres Dreamate, un asistente de calidad de sueño. 
    Un usuario te preguntó: "{user_query}"

    Yo busqué en internet (Brave Search) y encontré la siguiente información:
    ---
    {context}
    ---
    
    Basándote SOLAMENTE en la información encontrada, responde la pregunta del usuario 
    de forma amable y como un experto en sueño. Si la información no es
    suficiente para responder, dilo.
    """
    
    # 3. Pedir al Cerebro (Gemini) que genere la respuesta
    print("Dreamate (IA): Razonando con Gemini...")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error al generar respuesta de Gemini: {e}")
        return "Tuve un problema de conexión con el modelo de IA. (Revisa tu clave de Gemini)."
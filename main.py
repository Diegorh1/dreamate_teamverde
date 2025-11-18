# Importamos la función principal
from chatbot.logic import get_dreamate_response

def run_chatbot():
    """
    Inicia el bucle principal del chatbot en la consola.
    """
    print("******************************************")
    print("  Bienvenido a Dreamate 😴")
    print(" Tu asistente de calidad de sueño.")
    print("******************************************")
    print("Escribe 'adiós' para salir.")
    print("Prueba con 'hola', 'dormí 7 horas', o 'busca qué es la melatonina'")
    print("\n") 

    # Bucle infinito para que la conversación continúe
    while True:
        # 1. Pedir la entrada al usuario
        user_input = input("Tú: ")

        # 2. Obtener la respuesta de nuestra lógica
        response = get_dreamate_response(user_input)

        # 3. Imprimir la respuesta del bot
        print(f"Dreamate: {response}\n")

        # 4. Condición para romper el bucle y salir
        if "adiós" in user_input.lower() or "bye" in user_input.lower():
            break

if __name__ == "__main__":
    run_chatbot()
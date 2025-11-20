import customtkinter as ctk

# Configuración inicial
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ChatGPTUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana principal
        self.geometry("1000x650")
        self.title("ChatGPT UI - Python")

        # FRAME GENERAL (DIVIDE IZQUIERDA / DERECHA)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------
        # PANEL IZQUIERDO (HISTORIAL)
        # ----------------------------------------------
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        title = ctk.CTkLabel(self.sidebar, text="Historial", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        self.history_list = ctk.CTkScrollableFrame(self.sidebar, width=230, height=500)
        self.history_list.pack(pady=10)

        # Botón para crear nuevo chat
        new_chat_btn = ctk.CTkButton(self.sidebar, text="+ Nuevo Chat", width=200, command=self.nuevo_chat)
        new_chat_btn.pack(pady=15)

        # ----------------------------------------------
        # PANEL DERECHO (CHAT)
        # ----------------------------------------------
        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        # Caja de chat con scroll
        self.chat_box = ctk.CTkTextbox(self.main_panel, wrap="word")
        self.chat_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.chat_box.configure(state="disabled")

        # Marco inferior con ENTER + BOTÓN
        bottom_frame = ctk.CTkFrame(self.main_panel)
        bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.entrada = ctk.CTkEntry(bottom_frame, placeholder_text="Escribe tu mensaje...")
        self.entrada.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        send_btn = ctk.CTkButton(bottom_frame, text="Enviar", width=80, command=self.enviar)
        send_btn.grid(row=0, column=1, padx=5)

        # Historial interno de chats (estructura)
        self.conversaciones = []
        self.chat_actual = []

    # ----------------------------------------------
    # FUNCIONES DEL PROGRAMA
    # ----------------------------------------------

    def nuevo_chat(self):
        # Añadir a historial
        chat_btn = ctk.CTkButton(
            self.history_list,
            text=f"Chat {len(self.conversaciones)+1}",
            width=180,
            command=lambda i=len(self.conversaciones): self.cargar_chat(i)
        )
        chat_btn.pack(pady=5)

        # Crear nuevo chat vacío
        self.conversaciones.append([])
        self.chat_actual = self.conversaciones[-1]

        # Limpiar pantalla
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", "end")
        self.chat_box.configure(state="disabled")

    def cargar_chat(self, index):
        self.chat_actual = self.conversaciones[index]

        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", "end")

        # Cargar mensajes previos
        for autor, msg in self.chat_actual:
            self.insertar_burbuja(autor, msg)

        self.chat_box.configure(state="disabled")

    def enviar(self):
        texto = self.entrada.get()
        if not texto.strip():
            return

        self.chat_actual.append(("Tú", texto))
        self.insertar_burbuja("Tú", texto)
        self.entrada.delete(0, "end")

    # Inserta mensajes con estilo
    def insertar_burbuja(self, autor, mensaje):
        self.chat_box.configure(state="normal")

        if autor == "Tú":
            # Mensaje alineado a la derecha
            self.chat_box.insert("end", f"\n( Tú )\n", "autor_tu")
            self.chat_box.insert("end", f"{mensaje}\n", "msg_tu")
        else:
            # Mensaje alineado a la izquierda
            self.chat_box.insert("end", f"\nChatGPT:\n", "autor_ai")
            self.chat_box.insert("end", f"{mensaje}\n", "msg_ai")

        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

        # Estilos
        self.chat_box.tag_config("autor_tu", foreground="#6ab0ff")
        self.chat_box.tag_config("msg_tu", foreground="#ffffff")

        self.chat_box.tag_config("autor_ai", foreground="#72d572")
        self.chat_box.tag_config("msg_ai", foreground="#d0ffd0")


# --------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------

if __name__ == "__main__":
    app = ChatGPTUI()
    app.mainloop()

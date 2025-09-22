import tkinter as tk
from tkinter import messagebox
import hashlib
from utils import local_db
from utils import secureAES
import base64
import json

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login")
        self.root.geometry("400x300")
        self.root.configure(bg='#f0f0f0')
        
        # Base de datos simulada (usuario: contraseña_hasheada)
        self.users = {
            'admin': 'pass-hash'
        }
        
        self.create_widgets()
    
    def hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return 'pass-hash'
    
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Inicio de Sesión", 
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=(0, 30))
        
        # Frame para campos de entrada
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(pady=10)
        
        # Usuario
        user_label = tk.Label(
            input_frame, 
            text="Usuario:", 
            font=('Arial', 12),
            bg='#f0f0f0',
            anchor='w',
            width=15
        )
        user_label.grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        self.user_entry = tk.Entry(
            input_frame, 
            font=('Arial', 12),
            width=20
        )
        self.user_entry.grid(row=0, column=1, padx=5, pady=10)
        self.user_entry.focus()  # Focus al iniciar
        
        # Contraseña
        pass_label = tk.Label(
            input_frame, 
            text="Contraseña:", 
            font=('Arial', 12),
            bg='#f0f0f0',
            anchor='w',
            width=15
        )
        pass_label.grid(row=1, column=0, padx=5, pady=10, sticky='w')
        
        self.pass_entry = tk.Entry(
            input_frame, 
            font=('Arial', 12),
            width=20,
            show='*'  # Oculta la contraseña
        )
        self.pass_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Bind Enter key para login
        self.pass_entry.bind('<Return>', lambda event: self.login())
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(
            button_frame,
            text="Iniciar Sesión",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=12,
            command=self.login
        )
        
        sigin_btn = tk.Button(
            button_frame,
            text="Registrarse",
            font=('Arial', 12, 'bold'),
            bg="#4C65AF",
            fg='white',
            width=12,
            command=self.signin
        )
        
        login_btn.pack(pady=5)
        sigin_btn.pack(pady=1)
        
        clear_btn = tk.Button(
            button_frame,
            text="Limpiar",
            font=('Arial', 10),
            bg='#f44336',
            fg='white',
            width=10,
            command=self.clear_fields
        )
        clear_btn.pack(pady=5)
        
        # Información de usuarios demo
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(pady=20)
        

        
    def signin(self):

        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        #Si el usuario o contraseña estan vacios, muestra un error y termina el metodo

        if not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        #Carga users-db.json, si no existe crea una lista vacia
        try:
            users_data = local_db.load("users-db.json")
            if not isinstance(users_data, list):
                users_data = []
        except FileNotFoundError:
            users_data = []


        #Revisa si el user ya existe
        if any(user["username"] == username for user in users_data):
            messagebox.showerror("Error", "El usuario ya existe. Por favor, elija otro nombre.")
            return


        #Genara una clave unica de 32 bits
        key = secureAES.getKey(32)
        #Cifra la contraseña con la clave y obtine iv y pass_encrypted
        iv, pass_encrypted = secureAES.encode(key, password)


        # Añadimos el nuevo usuario a la lista
        new_user = {"username": username, "password hash": pass_encrypted, "iv": iv}
        users_data.append(new_user)



        # Guardamos la lista completa de usuarios
        local_db.save(users_data, "users-db.json")



        # Guardamos la clave tambien en la lista 
        try:
            keys_data = local_db.load("keys.json")
            if not isinstance(keys_data, list):
                keys_data = []
        except FileNotFoundError:
            keys_data = []



        #Guarda la clave en AES para poder guardarla como texto
        new_key = {"username": username, "key": base64.b64encode(key).decode("utf-8")}
        keys_data.append(new_key)
        local_db.save(keys_data, "keys.json")

        messagebox.showinfo("Registro", "Usuario registrado correctamente")

    
    def encrypt_password():{
        
         
    }


    def login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        #Muestra un error si hay un campo vacio
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return


        #Carga la lista de usuarios guardados
        try:
            users_data = local_db.load("users-db.json")
            if not isinstance(users_data, list):
                users_data = []
        except FileNotFoundError:
            users_data = []


        #Carga la lista de keys
        try:
            keys_data = local_db.load("keys.json")
            if not isinstance(keys_data, list):
                keys_data = []
        except FileNotFoundError:
            keys_data = []

        # Buscar usuario
        user_record = next((u for u in users_data if u["username"] == username), None)
        if not user_record:
            messagebox.showerror("Error", "Usuario no encontrado")
            return

        # Buscar clave
        key_record = next((k for k in keys_data if k["username"] == username), None)
        if not key_record:
            messagebox.showerror("Error", "Clave de usuario no encontrada")
            return

        # Decodificar clave base64
        key = base64.b64decode(key_record["key"])
        iv = user_record["iv"]
        pass_encrypted = user_record["password hash"]

        # Descifrar contraseña almacenada
        try:
            password_stored = secureAES.decode(key, iv, pass_encrypted)
        except Exception as e:
            messagebox.showerror("Error", "Error al descifrar la contraseña")
            return

        # Comparar con la contraseña ingresada
        if password == password_stored:
            messagebox.showinfo("Éxito", f"¡Bienvenido, {username}!")
            self.open_dashboard(username)
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    
    def clear_fields(self):
        """Limpia los campos de entrada"""
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.user_entry.focus()
    
    def open_dashboard(self, username):
        """Abre la ventana principal después del login exitoso"""
        # Cerrar ventana de login
        self.root.destroy()
        
        # Crear nueva ventana
        dashboard = tk.Tk()
        dashboard.title("Dashboard Principal")
        dashboard.geometry("600x400")
        dashboard.configure(bg='#ffffff')
        
        # Bienvenida
        welcome_label = tk.Label(
            dashboard,
            text=f"Bienvenido al Sistema, {username}!",
            font=('Arial', 16, 'bold'),
            bg='#ffffff',
            fg='#333333'
        )
        welcome_label.pack(pady=50)
        
        # Botón de salir
        logout_btn = tk.Button(
            dashboard,
            text="Cerrar Sesión",
            font=('Arial', 12),
            bg='#ff9800',
            fg='white',
            command=dashboard.quit
        )
        logout_btn.pack(pady=20)
        
        dashboard.mainloop()

def main():
    # Crear ventana principal
    root = tk.Tk()
    
    # Centrar ventana en la pantalla
    window_width = 400
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    # Iniciar aplicación
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
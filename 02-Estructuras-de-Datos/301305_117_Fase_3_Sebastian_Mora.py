#301305_117_Fase_3_Sebastian_Mora
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import deque
import re

# Ventana de Login
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("EPS Salvando Vidas - Login")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        # Frame principal
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Ingrese la contraseña:", font=('Arial', 12)).pack(pady=10)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=20)
        self.password_entry.pack(pady=5)
        self.password_entry.bind('<Return>', lambda e: self.verificar_login())
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Ingresar", command=self.verificar_login).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Acerca de", command=self.mostrar_acerca).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Salir", command=root.quit).grid(row=0, column=2, padx=5)

    def verificar_login(self):
        if self.password_var.get() == "unad":
            self.root.destroy()
            main_root = tk.Tk()
            app = AppGUI(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
            self.password_var.set("")
            self.password_entry.focus()

    def mostrar_acerca(self):
        messagebox.showinfo("Acerca de", "Fase 3 - Componente práctico\nEstudiante: Sebastián Daniel Mora Insuasti\nCurso: Estructuras de Datos")

# Reglas de negocio para copago (sin cambios)
def calcular_copago(estrato: int, tipo_atencion: str) -> float:
    tipo_atencion = tipo_atencion.lower()
    if tipo_atencion == "medicina general":
        if estrato in (1,2):
            return 0.0
        if estrato == 3:
            return 10000.0
        if estrato == 4:
            return 15000.0
        if estrato == 5:
            return 20000.0
        if estrato == 6:
            return 30000.0
    elif tipo_atencion == "examen laboratorio":
        if estrato in (1,2,3):
            return 0.0
        if estrato == 4:
            return 5000.0
        if estrato == 5:
            return 10000.0
        if estrato == 6:
            return 20000.0
    return 0.0

class EstructuraDatosUsuario:
    def __init__(self, tipo_identificacion: str, numero_id: str, nombre: str, edad: int,
                 estrato: int, tipo_atencion: str, fecha_registro: str):
        self.tipo_identificacion = tipo_identificacion
        self.numero_id = numero_id
        self.nombre = nombre
        self.edad = edad
        self.estrato = estrato
        self.tipo_atencion = tipo_atencion
        self.fecha_registro = fecha_registro
        self.valor_copago = calcular_copago(estrato, tipo_atencion)

class PilaManager:
    def __init__(self):
        self.stack = []
    def push(self, usuario: EstructuraDatosUsuario):
        self.stack.append(usuario)
    def pop(self):
        return self.stack.pop() if self.stack else None
    def get_all(self):
        return list(reversed(self.stack))
    def clear(self):
        self.stack.clear()
    def reporte(self):
        return sum(u.valor_copago for u in self.stack)

class ColaManager:
    def __init__(self):
        self.queue = deque()
    def enqueue(self, usuario: EstructuraDatosUsuario):
        self.queue.append(usuario)
    def dequeue(self):
        return self.queue.popleft() if self.queue else None
    def get_all(self):
        return list(self.queue)
    def clear(self):
        self.queue.clear()
    def reporte(self):
        return len(self.queue)

class ListaManager:
    def __init__(self):
        self.lista = []
    def add(self, usuario: EstructuraDatosUsuario):
        self.lista.append(usuario)
    def remove_by_id(self, numero_id: str):
        for i,u in enumerate(self.lista):
            if u.numero_id == numero_id:
                return self.lista.pop(i)
        return None
    def get_all(self):
        return list(self.lista)
    def clear(self):
        self.lista.clear()
    def reporte(self):
        if not self.lista:
            return 0
        return sum(u.edad for u in self.lista) / len(self.lista)

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EPS Salvando Vidas – Control de Usuarios")
        self.root.geometry("980x620")
        self.setup_managers()
        self.create_widgets()

    def setup_managers(self):
        self.pila = PilaManager()
        self.cola = ColaManager()
        self.lista = ListaManager()
        self.current_structure = tk.StringVar(value='pila')

    def create_widgets(self):
        # Frame de formulario
        form = ttk.LabelFrame(self.root, text="Registro de usuario")
        form.place(x=10, y=10, width=460, height=320)

        ttk.Label(form, text="Tipo ID:").grid(row=0, column=0, sticky='w', padx=6, pady=6)
        self.tipo_id_cb = ttk.Combobox(form, values=["CC","CE","NUIP","PAS"], state='readonly')
        self.tipo_id_cb.grid(row=0,column=1, padx=6, pady=6)
        self.tipo_id_cb.current(0)

        ttk.Label(form, text="Número ID:").grid(row=1, column=0, sticky='w', padx=6, pady=6)
        vcmd_numero = (self.root.register(self.validar_numero_id), '%P')
        self.numero_entry = ttk.Entry(form, validate='key', validatecommand=vcmd_numero)
        self.numero_entry.grid(row=1,column=1, padx=6, pady=6)

        ttk.Label(form, text="Nombre:").grid(row=2, column=0, sticky='w', padx=6, pady=6)
        vcmd_nombre = (self.root.register(self.validar_nombre), '%P')
        self.nombre_entry = ttk.Entry(form, validate='key', validatecommand=vcmd_nombre)
        self.nombre_entry.grid(row=2,column=1, padx=6, pady=6)

        ttk.Label(form, text="Edad:").grid(row=3, column=0, sticky='w', padx=6, pady=6)
        self.edad_entry = ttk.Entry(form)
        self.edad_entry.grid(row=3,column=1, padx=6, pady=6)

        ttk.Label(form, text="Estrato:").grid(row=4, column=0, sticky='w', padx=6, pady=6)
        self.estrato_cb = ttk.Combobox(form, values=[1,2,3,4,5,6], state='readonly')
        self.estrato_cb.grid(row=4,column=1, padx=6, pady=6)
        self.estrato_cb.current(0)

        ttk.Label(form, text="Tipo atención:").grid(row=5, column=0, sticky='w', padx=6, pady=6)
        self.tipo_att_var = tk.StringVar(value="Medicina general")
        r1 = ttk.Radiobutton(form, text="Medicina general", variable=self.tipo_att_var, value="Medicina general", command=self.update_copago)
        r2 = ttk.Radiobutton(form, text="Examen laboratorio", variable=self.tipo_att_var, value="Examen laboratorio", command=self.update_copago)
        r1.grid(row=5,column=1, sticky='w')
        r2.grid(row=6,column=1, sticky='w')

        ttk.Label(form, text="Fecha (dd/mm/yyyy):").grid(row=7, column=0, sticky='w', padx=6, pady=6)
        self.fecha_entry = ttk.Entry(form)
        self.fecha_entry.grid(row=7,column=1, padx=6, pady=6)
        self.fecha_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        ttk.Label(form, text="Valor copago:").grid(row=8, column=0, sticky='w', padx=6, pady=6)
        self.copago_var = tk.StringVar(value="0")
        self.copago_entry = ttk.Entry(form, textvariable=self.copago_var, state='readonly')
        self.copago_entry.grid(row=8,column=1, padx=6, pady=6)

        # Botones
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Registrar", command=self.registrar).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=1, padx=6)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar).grid(row=0, column=2, padx=6)
        ttk.Button(btn_frame, text="Reporte", command=self.mostrar_reporte).grid(row=0, column=3, padx=6)

        # Selección de estructura y Treeview
        structure_frame = ttk.LabelFrame(self.root, text="Estructuras en memoria")
        structure_frame.place(x=10, y=340, width=460, height=260)

        ttk.Radiobutton(structure_frame, text="Pila (LIFO)", variable=self.current_structure, value='pila', command=self.refresh_tree).pack(anchor='w', padx=6, pady=2)
        ttk.Radiobutton(structure_frame, text="Cola (FIFO)", variable=self.current_structure, value='cola', command=self.refresh_tree).pack(anchor='w', padx=6, pady=2)
        ttk.Radiobutton(structure_frame, text="Lista", variable=self.current_structure, value='lista', command=self.refresh_tree).pack(anchor='w', padx=6, pady=2)

        # Treeview para mostrar registros
        self.tree = ttk.Treeview(self.root, columns=("tipo","numero","nombre","edad","estrato","tipoatt","copago","fecha"), show='headings', height=18)
        for col, text in [("tipo","Tipo ID"),("numero","Número ID"),("nombre","Nombre"),("edad","Edad"),("estrato","Estrato"),("tipoatt","Tipo Atensión"),("copago","Copago"),("fecha","Fecha")]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=110)
        self.tree.place(x=480, y=10, width=480, height=560)

        # Menu
        menubar = tk.Menu(self.root)
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        ayuda_menu.add_command(label="Acerca de", command=self.mostrar_acerca)
        ayuda_menu.add_separator()
        ayuda_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        self.root.config(menu=menubar)

        self.refresh_tree()

    # Métodos de validación mejorados
    def validar_numero_id(self, valor):
        return valor.isdigit() or valor == ""

    def validar_nombre(self, valor):
        return all(c.isalpha() or c.isspace() for c in valor) or valor == ""

    def validar_fecha(self, fecha_str):
        try:
            datetime.strptime(fecha_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def update_copago(self):
        try:
            estrato = int(self.estrato_cb.get())
        except Exception:
            estrato = 1
        tipo = self.tipo_att_var.get()
        self.copago_var.set(str(int(calcular_copago(estrato, tipo))))

    def validar_campos(self):
        if not self.numero_entry.get().strip():
            messagebox.showwarning("Validación", "El número de identificación es obligatorio.")
            return False
        if not self.nombre_entry.get().strip():
            messagebox.showwarning("Validación", "El nombre es obligatorio.")
            return False
        try:
            edad = int(self.edad_entry.get())
            if edad <= 0:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Validación", "Edad inválida.")
            return False
        try:
            estrato = int(self.estrato_cb.get())
            if estrato < 1 or estrato > 6:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Validación", "Estrato inválido.")
            return False
        # Validar fecha
        if not self.validar_fecha(self.fecha_entry.get().strip()):
            messagebox.showwarning("Validación", "Formato de fecha inválido. Use dd/mm/yyyy.")
            return False
        return True

    def registrar(self):
        if not self.validar_campos():
            return
        tipo_id = self.tipo_id_cb.get()
        numero = self.numero_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        edad = int(self.edad_entry.get())
        estrato = int(self.estrato_cb.get())
        tipo_att = self.tipo_att_var.get()
        fecha = self.fecha_entry.get().strip()

        usuario = EstructuraDatosUsuario(tipo_id, numero, nombre, edad, estrato, tipo_att, fecha)
        estructura = self.current_structure.get()

        if estructura == 'pila':
            self.pila.push(usuario)
        elif estructura == 'cola':
            self.cola.enqueue(usuario)
        else:
            self.lista.add(usuario)

        self.refresh_tree()
        self.limpiar_campos(keep_tipo=True)

    def limpiar_campos(self, keep_tipo=False):
        if not keep_tipo:
            self.tipo_id_cb.set("CC")
        self.numero_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.edad_entry.delete(0, tk.END)
        self.estrato_cb.set(1)
        self.tipo_att_var.set("Medicina general")
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.copago_var.set("0")

    def eliminar(self):
        estructura = self.current_structure.get()
        eliminado = None
        if estructura == 'pila':
            eliminado = self.pila.pop()
            msg = "Elemento desapilado." if eliminado else "Pila vacía."
        elif estructura == 'cola':
            eliminado = self.cola.dequeue()
            msg = "Elemento desencolado." if eliminado else "Cola vacía."
        else:
            numero = self.numero_entry.get().strip()
            if not numero:
                messagebox.showinfo("Eliminar", "Para eliminar en Lista ingresa el Número ID en el campo correspondiente y presiona Eliminar.")
                return
            eliminado = self.lista.remove_by_id(numero)
            msg = f"Elemento con ID {numero} eliminado." if eliminado else "Elemento no encontrado en la lista."
        if eliminado:
            messagebox.showinfo("Eliminar", msg)
        else:
            messagebox.showwarning("Eliminar", msg)
        self.refresh_tree()

    def mostrar_reporte(self):
        estructura = self.current_structure.get()
        if estructura == 'pila':
            total = self.pila.reporte()
            messagebox.showinfo("Reporte Pila", f"Total copago (suma): {total}")
        elif estructura == 'cola':
            cantidad = self.cola.reporte()
            messagebox.showinfo("Reporte Cola", f"Cantidad de elementos en cola: {cantidad}")
        else:
            promedio = self.lista.reporte()
            messagebox.showinfo("Reporte Lista", f"Promedio de edades: {promedio:.2f}")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        estructura = self.current_structure.get()
        if estructura == 'pila':
            datos = self.pila.get_all()
        elif estructura == 'cola':
            datos = self.cola.get_all()
        else:
            datos = self.lista.get_all()
        for u in datos:
            self.tree.insert('', tk.END, values=(u.tipo_identificacion, u.numero_id, u.nombre, u.edad, u.estrato, u.tipo_atencion, int(u.valor_copago), u.fecha_registro))

    def mostrar_acerca(self):
        messagebox.showinfo("Acerca de", "Fase 3 - Componente práctico\nEstudiante: Sebastián Daniel Mora Insuasti\nCurso: Estructuras de Datos")

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginWindow(root)
    root.mainloop()
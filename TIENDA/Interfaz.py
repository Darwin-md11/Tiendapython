import tkinter as tk
from tkinter import ttk, messagebox
import uuid  

class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

class Cliente:
    def __init__(self, nombre, apellido, id_cliente=None):
        self.nombre = nombre
        self.apellido = apellido
        self.id_cliente = id_cliente if id_cliente else str(uuid.uuid4())  # Generar un ID único si no se proporciona

    def mostrar_info(self):
        return f"Cliente: {self.nombre} {self.apellido} (ID: {self.id_cliente})"

class ItemOrden:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad

class Orden:
    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []

    def agregar_item(self, item):
        self.items.append(item)

    def calcular_total(self):
        total = 0
        for item in self.items:
            total += item.calcular_subtotal()
        return total

class Producto:
    def __init__(self, nombre, precio, categoria):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def mostrar_info(self):
        return f"Nombre: {self.nombre}\nPrecio: ${self.precio:.2f}\nCategoría: {self.categoria}"

class Tienda:
    def __init__(self):
        self.productos = []
        self.clientes = []
        self.ordenes = []
        self.categorias = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agregar_categoria(self, categoria):
        self.categorias.append(categoria)

    def buscar_categoria_por_nombre(self, nombre):
        for categoria in self.categorias:
            if categoria.nombre == nombre:
                return categoria
        return None

    def buscar_cliente_por_id(self, id_cliente):
        for cliente in self.clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        return None

    def buscar_producto_por_nombre(self, nombre):
        for producto in self.productos:
            if producto.nombre == nombre:
                return producto
        return None

    def crear_orden(self, cliente):
        orden = Orden(cliente)
        self.ordenes.append(orden)
        return orden

    def calcular_total_compras_cliente(self, cliente):
        total = 0
        for orden in self.ordenes:
            if orden.cliente == cliente:
                total += orden.calcular_total()
        return total

class TiendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tienda App")

        # Ajustar tamaño de la ventana y centrar en la pantalla
        self.root.geometry("800x600")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")

        # Crear una instancia de Tienda
        self.tienda = Tienda()
        self.orden_actual = None

        # Estilo para los widgets
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TEntry", fieldbackground="#ffffff")
        self.style.configure("TButton", background="#e0e0e0", font=("Arial", 10))

        # Crear un notebook para las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Crear frames para cada pestaña
        self.tab_registro_producto = ttk.Frame(self.notebook)
        self.tab_registro_cliente = ttk.Frame(self.notebook)
        self.tab_gestion_orden = ttk.Frame(self.notebook)
        self.tab_total_compras = ttk.Frame(self.notebook)
        self.tab_registro_categoria = ttk.Frame(self.notebook)

        # Añadir las pestañas al notebook
        self.notebook.add(self.tab_registro_categoria, text="Registrar Categoría")
        self.notebook.add(self.tab_registro_producto, text="Registrar Producto")
        self.notebook.add(self.tab_registro_cliente, text="Registrar Cliente")
        self.notebook.add(self.tab_gestion_orden, text="Gestionar Orden")
        self.notebook.add(self.tab_total_compras, text="Calcular Total Compras")

        # Llamar a métodos de inicialización
        self._init_registro_producto()
        self._init_registro_cliente()
        self._init_gestion_orden()
        self._init_total_compras()
        self._init_registro_categoria()

        # Inicializar la interfaz
        self.inicializar_interfaz()

    def _init_registro_producto(self):
        # Frame para el registro de productos
        self.frame_registro_producto = ttk.LabelFrame(self.tab_registro_producto, text="Registrar Producto", style="TFrame")
        self.frame_registro_producto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.frame_registro_producto, text="Nombre").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre_producto = ttk.Entry(self.frame_registro_producto)
        self.entry_nombre_producto.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_registro_producto, text="Precio").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_precio_producto = ttk.Entry(self.frame_registro_producto)
        self.entry_precio_producto.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_registro_producto, text="Categoría").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_categorias = ttk.Combobox(self.frame_registro_producto, state="readonly", width=27)
        self.combo_categorias.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self.frame_registro_producto, text="Registrar Producto", command=self.registrar_producto).grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    def _init_registro_cliente(self):
        # Frame para el registro de clientes
        self.frame_registro_cliente = ttk.LabelFrame(self.tab_registro_cliente, text="Registrar Cliente", style="TFrame")
        self.frame_registro_cliente.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.frame_registro_cliente, text="Nombre").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre_cliente = ttk.Entry(self.frame_registro_cliente)
        self.entry_nombre_cliente.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_registro_cliente, text="Apellido").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_apellido_cliente = ttk.Entry(self.frame_registro_cliente)
        self.entry_apellido_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self.frame_registro_cliente, text="Registrar Cliente", command=self.registrar_cliente).grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    def _init_gestion_orden(self):
        # Frame para gestionar órdenes
        self.frame_gestion_orden = ttk.LabelFrame(self.tab_gestion_orden, text="Gestionar Orden", style="TFrame")
        self.frame_gestion_orden.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.frame_gestion_orden, text="Seleccionar Cliente").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_clientes = ttk.Combobox(self.frame_gestion_orden, state="readonly", width=30)
        self.combo_clientes.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self.frame_gestion_orden, text="Crear Orden", command=self.crear_orden).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.frame_gestion_orden, text="Seleccionar Producto").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_productos = ttk.Combobox(self.frame_gestion_orden, state="readonly", width=30)
        self.combo_productos.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.frame_gestion_orden, text="Cantidad").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_cantidad_producto = ttk.Entry(self.frame_gestion_orden)
        self.entry_cantidad_producto.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self.frame_gestion_orden, text="Agregar Producto", command=self.agregar_producto_a_orden).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(self.frame_gestion_orden, text="Total Orden").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.label_total_orden = ttk.Label(self.frame_gestion_orden, text="$0.00")
        self.label_total_orden.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    def _init_total_compras(self):
        # Frame para calcular el total de compras de un cliente
        self.frame_total_compras = ttk.LabelFrame(self.tab_total_compras, text="Calcular Total Compras de Cliente", style="TFrame")
        self.frame_total_compras.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.frame_total_compras, text="Seleccionar Cliente").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_clientes_total = ttk.Combobox(self.frame_total_compras, state="readonly", width=30)
        self.combo_clientes_total.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self.frame_total_compras, text="Calcular Total", command=self.calcular_total_compras).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.frame_total_compras, text="Total Compras").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.label_total_compras = ttk.Label(self.frame_total_compras, text="$0.00")
        self.label_total_compras.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def _init_registro_categoria(self):
        # Frame para el registro de categorías
        self.frame_registro_categoria = ttk.LabelFrame(self.tab_registro_categoria, text="Registrar Categoría", style="TFrame")
        self.frame_registro_categoria.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.frame_registro_categoria, text="Nombre de la Categoría").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre_categoria = ttk.Entry(self.frame_registro_categoria)
        self.entry_nombre_categoria.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self.frame_registro_categoria, text="Registrar Categoría", command=self.registrar_categoria).grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    def registrar_producto(self):
        nombre = self.entry_nombre_producto.get()
        precio = float(self.entry_precio_producto.get())
        nombre_categoria = self.combo_categorias.get()

        categoria = self.tienda.buscar_categoria_por_nombre(nombre_categoria)
        if categoria:
            producto = Producto(nombre, precio, categoria)
            self.tienda.agregar_producto(producto)
            messagebox.showinfo("Registro Exitoso", f"Producto '{nombre}' registrado exitosamente.")
            self.actualizar_combobox_productos()
        else:
            messagebox.showerror("Error", "La categoría seleccionada no existe.")

    def registrar_cliente(self):
        nombre = self.entry_nombre_cliente.get()
        apellido = self.entry_apellido_cliente.get()

        cliente = Cliente(nombre, apellido)
        self.tienda.agregar_cliente(cliente)
        messagebox.showinfo("Registro Exitoso", f"Cliente '{nombre} {apellido}' registrado exitosamente.")
        self.actualizar_combobox_clientes()

    def registrar_categoria(self):
        nombre_categoria = self.entry_nombre_categoria.get()

        categoria = Categoria(nombre_categoria)
        self.tienda.agregar_categoria(categoria)
        messagebox.showinfo("Registro Exitoso", f"Categoría '{nombre_categoria}' registrada exitosamente.")
        self.actualizar_combobox_categorias()

    def crear_orden(self):
        nombre_cliente = self.combo_clientes.get()
        cliente = self.tienda.buscar_cliente_por_id(nombre_cliente.split(" (ID: ")[-1][:-1])

        if cliente:
            self.orden_actual = self.tienda.crear_orden(cliente)
            messagebox.showinfo("Orden Creada", f"Orden creada para el cliente '{cliente.nombre} {cliente.apellido}'.")
            self.label_total_orden.config(text="$0.00")
        else:
            messagebox.showerror("Error", "El cliente seleccionado no existe.")

    def agregar_producto_a_orden(self):
        if self.orden_actual:
            nombre_producto = self.combo_productos.get()
            cantidad = int(self.entry_cantidad_producto.get())

            producto = self.tienda.buscar_producto_por_nombre(nombre_producto)
            if producto:
                item = ItemOrden(producto, cantidad)
                self.orden_actual.agregar_item(item)
                total = self.orden_actual.calcular_total()
                self.label_total_orden.config(text=f"${total:.2f}")
                messagebox.showinfo("Producto Agregado", f"Producto '{producto.nombre}' agregado a la orden.")
            else:
                messagebox.showerror("Error", "El producto seleccionado no existe.")
        else:
            messagebox.showerror("Error", "No hay una orden creada. Por favor, cree una orden primero.")

    def calcular_total_compras(self):
        nombre_cliente = self.combo_clientes_total.get()
        cliente = self.tienda.buscar_cliente_por_id(nombre_cliente.split(" (ID: ")[-1][:-1])

        if cliente:
            total_compras = self.tienda.calcular_total_compras_cliente(cliente)
            self.label_total_compras.config(text=f"${total_compras:.2f}")
        else:
            messagebox.showerror("Error", "El cliente seleccionado no existe.")

    def actualizar_combobox_categorias(self):
        categorias = [categoria.nombre for categoria in self.tienda.categorias]
        self.combo_categorias['values'] = categorias

    def actualizar_combobox_productos(self):
        productos = [producto.nombre for producto in self.tienda.productos]
        self.combo_productos['values'] = productos

    def actualizar_combobox_clientes(self):
        clientes = [f"{cliente.nombre} {cliente.apellido} (ID: {cliente.id_cliente})" for cliente in self.tienda.clientes]
        self.combo_clientes['values'] = clientes
        self.combo_clientes_total['values'] = clientes

    def inicializar_interfaz(self):
        self.actualizar_combobox_categorias()
        self.actualizar_combobox_clientes()
        self.actualizar_combobox_productos()
        self.notebook.select(self.tab_registro_categoria)  # Mostrar la pestaña de registrar categoría al inicio

if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaApp(root)
    root.mainloop()

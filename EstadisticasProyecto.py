import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Inicializar listas vacías para x e y
x = []
y = []

def calcular_coeficientes():
    global x, y
    n = len(x)

    if n == 0:
        messagebox.showerror("Error", "Por favor, ingrese los datos primero.")
        return

    # Cálculos
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_squared = sum(val ** 2 for val in x)
    sum_y_squared = sum(val ** 2 for val in y)
    sum_xy = sum(x[i] * y[i] for i in range(n))

    Sxx = sum_x_squared - (sum_x ** 2 / n)
    Syy = sum_y_squared - (sum_y ** 2 / n)
    Sxy = sum_xy - (sum_x * sum_y / n)

    # Coeficientes
    r = Sxy / ((Sxx * Syy) ** 0.5) if Sxx * Syy != 0 else 0
    r2 = r ** 2
    uno_menos_r2 = 1 - r2

    # Mostrar resultados
    resultados = f"""\nSxx = {Sxx:.2f}\nSyy = {Syy:.2f}\nSxy = {Sxy:.2f}\nr = {r:.4f}\nR^2 = {r2:.4f}\n1 - R^2 = {uno_menos_r2:.4f}\n
                \nInterpretación:
                \n- r indica la fuerza y dirección de la relación lineal entre las variables. Un valor de r cerca de 1 o -1 indica una fuerte relación, mientras que un valor cerca de 0 indica poca o ninguna relación.
                \n- R^2 indica la proporción de la varianza en la variable dependiente que se puede predecir a partir de la variable independiente. Un R^2 de 1 significa que el modelo explica toda la variabilidad, mientras que un R^2 de 0 significa que no explica nada."""
    #messagebox.showinfo("Resultados", resultados)

    resultados_text.delete(1.0, tk.END)  # Limpiar el cuadro de texto antes de insertar nuevos resultados
    resultados_text.insert(tk.END, resultados)


def estadisticas_adicionales():
    global x, y
    if len(x) == 0 or len(y) == 0:
        messagebox.showerror("Error", "Por favor, ingrese los datos primero.")
        return

    # Calcular media, mediana y desviación estándar
    def media(datos):
        return sum(datos) / len(datos)

    def mediana(datos):
        sorted_data = sorted(datos)
        n = len(sorted_data)
        mid = n // 2
        return (sorted_data[mid] + sorted_data[mid - 1]) / 2 if n % 2 == 0 else sorted_data[mid]

    def desviacion_estandar(datos):
        m = media(datos)
        return (sum((x - m) ** 2 for x in datos) / (len(datos) - 1)) ** 0.5

    media_x = media(x)
    media_y = media(y)
    mediana_x = mediana(x)
    mediana_y = mediana(y)
    desviacion_x = desviacion_estandar(x)
    desviacion_y = desviacion_estandar(y)

    resultados_estadisticas = f"""\
Estadísticas Adicionales:
Media de Pub: {media_x:.2f}
Media de Vtas: {media_y:.2f}
Mediana de Pub: {mediana_x:.2f}
Mediana de Vtas: {mediana_y:.2f}
Desviación Estándar de Pub: {desviacion_x:.2f}
Desviación Estándar de Vtas: {desviacion_y:.2f}
"""
    messagebox.showinfo("Estadísticas Adicionales", resultados_estadisticas)


def agregar_fila():
    tree.insert('', 'end', values=(len(tree.get_children()) + 1, "", "", "", ""))
    ajustar_tamaño()
    

def ajustar_tamaño():
    # Actualiza el tamaño del Treeview
    num_filas = len(tree.get_children()) + 1  # +1 para incluir el encabezado
    root.geometry(f"1200x700")

    if (num_filas < 21):
        tree.config(height=num_filas)
        

def obtener_datos():
    global x, y
    x.clear()
    y.clear()

    sum_x = 0
    sum_y = 0
    sum_x_squared = 0
    sum_y_squared = 0

    for row in tree.get_children():  # Iterar sobre todas las filas
        valores = tree.item(row, 'values')

        try:
            x_val = float(valores[1])  # "Pub" está en la segunda columna (índice 1)
            y_val = float(valores[2])  # "Vtas" está en la tercera columna (índice 2)
            x.append(x_val)
            y.append(y_val)

            # Calcular sumatorias
            sum_x += x_val
            sum_y += y_val
            sum_x_squared += x_val ** 2
            sum_y_squared += y_val ** 2

            tree.item(row, values=(valores[0], x_val, y_val, x_val ** 2, y_val ** 2))

        except ValueError:
            messagebox.showerror("Error", "Los valores ingresados deben ser numéricos.")
            return

    # Limpiar la fila de sumatorias si existe

    # Actualizar la fila de sumatorias
    tree.insert('', 'end', values=("Sumas", f"{sum_x:.2f}", f"{sum_y:.2f}", f"{sum_x_squared:.2f}", f"{sum_y_squared:.2f}"))

    messagebox.showinfo("Datos", "Datos ingresados y sumatorias calculadas correctamente.")

def crear_grafica_dispersion():
    global x, y

    # Verificar si hay datos
    if len(x) == 0 or len(y) == 0:
        messagebox.showerror("Error", "Por favor, ingrese los datos primero.")
        return

    # Crear gráfico de dispersión
    fig, ax = plt.subplots()
    ax.scatter(x, y)

    ax.set_title('Gráfico de Dispersión')
    ax.set_xlabel('Pub')
    ax.set_ylabel('Vtas')

    # Mostrar gráfico en la interfaz
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def on_cell_edit(event):
    item = tree.selection()[0]  # Obtén el item seleccionado
    column = tree.identify_column(event.x)  # Obtén la columna que fue editada
    column_index = int(column.replace('#', '')) - 1  
    print(column_index)# Convertir a índice 0-based

    # Permitir solo edición en columnas "Pub" y "Vtas" (índices 1 y 2)
    if column_index not in [1, 2]:
        return

    # Obtener la posición de la celda
    bbox = tree.bbox(item, column)
    if bbox:
        x, y, width, height = bbox
        entry = tk.Entry(root)
        entry.place(x=x + tree.winfo_x(), y=y + tree.winfo_y(), width=width)
        entry.insert(0, tree.item(item)['values'][column_index])
        entry.focus_set()

        def save_edit(event):
            new_value = entry.get()
            try:
                # Solo permitir números
                float(new_value)
                # Actualizar el valor en la celda
                new_values = list(tree.item(item)['values'])
                new_values[column_index] = new_value  # Mantener el número de fila
                tree.item(item, values=new_values)
            except ValueError:
                messagebox.showerror("Error", "El valor debe ser numérico.")
            entry.destroy()

        entry.bind("<Return>", save_edit)  # Guardar en Enter
        entry.bind("<FocusOut>", lambda e: entry.destroy())  # Cerrar el Entry si se pierde el foco

def eliminar_fila():
    selected_item = tree.selection()
    
    if not selected_item:
        messagebox.showwarning("Advertencia", "Por favor, seleccione una fila para eliminar.")
        return

    # Eliminar la fila seleccionada
    tree.delete(selected_item)

    # Actualizar la numeración de las filas restantes
    filas = tree.get_children()
    for index, fila in enumerate(filas):
        valores = list(tree.item(fila, 'values'))
        valores[0] = index + 1  # Actualizar el número de fila
        tree.item(fila, values=valores)

    ajustar_tamaño()  # Ajustar el tamaño de la ventana si es necesario

def reiniciar_datos_y_grafico():
    global x, y
    x.clear()
    y.clear()
    for row in tree.get_children():
        tree.delete(row)
    agregar_fila()

    for widget in plot_frame.winfo_children():
        widget.destroy()

    resultados_text.delete(1.0, tk.END)  # Limpiar el cuadro de texto antes de insertar nuevos resultados

    messagebox.showinfo("Reiniciar", "Datos y gráfico reiniciados correctamente.")



# Crear la interfaz
def crear_interfaz():
    # Crear el frame para los botones
    button_frame = tk.Frame(root, bg='pink')  # Cambiar el color de fondo a rosa
    button_frame.pack(side=tk.TOP, fill=tk.X)

    # Crear botones directamente en el panel
    btn_agregar_fila = tk.Button(button_frame, text="Agregar Fila", command=agregar_fila, bg='#FF1493')
    btn_agregar_fila.pack(side=tk.LEFT, padx=0, pady=0)

    btn_eliminar_fila = tk.Button(button_frame, text="Eliminar Fila", command=eliminar_fila, bg='#FF1493')
    btn_eliminar_fila.pack(side=tk.LEFT, padx=0, pady=0)

    btn_obtener_datos = tk.Button(button_frame, text="Obtener Datos", command=obtener_datos, bg='#FF69B4')
    btn_obtener_datos.pack(side=tk.LEFT, padx=5, pady=0)

    btn_calcular = tk.Button(button_frame, text="Calcular Coeficientes", command=calcular_coeficientes, bg='pink')
    btn_calcular.pack(side=tk.LEFT, padx=0, pady=0)

    btn_estadisticas = tk.Button(button_frame, text="Estadísticas Adicionales", command=estadisticas_adicionales, bg='pink')
    btn_estadisticas.pack(side=tk.LEFT, padx=0, pady=0)

    btn_grafica_dispersion = tk.Button(button_frame, text="Crear Gráfico de Dispersión", command=crear_grafica_dispersion, bg='pink')
    btn_grafica_dispersion.pack(side=tk.LEFT, padx=0, pady=0)

    btn_reiniciar = tk.Button(button_frame, text="Reiniciar Datos y Gráfico", command=reiniciar_datos_y_grafico, bg='#FF69B4')
    btn_reiniciar.pack(side=tk.LEFT, padx=5, pady=0)

    

# Crear el frame principal para la tabla y gráficos
    main_frame = tk.Frame(root, bg='pink')
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Crear un frame para la tabla y el cuadro de texto
    table_and_text_frame = tk.Frame(main_frame, bg='pink')
    table_and_text_frame.pack(side=tk.LEFT, fill=tk.BOTH)

    # Crear el frame para la tabla
    table_frame = tk.Frame(table_and_text_frame, bg='pink')
    table_frame.pack(side=tk.TOP, fill=tk.BOTH)

    # Crear tabla para la entrada de datos
    global tree
    tree = ttk.Treeview(table_frame, columns=("sem", "pub", "vtas", "x2", "y2"), show='headings')
    tree.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

    # Configurar encabezados
    tree.heading("sem", text="Sem")
    tree.heading("pub", text="Pub")
    tree.heading("vtas", text="Vtas")
    tree.heading("x2", text="X²")
    tree.heading("y2", text="Y²")

    tree.column("sem", width=50, stretch=False)  # Ajustar el ancho de la columna "Sem"
    tree.column("pub", width=100, stretch=False)  # Ajustar el ancho de la columna "Pub"
    tree.column("vtas", width=100, stretch=False)  # Ajustar el ancho de la columna "Vtas"
    tree.column("x2", width=100, stretch=False)  # Ajustar el ancho de la columna "X²"
    tree.column("y2", width=100, stretch=False)

    # Ajustar el tamaño de la fuente para filas más cuadradas
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 10))

    global resultados_text
    # Crear un cuadro de texto para mostrar resultados
    resultados_text = tk.Text(table_and_text_frame, height=15, width=30, bg='pink',borderwidth=0, highlightthickness=0)
    resultados_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    # Añadir una fila vacía al principio
    agregar_fila()  # Fila inicial vacía

    # Crear el frame para el gráfico
    global plot_frame
    plot_frame = tk.Frame(main_frame , bg='pink')
    plot_frame.pack(side=tk.RIGHT,fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Vincular el evento de doble clic para editar celdas
    tree.bind("<Double-1>", on_cell_edit)

# Crear la ventana principal
root = tk.Tk()
root.title("Cálculo de Coeficiente de Correlación")




# Crear la interfaz de usuario
crear_interfaz()

# Ejecutar la aplicación
root.mainloop()

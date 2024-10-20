import tkinter as tk
from tkinter import messagebox
import os
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
    resultados = f"""\ 
Sxx = {Sxx:.2f}
Syy = {Syy:.2f}
Sxy = {Sxy:.2f}
r = {r:.4f}
R^2 = {r2:.4f}
1 - R^2 = {uno_menos_r2:.4f}

Interpretación:
- r indica la fuerza y dirección de la relación lineal entre las variables. Un valor de r cerca de 1 o -1 indica una fuerte relación, mientras que un valor cerca de 0 indica poca o ninguna relación.
- R^2 indica la proporción de la varianza en la variable dependiente que se puede predecir a partir de la variable independiente. Un R^2 de 1 significa que el modelo explica toda la variabilidad, mientras que un R^2 de 0 significa que no explica nada.
"""
    messagebox.showinfo("Resultados", resultados)

def mostrar_tabla():
    # Crear ventana para mostrar la tabla
    ventana_tabla = tk.Toplevel(root)
    ventana_tabla.title("Tabla de Datos")

    # Crear un texto para mostrar la tabla
    texto_tabla = tk.Text(ventana_tabla, wrap='word')
    texto_tabla.pack(expand=True, fill='both')

    # Limpiar el texto antes de insertar datos
    texto_tabla.delete(1.0, tk.END)

    # Insertar los encabezados
    texto_tabla.insert(tk.END, f"{'Sem':<5} {'Pub':<10} {'Vtas':<10} {'X^2':<10}\n")
    texto_tabla.insert(tk.END, "-" * 35 + "\n")

    # Insertar los datos
    for i in range(len(x)):
        texto_tabla.insert(tk.END, f"{i + 1:<5} {x[i]:<10} {y[i]:<10} {x[i] ** 2:<10}\n")
    
    # Agregar una fila de totales
    total_values = [sum(x), sum(y), sum(val ** 2 for val in x)]
    texto_tabla.insert(tk.END, f"{'Total':<5} {total_values[0]:<10} {total_values[1]:<10} {total_values[2]:<10}\n")

def obtener_datos():
    # Crear ventana para entrada de datos
    ventana_datos = tk.Toplevel(root)
    ventana_datos.title("Entrada de Datos")

    tk.Label(ventana_datos, text="Valores de Pub (separados por coma):").pack()
    entry_pub = tk.Entry(ventana_datos)
    entry_pub.pack()

    tk.Label(ventana_datos, text="Valores de Vtas (separados por coma):").pack()
    entry_vtas = tk.Entry(ventana_datos)
    entry_vtas.pack()

    def procesar_datos():
        global x, y
        try:
            x = list(map(float, entry_pub.get().split(',')))
            y = list(map(float, entry_vtas.get().split(',')))
            if len(x) != len(y):
                raise ValueError("Los valores de Pub y Vtas deben tener la misma cantidad.")
            ventana_datos.destroy()
            messagebox.showinfo("Éxito", "Datos ingresados correctamente.")
        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    btn_procesar = tk.Button(ventana_datos, text="Procesar Datos", command=procesar_datos)
    btn_procesar.pack()

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

def mostrar_dispersion():
    global x, y
    if len(x) == 0 or len(y) == 0:
        messagebox.showerror("Error", "Por favor, ingrese los datos primero.")
        return

    # Crear la figura de matplotlib
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='blue')
    ax.set_title("Gráfico de Dispersión de Pub vs Vtas")
    ax.set_xlabel("Publicidad (Pub)")
    ax.set_ylabel("Ventas (Vtas)")

    # Insertar el gráfico en una ventana de Tkinter
    ventana_grafico = tk.Toplevel(root)
    ventana_grafico.title("Gráfico de Dispersión")
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Crear la ventana principal
root = tk.Tk()
root.title("Cálculo de Coeficiente de Correlación")

# Botones para calcular y mostrar tabla
btn_ingresar_datos = tk.Button(root, text="Ingresar Datos", command=obtener_datos)
btn_ingresar_datos.pack(pady=10)

btn_calcular = tk.Button(root, text="Calcular Coeficientes", command=calcular_coeficientes)
btn_calcular.pack(pady=10)

btn_mostrar_tabla = tk.Button(root, text="Mostrar Tabla de Datos", command=mostrar_tabla)
btn_mostrar_tabla.pack(pady=10)

btn_estadisticas = tk.Button(root, text="Estadísticas Adicionales", command=estadisticas_adicionales)
btn_estadisticas.pack(pady=10)

btn_dispersion = tk.Button(root, text="Mostrar Gráfico de Dispersión", command=mostrar_dispersion)
btn_dispersion.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()

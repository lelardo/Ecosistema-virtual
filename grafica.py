import tkinter as tk
from main import *
from tkinter import messagebox

AZUL_OSCURO = "#9999FF"
AZUL_CLARO = "#99CCFF"
AZUL_BOTON = "#6699FF"
VERDE = "#00ff00"
ROJO = "#ff0000"
pantalla = tk.Tk()
pantalla.title("Simulacion Ecosistema")
pantalla.configure(bg=AZUL_OSCURO)
width = 1280
height = 720
lienzo = tk.Canvas(pantalla, width=width, height=height, bg=AZUL_OSCURO)
lienzo.pack()


def dibujar_cuadrilla(num_puntos, dimension, start_x=50, start_y=50):
    """
    Dibuja una cuadrícula con un número específico de cuadros dentro de un área delimitada en el lienzo.
    :param num_puntos: Número total de cuadros en una fila o columna.
    :param dimension: Tamaño de cada cuadro (en píxeles).
    :param start_x: Coordenada inicial en el eje X.
    :param start_y: Coordenada inicial en el eje Y.
    """
    end_x = start_x + (num_puntos - 1) * dimension
    end_y = start_y + (num_puntos - 1) * dimension

    # Dibujar líneas verticales
    for i in range(start_x, end_x + 1, dimension):
        lienzo.create_line(i, start_y, i, end_y, fill="black")

    # Dibujar líneas horizontales
    for j in range(start_y, end_y + 1, dimension):
        lienzo.create_line(start_x, j, end_x, j, fill="black")


# Metodo para dibujar la comida, con un reescalado para poder notar bien la separacion en la pantalla
def dibujar_comida(comida, dimension, start_x=50, start_y=50):
    """
    Dibuja puntos de comida dentro de la cuadrícula ajustada, manteniendo su tamaño original.
    """
    if comida.status:
        x = start_x + comida.Xaxis * dimension
        y = start_y + comida.Yaxis * dimension
        return lienzo.create_oval(
            x - 5,
            y - 5,
            x + 5,  # Mantener tamaño original
            y + 5,  # Mantener tamaño original
            fill="green",
            outline=""
        )


def dibujar_particula(particula, dimension, start_x=50, start_y=50):
    """
    Dibuja una partícula en su posición dentro de la cuadrícula, manteniendo su tamaño original.
    También escribe el nombre de la partícula encima de ella.
    """
    x = start_x + particula.Xaxis * dimension
    y = start_y + particula.Yaxis * dimension

    # Dibujar la partícula como un óvalo
    particula_id = lienzo.create_oval(
        x - 5,
        y - 5,
        x + 5,
        y + 5,
        fill="blue"
    )

    # Dibujar el nombre de la partícula encima del óvalo
    texto_id = lienzo.create_text(
        x,
        y - 10,  # Posicionar un poco más arriba de la partícula
        text=particula.name,
        fill="black",
        font=("Arial", 10)
    )

    identificador_id = lienzo.create_text(
        x,
        y + 15,  # Posicionar un poco más abajo de la partícula
        text=particula.id,
        fill="red",
        font=("Arial", 14)
    )

    return particula_id, texto_id, identificador_id


def dibujar_particula_final(particula, dimension, start_x=50, start_y=50):
    """
    Dibuja una partícula en su posición dentro de la cuadrícula, manteniendo su tamaño original.
    """
    xAux, yAux = particula.recorrido[len(particula.recorrido) - 1]
    x = start_x + xAux * dimension
    y = start_y + yAux * dimension
    return lienzo.create_oval(
        x - 5,
        y - 5,
        x + 5,  # Mantener tamaño original
        y + 5,  # Mantener tamaño original
        fill="red"
    )


def simulacion(particulas, comidas, dimension_dibujo, num_puntos, cant_particulas):
    # Limpiar lienzo antes de iniciar un nuevo ciclo
    lienzo.delete("all")  # Eliminar todos los elementos del lienzo (partículas y comida)

    # Dibujar comida
    comida_ids = []  # Array para guardar los ids de las comidas
    for comida in comidas:
        comida_ids.append(dibujar_comida(comida, dimension_dibujo))  # Dibujar cada comida y guardar su ID
    dibujar_cuadrilla(num_puntos, dimension_dibujo)

    # Texto para indicar el ciclo actual
    texto_ciclo = lienzo.create_text(10, 10, text="🔄 Ciclo 1", anchor="nw", fill="black", font=("Arial", 16))
    aux_particulas_vivas = len(particulas[-1])
    lienzo.create_text(900, 50, text="📈 Datos de Entrada", fill="black", font=("Arial", 16))
    lienzo.create_text(900, 100, text=f"🔴 Particulas: {cant_particulas}", fill="black", font=("Arial", 16))
    lienzo.create_text(900, 150, text=f"🍔 Comida: {len(comidas)}", fill="black", font=("Arial", 16))
    lienzo.create_text(900, 200, text=f"⚫ Dimension del mapa: {num_puntos - 1} * {num_puntos - 1}", fill="black", font=("Arial", 16))
    lienzo.create_text(900, 250, text=f"➡️ Pasos: {len(particulas[1][0].recorrido) - 1}", fill="black", font=("Arial", 16))

    particula_ids = []  # Lista para almacenar tuplas (ID partícula, ID texto)
    particula_final_ids = []  # Guardamos los ids de las partículas finales
    identificador_particula = []  # Guardamos los ids de las partículas finales

    # Simular el movimiento de todas las partículas simultáneamente
    for ciclo, partic in enumerate(particulas, start=1):
        # Actualizar el mensaje del ciclo
        lienzo.itemconfig(texto_ciclo, text=f"🔄 Ciclo {ciclo}")
        lienzo.update()

        # Dibujar las partículas originales para el ciclo actual
        particula_ids = []  # Limpiar las listas de partículas y textos
        particula_final_ids = []

        lienzo.after(1000)
        for p in partic:  # Dibujar las partículas del ciclo actual
            particula_id, texto_id, identificador_id = dibujar_particula(p, dimension_dibujo)
            particula_ids.append((particula_id, texto_id, identificador_id))  # Guardamos la tupla de IDs
        # Actualizar posiciones de todas las partículas de forma simultánea
        actualizar_particulas_simultaneas(partic, comidas, particula_ids, dimension_dibujo, comida_ids)

        def eliminar_final_punto():
            # Eliminar las partículas finales después de un ciclo
            for particula_final_id in particula_final_ids:
                lienzo.delete(particula_final_id)
            for coso in particula_ids:  # Eliminar partículas y textos
                lienzo.delete(coso[1])
            for particula_id in particula_ids:
                lienzo.delete(particula_id[0])
            for identificador in particula_ids:
                lienzo.delete(identificador[2])

        # Llamar a la función de eliminación 600 ms después de haber mostrado la partícula final

        lienzo.after(600, eliminar_final_punto())
        lienzo.update()  # Actualizar la vista
    lienzo.create_text(900, 350, text=f"Se acabaron las particulas en el ciclo: {ciclo}", fill="black", font=("Arial", 16))
    lienzo.create_text(900, 400, text=f"🍔 Comida restante: {len(comida_ids)}", fill="black", font=("Arial", 16))
    lienzo.create_text(900, 450, text=f"✅ Particulas que llegaron al ultimo ciclo: {aux_particulas_vivas}", fill="black", font=("Arial", 16))


def actualizar_particulas_simultaneas(particulas, comidas, particula_ids, dimension, comida_ids, start_x=50, start_y=50):
    """
    Actualiza las posiciones de todas las partículas simultáneamente en cada paso de su recorrido.
    """
    max_pasos = len(particulas[len(particulas) - 1].recorrido)  # Determinar el recorrido más largo

    for paso in range(max_pasos):
        for i, particula in enumerate(particulas):
            if paso < len(particula.recorrido):  # Verificar si esta partícula tiene un paso en este ciclo
                x, y = particula.recorrido[paso]

                # Calcular coordenadas en píxeles
                x_px = start_x + x * dimension
                y_px = start_y + y * dimension

                # Verificar si la partícula está en la posición de una comida
                for j in range(len(comidas) - 1, -1, -1):  # Iterar al revés para eliminar comida
                    comida_x, comida_y = comidas[j].Xaxis, comidas[j].Yaxis

                    # Verificar si la partícula está exactamente en la posición de la comida
                    if (x, y) == (comida_x, comida_y):
                        lienzo.delete(comida_ids[j])  # Eliminar comida del lienzo
                        comida_ids.pop(j)  # Eliminar el ID de comida
                        comidas.pop(j)  # Eliminar la comida

                # Verificar si la partícula pasa en línea recta entre dos pasos consecutivos
                if paso > 0:  # Si no es el primer paso
                    x_prev, y_prev = particula.recorrido[paso - 1]  # Paso anterior

                    for j in range(len(comidas) - 1, -1, -1):  # Iterar al revés para eliminar comida
                        comida_x, comida_y = comidas[j].Xaxis, comidas[j].Yaxis

                        # Movimiento vertical
                        if x_prev == x and min(y_prev, y) <= comida_y <= max(y_prev, y) and comida_x == x:
                            lienzo.delete(comida_ids[j])
                            comida_ids.pop(j)
                            comidas.pop(j)
                        # Movimiento horizontal
                        elif y_prev == y and min(x_prev, x) <= comida_x <= max(x_prev, x) and comida_y == y:
                            lienzo.delete(comida_ids[j])
                            comida_ids.pop(j)
                            comidas.pop(j)

                # Actualizar la posición visual de la partícula y su texto
                particula_id, texto_id, identificador_id = particula_ids[i]
                lienzo.coords(identificador_id, x_px, y_px + 10)
                lienzo.coords(particula_id, x_px - 5, y_px - 5, x_px + 5, y_px + 5)
                lienzo.coords(texto_id, x_px, y_px - 15)  # Mover el texto junto con la partícula

        lienzo.update()
        lienzo.after(500)  # Pausa entre pasos





def actualizar_particula(particula, comidas, particula_id, dimension, comida_ids, start_x=50, start_y=50):
    """
    Actualiza la posición de una partícula durante su recorrido, moviendo tanto el óvalo como el texto.
    """
    particula_oval_id, particula_texto_id = particula_id  # Desempaquetar IDs del óvalo y texto
    for i, camino in enumerate(particula.recorrido):
        x1, y1 = camino
        x2, y2 = particula.recorrido[i + 1] if i + 1 < len(particula.recorrido) else camino

        # Ajustar posiciones según la cuadrícula
        x1_px = start_x + x1 * dimension
        y1_px = start_y + y1 * dimension
        x2_px = start_x + x2 * dimension
        y2_px = start_y + y2 * dimension

        # Verificar si la partícula pasa por una posición con comida
        for j in range(len(comidas) - 1, -1, -1):  # Iterar en orden inverso
            comida_x, comida_y = comidas[j].Xaxis, comidas[j].Yaxis

            # Verificar si la comida está exactamente en x1, y1
            if (x1, y1) == (comida_x, comida_y):
                print('Se eliminó en posición exacta')
                lienzo.delete(comida_ids[j])  # Eliminar comida del lienzo
                comida_ids.pop(j)  # Eliminar de los IDs
                comidas.pop(j)  # Eliminar de la lista de comidas
                continue  # Pasar al siguiente elemento

            # Verificar si la comida está en línea recta entre (x1, y1) y (x2, y2)
            if x1 == x2:  # Movimiento vertical
                if comida_x == x1 and min(y1, y2) <= comida_y <= max(y1, y2):
                    print('Se eliminó en línea recta (vertical)')
                    print('Entro en eliminar en medio horizonte')
                    lienzo.delete(comida_ids[j])
                    comida_ids.pop(j)
                    comidas.pop(j)
            elif y1 == y2:  # Movimiento horizontal
                if comida_y == y1 and min(x1, x2) <= comida_x <= max(x1, x2):
                    print('Se eliminó en línea recta (horizontal)')
                    print('Entro en eliminar en medio vertical')
                    lienzo.delete(comida_ids[j])
                    comida_ids.pop(j)
                    comidas.pop(j)



        # Actualizar las coordenadas de la partícula (óvalo)
        lienzo.coords(particula_oval_id, x1_px - 5, y1_px - 5, x1_px + 5, y1_px + 5)

        # Actualizar las coordenadas del texto de la partícula
        lienzo.coords(particula_texto_id, x1_px, y1_px - 10)

        lienzo.update()
        lienzo.after(500)  # Esperar medio segundo antes de hacer la siguiente acción


def main_simulation(cicles, cant_particles, num_puntos, num_comidas, cant_pasos):
    # Aquí va el código de la simulación que quieres ejecutar
    dimension_dibujo = int(height / num_puntos) - 1  # Ajustar según tu pantalla
    simu = ejecutable(cicles, cant_particles, num_puntos)
    simu.super_simulation(cant_pasos, num_comidas)
    comidas = simu.foods_copy
    mega_particulas = simu.mega_particulas
    simulacion(mega_particulas, comidas, dimension_dibujo, num_puntos, cant_particles)

def crear_ventana():
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Configuración y Simulación")
    ventana.configure(bg=AZUL_OSCURO)

    # Variables para los valores configurables
    cicles_var = tk.StringVar(value="3")
    cant_particles_var = tk.StringVar(value="10")
    num_puntos_var = tk.StringVar(value="5")
    num_comidas_var = tk.StringVar(value="5")
    cant_pasos_var = tk.StringVar(value="15")

    # Etiquetas y campos de entrada para los valores
    tk.Label(ventana, text="🔄 Ciclos:", bg=AZUL_OSCURO).grid(row=0, column=0)
    cicles_entry = tk.Entry(ventana, textvariable=cicles_var, bg=AZUL_CLARO, fg="black")
    cicles_entry.grid(row=0, column=1)

    tk.Label(ventana, text="🔴 Cantidad de partículas:", bg=AZUL_OSCURO).grid(row=1, column=0)
    cant_particles_entry = tk.Entry(ventana, textvariable=cant_particles_var, bg=AZUL_CLARO, fg="black")
    cant_particles_entry.grid(row=1, column=1)

    tk.Label(ventana, text="⚫ Número de puntos:", bg=AZUL_OSCURO).grid(row=2, column=0)
    num_puntos_entry = tk.Entry(ventana, textvariable=num_puntos_var, bg=AZUL_CLARO, fg="black")
    num_puntos_entry.grid(row=2, column=1)

    tk.Label(ventana, text="🍔 Número de comidas:", bg=AZUL_OSCURO).grid(row=3, column=0)
    num_comidas_entry = tk.Entry(ventana, textvariable=num_comidas_var, bg=AZUL_CLARO, fg="black")
    num_comidas_entry.grid(row=3, column=1)

    tk.Label(ventana, text="➡️ Cantidad de pasos:", bg=AZUL_OSCURO).grid(row=4, column=0)
    cant_pasos_entry = tk.Entry(ventana, textvariable=cant_pasos_var, bg=AZUL_CLARO, fg="black")
    cant_pasos_entry.grid(row=4, column=1)

    # Variable para el mensaje de error
    error_message = tk.Label(ventana, text="", fg="red", bg=AZUL_OSCURO)
    error_message.grid(row=6, column=0, columnspan=2)

    # Función para validar que se ingresen solo números enteros
    def validar_entrada():
        try:
            cicles = int(cicles_entry.get())
            cant_particles = int(cant_particles_entry.get())
            num_puntos = int(num_puntos_entry.get())
            num_comidas = int(num_comidas_entry.get())
            cant_pasos = int(cant_pasos_entry.get())

            # Validar que todos los valores sean mayores que 0
            if cicles <= 0 or cant_particles <= 0 or num_puntos <= 0 or num_comidas <= 0 or cant_pasos <= 0:
                error_message.config(text="Error: Todos los valores deben ser mayores que 0.")
                return  # No continuar con la simulación si hay valores incorrectos

            # Validar que el número de comidas no exceda el máximo posible
            max_food_possible = (num_puntos - 1) * (num_puntos - 1)
            if num_comidas > max_food_possible:
                error_message.config(text=f"Error: El número máximo de comidas es {max_food_possible}.")
                return  # No continuar con la simulación si el número de comidas es inválido

            # Si todos los valores son correctos, ejecutar la simulación
            ventana.destroy()  # Cerrar la ventana de configuración
            main_simulation(cicles, cant_particles, num_puntos, num_comidas, cant_pasos)  # Ejecutar simulación
        except ValueError:
            error_message.config(text="Error: Todos los valores deben ser números enteros.")

    # Botón para iniciar la simulación
    iniciar_button = tk.Button(ventana, text="Iniciar Simulación", command=validar_entrada, bg=AZUL_BOTON)
    iniciar_button.grid(row=5, column=0, columnspan=2)

    ventana.mainloop()

if __name__ == "__main__":
    crear_ventana()

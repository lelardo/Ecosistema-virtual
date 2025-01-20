import tkinter as tk
from main import *

pantalla = tk.Tk()
pantalla.title("Simulacion Ecosistema")
pantalla.configure(bg="white")
width = 1280
height = 720
lienzo = tk.Canvas(pantalla, width=width, height=height)
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

    return particula_id, texto_id


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


def simulacion(particulas, comidas, dimension_dibujo, num_puntos):
    # Limpiar lienzo antes de iniciar un nuevo ciclo
    lienzo.delete("all")  # Eliminar todos los elementos del lienzo (partículas y comida)

    # Dibujar comida
    comida_ids = []  # Array para guardar los ids de las comidas
    for comida in comidas:
        comida_ids.append(dibujar_comida(comida, dimension_dibujo))  # Dibujar cada comida y guardar su ID
    dibujar_cuadrilla(num_puntos, dimension_dibujo)

    # Texto para indicar el ciclo actual
    texto_ciclo = lienzo.create_text(10, 10, text="Ciclo 1", anchor="nw", fill="black", font=("Arial", 16))

    particula_ids = []  # Lista para almacenar tuplas (ID partícula, ID texto)
    particula_final_ids = []  # Guardamos los ids de las partículas finales

    # Simular el movimiento de todas las partículas simultáneamente
    for ciclo, partic in enumerate(particulas, start=1):
        # Actualizar el mensaje del ciclo
        lienzo.itemconfig(texto_ciclo, text=f"Ciclo {ciclo}")
        lienzo.update()

        # Dibujar las partículas originales para el ciclo actual
        particula_ids = []  # Limpiar las listas de partículas y textos
        particula_final_ids = []

        lienzo.after(1000)
        for p in partic:  # Dibujar las partículas del ciclo actual
            particula_id, texto_id = dibujar_particula(p, dimension_dibujo)
            particula_ids.append((particula_id, texto_id))  # Guardamos la tupla de IDs
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

        # Llamar a la función de eliminación 600 ms después de haber mostrado la partícula final

        lienzo.after(600, eliminar_final_punto())
        lienzo.update()  # Actualizar la vista
    lienzo.create_text(900, 350, text=f"Se acabaron las particulas en el ciclo {ciclo}", fill="black", font=("Arial", 16))


def actualizar_particulas_simultaneas(particulas, comidas, particula_ids, dimension, comida_ids, start_x=50, start_y=50):
    """
    Actualiza las posiciones de todas las partículas simultáneamente en cada paso de su recorrido.
    """
    max_pasos = len(particulas[len(particulas) - 1].recorrido) # Determinar el recorrido más largo

    for paso in range(max_pasos):
        for i, particula in enumerate(particulas):
            if paso < len(particula.recorrido):  # Verificar si esta partícula tiene un paso en este ciclo
                x, y = particula.recorrido[paso]

                # Calcular coordenadas en píxeles
                x_px = start_x + x * dimension
                y_px = start_y + y * dimension

                # Verificar si la partícula está en la posición de una comida
                for j in range(len(comidas) - 1, -1, -1):  # Iterar al revés para eliminar comida
                    if (x, y) == (comidas[j].Xaxis, comidas[j].Yaxis):
                        lienzo.delete(comida_ids[j])  # Eliminar comida del lienzo
                        comida_ids.pop(j)  # Eliminar el ID de comida
                        comidas.pop(j)  # Eliminar la comida

                # Actualizar la posición visual de la partícula y su texto
                particula_id, texto_id = particula_ids[i]
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

        # Verificar si la partícula se encuentra en una posición con comida
        for j in range(len(comidas) - 1, -1, -1):  # Iterar en orden inverso
            if (x1, y1) == (comidas[j].Xaxis, comidas[j].Yaxis):
                print('Se elimino')
                lienzo.delete(comida_ids[j])  # Eliminar comida del lienzo
                comida_ids.pop(j)  # Eliminar de los IDs
                comidas.pop(j)  # Eliminar de la lista de comidas

        # Actualizar las coordenadas de la partícula (óvalo)
        lienzo.coords(particula_oval_id, x1_px - 5, y1_px - 5, x1_px + 5, y1_px + 5)

        # Actualizar las coordenadas del texto de la partícula
        lienzo.coords(particula_texto_id, x1_px, y1_px - 10)

        lienzo.update()
        lienzo.after(500)  # Esperar medio segundo antes de hacer la siguiente acción



def main():
    # valores configurables, SOLO ENTEROS

    cicles = 3  # Puedes modificar para ingresar manualmente
    cant_particles = 5 # CANTIDAD DE PARTICULAS A SIMULAR
    num_puntos = 50 # El numero de puntos por lado de la cuadricula
    num_comidas = 3  # Puedes modificar para ingresar manualmente
    cant_pasos = 10  # Puedes modificar para ingresar

    #elementos de ejecucion, NO TOCARRRR
    if cicles > 0 and num_puntos > 0 and num_comidas > 0 and cant_pasos > 0:
        dimension_dibujo = int(height / num_puntos)-1 # Dimension para dibujar particulas y comida
        simu = ejecutable(cicles, cant_particles, num_puntos)
        global pantalla
        simu.super_simulation(cant_pasos, num_comidas)  # Esto es para poder generar comidas, y particulas en ejecutable
        print("Entroa11")
        comidas = simu.foods_copy # Obtenemos el array de las comidas para poder graficar
        mega_particulas = simu.mega_particulas  # Atributo modificado de ejecutable, ahora tiene una lista de particulas)
        simulacion(mega_particulas, comidas, dimension_dibujo, num_puntos)
        pantalla.mainloop()
    else:
        print("Error: Todos los valores deben ser mayores que 0.")
        pantalla.destroy()

if __name__ == "__main__":
    main()

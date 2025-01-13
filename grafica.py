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
    """
    x = start_x + particula.Xaxis * dimension
    y = start_y + particula.Yaxis * dimension
    return lienzo.create_oval(
        x - 5,
        y - 5,
        x + 5,  # Mantener tamaño original
        y + 5,  # Mantener tamaño original
        fill="blue"
    )

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
    comida_ids = [] # Array para guardar los ids de las comidas, y en caso de ser comidas, poder eliminarlos en la parte visual
    for comida in comidas:
        comida_ids.append(dibujar_comida(comida, dimension_dibujo)) # Por cada comida se dibuja, y lo guardamos para mas tarde borrarlo
    dibujar_cuadrilla(num_puntos, dimension_dibujo)

    # Crear y dibujar la nueva partícula para el ciclo actual
    for particula in particulas:
        particula_id = dibujar_particula(particula, dimension_dibujo)
        # Comienza la animación de la partícula
        lienzo.after(1000)
        actualizar_particula(particula, comidas, particula_id, dimension_dibujo, comida_ids)
        # Termina la función cuando una partícula comienza su animación
        aux = dibujar_particula_final(particula, dimension_dibujo)
        # Hacer que el punto verde sea visible durante 2 o 3 segundos (2 segundos en este caso)
        def eliminar_punto_verde():
            lienzo.delete(aux)  # Eliminar el punto verde después del tiempo determinado

        # Esperar 2000 ms (2 segundos) antes de eliminar el punto verde
        lienzo.after(600, eliminar_punto_verde)

        # Borrar la partícula original después de 1000 ms
        lienzo.after(500, lambda id=particula_id: lienzo.delete(id))

        lienzo.update()


def actualizar_particula(particula, comidas, particula_id, dimension, comida_ids, start_x=50, start_y=50):
    """
    Actualiza la posición de una partícula durante su recorrido.
    """
    x1_px = 0
    y1_px = 0
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

        # Actualizar las coordenadas de la partícula original (su color inicial)
        lienzo.coords(particula_id, x1_px - 5, y1_px - 5, x1_px + 5, y1_px + 5)

        lienzo.update()
        lienzo.after(500)  # Esperar medio segundo antes de hacer la siguiente acción


def main():
    # valores configurables

    cicles = 5  # Puedes modificar para ingresar manualmente
    num_puntos = 10 # El numero de puntos por lado de la cuadricula
    num_comidas = 3  # Puedes modificar para ingresar manualmente
    cant_pasos = 15  # Puedes modificar para ingresar

    #elementos de ejecucion, NO TOCARRRR
    if cicles > 0 and num_puntos > 0 and num_comidas > 0 and cant_pasos > 0:
        dimension_dibujo = int(height / num_puntos) -10 # Dimension para dibujar particulas y comida
        simu = ejecutable(cicles, cicles, num_puntos)
        global pantalla
        simu.simulate(cant_pasos, num_comidas)  # Esto es para poder generar comidas, y particulas en ejecutable
        comidas = simu.foods_copy # Obtenemos el array de las comidas para poder graficar
        particulas = simu.particles  # Atributo modificado de ejecutable, ahora tiene una lista de particulas
        simulacion(particulas, comidas, dimension_dibujo, num_puntos)
        pantalla.mainloop()
    else:
        print("Error: Todos los valores deben ser mayores que 0.")
        pantalla.destroy()

if __name__ == "__main__":
    main()

import tkinter as tk
from main import *

pantalla = tk.Tk()
pantalla.title("Simulacion Ecosistema")
pantalla.configure(bg="white")
width = 1280
height = 720
lienzo = tk.Canvas(pantalla, width=width, height=height)
lienzo.pack()


def dibujar_cuadrilla(dimension):
    for i in range(0, width, dimension):
        lienzo.create_line(i, 0, i, height, fill="black")
        lienzo.create_line(0, i, width, i, fill="black")

#Metodo para dibujar la comida, con un reescalado para poder notar bien la separacion en la pantalla
def dibujar_comida(comidas):
    for comida in comidas:
        if comida.status:
            lienzo.create_oval(
                comida.Xaxis * 20,
                comida.Yaxis * 20,
                comida.Xaxis * 20 + 10,
                comida.Yaxis * 20 + 10,
                fill="red",
                outline="",
            )


def dibujar_particula(particula):
    x, y = particula.Xaxis, particula.Yaxis
    return lienzo.create_oval(x * 20, y * 20, x * 20 + 10, y * 20 + 10, fill="blue")


def simulacion(particulas, comidas, dimension):
    # Limpiar lienzo antes de iniciar un nuevo ciclo
    lienzo.delete("all")  # Eliminar todos los elementos del lienzo (partículas y comida)

    # Dibujar comida
    dibujar_comida(comidas)

    # Crear y dibujar la nueva partícula para el ciclo actual
    for particula in particulas:
        print("Ciclo 1")
        particula_id = dibujar_particula(particula)
        # Comienza la animación de la partícula
        actualizar_particula(particula, comidas, particula_id)
        # Termina la función cuando una partícula comienza su animación
        lienzo.delete(particula_id)


def actualizar_particula(particula, comidas, particula_id):
    for i, camino in enumerate(particula.recorrido):
        x1, y1 = camino
        x2, y2 = particula.recorrido[i + 1] if i + 1 < len(particula.recorrido) else camino
        lienzo.coords(particula_id, x1 * 20, y1 * 20, x1 * 20 + 10, y1 * 20 + 10)
        lienzo.update()
        lienzo.after(1000)


def main():
    cicles = 3 # Puedes modificar para ingresar manualmente
    dimension = width // 20 #Dimension para dibujar particulas y comida
    simu = ejecutable(cicles, dimension, 20)
    global pantalla

    num_comidas = 5  # Puedes modificar para ingresar manualmente
    simu.simulate(5, num_comidas) #Esto es para poder generar comidas, y particulas en ejecutable
    comidas = simu.foods #Nuevo atributo de ejecutable para poder obtener las comidas y dibujarlas despues
    particulas = simu.particles # Atributo modificado de ejecutable, ahora tiene una lista de particulas

    simulacion(particulas, comidas, dimension)
    pantalla.mainloop()


if __name__ == "__main__":
    main()

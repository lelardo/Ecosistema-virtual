import random
import copy
import threading


# Clase que representa una partícula
class particle:
    def __init__(self, name, Xaxis, Yaxis, lifetime, id):
        self.name = name  # nombre de la particula
        self.id = id
        self.Xaxis = Xaxis  # posicion en x
        self.Yaxis = Yaxis  # posicion en y
        self.lifetime = lifetime  # tiempo de vida de la particula, mas bien deberian ser los pasos, pero yo no pongo las reglas
        self.originalTime = lifetime  # guardamos el tiempo original pa cuando coma, le devolvemos la vida que le quitamos
        self.recorrido = [[Xaxis, Yaxis]]  # array pa almacenar los puntos donde pasa
        self.suvive_status = False  # si sobrevive o no al siguiente ciclo

    def presentation(self):  # metodo para presentarse, esto para imprimir su nacimiento
        print(  # lo presentamos al mundo cruel
            "😊 Soy "
            + self.name
            + " y nací en la posición "
            + str(self.Xaxis)
            + ", "
            + str(self.Yaxis)
            + ", mi vida es de ",
            self.lifetime,
        )

    # Método que simula un movimiento aleatorio simple
    # esto es requisito y define los aleatorios
    def simple_random_walk(self):
        return random.choice([True, False])

    # Método que simula un movimiento complejo de la partícula
    def complex_movement(self):
        while self.lifetime > 0:  # mientras la vida no sea 0 o menor demole
            if (
                self.lifetime
                <= 0  # una verificacion extra para cortarlo en caso de vainas
            ):
                print(f"La partícula {self.name} ya ha muerto, terminando el ciclo.")
                break  # Termina el ciclo si la vida es 0 o negativa

            aux_Xaxis = self.Xaxis
            aux_Yaxis = self.Yaxis

            if (
                self.simple_random_walk()
            ):  # nos aventamos el aleatorio pa ver si x o y, True sera x
                if (
                    self.simple_random_walk()
                ):  # ahora en x nos aventamos otro pa ver si palante o patras
                    self.Xaxis += 1  # palante
                    self.lifetime -= 1  # como se movio le quitamos vida, ahorremos comentarios, no lo pondre en los otros
                else:
                    self.Xaxis -= 1  # patras
                    self.lifetime -= 1
            else:
                if (
                    self.simple_random_walk()
                ):  # ahora en y nos aventamos otro pa ver si pariba o pabajo
                    self.Yaxis += 1  # pariba
                    self.lifetime -= 1
                else:
                    self.Yaxis -= 1  # pabajo
                    self.lifetime -= 1

            if (
                self.Xaxis < 0
                or self.Xaxis >= global_dimension
                or self.Yaxis < 0
                or self.Yaxis >= global_dimension
            ):  # si se sale de la dimension
                self.Yaxis = aux_Yaxis  # volvemos a la posicion anterior
                self.Xaxis = aux_Xaxis
                self.lifetime += 1  # le devolvemos la vida que le quitamos, y descartamos el movimiento
            else:
                print(
                    f"Posición actual: ({self.Xaxis}, {self.Yaxis}), vida restante: {self.lifetime}"  # en cada paso tambien imprimimos la posicion y la vida restante
                )
            self.recorrido.append(
                (self.Xaxis, self.Yaxis)
            )  # guardamos la posicion en la que estuvo
            self.has_ate()  # en cada movimiento verificamos si cayo en comidita ica

        print(
            f"La partícula {self.name} ha muerto en la posición ({self.Xaxis}, {self.Yaxis})"
        )  # aqui afuera del ciclo sabemos que murio, veamos donde fue

    def simple_movement(self): 
        # metodo no iterativo para ejecutar un solo movimiento de la particula
        # no revisa si comio, ni es responsable de frenar si ha muerto, eso depende de un metodo externo super_simmulation

        aux_Xaxis = self.Xaxis # valores auxiliares para regresar si se sale de la dimension
        aux_Yaxis = self.Yaxis # lo mismo de arriba

        if (self.simple_random_walk()):  # nos aventamos el aleatorio pa ver si x o y, True sera x
            if (self.simple_random_walk()):  # ahora en x nos aventamos otro pa ver si palante o patras
                self.Xaxis += 1  # palante
            else:
                self.Xaxis -= 1  # patras
        else:
            if (self.simple_random_walk()):  # ahora en y nos aventamos otro pa ver si pariba o pabajo
                self.Yaxis += 1  # pariba
            else:
                self.Yaxis -= 1  # pabajo

        if (
            self.Xaxis < 0
            or self.Xaxis >= global_dimension
            or self.Yaxis < 0
            or self.Yaxis >= global_dimension
            ):  # si se sale de la dimension
            self.Yaxis = aux_Yaxis  # volvemos a la posicion anterior
            self.Xaxis = aux_Xaxis
            self.simple_movement()  # descartamos el movimiento e intentamos nuevamente
        else:
            print(
                f"➡️{"  "}{self.name} , posición actual: ({self.Xaxis}, {self.Yaxis}), vida restante: {self.lifetime}"  # en cada paso tambien imprimimos la posicion y la vida restante
            )
        self.recorrido.append((self.Xaxis, self.Yaxis))  # guardamos la posicion en la que estuvo
        self.has_ate()  # en cada movimiento verificamos si cayo en comidita ica

        if self.lifetime == 0:  # mientras la vida no sea 0 o menor demole
            print(
                f"⛔ La partícula {self.name} ha parado en la posición ({self.Xaxis}, {self.Yaxis})"
            )  # si esta aqui es porque no tiene mas vidas



    # Método que verifica si la partícula ha comido
    def has_ate(self):
        for food_item in global_foods:
            if (
                food_item.status
                and food_item.Xaxis == self.Xaxis
                and food_item.Yaxis == self.Yaxis
            ):
                #food_item.disappear()
                #self.lifetime += self.originalTime #reincio de pasos desactivado por ahora
                self.suvive_status = True  # si come aguanta al siguiente ciclo

                #print(
                #    f"{self.name} comió en la posición {self.Xaxis}, {self.Yaxis}, su vida es ahora {self.lifetime}"
                #)

                #ver el estado de las comidas
                #for food_item in global_foods:
                #    print("Comida ", food_item.Xaxis, food_item.Yaxis, food_item.status)



# Clase que representa la comida
class food:
    def __init__(self, status, Xaxis, Yaxis):
        self.status = status  # estado True es activa, False es porque se la comieron
        self.Xaxis = Xaxis  # eje x
        self.Yaxis = Yaxis  # eje y

    # Método que hace desaparecer la comida
    def disappear(self):
        self.status = False  # la tiramos a false
        self.Xaxis = None  # chau
        self.Yaxis = None  # chau


# Clase que ejecuta la simulación, le iba poner universo pero me parecio muy pretencioso
class ejecutable:
    def __init__(self, cicles, cant_particles, dimension):
        self.foods = []  # array de comidas
        self.cicles = cicles  # ciclos pa la simulacion
        self.cant_particles = cant_particles  # la partícula, actualmente solo es una, pero podria ser un array de particulas
        self.dimension = dimension  # dimension del universo, solo recibimos una porque va a ser cuadrado a menos que esto se cambie, lo que nos joderia mucho, ojala quen o pase
        self.particles = []  # arreglo de particulas
        self.foods_copy = (
            []
        )  # Arreglo auxiliar para poder llevar las comidas a una interfaz grafica
        print(  # info util
            "La simulacion se ejecutara por",
            cicles,
            "ciclos, con las dimensiones de ",
            dimension,
            "x",
            dimension,
        )

        global global_dimension  # programacion sucia cochina puerca, pero asi toca, si encuentras una alternativa que no perjudique mi curriculum me dices
        global_dimension = (
            self.dimension
        )  # la copio pa mandarla a la partícula, es otra pa no ser mas puercos

        global global_foods  # otro caso de programacion asquerosa, revisar
        global_foods = self.foods  # otra copia que se manda a particula

    # Método que elige un nombre aleatorio de una lista, me gusta que las particulas tengan identidad
    # creo que es un poco pesado de ejecutar, posible descarte
    def select_name(self):
        # Abrir el archivo nombres.txt y leer los nombres
        # si puedes pon algunos nombres chistosos ahi
        with open("nombres.txt", "r", encoding="utf-8") as archivo:
            nombres = archivo.readlines()  # Lee todas las líneas del archivo

        # Eliminar los saltos de línea al final de cada nombre
        nombres = [nombre.strip() for nombre in nombres]

        # Elegir un nombre aleatorio de la lista
        nombre_elegido = random.choice(nombres)

        return nombre_elegido

    def create_particle(self, lifetime, name, id):  
        # aqui creo la particula, pide los datos basicos como se llama y cuanto vive
        # recuerda que siempre aparecen en los bordes, por eso es que si o si una es 0, de lo contrario estaran adentradas en el mapa
        # puse el random walk para particula, piensas que deberiamos sacarla? digo, para aprovecharla en ocasiones como esta
        if random.choice([True, False]):  # si es true optamos por algun margen de x
            x = random.choice(
                [0, self.dimension - 1]
            )  # sera el margen de x mas bajo o mas alto, 0 o top
            y = random.randint(
                0, self.dimension - 1
            )  # y sera el que sea, igual no saldra de x
        else:  # de lo contrario optamos por algun margen de y
            x = random.randint(0, self.dimension - 1)  # cualquier valor pa x
            y = random.choice(
                [0, self.dimension - 1]
            )  # el y sera el borde izquierdo (0) o el derecho (top)

        return particle(name, x, y, lifetime, id)  # la mandamos bien peinadita a la particula

    # Método que crea la comida en la simulación, nomas te pide la cantidad
    # de aumentar los atributos de la comida, creo que sufriremos aqui
    def create_food(self, quantity):
        # Calcular el número máximo de posiciones disponibles, para saber cuanto puede haber de comida y no exceder
        max_food_possible = (self.dimension - 1) * (self.dimension - 1)

        # si la comida se pide negativa o excede el limite, cerramos el programa, me gustaria que se pueda volver a solicitar
        if quantity < 0:
            print("Error: La cantidad de comida no puede ser negativa.")
            exit()  # Detiene el programa si la cantidad es negativa
        elif quantity > max_food_possible:
            print(
                f"Error: La cantidad de comida solicitada ({quantity}) excede el límite máximo de {max_food_possible}."
            )
            exit()  # Detiene el programa si la cantidad excede el límite

        # Función que verifica si una posición ya está ocupada
        # esto se debe de optimizar, pero no se me ocurre como, si se te ocurre algo me dices
        # digo que se debe de optimizar por que es fuerza bruta, de haber mucha comida tardara revisando la posicion de cada una
        def is_position_occupied(
            x, y
        ):  # submetodo, va aqui porque es exclusivo de esta funcionalidad
            for food_item in self.foods:  # por cada comida
                if (
                    food_item.Xaxis == x and food_item.Yaxis == y
                ):  # si la comida esta en la posicion que queremos revisar
                    return True
            return False

        # Crear comida
        for i in range(quantity):  # por cada comida que se quiera crear
            while True:  # es while porque si la posicion esta ocupada, se repite
                # Generar posición aleatoria
                Xaxis = random.randint(1, self.dimension - 1)
                Yaxis = random.randint(1, self.dimension - 1)

                # Verificar si la posición está ocupada
                if not is_position_occupied(
                    Xaxis, Yaxis
                ):  # esto no es recursividad, es otro metodo mira bien
                    self.foods.append(
                        food(True, Xaxis, Yaxis)
                    )  # mandamos la nueva comida calientita al array de comidas
                    break  # Salir del ciclo while cuando la posición es válida

            print(
                "🍎 Comida en la posición", Xaxis, Yaxis
            )  # imprimimos la posicion de la comida
        print("----------------------------------------------")

    # Método que ejecuta la simulación, este es el duro, pero por ahora jala pa uno nomas, cambiar si o si
    def simulate(
        self, lifetime, food_quantity
    ):  # aqui se ejecuta la simulacion, pide el nombre de la particula, cuanto vive y cuanta comida
        self.create_food(food_quantity)  # creamos la comida
        self.foods_copy = copy.deepcopy(
            self.foods
        )  # copiamos la comida para la particula
        print("----------------------------------------------")
        for i in range(
            self.cicles
        ):  # repetimos la simulacion por el numero de ciclos que se pidio
            print("Ciclo ", i + 1)  # informamos el ciclo actual
            print("----------------------------------------------")
            for i in range(self.cant_particles):  # por cada particula que se quiera crear
                aux = self.create_particle(lifetime, self.select_name(), i)  # creamos la particula y la agregamos
            print("----------------------------------------------")

            aux.presentation()  # presentamos a la particula
            # Ejecuta el movimiento complejo de la partícula durante el número de ciclos especificado
            aux.complex_movement()
            print("----------------------------------------------")
            self.particles.append(aux)  # limpiamos el array de particulas para el siguiente ciclo


    def check_ate(self): 
        # metodo para checar en tiempo real si alguna o varias particulas comieron
        # para cada comida revisara si alguien la comio, como son varias particulas no podemos desaparecerla al instante
        # necesitamos ver si varias particulas la comieron al mismo instante antes de desvanecerla
        # finalmente, a las que comieron les permitimos sobrevivir
        someone_ate = False
        for i in range(len(self.foods)):
            for j in range(len(self.particles)):
                if (self.foods[i].Xaxis == self.particles[j].Xaxis
                    and self.foods[i].Yaxis == self.particles[j].Yaxis):
                    someone_ate = True
                    print("🍽  La partícula ", self.particles[j].name, " ha comido en la posición ", self.foods[i].Xaxis, ", ", self.foods[i].Yaxis)

            if someone_ate:
                    self.foods[i].disappear()
                    someone_ate = False

    def restore_health(self):
        for i in range(len(self.particles)):
            self.particles[i].lifetime = self.particles[i].originalTime
            self.particles[i].suvive_status = False
    
    def depurate_particles(self):
        for i in range(len(self.particles) -1, -1, -1):
            print("🔍 Revisando si la partícula ", self.particles[i].name, " con estado ", self.particles[i].suvive_status,"")
            if self.particles[i].suvive_status == False:
                self.particles.pop(i)
                self.cant_particles -= 1
                

    def super_simulation(self, lifetime, food_quantity):
        self.create_food(food_quantity)

        for i in range(self.cant_particles):
            self.particles.append(self.create_particle(lifetime, self.select_name(), i))
            self.particles[i].presentation()
            print("----------------------------------------------")

        for i in range(self.cicles):  # repetimos la simulacion por el numero de ciclos que se pidio
            print("🔄 Ciclo ", i + 1)  # informamos el ciclo actual
            print("----------------------------------------------")

            if self.cant_particles == 0:
                print("🚫 No hay partículas en el ciclo ", i + 1)
                exit()

            for i in range(self.cant_particles):
                self.particles[i].presentation()
                print("----------------------------------------------")

            for _ in range(lifetime):
                for i in range(self.cant_particles):
                    self.particles[i].simple_movement()
                    self.particles[i].lifetime -= 1
                self.check_ate()
                print("----------------------------------------------")
            for _ in range(self.cant_particles):
                if self.particles[_].suvive_status:
                    print("✅ La partícula ", self.particles[_].name, " ha sobrevivido al ciclo")
                else:
                    print("💀 La partícula ", self.particles[_].name, " ha muerto")
            print("----------------------------------------------")

            self.depurate_particles()
            self.restore_health()

            

if __name__ == "__main__":
    sim = ejecutable(cicles=2, cant_particles=3, dimension=5)
    sim.super_simulation(3, 5)

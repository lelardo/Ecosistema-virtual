import random
import copy


# Método que simula un movimiento aleatorio simple
# esto es requisito y define los aleatorios
def simple_random_walk():
    return random.choice([True, False])

# Clase que representa una partícula


class particle:
    def __init__(self, name, Xaxis, Yaxis, lifetime, id):
        self.name = name  # nombre de la particula
        self.id = id
        self.Xaxis = Xaxis  # posicion en x
        self.Yaxis = Yaxis  # posicion en y
        self.full_food = False  # si esta lleno o no
        self.superpower = False  # si tiene superpoderes
        self.step_size = 1  # tamaño de paso
        
        self.hunting = False  # si esta cazando o no
        self.target_food = None  # comida que esta cazando
        self.smell_range = 2 # rango de olfato, es una varible que a futuro pueda ser mejorada

        # tiempo de vida de la particula, mas bien deberian ser los pasos, pero yo no pongo las reglas
        self.lifetime = lifetime
        # guardamos el tiempo original pa cuando coma, le devolvemos la vida que le quitamos
        self.originalTime = lifetime
        # array pa almacenar los puntos donde pasa
        self.recorrido = [[Xaxis, Yaxis]]
        self.suvive_status = False  # si sobrevive o no al siguiente ciclo
        self.changing_cycle = False

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

    def detect_food_in_range(self):
            if self.target_food and self.target_food.status:
                return  # Si ya tiene objetivo y sigue existiendo, mantenerlo
                
            self.target_food = None
            self.hunting = False
            
            for food in global_foods:
                if not food.status:
                    continue
                    
                dx = abs(food.Xaxis - self.Xaxis)
                dy = abs(food.Yaxis - self.Yaxis)
                
                if dx <= self.smell_range and dy <= self.smell_range:
                    self.target_food = food
                    self.hunting = True
                    print(f"👃 {self.name} ha detectado comida en ({food.Xaxis}, {food.Yaxis})")
                    break

    def simple_movement(self):
        aux_paso_incorrecto = False; # Variable para comprobar si la particula se salio de la dimension, o dio un paso inccorecto
        #self.detect_food_in_range()
        aux_Xaxis = self.Xaxis
        aux_Yaxis = self.Yaxis
        
        if self.hunting and self.target_food:
            # Move one step towards food
            if abs(self.Xaxis - self.target_food.Xaxis) >= abs(self.Yaxis - self.target_food.Yaxis):
                # Move in X direction first
                if self.Xaxis < self.target_food.Xaxis:
                    self.Xaxis += self.step_size
                else:
                    self.Xaxis -= self.step_size
            else:
                # Move in Y direction first
                if self.Yaxis < self.target_food.Yaxis:
                    self.Yaxis += self.step_size
                else:
                    self.Yaxis -= self.step_size
        else:
            # Random movement
            if simple_random_walk():
                if simple_random_walk():
                    self.Xaxis += self.step_size
                else:
                    self.Xaxis -= self.step_size
            else:
                if simple_random_walk():
                    self.Yaxis += self.step_size
                else:
                    self.Yaxis -= self.step_size

        if self.step_size == 1:
            if (((self.Xaxis < 0) and (aux_Xaxis == 0))
                or ((self.Xaxis >= global_dimension) and (aux_Xaxis == global_dimension-1))
                or ((self.Yaxis < 0) and (aux_Yaxis == 0))
                or ((self.Yaxis >= global_dimension) and (aux_Yaxis == global_dimension-1))):
                self.Yaxis = aux_Yaxis
                self.Xaxis = aux_Xaxis
                print("me sali de la dimension con un pasito")
                aux_paso_incorrecto = True # Si la particula se sale de la dimension, se marca como paso incorrecto
            else:
                print(f"➡️{'  '}{self.name} , posición actual: ({self.Xaxis}, {self.Yaxis}), vida restante: {self.lifetime}")
        else:
            if (aux_Xaxis == 0 and self.Xaxis < 0
                or aux_Yaxis == 0 and self.Yaxis < 0
                or aux_Xaxis == global_dimension - 1 and self.Xaxis >= global_dimension
                or aux_Yaxis == global_dimension - 1 and self.Yaxis >= global_dimension):
                self.Yaxis = aux_Yaxis
                self.Xaxis = aux_Xaxis
                print("me sali de la dimension con superpoder")
                aux_paso_incorrecto = True # Si la particula se sale de la dimension, se marca como paso incorrecto
            else:
                if self.Xaxis < 0:
                    self.Xaxis = 0
                    print("me sali atras de x")
                if self.Xaxis >= global_dimension:
                    self.Xaxis = global_dimension - 1
                    print("me sali adelante de x")
                if self.Yaxis < 0:
                    self.Yaxis = 0
                    print("me sali atras de y")
                if self.Yaxis >= global_dimension:
                    self.Yaxis = global_dimension - 1
                    print("me sali adelante de y")
                print(f"➡️{'  '}{self.name} , posición actual: ({self.Xaxis}, {self.Yaxis}), vida restante: {self.lifetime}")

            x_range = range(min(aux_Xaxis, self.Xaxis), max(aux_Xaxis, self.Xaxis) + 1)
            y_range = range(min(aux_Yaxis, self.Yaxis), max(aux_Yaxis, self.Yaxis) + 1)
            if not self.changing_cycle:
                for i in range(len(global_foods)):
                    if (global_foods[i].Xaxis in x_range and global_foods[i].Yaxis in y_range) and not (global_foods[i].Xaxis == self.Xaxis and global_foods[i].Yaxis == self.Yaxis):
                        print(f"🍽  La partícula {self.name} ha pillado comida en la posición intermedia ({global_foods[i].Xaxis}, {global_foods[i].Yaxis})")
                        global_foods[i].disappear()

        if not aux_paso_incorrecto: # Comprobamos si la particula dio un paso incorrecto
            self.recorrido.append((self.Xaxis, self.Yaxis)) # Si el paso fue correcto, almacenamos la posicion en el recorrido
        else:
            self.simple_movement() # En caso de que el paso haya sido incorrecto, se vuelve a llamar al metodo para que la particula de un paso correcto

        if self.lifetime == 0:
            print(f"⛔ La partícula {self.name} ha parado en la posición ({self.Xaxis}, {self.Yaxis})")


    def upgrade_step(self):  # metodo para mejorar el tamaño de paso
        self.step_size += 1  # aumentamos el tamaño de paso en 1]
        self.superpower = True  # ahora tiene superpoderes
        print(f"🚀 La partícula {
              self.name} ha obtenido un superpoder, su tamaño de paso ha aumentado a {self.step_size}")



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
        # la partícula, actualmente solo es una, pero podria ser un array de particulas
        self.cant_particles = cant_particles
        self.dimension = dimension  # dimension del universo, solo recibimos una porque va a ser cuadrado a menos que esto se cambie, lo que nos joderia mucho, ojala quen o pase
        self.particles = []  # arreglo de particulas
        # mapeado de las comidas para identificar zonas circuindantes
        self.foodmap = [[None for i in range(dimension)] for j in range(dimension)]
        self.foods_copy = (
            []
        )  # Arreglo auxiliar para poder llevar las comidas a una interfaz grafica
        self.mega_particulas = []  # Arreglo para guardar las particulas por cada simulacion
        print(  # info util
            "La simulacion se ejecutara por",
            cicles,
            "ciclos, con las dimensiones de ",
            dimension,
            "x",
            dimension,
        )
        print("----------------------------------------------")

        # programacion sucia cochina puerca, pero asi toca, si encuentras una alternativa que no perjudique mi curriculum me dices
        global global_dimension
        global_dimension = (
            self.dimension
        )  # la copio pa mandarla a la partícula, es otra pa no ser mas puercos

        global global_foods  # otro caso de programacion asquerosa, revisar
        global_foods = self.foods  # otra copia que se manda a particula

        global global_food_map
        global_food_map = self.foodmap

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
        if simple_random_walk():  # si es true optamos por algun margen de x
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

        # la mandamos bien peinadita a la particula
        return particle(name, x, y, lifetime, id)

    def restar_locations(self):
        for i in range(len(self.particles)):
            self.particles[i].changing_cycle = True
            if random.choice([True, False]):  # si es true optamos por algun margen de x
                x = random.choice(
                    [0, self.dimension - 1]
                )  # sera el margen de x mas bajo o mas alto, 0 o top
                y = random.randint(
                    0, self.dimension - 1
                )  # y sera el que sea, igual no saldra de x
            else:  # de lo contrario optamos por algun margen de y
                # cualquier valor pa x
                x = random.randint(0, self.dimension - 1)
                y = random.choice(
                    [0, self.dimension - 1]
                )  # el y sera el borde izquierdo (0) o el derecho (top)
            self.particles[i].Xaxis = x
            self.particles[i].Yaxis = y
            print(f"La partícula {
                  self.particles[i].name} ha sido reubicada en la posición ({x}, {y})")
            self.particles[i].changing_cycle = False
            self.particles[i].recorrido.append((x, y)) # Se añade punto de origen a la particula

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
                f"Error: La cantidad de comida solicitada ({quantity}) excede el límite máximo de {
                    max_food_possible}."
            )
            exit()  # Detiene el programa si la cantidad excede el límite

        # Función que verifica si una posición ya está ocupada
        # esto se debe de optimizar, pero no se me ocurre como, si se te ocurre algo me dices
        # digo que se debe de optimizar por que es fuerza bruta, de haber mucha comida tardara revisando la posicion de cada una
        def is_position_occupied(x, y):  # submetodo, va aqui porque es exclusivo de esta funcionalidad
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
                Xaxis = random.randint(0, self.dimension - 1)
                Yaxis = random.randint(0, self.dimension - 1)
                
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

    def check_ate(self):
        # metodo para checar en tiempo real si alguna o varias particulas comieron
        # para cada comida revisara si alguien la comio, como son varias particulas no podemos desaparecerla al instante
        # necesitamos ver si varias particulas la comieron al mismo instante antes de desvanecerla
        # finalmente, a las que comieron les permitimos sobrevivir
        fighters = []  # arreglo para guardar los indices de las particulas que pelearan
        for i in range(len(self.foods)):  # para todas las comidas
            for j in range(len(self.particles)):  # revisemos las particulas
                if (self.foods[i].Xaxis == self.particles[j].Xaxis  # si la particula esta en la misma posicion que la comida
                        and self.foods[i].Yaxis == self.particles[j].Yaxis):
                    # guardamos el indice de la particula que peleara
                    fighters.append(j)
            winner = self.epic_battle(fighters)  # peleamos
            if winner != None:  # si hay ganador
                print("🍽  La partícula ", self.particles[winner].name, " ha comido en la posición ",
                      self.foods[i].Xaxis, ", ", self.foods[i].Yaxis)

                # si tiene superpoderes
                if self.particles[winner].full_food and not self.particles[winner].superpower:
                    self.particles[winner].upgrade_step()
                    self.particles[winner].direction = None
                else:
                    # la dejamos vivir
                    self.particles[winner].suvive_status = True
                    # le damos superpoderes
                    self.particles[winner].full_food = True
                    self.particles[winner].direction = None
                winner = None  # reseteamos el ganador
                fighters.clear()  # limpiamos el arreglo de peleadores
                self.foods[i].disappear()

    # metodo para que peleen las comidas
    # recibe el arreglo con los indices de las particulas que pelearan
    def epic_battle(self, array):
        if not array:  # si no hay nadie que pelee
            return None  # regresamos nada
        # aleatoriamente elige el indice de la ganadora y lo retorna
        return array[random.randint(0, len(array) - 1)]

    def restore_health(self):
        for i in range(len(self.particles)):
            self.particles[i].lifetime = self.particles[i].originalTime
            self.particles[i].suvive_status = False
            self.particles[i].superpower = False
            self.particles[i].full_food = False

    def depurate_particles(self):
        for i in range(len(self.particles) - 1, -1, -1):
            # print("🔍 Revisando si la partícula ",
            #      self.particles[i].name, " con estado ", self.particles[i].suvive_status, "")
            if self.particles[i].suvive_status == False:
                self.particles.pop(i)
                self.cant_particles -= 1

    def super_simulation(self, lifetime, food_quantity):
        self.create_food(food_quantity)
        self.foods_copy = copy.deepcopy(self.foods)

        for i in range(self.cant_particles):
            self.particles.append(self.create_particle(
                lifetime, self.select_name(), i))

        # repetimos la simulación por el número de ciclos que se pidió
        for i in range(self.cicles):
            print("🔄 Ciclo ", i + 1)  # informamos el ciclo actual
            print("----------------------------------------------")

            if i != 0:
                self.restar_locations()

            if self.cant_particles == 0:
                print("🚫 No hay partículas en el ciclo ", i + 1)
                continue

            for i in range(self.cant_particles):
                self.particles[i].presentation()
                print("----------------------------------------------")

            for _ in range(lifetime):
                for i in range(self.cant_particles):
                    self.particles[i].simple_movement()
                    self.particles[i].lifetime -= 1
                        
                self.check_ate()
                print("----------------------------------------------")

            self.mega_particulas.append(copy.deepcopy(self.particles))

            for _ in range(self.cant_particles):
                if self.particles[_].suvive_status:
                    print("✅ La partícula ",
                          self.particles[_].name, " ha sobrevivido al ciclo")
                else:
                    print("💀 La partícula ",
                          self.particles[_].name, " ha muerto")
            print("----------------------------------------------")

            for i in range(self.cant_particles):
                self.particles[i].recorrido = [] # Reiniciamos el recorrido para poder graficar de mejor manera
            # Depurar y reiniciar atributos para el próximo ciclo
            self.depurate_particles()
            self.restore_health()


if __name__ == "__main__":
    sim = ejecutable(cicles=1, cant_particles=4, dimension=6)
    sim.super_simulation(lifetime=7, food_quantity=10)

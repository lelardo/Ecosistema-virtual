import matplotlib.pyplot as plt
from collections import defaultdict

def plot_points_with_repeated_paths(points, title="Trayectoria del arreglo"):
    """
    Grafica los puntos de un arreglo, resaltando las líneas recorridas más de una vez.

    :param points: Lista de tuplas (x, y) representando las coordenadas a graficar.
    :param title: Título del gráfico.
    """
    if not points:
        print("El arreglo de puntos está vacío. Nada que graficar.")
        return

    # Extraer los segmentos entre puntos y contar repeticiones
    segment_counts = defaultdict(int)
    for i in range(len(points) - 1):
        segment = tuple(sorted([points[i], points[i + 1]]))  # Ordenar para evitar (A, B) y (B, A) como diferentes
        segment_counts[segment] += 1

    # Crear el gráfico
    plt.figure(figsize=(8, 8))
    plt.gca().set_aspect('equal', adjustable='box')
    
    
    
    for i in range(len(points) - 1):
        # Extraer los puntos del segmento actual
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        # Calcular la frecuencia del segmento
        segment = tuple(sorted([(x1, y1), (x2, y2)]))
        count = segment_counts[segment]
        
        # Ajustar la transparencia en función de la frecuencia
        alpha = min(1.0, 0.4 + 0.2 * count)  # Más opaco si se recorre más veces
        plt.plot([x1, x2], [y1, y2], color='blue', alpha=alpha, linewidth=2)

    # Puntos de inicio y fin
    x_coords, y_coords = zip(*points)
    plt.scatter(x_coords[0], y_coords[0], color='green', label="Inicio")  # Punto de inicio
    plt.scatter(x_coords[-1], y_coords[-1], color='red', label="Fin")  # Punto final

    # Personalizar el gráfico
    plt.title(title)
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.legend()
    plt.grid(True)

    # Mostrar el gráfico
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    puntos = [
        (4, 5), (4, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), 
        (4, 2), (4, 3), (4, 2), (4, 3), (3, 3), (3, 4), (2, 4),
        (2, 3), (2, 2), (1, 2), (2, 2), (1, 2), (0, 2), (0, 1),
        (0, 2), (0, 3), (0, 2), (1, 2)
    ]
    plot_points_with_repeated_paths(puntos)

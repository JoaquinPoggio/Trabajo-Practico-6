class Grafo:
    def __init__(self, dirigido=False):
        self.vertices = {}

    def insertar_vertices(self, vertice):
        if vertice not in self.vertices:
            self.vertices[vertice]=[]
    
    def insertar_aristas(self, vertice1, vertice2, peso):
        if vertice1 in self.vertices and vertice2 in self.vertices:
            self.vertices[vertice1].append((vertice2, peso))
            self.vertices[vertice2].append((vertice1, peso))

    def obtener_aristas(self):
        aristas = []
        for vertice in self.vertices:
            for adyacente, peso in self.vertices[vertice]:
                if (adyacente, vertice, peso) not in aristas:
                    aristas.append((adyacente, vertice, peso))
        return aristas
    
    def kruskal(self):
        aristas = self.obtener_aristas()
        aristas.sort(key=lambda arista:arista[2])
        padre = {}
        rango = {}

        def encontrar_vertice(vertice):
            if padre[vertice] != vertice:
                padre[vertice] = encontrar_vertice(padre[vertice])
            return padre[vertice]
        
        def unir_vertices(vertice1, vertice2):
            raiz1 = encontrar_vertice(vertice1)
            raiz2 = encontrar_vertice(vertice2)
            if rango[raiz1] > rango[raiz2]:
                padre[raiz2] = raiz1
                raiz_unido = raiz1
            else:
                padre[raiz1] = raiz2
                raiz_unido = raiz2
                if rango[raiz1]==rango[raiz2]:
                    rango[raiz2] += 1
        
        for vertice in self.vertices:
            padre[vertice]=vertice
            rango[vertice]= 0
        
        arbol_expansion = []
        for vertice1, vertice2, peso in aristas:
            if encontrar_vertice(vertice1) != encontrar_vertice(vertice2):
                unir_vertices(vertice1, vertice2)
                arbol_expansion.append((vertice1, vertice2, peso))
        
        metros_cable = sum(peso for _, _, peso in arbol_expansion)
        print(f"Metros de cable para conectar los ambientes {metros_cable}")
        return arbol_expansion
    
    def dijkstra(self, inicio, fin):
        import heapq
        distancias = {vertice: float('Infinity') for vertice in self.vertices}
        distancias[inicio] = 0
        cola_de_prioridad = [(0, inicio)]
        padre = {inicio: None}

        while cola_de_prioridad:
            distancia_actual, vertice_actual = heapq.heappop(cola_de_prioridad)
            if vertice_actual == fin:
                break
            for adyacente, peso in self.vertices[vertice_actual]:
                distacia = distancia_actual + peso
                if distacia < distancias[adyacente]:
                    distancias[adyacente]= distacia
                    padre[adyacente]=vertice_actual
                    heapq.heappush(cola_de_prioridad, (distacia, adyacente))
    
        camino = []
        actual = fin
        while actual is not None:
            camino.insert(0, actual)
            actual = padre[actual]
        print(f"El camino mas corto de {inicio} a {fin} es")
        for vertice in camino:
            print(vertice)
        print(f"Los mts de cable necesarios para conectar el cable del router al SMART son {distancias[fin]} mts")
        return camino, distancias[fin]
    
grafo = Grafo()
ambientes = ["cocina", "comedor", "cochera", "quincho",
    "baño 1", "baño 2", "habitacion 1", "habitacion 2",
    "sala de estar", "terraza", "patio"
    ]

for ambiente in ambientes:
    grafo.insertar_vertices(ambiente)

aristas = [
    ("cocina", "comedor", 5),
    ("cocina", "baño 1", 8),
    ("cocina", "habitación 1", 10),
    ("comedor", "sala de estar", 6),
    ("comedor", "terraza", 7),
    ("comedor", "patio", 9),
    ("cochera", "patio", 10),
    ("cochera", "quincho", 12),
    ("cochera", "comedor", 15),
    ("quincho", "terraza", 10),
    ("quincho", "habitacion 2", 12),
    ("baño 1", "habitacion 1", 5),
    ("baño 1", "sala de estar", 12),
    ("baño 2", "habitacion 2", 6),
    ("habitacion 1", "habitacion 2", 8),
    ("habitacion 1", "baño 2", 10),
    ("habitacion 2", "sala de estar", 4),
    ("sala de estar", "terraza", 5),
    ("terraza", "patio", 10)
]

for vertice1, vertice2, peso in aristas:
    grafo.insertar_aristas(vertice1, vertice2, peso)

grafo.kruskal()
grafo.dijkstra("habitacion 1", "sala de estar")
class HeapMin():

    def __init__(self):
        self.elements = []
    
    def add(self, value):
        self.elements.append(value)
        self.float(len(self.elements)-1)

    def remove(self):
        if len(self.elements) > 0:
            self.interchange(0, len(self.elements)-1)
            value = self.elements.pop()
            self.sink(0)
            return value
        else:
            return None

    def interchange(self, index_1, index_2):
        self.elements[index_1], self.elements[index_2] = self.elements[index_2], self.elements[index_1]

    def float(self, index):
        father = (index-1) // 2
        while index > 0 and self.elements[index] < self.elements[father]:
            self.interchange(index, father)
            index = father
            father = (index-1) // 2

    def sink(self, index):
        left_child = (index * 2) + 1
        control = True
        while control and left_child < len(self.elements):
            right_child = (index * 2) + 2
            min = left_child
            if right_child < len(self.elements):
                if self.elements[right_child] < self.elements[left_child]:
                    min = right_child
            if self.elements[index] > self.elements[min]:
                self.interchange(index, min)
                index = min
                left_child = (index * 2) + 1
            else:
                control = False

    def heapify(self, elements):
        self.elements = elements
        for i in range(len(self.elements)):
            self.float(i)

    def sort(self):
        result = []
        amount_elements = len(self.elements)
        for i in range(amount_elements):
            value = self.remove()
            result.append(value)
        return result

    def search(self, value):
        for index, element in enumerate(self.elements):
            if element[1][0] == value:
                return index

    def arrive(self, value, priority):
        self.add([priority, value])

    def atention(self):
        return self.remove()

    def change_proirity(self, index, new_priority):
        if index < len(self.elements):
            previous_priority = self.elements[index][0]
            self.elements[index][0] = new_priority
            if new_priority < previous_priority:
                self.float(index)
            elif new_priority > previous_priority:
                self.sink(index)

class Grafo:
    def __init__(self, dirigido=False):
        self.elements = []
        self.dirigido = dirigido

    def insert_vertice(self, value, tipo, paises):
        nodo = {
            'value': value,
            'aristas': [],
            'visitado': False,
            'tipo': tipo,
            'paises': paises
        }
        self.elements.append(nodo)

    def insert_arista(self, origen, destino, peso):
        pos_origen = self.search(origen)
        pos_destino = self.search(destino)
        if pos_origen is not None and pos_destino is not None:
            arista_origen = {
                'value': destino,
                'peso' : peso
            }
        self.elements[pos_origen]['aristas'].append(arista_origen)
        if not self.dirigido:
            arista_destino = {
                'value' : origen,
                'peso' : peso
                }
            self.elements[pos_destino]['aristas'].append(arista_destino)
    
    def search(self, value):
        for index, element in enumerate(self.elements):
            if element['value'] == value:
                return index
        return None

    def kruskal(self):
        def buscar_en_bosque(bosque, buscado):
            for index, arbol in enumerate(bosque):
                if buscado in arbol:
                    return index
                
        bosque = [{nodo['value']} for nodo in self.elements]
        aristas = HeapMin()
        
        for nodo in self.elements:
            bosque.append(nodo['value'])
            adjacentes = nodo['aristas']
            for adjacente in adjacentes:
                aristas.arrive([nodo['value'], adjacente['value']], adjacente['peso'])
    
        resultado_arbol = []
        while len(bosque) > 1 and len(aristas.elements) > 0:
            arista = aristas.atention()
            origen = buscar_en_bosque(bosque, arista[1][0])
            destino = buscar_en_bosque(bosque, arista[1][1])
            if origen != destino:
                resultado_arbol.append((arista[1][0], arista[1][1], arista[0]))
                bosque[origen].update(bosque[destino])
                bosque.pop(destino)

        return resultado_arbol
    
    def mostrar_grafo(self):
        for nodo in self.elements:
            print(f"{nodo['value']} ({nodo['tipo']}) - Paises: {' , ' .join(nodo['paises'])}")
            for arista in nodo['aristas']:
                print(f"Conecta con {arista['value']} - Distancia: {arista['peso']}")

    def paises_con_ambas_maravillas(self):
        pais_maravillas = {}
        for nodo in self.elements:
            for pais in nodo['paises']:
                if pais not in pais_maravillas:
                    pais_maravillas[pais] = {'natural': 0, 'arquitectonica': 0}
                pais_maravillas[pais][nodo['tipo']] += 1

        paises_ambas = [pais for pais, tipos in pais_maravillas.items() if tipos['natural'] > 0 and tipos['arquitectonica'] > 0]
        return paises_ambas
    
    def paises_varias_misma_tipo(self):
        pais_maravillas = {}
        for nodo in self.elements:
            for pais in nodo['paises']:
                if pais not in pais_maravillas:
                    pais_maravillas[pais] = {'natural': 0, 'arquitectonica': 0}
                pais_maravillas[pais][nodo['tipo']] += 1

        paises_multiples = {pais: tipos for pais, tipos in pais_maravillas.items() if tipos['natural'] > 1 or tipos['arquitectonica'] > 1}
        return paises_multiples


grafo = Grafo(dirigido=False)
grafo.insert_vertice("Taj Mahal", "arquitectónica", ["India"])
grafo.insert_vertice("Cristo Redentor", "arquitectónica", ["Brasil"])
grafo.insert_vertice("Machu Picchu", "arquitectónica", ["Perú"])
grafo.insert_vertice("Chichen Itza", "arquitectónica", ["México"])
grafo.insert_vertice("Coliseo", "arquitectónica", ["Italia"])
grafo.insert_vertice("Petra", "arquitectónica", ["Jordania"])
grafo.insert_vertice("Gran Muralla China", "arquitectónica", ["China"])

grafo.insert_vertice("Amazonas", "natural", ["Brasil", "Colombia", "Perú"])
grafo.insert_vertice("Bahía de Ha-Long", "natural", ["Vietnam"])
grafo.insert_vertice("Iguazú", "natural", ["Argentina", "Brasil"])
grafo.insert_vertice("Isla de Jeju", "natural", ["Corea del Sur"])
grafo.insert_vertice("Parque Nacional de Komodo", "natural", ["Indonesia"])
grafo.insert_vertice("Río Subterráneo de Puerto Princesa", "natural", ["Filipinas"])
grafo.insert_vertice("Montaña de la Mesa", "natural", ["Sudáfrica"])

grafo.insert_arista("Taj Mahal", "Cristo Redentor", 1000)
grafo.insert_arista("Machu Picchu", "Cristo Redentor", 1500)

grafo.mostrar_grafo()

arbol_minimo = grafo.kruskal()
print("\nÁrbol de expansión mínimo:", arbol_minimo)
print("\nPaises con ambas maravillas:", grafo.paises_con_ambas_maravillas())
print("\nPaises con múltiples maravillas del mismo tipo:", grafo.paises_varias_misma_tipo())
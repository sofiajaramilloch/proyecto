import heapq
import pandas as pd 
import gmplot
import webbrowser
import time

data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")
data.harassmentRisk = data.harassmentRisk.fillna(data.harassmentRisk.mean())
graph = dict()

uniqueOrigin = data.origin.unique()

for i in range(len(uniqueOrigin)):
    graph[uniqueOrigin[i]] = dict()

for i in data.index:
    if data['oneway'][i]==False: 
        graph[data['origin'][i]][data['destination'][i]]=(data['length'][i],data['harassmentRisk'][i])
    else:
        try:
            graph[data['origin'][i]][data['destination'][i]]=(data['length'][i],data['harassmentRisk'][i])
            graph[data['destination'][i]][data['origin'][i]]=(data['length'][i],data['harassmentRisk'][i])
        except KeyError:
            continue
        
def getRoute(prev, i, route):
    if prev[i] == -1:
        route.append(i)
        return
    getRoute(prev, prev[i], route)
    route.append(i)

def SafestAndShortestAB(InitialPos, FinalPos, graph):

    DistanceAndHarassment = {vertex: float('inf') for vertex in graph}
    DistanceAndHarassment[InitialPos] = 0
    prev = {vertex: -1 for vertex in graph}

    pq = [(0, InitialPos, 0, 0)]

    while len(pq) > 0:

        currentNewVariable, currentVertex, currentRisk, currentDistance = heapq.heappop(pq)

        if currentVertex == FinalPos: break
        
        if currentNewVariable > DistanceAndHarassment[currentVertex]: continue
        
        for neighbor, weight in graph[currentVertex].items():

            path = currentNewVariable + (weight[0] * weight[1])
            try:
                if path < DistanceAndHarassment[neighbor]:
                    DistanceAndHarassment[neighbor] = path
                    prev[neighbor] = currentVertex
                    heapq.heappush(pq, (path, neighbor, currentRisk+weight[1], currentDistance+weight[0]))
            except KeyError:
                continue

    route = []
    getRoute(prev, FinalPos, route)
    print("La distancia total del algoritmo 1 es: " + str(currentDistance) + " metros")
    print("El riesgo de acoso promedio del algoritmo 1 es: " + str(currentRisk/len(route)))
    return route  


def Map(path):
    
    route = []

    for i in range(len(path)-1):

        separation = path[i].find(",")
        lat = float(path[i][separation+1:-1])
        lon = float(path[i][1:separation])
        coordinates = (lat,lon)
        route.append(coordinates)
    

    CharminarTopAttractionLats, CharminarTopAttractionLons = zip(*route)
    Gmap = gmplot.GoogleMapPlotter(6.267203842477565, -75.579710387, 12)  
    Gmap.plot(CharminarTopAttractionLats, CharminarTopAttractionLons, 'navy', edge_width = 3.0)
    Gmap.marker(CharminarTopAttractionLats[0],CharminarTopAttractionLons[0] , label = 'A')
    Gmap.marker(CharminarTopAttractionLats[-1],CharminarTopAttractionLons[-1] ,  label = 'B')
    Gmap.draw("MapRoute.html")  
    webbrowser.open_new_tab('MapRoute.html')

def main():
    print("Este es un programa diseñado para encontrar el camino más corto y más seguro en base a las variables (donde d es la distancia y r es el riesgo de acoso):")
    print("Variable 1: v = d*r -> color: azul")
    tiempoInicial = time.time()
    Map(SafestAndShortestAB("(-75.5778046, 6.2029412)","(-75.5762232, 6.266327)", graph))
    tiempoFinal = time.time()
    tiempoTotal = tiempoFinal - tiempoInicial
    print("El algoritmo 1 se demoró: ", tiempoTotal ," segundos en encontrar el camino")
        

main()
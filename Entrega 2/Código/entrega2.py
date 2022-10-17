import heapq
import pandas as pd 
import gmplot
import webbrowser

print("Para calcular la distancia más segura y más corta en el archivo de calles de Medellín debe ingresar correctamente las coordenadas.")
print("La estructura debe ser: (x,y)")
print("Ingrese el origen:")
UserOrigin = str(input())
print("Ingrese el destino:")
UserDestination = str(input())
print("A representa el punto de origen y B el punto de destino")

list = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")
list = list.fillna({"harassmentRisk": list["harassmentRisk"].mean()})
graph = {} 

uniqueOrigin = list.origin.unique()

for i in range(len(uniqueOrigin)):
    graph[uniqueOrigin[i]] = {} 

for i in list.index:
    if list['oneway'][i]==False: 
        graph[list['origin'][i]][list['destination'][i]]=(list['length'][i],list['harassmentRisk'][i])
    else:
        graph[list['origin'][i]][list['destination'][i]]=(list['length'][i],list['harassmentRisk'][i])
        try:
            graph[list['destination'][i]][list['origin'][i]]=(list['length'][i],list['harassmentRisk'][i])
        except KeyError: 
            graph[list['destination'][i]]={list["origin"][i]:(list["length"][i],list["harassmentRisk"][i])}

def getRoute(prev, i, route):
    if prev[i]==-1:
        route.append(i)
        return
    getRoute(prev, prev[i], route)
    route.append(i)

def SafestAndShortestAB(InitialPos, FinalPos, graph):

    DistanceAndHarassment = {vertex: [float('inf')] for vertex in graph}
    DistanceAndHarassment[InitialPos][0] = 0
    prev = {vertex: -1 for vertex in graph}

    pq = [(0, InitialPos)]

    while len(pq) > 0:

        currentNewVariable, currentVertex = heapq.heappop(pq)

        if currentVertex == FinalPos: break
        
        if currentNewVariable > DistanceAndHarassment[currentVertex][0]: continue
        
        for neighbor, weight in graph[currentVertex].items():

            path = float(currentNewVariable) + float((float(weight[0]) + float((weight[1])))/2)

            if path < DistanceAndHarassment[neighbor][0]:
                DistanceAndHarassment[neighbor][0] = path
                prev[neighbor] = currentVertex
                heapq.heappush(pq, (path, neighbor))

    route = []
    getRoute(prev, FinalPos, route)
    return(route)

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
    Gmap.plot(CharminarTopAttractionLats, CharminarTopAttractionLons, 'cornflowerblue', edge_width = 3.0)
    Gmap.marker(CharminarTopAttractionLats[0],CharminarTopAttractionLons[0] , label = 'A')
    Gmap.marker(CharminarTopAttractionLats[-1],CharminarTopAttractionLons[-1] ,  label = 'B')
    Gmap.draw("MapRoute.html")  
    webbrowser.open_new_tab('MapRoute.html')

Map(SafestAndShortestAB(UserOrigin,UserDestination, graph))

        

    
    
#Recorremos la lista una sola vez y vamos acumulando en el diccionario conteos la frecuencia de cada número.
#Al final usamos min sobre las claves del diccionario, 
#con una clave de ordenación que prioriza primero la mayor frecuencia (-conteos[k]) y en caso de empate el valor más pequeño (k).
def numero_mas_frecuente(lista):
    conteos = {}
    for n in lista:
        conteos[n] = conteos.get(n, 0) + 1
    return min(conteos, key=lambda k: (-conteos[k], k))

print(numero_mas_frecuente([1, 3, 1, 3, 2, 1]))  
print(numero_mas_frecuente([4, 4, 5, 5]))   

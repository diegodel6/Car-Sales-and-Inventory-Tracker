import csv
from prettytable import PrettyTable


def registro_venta(x, y):
    id = input("Ingresa ID de vendedor: ")

    vendedor_existe = False  #Determina si el id del vendedor existe en el archivo csv
    for sub in y:
        if id == sub[0]:
            vendedor_existe = True
            fila = y.index(sub)
            break

    if not vendedor_existe:
        print("El ID de vendedor no existe.\n")
        return

    while True:
        modelo = int(input("Ingresa el modelo de vehículo (Del 1 al 15): "))

        if 1 <= modelo <= 15:  #Determina si el modelo ingresado esta dentro de los parámetros
            cantidad = int(input("Ingresa cantidad de ventas: "))

            if cantidad <= x[modelo][2]:
                x[modelo][2] -= cantidad

                print("Se ha registrado la venta con éxito \n")

                y[fila][modelo + 1] = int(y[fila][modelo + 1]) + cantidad

            else:
                print("No contamos con esa cantidad de vehiculos.")

            break
        else:
            print("Ingrese un modelo válido \n")
            continue

    with open(
            'inventario.csv', 'w', newline=''
    ) as file:  #Modifica la información en el archivo inventario con lo que se cambio en la funcion
        escribir = csv.writer(file)
        escribir.writerows(x)

    with open(
            'vendedores.csv', 'w', newline=''
    ) as file2:  #Modifica la información en el archivo vendedores con lo que se cambio en la funcion
        escribir = csv.writer(file)
        escribir2 = csv.writer(file2)
        escribir2.writerows(y)


#Funcion para agregar vehiculos al archivo inventario
def nuevo_articulo(x):

    while True:
        modelo = int(input("Ingresa el modelo de vehículo (Número): "))
        #Aqui revisa que el modelo ingresado este dentro de los parametros
        if 1 <= modelo <= 15:
            cantidad = int(input("Ingresa la cantidad de vehiculos: "))
            x[modelo][2] += cantidad

            break
        else:
            print("Ingrese un modelo válido \n")
            continue
    #Aqui se modifica el archivo inventario con la nueva informacion
    with open('inventario.csv', 'w', newline='') as file:
        escribir = csv.writer(file)
        escribir.writerows(x)

    print("Se ha registrado el artículo con éxito \n")


#Funcion que accede al archivo inventario y muestra la informacion de los inventarios y los imprime en forma de tabla
def consulta_inventario(x):
    tabla = PrettyTable()
    encabezados = x[0]
    tabla.field_names = encabezados
    for fila in x[1:]:
        tabla.add_row(fila)
    print(tabla)

    print(" ")


#Funcion que compara todas las ventas de los vendedores y los suma por modelo de vehiculo, de esta manera calcula que modelo de vehiculo es el mas vendido
def mas_vendido(x, y):
    s2 = 0
    n = 0
    for i in range(2, 17):  #Aqui se revisa cada modelo de vehiculo
        s1 = 0
        for j in range(1, 6):
            s1 += int(y[j][i])

        if s1 > s2:
            s2 = s1
            n = i

    if s2 == 0:
        print("No hay ventas registradas.")

    else:
        print(
            f"El modelo más vendido es el {x[n-1][0]} {x[n-1][1]}, con {s2} ventas."
        )


#Funcion que compara todas las ventas de los vendedores y los suma para calcular que vendedor tiene mas ventas
def mejor_vendedor(x):
    max_ventas = 0
    mejor_vend = ""

    for i in range(1, len(x)):
        total_ventas = 0

        for j in range(2, 17):
            total_ventas += int(x[i][j])

        if total_ventas > max_ventas:
            max_ventas = total_ventas
            mejor_vend = x[i][1]

    if max_ventas == 0:
        print("No hay ventas registradas.")

    else:
        print(
            f"El vendedor que más ha vendido es {mejor_vend} con {max_ventas} ventas.\n"
        )


#Funcion que crea un archivo en el que se ve las ventas de el vendedor dado por cada modelo de vehiculo
def reporte_vendedor(x):
    id = input("Ingresa ID de vendedor: ")

    print(" ")

    titulo = x[0]

    matriz = []

    vendedor_existe = False
    for sub in x:
        if id == sub[0]:
            vendedor_existe = True
            fila = x.index(sub)
            lista = []
            lista.append(x[fila][0])
            lista.append(x[fila][1])

            break

    if not vendedor_existe:
        print("El ID de vendedor no existe.\n")
        return

    total_ventas = 0

    for j in range(2, 17):
        total_ventas += int(x[fila][j])
        lista.append(int(x[fila][j]))

    matriz.append(titulo)
    matriz.append(lista)

    archivo_csv = f"reporte_{x[fila][1]}.csv"

    with open(archivo_csv, mode='w', newline='') as file:
        writer = csv.writer(file)

        #Recorre la matriz y escribe cada fila en el archivo CSV
        for f in matriz:
            writer.writerow([*f])

    print(f"El vendedor {x[fila][1]} ha vendido {total_ventas} vehículos. \n")


#Funcion que suma las ventas por vendedor y las ordena de mayor a menor
def ranking(x):
    ranking_vendedores = []

    for i in range(1, len(x)):
        total_ventas = 0
        for j in range(2, 17):
            total_ventas += int(x[i][j])
        ranking_vendedores.append([x[i][1], total_ventas])

    ranking_vendedores.sort(key=lambda x: x[1], reverse=True)

    #Aqui se crea una tabla con los vendedores y sus ventas
    tabla = PrettyTable()
    tabla.field_names = ("Vendedor", "Total de ventas")
    for vendedor, total in ranking_vendedores:
        tabla.add_row([vendedor, total])
    print(tabla)


#Funcion que compara todas las ventas por vehiculo e imprime cual ha sido menos vendido
def menos_vendido(x, y):
    s2 = float("inf")
    n = 0
    ventas_totales = False

    for i in range(2, 17):
        s1 = 0
        for j in range(1, 6):
            s1 += int(y[j][i])

        if s1 > 0:
            ventas_totales = True

        if s1 < s2:
            s2 = s1
            n = i

    if not ventas_totales:
        print("No hay ventas registradas.")

    else:
        print(f"El modelo menos vendido es el {x[n-1][1]}, con {s2} ventas")

    print(" ")


def main():  #Funcion principal que llama a todas las funciones
    file = open('inventario.csv', 'r')
    archivo = csv.reader(file)

    #Aqui se crea una matriz con la informacion del archivo inventario

    file2 = open('vendedores.csv', 'r')
    archivo2 = csv.reader(file2)

    #Aqui se crea una matriz con la informacion del archivo vendedores

    inventario = []
    vendedores = []

    #Aqui se leen los archivos y se guardan en las matrices
    for f in archivo:
        inventario.append(f)

    for f2 in archivo2:
        vendedores.append(f2)

    #Aqui se hacen enteros las cantidades de vehiculos y de ventas
    for i in range(1, len(inventario)):
        inventario[i][2] = int(inventario[i][2])

    for i in range(1, len(vendedores)):
        for j in range(2, 17):
            vendedores[i][j] = int(vendedores[i][j])

    #Imprime las opciones del menu
    while True:
        print("1. Registrar una venta")
        print("2. Registrar llegada de artículos al almacén")
        print("3. Consultar el inventario disponible")
        print("4. Consultar cuál es el modelo del artículo más vendido.")
        print(
            "5. Consultar cuál vendedor ha vendido una cantidad mayor de artículos"
        )
        print("6. Reporte de ventas de un vendedor")
        print("7. Ranking vendedores")
        print("8. Consultar cuál es el modelo del artículo menos vendido")
        print('9. Salir\n')

        opcion = input("Seleccione una opción: ")
        print(" ")

        #Aqui se llaman la funcion que el usuario ingresó
        if opcion == "1":
            registro_venta(inventario, vendedores)
        elif opcion == "2":
            nuevo_articulo(inventario)
        elif opcion == "3":
            consulta_inventario(inventario)
        elif opcion == "4":
            mas_vendido(inventario, vendedores)
        elif opcion == "5":
            mejor_vendedor(vendedores)
        elif opcion == "6":
            reporte_vendedor(vendedores)
        elif opcion == "7":
            ranking(vendedores)
        elif opcion == "8":
            menos_vendido(inventario, vendedores)
        elif opcion == "9":
            print("Programa ha terminado")
            break
        else:
            print("Error, ingrese un número válido.\n")

    #Aqui se cierran los archivos
    file.close()
    file2.close()


print("Menú principal \n")
main()

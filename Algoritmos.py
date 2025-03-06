import matplotlib.pyplot as plt


def MostrarMenu():
    print("Seleccione el algoritmo a escoger: ")
    print("1. FIFO (First In First Out)")
    print("2. SJF (Shortest Job First)")
    print("3. RR (Round Robin)")
    print("4. Salir")

    opcion = input("Ingrese el número de la opción: ")
    return opcion

while True:
    opcion = MostrarMenu()

    if opcion == "1":
        print("Ha seleccionado FIFO")
    elif opcion == "2":
        print("Ha seleccionado SJF")
    elif opcion == "3":
        print("Ha seleccionado RR")
    elif opcion == "4":
        print("Saliendo del programa...")
        break
    else:
        print("Opción incorrecta")
   


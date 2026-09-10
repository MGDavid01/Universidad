import random

personaje = {"nombre": "", "clase": "", "nivel": 1,"estadisticas": {"vida": 0, "fuerza": 0, "mana": 0}, "inventario": []}
def menu():
    while True:
        print("1. Crear personaje")
        print("2. Mostrar personaje")
        print("3. Modificar Personaje")
        print("4. Gestionar Inventario")
        print("5. Salir")
        opcion = input("Ingrese una opcion: ")
        match opcion:
            case "1":
                crear_personaje()
            case "2":
                mostrar_personaje(personaje)
            case "3":
                modificar_personaje()
            case "4":
                gestionar_inventario()
            case "5":
                print("Saliendo...")
                break
            case _:
                print("Opcion no valida")

def crear_personaje():
        personaje["nombre"] = validar_texto(input("Nombre del personaje: "), "nombre")
        personaje["clase"] = validar_texto(input("Elige una clase: Guerrero, Mago, Arquero, Sanador: "), "clase")
        randomizar_estadisticas()

def randomizar_estadisticas():
       personaje["estadisticas"]["vida"] = random.randint(0, 10)
       personaje["estadisticas"]["fuerza"] = random.randint(0, 10)
       personaje["estadisticas"]["mana"] = random.randint(0, 10)    

def gestionar_inventario():
    while True:
        print("1. Agregar item")
        print("2. Eliminar item")
        print("3. Ver inventario")
        print("4. Salir")
        opcion = input("Ingrese una opcion: ")
        match opcion:
            case "1":
                agregar_item()
            case "2":
                eliminar_item()
            case "3":
                ver_inventario()
            case "4":
                break
            case _:
                print("Opcion no valida")

def ver_inventario():
    for i in range(len(personaje["inventario"])):
        print(f"{i}. {personaje['inventario'][i]}")

def agregar_item():
    item = input("Ingrese el nombre del item a agregar: ")
    if item in personaje["inventario"]:
        print("Item ya existe en el inventario")
        return
    personaje["inventario"].append(item)
    print(f"{item} agregado al inventario")

def eliminar_item():
    item = int(input("Ingrese el numero del item a eliminar: "))
    if item not in range(len(personaje["inventario"])):
        print("Item no encontrado en el inventario")
        return
    objetoremovido = personaje["inventario"][item]
    del personaje["inventario"][item]
    print(f"{objetoremovido} eliminado del inventario")
    objetoremovido = ""

def mostrar_personaje(personaje: dict):
    print(personaje)

def modificar_personaje():
    personaje["nivel"] = validar_texto(input("Nivel del personaje: "), "nivel")
    personaje["estadisticas"]["vida"] = validar_texto(input("Vida Maxima del personaje: "), "estadisticas")
    personaje["estadisticas"]["fuerza"] = validar_texto(input("Fuerza del personaje: "), "estadisticas")
    personaje["estadisticas"]["mana"] = validar_texto(input("Mana Maximo del personaje: "), "estadisticas")

def validar_texto(valor, tipo):
    while True:
        valor = valor.strip().title()
        match tipo:
            case "nombre":
                if 3 <= len(valor) <= 20:
                    return valor
                print("Nombre debe tener entre 3 y 20 Caracteres")
            case "clase":
                if valor in ["Guerrero", "Mago", "Arquero", "Sanador"]:
                    return valor
                print("La clase debe ser: Guerrero, Mago, Arquero, Sanador")
            case "nivel":
                try:
                    if 1 <= int(valor) <= 10:
                        return int(valor)
                    print("El nivel debe ser entre 1 y 10")
                except ValueError:
                    print("Ingrese un numero valido")
            case "estadisticas":
                try:
                    if 1 <= int(valor) <= 10:
                        return int(valor)
                    print("Las estadisticas deben ser entre 1 y 10")
                except ValueError:
                    print("Ingrese un numero valido")
            case _:
                print("Tipo no valido")
        valor = input("Ingrese un valor valido: ")

menu()
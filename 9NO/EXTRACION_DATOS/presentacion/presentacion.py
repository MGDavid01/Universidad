import os
import random
import sys

perfilBase = {
    "nombre": "David Mejia",
    "género": "Masculino",
    "carrera": "Ingeniería en Desarrollo y Gestión de Software",
    "hobbies": ["Programar", "Jugar videojuegos", "Ver anime", "Leer"],
}

animes = {
    "Made in Abyss": {"capitulos": 13, "actual": 1},
    "No game No life": {"capitulos": 12, "actual": 1},
    "Shoku": {"capitulos": 24, "actual": 1},
    "Re:Zero": {"capitulos": 25, "actual": 1},
}

juegos = {
    "Helldivers II": 0,
    "Overwatch 2": 0,
    "Albion Online": 0,
    "Wuthering Waves": 0,
}

deberesMaximos = {
    "Lavar trastes": 1,
    "Hacer desayuno": 1,
    "Hacer cena": 1,
    "Tirar basura": 1,
}
deberesHechos = {nombre: 0 for nombre in deberesMaximos}

MATERIAS = [
    "ADMINISTRACIÓN DE PROYECTOS DE TI",
    "EXTRACCIÓN DE CONOCIMIENTOS EN BASE DE DATOS",
    "DESARROLLO WEB INTEGRAL",
    "DESARROLLO PARA DISPOSITIVOS INTELIGENTES",
    "DIRECCIÓN DE EQUIPOS DE ALTO RENDIMIENTO",
    "INGLÉS VIII",
]

energia = random.randint(15, 33)
energia_inicial = energia

universidad = {}
materias_con_proyecto = set(
    random.sample(MATERIAS, k=random.randint(0, min(2, len(MATERIAS))))
)
for materia in MATERIAS:
    universidad[materia] = {
        "tarea_pendiente": random.randint(0, 1),
        "proyecto_meta": (
            random.randint(2, 3) if materia in materias_con_proyecto else 0
        ),
        "proyecto_avance": 0,
    }


def ingresar(tipo):
    return input("Ingrese " + tipo + ": ")


def mostrar_energia():
    print(f"Energía: {energia} / {energia_inicial}")


def a_mimir():
    os.system("clear")
    print("A mimir")
    sys.exit(0)


def gastar_energia(costo):
    global energia
    if energia < costo:
        print(f"No tienes suficiente energía (necesitas {costo}, tienes {energia}).")
        if energia <= 0.5:
            a_mimir()
        return False
    energia = round(energia - costo, 1)
    if energia == int(energia):
        energia = int(energia)
    print(f"-{costo} energía. Quedan {energia}.")
    if energia <= 0.5:
        a_mimir()
    return True


def recuperar_energia(cantidad):
    global energia
    anterior = energia
    energia = min(energia_inicial, round(energia + cantidad, 1))
    if energia == int(energia):
        energia = int(energia)
    ganado = round(energia - anterior, 1)
    if ganado == int(ganado):
        ganado = int(ganado)
    if ganado > 0:
        print(f"+{ganado} energía. Ahora tienes {energia} / {energia_inicial}.")
    else:
        print(f"Energía al máximo ({energia_inicial}).")


def costo_ligero():
    return random.choice([1, 1.5])


def costo_proyecto():
    return random.choice([1, 3])


def menu(opciones, titulo=""):
    while True:
        lista = opciones() if callable(opciones) else opciones

        if not lista:
            return

        if titulo:
            print(f"\n=== {titulo} ===")
            mostrar_energia()

        for i, (texto, _) in enumerate(lista, start=1):
            print(f"{i}. {texto}")

        entrada = ingresar("opción")

        try:
            n = int(entrada)
        except ValueError:
            print("Opción no válida")
            continue

        match n:
            case eleccion if 1 <= eleccion <= len(lista):
                _, accion = lista[eleccion - 1]
                if accion is None:
                    return
                accion()
            case _:
                print("Opción no válida")


def perfil():
    print("\n=== Perfil ===")
    mostrar_energia()
    print(f"Nombre: {perfilBase['nombre']}")
    print(f"Género: {perfilBase['género']}")
    print(f"Carrera: {perfilBase['carrera']}")

    print("\n--- Hobbies ---")
    for hobby in perfilBase["hobbies"]:
        print(f"- {hobby}")

    print("\n--- Animes ---")
    if animes:
        for nombre, datos in animes.items():
            if datos["actual"] > datos["capitulos"]:
                print(
                    f"- {nombre}: terminado "
                    f"({datos['capitulos']}/{datos['capitulos']})"
                )
            else:
                print(
                    f"- {nombre}: Capítulo "
                    f"{datos['actual']} / {datos['capitulos']}"
                )
    else:
        print("(sin animes)")

    print("\n--- Juegos ---")
    total_horas = 0
    if juegos:
        for nombre, horas in juegos.items():
            print(f"- {nombre}: {horas} hrs")
            total_horas += horas
        print(f"Total de horas: {total_horas} hrs")
    else:
        print("(sin juegos)")

    print("\n--- Deberes ---")
    for nombre, maximos in deberesMaximos.items():
        hechos = deberesHechos[nombre]
        print(f"- {nombre}: {hechos}/{maximos}")

    print("\n--- Universidad ---")
    for materia, datos in universidad.items():
        print(f"\n{materia}")
        if datos["tenia_tarea"]:
            estado_t = "pendiente" if datos["tarea_pendiente"] else "hecha"
        else:
            estado_t = "no asignada"
        print(f"  Tarea: {estado_t}")

        if datos["proyecto_meta"] > 0:
            av = datos["proyecto_avance"]
            meta = datos["proyecto_meta"]
            if av >= meta:
                print(f"  Proyecto: concluido ({meta}/{meta})")
            else:
                print(f"  Proyecto: {av}/{meta}")
        else:
            print("  Proyecto: no asignado")


def _marcar_origen_tareas():
    for datos in universidad.values():
        datos["tenia_tarea"] = datos["tarea_pendiente"] == 1


_marcar_origen_tareas()


def jugar_uno(nombre):
    if not gastar_energia(costo_ligero()):
        return
    juegos[nombre] += 2
    print(f"Jugaste {nombre}. Ahora llevas {juegos[nombre]} hrs.")


def jugar_juego():
    def opciones():
        if not juegos:
            print("No hay juegos instalados")
            return []
        lista = [
            (f"{nombre} ({horas} hrs)", lambda n=nombre: jugar_uno(n))
            for nombre, horas in juegos.items()
        ]
        lista.append(("Volver", None))
        return lista

    menu(opciones, titulo="Elegir juego")


def instalar_juego():
    nombre = ingresar("nombre del juego").strip()
    if not nombre:
        print("Nombre vacío")
        return
    if nombre in juegos:
        print("Ese juego ya está instalado")
        return
    juegos[nombre] = 0
    print(f"Instalado: {nombre}")


def desinstalar_uno(nombre):
    del juegos[nombre]
    print(f"Desinstalado: {nombre}")


def desinstalar_juego():
    def opciones():
        if not juegos:
            print("No hay juegos para desinstalar")
            return []
        lista = [
            (nombre, lambda n=nombre: desinstalar_uno(n))
            for nombre in list(juegos.keys())
        ]
        lista.append(("Volver", None))
        return lista

    menu(opciones, titulo="Desinstalar juego")


def ver_uno(nombre):
    datos = animes[nombre]
    if datos["actual"] > datos["capitulos"]:
        print(f"Ya terminaste {nombre} ({datos['capitulos']} caps).")
        return

    if not gastar_energia(costo_ligero()):
        return

    print(f"Viste el capítulo {datos['actual']} de {nombre}.")
    datos["actual"] += 1

    if datos["actual"] > datos["capitulos"]:
        print("¡Anime terminado!")
    else:
        print(f"Capítulo {datos['actual']} / {datos['capitulos']}.")


def ver_anime():
    def opciones():
        if not animes:
            print("No hay animes en pendientes")
            return []
        lista = [
            (
                f"{nombre} (cap {d['actual']}/{d['capitulos']})"
                if d["actual"] <= d["capitulos"]
                else f"{nombre} [terminado]",
                lambda n=nombre: ver_uno(n),
            )
            for nombre, d in animes.items()
        ]
        lista.append(("Volver", None))
        return lista

    menu(opciones, titulo="Ver anime")


def anadir_pendiente():
    nombre = ingresar("nombre del anime").strip()
    if not nombre:
        print("Nombre vacío")
        return
    if nombre in animes:
        print("Ese anime ya está en la lista")
        return

    try:
        capitulos = int(ingresar("cantidad de capítulos"))
    except ValueError:
        print("Debe ser un número")
        return

    if capitulos < 1:
        print("Debe haber al menos 1 capítulo")
        return

    animes[nombre] = {"capitulos": capitulos, "actual": 1}
    print(f"Añadido: {nombre} ({capitulos} caps, empiezas en el 1)")


def eliminar_uno(nombre):
    del animes[nombre]
    print(f"Eliminado: {nombre}")


def eliminar_pendiente():
    def opciones():
        if not animes:
            print("No hay animes para eliminar")
            return []
        lista = [
            (nombre, lambda n=nombre: eliminar_uno(n))
            for nombre in list(animes.keys())
        ]
        lista.append(("Volver", None))
        return lista

    menu(opciones, titulo="Eliminar anime")


def completar_deber(nombre):
    maximos = deberesMaximos[nombre]
    hechos = deberesHechos[nombre]

    if hechos >= maximos:
        print(f"'{nombre}' ya no se puede hacer más en esta ejecución.")
        return

    if not gastar_energia(costo_ligero()):
        return

    deberesHechos[nombre] += 1
    print(f"Hecho: {nombre} ({deberesHechos[nombre]}/{maximos})")

    if nombre in ("Hacer desayuno", "Hacer cena"):
        recuperar_energia(5)


def hacer_deberes():
    def opciones():
        lista = []
        for nombre, maximos in deberesMaximos.items():
            hechos = deberesHechos[nombre]
            etiqueta = f"{nombre} ({hechos}/{maximos})"
            if hechos >= maximos:
                etiqueta += " [completado]"
            lista.append((etiqueta, lambda n=nombre: completar_deber(n)))
        lista.append(("Volver", None))
        return lista

    menu(opciones, titulo="Deberes")


def hacer_tarea_materia(materia):
    datos = universidad[materia]
    if not datos["tarea_pendiente"]:
        print("No hay tarea pendiente en esta materia.")
        return

    if not gastar_energia(3):
        return

    datos["tarea_pendiente"] = 0
    print(f"Tarea de {materia} completada.")


def avanzar_proyecto(materia):
    datos = universidad[materia]
    if datos["proyecto_meta"] == 0:
        print("No hay proyecto en esta materia.")
        return

    if datos["proyecto_avance"] >= datos["proyecto_meta"]:
        print(f"El proyecto de {materia} ya está concluido.")
        return

    if not gastar_energia(costo_proyecto()):
        return

    datos["proyecto_avance"] += 1
    av = datos["proyecto_avance"]
    meta = datos["proyecto_meta"]
    print(f"Avance en {materia}: {av}/{meta}")
    if av >= meta:
        print(f"¡Proyecto de {materia} concluido!")


def hacer_tarea():
    def opciones():
        lista = []
        for materia, datos in universidad.items():
            if datos["tarea_pendiente"]:
                lista.append(
                    (
                        f"Tarea: {materia}",
                        lambda m=materia: hacer_tarea_materia(m),
                    )
                )
            if (
                datos["proyecto_meta"] > 0
                and datos["proyecto_avance"] < datos["proyecto_meta"]
            ):
                lista.append(
                    (
                        f"Proyecto: {materia} "
                        f"({datos['proyecto_avance']}/{datos['proyecto_meta']})",
                        lambda m=materia: avanzar_proyecto(m),
                    )
                )

        if not lista:
            print("No hay tareas ni proyectos pendientes.")
            lista.append(("Volver", None))
            return lista

        lista.append(("Volver", None))
        return lista

    menu(opciones, titulo="Universidad")


def jugar():
    menu(
        [
            ("Jugar un juego", jugar_juego),
            ("Instalar un juego", instalar_juego),
            ("Desinstalar un juego", desinstalar_juego),
            ("Volver", None),
        ],
        titulo="Juegos",
    )


def anime():
    menu(
        [
            ("Ver un Anime", ver_anime),
            ("Añadir en Pendientes", anadir_pendiente),
            ("Eliminar de Pendiente", eliminar_pendiente),
            ("Volver", None),
        ],
        titulo="Animes",
    )


def tarea():
    menu(
        [
            ("Hacer deberes", hacer_deberes),
            ("Hacer tarea", hacer_tarea),
            ("Volver", None),
        ],
        titulo="Tareas",
    )


def yoMero(nombre):
    print(f"Hola, {nombre}")
    mostrar_energia()
    print("\nCarga académica de hoy:")
    for materia, datos in universidad.items():
        partes = []
        if datos["tenia_tarea"]:
            partes.append("1 tarea")
        if datos["proyecto_meta"] > 0:
            partes.append(f"proyecto ({datos['proyecto_meta']} avances)")
        if not partes:
            partes.append("libre")
        print(f"- {materia}: {', '.join(partes)}")

    menu(
        [
            ("Perfil", perfil),
            ("Juegos", jugar),
            ("Animes", anime),
            ("Tareas", tarea),
            ("Salir", None),
        ],
        titulo="Menú principal",
    )
yoMero("David Mejia")
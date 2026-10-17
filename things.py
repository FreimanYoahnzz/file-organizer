import utilidades
import os
import json
import shutil
import sys
import subprocess

NOMBRE_TAREA = "FileOrgAutomatico"
NOMBRE_EXE_AUTO = "FileOrganizerAuto.exe"

def pedir_ruta(mensaje):

    while True:
        ruta = utilidades.lea(mensaje)
        if os.path.exists(ruta) == True:
            utilidades.imp("Ruta encontrada con éxito.")
            return ruta
        else:
            utilidades.imp(f"No se logro encontrar la ruta({ruta}), por favor verifiquela e intente nuevamente.")


def agg_proceso(datos):

    origen = pedir_ruta("Ingrese la ruta origen de la carpeta DE donde se van a mover los archivos:\n")
    destino = pedir_ruta("Ingrese la ruta destino de la carpeta A donde se van a mover los archivos:\n")

    listaCategorias = cargar_categorias()

    utilidades.imp("LISTA DE CATEGORIAS")

    for i in range(len(listaCategorias)):
        num = i + 1
        utilidades.imp(f"{num}. {listaCategorias[i]}")

    while True:
        numCategoria = utilidades.intLea("Ingrese el número correspondiente al tipo de archivo al cual se le realizara el proceso de movención:\n",
                                    "El dato ingresado es invalido, por favor intente nuevamente")
        
        if numCategoria <= len(listaCategorias) and numCategoria > 0:
            categoria = listaCategorias[numCategoria - 1]
            proceso = {
                "origen": origen,
                "destino": destino,
                "categoria": categoria
            }
            datos["procesos"].append(proceso)

            with open(utilidades.ruta_completa("rutas.json"), "w", encoding= "utf-8") as f:
                json.dump(datos, f)

            break
        else:
            utilidades.imp("Por favor ingrese una opción que se encuentre en la lista de categorias")


def lista_procesos(datos):
    
    for i in range(len(datos["procesos"])):
        num = i + 1
        utilidades.imp(f"{num}.\n Ruta origen: {datos["procesos"][i]["origen"]} | Ruta destino: {datos["procesos"][i]["destino"]} | Categoria: {datos["procesos"][i]["categoria"]}")


def mod_otro_proceso():

    while True:

        utilidades.imp("¿Desea modificar algún otro proceso?")
        utilidades.imp("1. Si")
        utilidades.imp("2. No")
        opcion = utilidades.intLea("Ingrese el numero asignado a una de las opciones anteriores:\n", "El dato ingresado es invalido, por favor intente nuevamente")
        match opcion:
            case 1:
                return True

            case 2:
                return False
            
            case _:
                    utilidades.imp("Por favor ingrese una opción que se encuentre en el menú de opciones")


def cargar_categorias():

    with open(utilidades.ruta_completa("config.json"), "r", encoding= "utf-8") as f:
        datosConf = json.load(f)

    listClavesPredeterminadas = list(datosConf["predeterminados"].keys())
    listClavesPersonalizadas =  list(datosConf["personalizados"].keys())
    listClaves = (listClavesPredeterminadas + listClavesPersonalizadas)
    return listClaves


def pedir_categorias():
    listaCategorias = cargar_categorias()
    
    utilidades.imp("LISTA DE CATEGORIAS")

    for i in range(len(listaCategorias)):
        num = i + 1
        utilidades.imp(f"{num}. {listaCategorias[i]}")

    while True:
        numCategoria = utilidades.intLea("Ingrese el número correspondiente al tipo de archivo al cual se le realizara el proceso de movención:\n",
                                    "El dato ingresado es invalido, por favor intente nuevamente")
        if numCategoria <= len(listaCategorias) and numCategoria > 0:
            categoria = listaCategorias[numCategoria - 1]
            return categoria
        else:
            utilidades.imp("Por favor ingrese una opción que se encuentre en la lista de categorias")


def modificar_categoria(mensaje):
    while True:

        utilidades.imp(mensaje)
        utilidades.imp("1. Si")
        utilidades.imp("2. No")
        opcion = utilidades.intLea("Ingrese el numero asignado a una de las opciones anteriores:\n", "El dato ingresado es invalido, por favor intente nuevamente")

        match opcion:
            case 1:
                return pedir_categorias()
            
            case 2:
                return

            case _:
                utilidades.imp("Por favor ingrese una opción que se encuentre en el menú de opciones")

        
def cargar_extensiones(categoria):

    with open(utilidades.ruta_completa("config.json"), "r", encoding= "utf-8") as f:
        datosConf = json.load(f)

    if categoria in datosConf["predeterminados"]:
        return datosConf["predeterminados"][categoria]
    elif categoria in datosConf["personalizados"]:
        return datosConf["personalizados"][categoria]
    else:
        return []   


def buscar_archivos(proceso):
    listArchValidos = []
    try:
        listArchivos = os.listdir(proceso["origen"])
    except OSError:
        utilidades.escribir_log(f'No se pudo acceder a la ruta origen "{proceso["origen"]}"')
        return listArchValidos
    
    extensiones = cargar_extensiones(proceso["categoria"])

    for nomArch in listArchivos:
        nombre, extension = os.path.splitext(nomArch)

        if extension.lower() in extensiones:
            listArchValidos.append(nomArch)

    return listArchValidos


def mover_archivo(nombre, proceso):
    origen = proceso["origen"]
    destino = proceso["destino"]

    rutaOrigen = os.path.join(origen, nombre)
    rutaDestino = os.path.join(destino, nombre)


    nom, extenc = os.path.splitext(nombre)
    contador = 1
    nuevoNom = ""
    while os.path.exists(rutaDestino):
        nuevoNom = nom + str(contador) + extenc
        rutaDestino = os.path.join(destino, nuevoNom)
        contador += 1
    try:
        shutil.move(rutaOrigen, rutaDestino)

    except OSError:
        return False, nuevoNom

    return True, nuevoNom


def ejecutar_proceso(proceso):
    listaArchivos = buscar_archivos(proceso)

    for archivo in listaArchivos:
        seMovio, cambioNom = mover_archivo(archivo, proceso)
        if seMovio == True:
            if cambioNom == "":
                utilidades.escribir_log(f"El archivo '{archivo}' se movio de {proceso["origen"]} a {proceso["destino"]} correctamente.")
            else:
                utilidades.escribir_log(f"El archivo '{archivo}' se movio de {proceso["origen"]} a {proceso["destino"]} correctamente, y fue renombrado '{cambioNom}'.")                            
        else:
            utilidades.escribir_log(f"No se pudo mover el archivo '{archivo}' de {proceso["origen"]} a {proceso["destino"]}")


def ejecutar_todos_los_procesos(datos):
    for dato in datos["procesos"]:
        ejecutar_proceso(dato)


def modo_automatico(datos):
    if len(datos["procesos"]) == 0:
        if apagar_tarea() == True:
            utilidades.escribir_log("El modo automático fue apagado ya que NO hay procesos para ejecutar")

        return
    else:
        ejecutar_todos_los_procesos(datos)


def procesos_tareas(listComando, mensajeExito, mensajeFracaso):
    resultado = subprocess.run(listComando, capture_output=True, text=True)

    if resultado.returncode == 0:
        utilidades.escribir_log(f"{mensajeExito} - nombre tarea: {NOMBRE_TAREA}")
        return True
    else:
        utilidades.escribir_log(f'{mensajeFracaso} - motivo: "{resultado.stderr}" - nombre tarea: {NOMBRE_TAREA}')
        return False


def crear_tarea(intervaloEjec = 2):
    ruta = sys.executable
    carpeta = os.path.dirname(ruta)

    if getattr(sys, "frozen", False):
        rutaPyW = os.path.join(carpeta, NOMBRE_EXE_AUTO)
        if os.path.exists(rutaPyW):
            textoTR = f'"{rutaPyW}" "autoejecutar"'
        else:
            utilidades.escribir_log(f'No se encontro el archivo "{rutaPyW}"')
            return False
    else:
        rutaPyW = os.path.join(carpeta, "pythonw.exe")
        rutaPrograma = utilidades.ruta_completa("program.py")
        textoTR = f'"{rutaPyW}" "{rutaPrograma}" "autoejecutar"'
        
    comando = ["schtasks","/Create","/TN",NOMBRE_TAREA,"/TR", textoTR, "/SC", "MINUTE","/MO", str(intervaloEjec), "/F"]
    return procesos_tareas(comando, "Tarea creada con éxito", "Error, la tarea falló")
  
     
def apagar_tarea():
    return procesos_tareas(["schtasks","/Change", "/TN", NOMBRE_TAREA, "/DISABLE" ], "Modo ejecución automática APAGADO", 
                           "No se pudo apagar la ejecución automática")


def encender_tarea():
    return procesos_tareas(["schtasks","/Change", "/TN", NOMBRE_TAREA, "/ENABLE" ], "Modo ejecución automática ENCENDIDO",
                            "No se pudo encender la ejecución automática")


def eliminar_tarea():
    return procesos_tareas(["schtasks","/Delete", "/TN", NOMBRE_TAREA, "/F" ], "Se eliminó la tarea de ejecución automática", 
                           "No se pudo eliminar la tarea de la ejecución automática")

def tarea_existe():
    comando = ["schtasks", "/Query", "/TN", NOMBRE_TAREA]
    resultado = subprocess.run(comando, capture_output=True, text=True)

    if resultado.returncode == 0:
        return True
    return False

#USAR EN CONJUNTO CON LA FUNCIÓN tarea_existe()
def estado_tarea():
    comando = ["schtasks", "/Query", "/TN", NOMBRE_TAREA, "/XML"]
    resultado = subprocess.run(comando, capture_output=True, text=True)

    if resultado.returncode == 0 and "<Enabled>false</Enabled>" in resultado.stdout:
        #tarea esta APAGADA
        return False
    elif resultado.returncode == 0:
        #tarea esta ENCENDIDA
        return True


def preguntar_si_no(mensaje):
    utilidades.imp(f"{mensaje}\n1. Si\n2. No")
    while True:
        opcion = utilidades.intLea("Ingrese una opción:\n","El dato ingresado es invalido, por favor intente nuevamente")
        match opcion:
            case 1:
                return True
            case 2:
                return False
            case _:
                utilidades.imp("Opción invalida, por favor ingrese una opción que se encuentre en el menú de opciones")
                           

def activar_autoejecucion():
    if tarea_existe() == True:
        if estado_tarea() == True:
            utilidades.imp("La tarea de autoejecutar ya está ENCENDIDA")
        else:
            if encender_tarea() == True:
                utilidades.imp("La tarea de autoejecutar quedó ENCENDIDA")
            else:
                utilidades.imp("No se pudo encender la tarea de autoejecutar, consulte el historial de actividad para ver el motivo")
    else:
        utilidades.imp("La tarea de autoejecutar NO existe aún")
        if preguntar_si_no("¿Desea crearla?") == True:
            if crear_tarea() == True:
                utilidades.imp("Tarea de autoejecutar creada correctamente")
                if preguntar_si_no("¿Desea dejar encendida la tarea de autoejecutar?") == True:
                    utilidades.imp("La tarea de autoejecutar quedó ENCENDIDA")
                else:
                    if apagar_tarea() == True:
                        utilidades.imp("La tarea de autoejecutar ha sido APAGADA")
                    else:
                        utilidades.imp("No se pudo apagar la tarea de autoejecutar, consulte el historial de actividad para ver el motivo")
            else:
                utilidades.imp("No se pudo crear la tarea de autoejecutar")
        else:
            utilidades.imp("OK")
            

def desactivar_autoejecucion():
    if tarea_existe() == True:
        if estado_tarea() == True:
            if apagar_tarea() == True:
                utilidades.imp("La tarea de autoejecutar ha sido APAGADA")
            else:
                utilidades.imp("No se pudo apagar la tarea de autoejecutar, consulte el historial de actividad para ver el motivo")
        else:
            utilidades.imp("La tarea de autoejecutar ya se encuentra APAGADA")
    else:
        utilidades.imp("La tarea de autoejecutar NO existe aún")


def mostrar_estado_autoejecucion():
    utilidades.imp("MODO AUTOEJECUTAR")
    if tarea_existe() == True:
        if estado_tarea() == True:
            utilidades.imp(f"Nombre tarea: {NOMBRE_TAREA} - Estado: ENCENDIDA")
        else:
            utilidades.imp(f"Nombre tarea: {NOMBRE_TAREA} - Estado: APAGADA")
    else:
        utilidades.imp("Estado: No se ha creado aún")

    
def eliminar_autoejecucion():
    if tarea_existe() == True:
        if preguntar_si_no("¿Esta seguro de que quiere eliminar la tarea de AUTOEJECUTAR?") == True:
            if eliminar_tarea() == True:
                utilidades.imp("Se elimino la tarea de autoejecutar correctamente")
            else:
                utilidades.imp("No se pudo eliminar la tarea de autoejecutar, consulte el historial de actividad para ver el motivo")
        else:
            utilidades.imp("OK")
    else:
        utilidades.imp("La tarea de autoejecutar NO existe, por ende no se puede eliminar")


def menu_modo_automatico():
    while True:
        mostrar_estado_autoejecucion()
        utilidades.imp("\n¿Que desea hacer?\nOpciones:")
        utilidades.imp("1. Activar modo autoejecutar")
        utilidades.imp("2. Desactivar modo autoejecutar")
        utilidades.imp("3. Eliminar tarea de autoejecutar")
        utilidades.imp("4. Volver al menú")

        opcion = utilidades.intLea("Ingrese el numero asignado a una de las opciones anteriores:\n", "El dato ingresado es invalido, por favor intente nuevamente")
        match opcion:
            case 1:
                activar_autoejecucion()

            case 2:
                desactivar_autoejecucion()

            case 3:
                eliminar_autoejecucion()

            case 4:
                break

            case _:
                utilidades.imp("Opción invalida, por favor ingrese una opción que se encuentre en el menú de opciones")


def mostrar_categorias(datos):

    with open(utilidades.ruta_completa("config.json"), "r", encoding= "utf-8") as f:
        tiposCategorias = json.load(f) 

    utilidades.imp("\n\tCATEGORIAS PREDETERMINADAS\n")
    num = 0
    for nombreTPred, extensionesTPred in tiposCategorias["predeterminados"].items():
        numeroProcesosUsandola = procesos_con_categoria_usandose(datos, nombreTPred)
        num += 1
        if len(numeroProcesosUsandola) == 1:
            utilidades.imp(f"{num}.\nNombre: {nombreTPred} - Tipos de archivos: [ {" | ".join(extensionesTPred)} ] -> hay {len(numeroProcesosUsandola)} proceso usando la categoria")
        elif len(numeroProcesosUsandola) > 1:
            utilidades.imp(f"{num}.\nNombre: {nombreTPred} - Tipos de archivos: [ {" | ".join(extensionesTPred)} ] -> hay {len(numeroProcesosUsandola)} procesos usando la categoria")
        else:
            utilidades.imp(f"{num}.\nNombre: {nombreTPred} - Tipos de archivos: [ {" | ".join(extensionesTPred)} ] -> No hay procesos usando la categoria")  

    utilidades.imp("\n\tCATEGORIAS PERSONALIZADAS\n")
    if len(tiposCategorias["personalizados"]) == 0:
        utilidades.imp("No hay categorias personalizadas registradas")
    else:
        for nombreTPers, extensionesTPers in tiposCategorias["personalizados"].items():
            numeroProcesosUsandola = procesos_con_categoria_usandose(datos, nombreTPers)
            num += 1
            if len(numeroProcesosUsandola) == 1:
                utilidades.imp(f"{num}.\nNombre: {nombreTPers} - Tipos de archivos: [ {" | ".join(extensionesTPers)} ] -> hay {len(numeroProcesosUsandola)} proceso usando la categoria") 
            elif len(numeroProcesosUsandola) > 1:
                utilidades.imp(f"{num}.\nNombre: {nombreTPers} - Tipos de archivos: [ {" | ".join(extensionesTPers)} ] -> hay {len(numeroProcesosUsandola)} procesos usando la categoria") 
            else:
                utilidades.imp(f"{num}.\nNombre: {nombreTPers} - Tipos de archivos: [ {" | ".join(extensionesTPers)} ] -> No hay procesos usando la categoria")  


def crear_categoria():
    utilidades.imp("NOMBRE DE LA CATEGORIA")

    while True:
        
        nombreCategoria = utilidades.lea("¿Que nombre desea ponerle a la categoria que va a crear?\nIngrese el nombre:\n").strip()

        if nombreCategoria not in cargar_categorias() and nombreCategoria != "":
            utilidades.imp("EXTENSIONES DE LA CATEGORIA")
            utilidades.imp("Por favor tenga en cuenta esto al momento de ingresar las extensiones de la categoria: Las extensiones tienen que ser ingresadas con un punto(.)\n" \
            "seguido de la extensión del archivo, y a su vez separadas por comas(,) para que los procesos se puedan ejecutar correctamente.\n" \
            "ejemplo: .jpg, .png, .txt")

            while True:

                listaExtCategoria = []
                extensionesCategoria = utilidades.lea("Ingrese las extensiones:\n").lower().split(",")
                for ext in extensionesCategoria:

                    if ext.strip().startswith(".") and len(ext.strip()) > 1:

                        listaExtCategoria.append(ext.strip())
                    else:
                        utilidades.imp(f'La extensión "{ext}" no pudo ser agregada a la categoria, ya que no cuenta con el formato indicado')
                        utilidades.escribir_log(f'No se pudo agregar la extensión "{ext}" a la categoria "{nombreCategoria}" ya que no cuenta con el formato indicado')

                
                if len(listaExtCategoria) != 0:
                    with open(utilidades.ruta_completa("config.json"), "r", encoding= "utf-8") as f:
                        categorias = json.load(f)

                    categorias["personalizados"][nombreCategoria] = listaExtCategoria

                    with open(utilidades.ruta_completa("config.json"), "w", encoding= "utf-8") as f:
                        json.dump(categorias, f, indent= 2)

                    utilidades.escribir_log(f'Se creo una categoria llamada "{nombreCategoria}"')
                    utilidades.imp("Categoria creada correctamente")
                    break
                else:
                    utilidades.imp("No se pudo crear la categoria ya que ninguna de las extensiones cuentan con el formato indicado\n")
                    utilidades.imp("Las extensiones tienen que ser ingresadas con un punto(.)\n" \
                    "seguido de la extensión del archivo, y a su vez separadas por comas(,) para que los procesos se puedan ejecutar correctamente.\n" \
                    "ejemplo: .jpg, .png, .txt")
            break

        else:
            if nombreCategoria in cargar_categorias():
                utilidades.imp(f'Error de asignación\nEl nombre "{nombreCategoria}" ya se encuentra asignado a una categoria, por favor pruebe con otro')
            else:
                utilidades.imp(f'Error de asignación\nEl nombre "{nombreCategoria}" es invalido, NO se le puede asignar un nombre invisible a una categoria')


def procesos_con_categoria_usandose(datos, categoria):
    listaNumProcesos = []

    for i in range(len(datos["procesos"])):
        if datos["procesos"][i]["categoria"] == categoria:
            listaNumProcesos.append(i + 1)

    return listaNumProcesos

def eliminar_categoria(datos):
    with open(utilidades.ruta_completa("config.json"), "r", encoding= "utf-8") as f:
        categorias = json.load(f)

    catPersonalizadas = categorias["personalizados"]


    if len(catPersonalizadas) == 0:
        utilidades.imp("No hay categorias que se puedan eliminar")
        return
    else:
        num = 0
        listNomCat = []
        for nombreCat, extensionesCat in catPersonalizadas.items():
            num += 1
            utilidades.imp(f"{num}. Categoria: {nombreCat} - Tipos de archivos: [ {" | ".join(extensionesCat)} ]")
            listNomCat.append(nombreCat)

        while True:
            eliminarCatNum = utilidades.intLea("Ingrese el numero asignado a la categoria que desea eliminar:\n", 
                        "El dato ingresado es invalido, por favor intente nuevamente")
            if eliminarCatNum >= 1 and eliminarCatNum <= num:
                nombre = listNomCat[eliminarCatNum - 1]
                break
            else:
                utilidades.imp(f'El número "{eliminarCatNum}" NO tiene asignado ninguna categoria de la lista\nIntente nuevamente')

        numProcesosUsCat = procesos_con_categoria_usandose(datos, nombre)

        if len(numProcesosUsCat) != 0:
            utilidades.imp(f'No se puede eliminar la categoria "{nombre}" ya que hay {len(numProcesosUsCat)} procesos que la están utilizando, los cuales son:\n')
            for numProceso in numProcesosUsCat:
                proceso = datos["procesos"][numProceso - 1]
                utilidades.imp(f"Número proceso: {numProceso} - Ruta origen: {proceso["origen"]} - Ruta destino: {proceso["destino"]}")
            return
        else:
            if preguntar_si_no(f'¿Seguro que quiere eliminar la categoria "{nombre}"?') == True:
                del categorias["personalizados"][nombre]
                with open(utilidades.ruta_completa("config.json"), "w", encoding= "utf-8") as f:
                    json.dump(categorias, f, indent=2)

                utilidades.escribir_log(f'La categoria "{nombre}" fue eliminada')
                utilidades.imp(f'La categoria "{nombre}" fue eliminada correctamente')
            else:
                utilidades.imp("OK")
                return


def menu_categorias(datos):
    while True:
        mostrar_categorias(datos)
        utilidades.imp("")
        utilidades.imp("1. Crear categoria")
        utilidades.imp("2. Eliminar categoria")
        utilidades.imp("3. Volver")

        opcion = utilidades.intLea("Ingrese el numero asignado a una de las opciones anteriores:\n", 
                        "El dato ingresado es invalido, por favor intente nuevamente")

        match opcion:
            case 1:
                crear_categoria()

            case 2:
                eliminar_categoria(datos)

            case 3:
                break

            case _:
                utilidades.imp("Opción invalida, por favor ingrese una opción que se encuentre en el menú de opciones")


def ver_historial():

    try:
        with open(utilidades.ruta_completa("log.txt"), "r", encoding= "utf-8") as f:
            lineas = f.readlines()

    except FileNotFoundError:
        utilidades.imp("El archivo que contiene el historial NO existe")
        return

    if len(lineas) == 0:
        utilidades.imp("El historial esta vacío")
        return
    else:
        for linea in lineas:
            utilidades.imp(linea.strip("\n"))


def limpiar_historial():
    try:
        with open(utilidades.ruta_completa("log.txt"), "r", encoding= "utf-8") as f:
            lineas = f.readlines()
    
    except FileNotFoundError:
        utilidades.imp("El archivo que contiene el historial NO existe")
        return
    
    if len(lineas) != 0:
        if preguntar_si_no("¿Seguro que quiere limpiar el historial?") == True:
            with open(utilidades.ruta_completa("log.txt"), "w", encoding= "utf-8") as f:
                pass
            utilidades.imp("El historial ha sido limpiado correctamente")
        else:
            utilidades.imp("OK")
            return
    else:
        utilidades.imp("No es necesario limpiar el historial ya que este se encuentra vacío")
        return


def menu_historial():
    while True:
        ver_historial()
        utilidades.imp("\n1. Limpiar el historial")
        utilidades.imp("2. Volver")

        opcion = utilidades.intLea("Ingrese el numero asignado a una de las opciones anteriores:\n", 
                        "El dato ingresado es invalido, por favor intente nuevamente")

        match opcion:
            case 1:
                limpiar_historial()

            case 2:
                break

            case _:
                utilidades.imp("Opción invalida, por favor ingrese una opción que se encuentre en el menú de opciones")
                

def eliminar_procesos(datos):
    while True:

        lista_procesos(datos)
        numero = utilidades.intLea("Ingrese el número asociado al proceso que desea eliminar:\n",
                                "El dato ingresado es invalido, por favor intente nuevamente")
        
        if numero >= 1 and numero <= len(datos["procesos"]):
            proceso = datos["procesos"][numero - 1]
            utilidades.imp(f"{numero}. Origen: {proceso["origen"]} - Destino: {proceso["destino"]} - Categoria: {proceso["categoria"]}")

            if preguntar_si_no("¿Seguro que quiere eliminar ese proceso?") == True:
                del datos["procesos"][numero - 1]

                with open(utilidades.ruta_completa("rutas.json"), "w", encoding= "utf-8") as f:
                    json.dump(datos, f)

                utilidades.escribir_log(f'Se elimino el proceso "{proceso}"')
                utilidades.imp("El proceso ha sido eliminado correctamente")

                if len(datos["procesos"]) == 0:
                    utilidades.imp("Ya no quedan procesos por eliminar")
                    break

                if preguntar_si_no("¿Desea eliminar otro proceso?") == False:
                    break
            else:
                utilidades.imp("OK")
                break
        else:
            utilidades.imp(f'El número "{numero}" NO tiene asignado ningún proceso de la lista\nIntente nuevamente')


def crear_archivos_por_defecto():
    config = utilidades.ruta_completa("config.json")
    rutas = utilidades.ruta_completa("rutas.json")

    if os.path.exists(config) == False:
        porDefectoConf = {
            "predeterminados": {
                "Imagenes": [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".webp"
                ],
                "Documentos": [
                ".pdf",
                ".docx",
                ".txt",
                ".xlsx"
                ]
            },
            "personalizados": {}
            }
        
        with open(config, "w", encoding= "utf-8") as f:
            json.dump(porDefectoConf, f, indent= 2)

    if os.path.exists(rutas) == False:
        porDefectoRut = {"procesos": []}

        with open(rutas, "w", encoding= "utf-8") as f:
            json.dump(porDefectoRut, f, indent= 2)

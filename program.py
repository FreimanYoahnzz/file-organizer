import things
import utilidades
import json
import sys

NOM_DES = "FREIMHZZ STUDIO"

things.crear_archivos_por_defecto()

with open(utilidades.ruta_completa("rutas.json"),"r", encoding= "utf-8") as f:
    datos = json.load(f)

if "autoejecutar" in sys.argv:
    things.modo_automatico(datos)
    sys.exit()

while True:
    if len(datos["procesos"]) == 0:
        if things.preguntar_si_no("Aún NO hay procesos en ejecución\n¿Desea agregar uno?") == True:
            things.agg_proceso(datos)
        else:
            utilidades.salir()

    else:

        utilidades.imp_derecha(f"Programa desarrollado por: {NOM_DES}\n")

        things.mostrar_estado_autoejecucion()
        if len(datos["procesos"]) == 1:
            utilidades.imp(f"Hay {len(datos["procesos"])} proceso en ejecución:\n")
        else:
            utilidades.imp(f"Hay {len(datos["procesos"])} procesos en ejecución:\n")
        
        things.lista_procesos(datos)

        utilidades.imp("\n¿Que desea hacer?\nOpciones:")
        utilidades.imp("1. Usar los procesos con las rutas actuales")
        utilidades.imp("2. Agregar un nuevo proceso")
        utilidades.imp("3. Modificar un proceso existente")
        utilidades.imp("4. Modo automático")
        utilidades.imp("5. Categorias(Tipos de archivos a mover)")
        utilidades.imp("6. Ver historial de actividad")
        utilidades.imp("7. Eliminar procesos")
        utilidades.imp("8. Salir del programa")
        opcion = utilidades.intLea("Ingrese el numero asignado a una de las opciones anteriores:\n", "El dato ingresado es invalido, por favor intente nuevamente")

        match opcion:
            case 1:
                utilidades.imp("\tEJECUTAR PROCESOS ACTUALES\n")
                things.ejecutar_todos_los_procesos(datos)

            case 2:
                utilidades.imp("\tAGREGAR NUEVO PROCESO\n")
                things.agg_proceso(datos)

            case 3:
                utilidades.imp("\tMODIFICAR PROCESO EXISTENTE\n") 

                while True:
                    things.lista_procesos(datos)
                    utilidades.imp("\n¿Que proceso desea modificar?")
                    
                    busProceso = utilidades.intLea("Ingrese el número del proceso a modificar:\n", "El dato ingresado es invalido, por favor intente nuevamente")

                    if busProceso <= len(datos["procesos"]) and busProceso > 0:
                        categoria = things.modificar_categoria("¿Desea modificar solo la categoria?")

                        categoriaVieja = datos["procesos"][busProceso - 1]["categoria"]

                        if categoria != None:
                            datos["procesos"][busProceso - 1]["categoria"] = categoria

                            with open(utilidades.ruta_completa("rutas.json"), "w", encoding= "utf-8") as f:
                                json.dump(datos, f)

                            utilidades.imp(f"la categoria del archivo paso de: {categoriaVieja} A {categoria}")

                            if things.mod_otro_proceso() == False:
                                break

                        elif categoria == None:

                            rutaOrigenVieja = datos["procesos"][busProceso - 1]["origen"]
                            rutaDestinoVieja = datos["procesos"][busProceso - 1]["destino"]
                        
                            utilidades.imp("¿Que ruta/s desea modificar?")
                            utilidades.imp("1. Ambas rutas")
                            utilidades.imp("2. Ruta origen")
                            utilidades.imp("3. Ruta destino")

                            while True:
                                opcion = utilidades.intLea("Ingrese el numero asignado a una de las opciones anteriores:\n", 
                                                            "El dato ingresado es invalido, por favor intente nuevamente")

                                match opcion:
                                    case 1:
                                        utilidades.imp("\tMODIFICAR RUTAS ORIGEN Y DESTINO\n")

                                        origen = things.pedir_ruta("Ingrese la ruta origen de la carpeta DE donde se van a mover los archivos:\n")
                                        destino = things.pedir_ruta("Ingrese la ruta destino de la carpeta A donde se van a mover los archivos:\n")
                                        categoria = things.modificar_categoria("¿Desea modificar también la categoria?")

                                        datos["procesos"][busProceso - 1]["origen"] = origen    
                                        datos["procesos"][busProceso - 1]["destino"] = destino
                                        if categoria != None:
                                            datos["procesos"][busProceso - 1]["categoria"] = categoria

                                        with open(utilidades.ruta_completa("rutas.json"), "w", encoding= "utf-8") as f:
                                            json.dump(datos, f)

                                        utilidades.imp("Rutas origen y destino modificadas con éxito")
                                        utilidades.imp(f"La ruta  origen paso de: {rutaOrigenVieja} A {origen}")
                                        utilidades.imp(f"La ruta destino paso de: {rutaDestinoVieja} A {destino}")
                                        if categoria != None:
                                            utilidades.imp(f"la categoria del archivo paso de: {categoriaVieja} A {categoria}")

                                        break

                                    case 2:
                                        utilidades.imp("\tMODIFICAR RUTA ORIGEN\n")

                                        origen = things.pedir_ruta("Ingrese la ruta origen de la carpeta DE donde se van a mover los archivos:\n")
                                        categoria = things.modificar_categoria("¿Desea modificar también la categoria?")

                                        datos["procesos"][busProceso - 1]["origen"] = origen
                                        if categoria != None:
                                            datos["procesos"][busProceso - 1]["categoria"] = categoria
                                        
                                        with open(utilidades.ruta_completa("rutas.json"), "w", encoding= "utf-8") as f:
                                            json.dump(datos, f)

                                        utilidades.imp("Ruta origen modificada con éxito")
                                        utilidades.imp(f"La ruta  origen paso de: {rutaOrigenVieja} A {origen}")
                                        if categoria != None:
                                            utilidades.imp(f"la categoria del archivo paso de: {categoriaVieja} A {categoria}")

                                        break

                                    case 3:
                                        utilidades.imp("\tMODIFICAR RUTA DESTINO\n")

                                        destino = things.pedir_ruta("Ingrese la ruta destino de la carpeta A donde se van a mover los archivos:\n")
                                        categoria = things.modificar_categoria("¿Desea modificar también la categoria?")

                                        datos["procesos"][busProceso - 1]["destino"] = destino
                                        if categoria != None:
                                            datos["procesos"][busProceso - 1]["categoria"] = categoria

                                        with open(utilidades.ruta_completa("rutas.json"), "w", encoding= "utf-8") as f:
                                            json.dump(datos, f)

                                        utilidades.imp("Ruta destino modificada con éxito")
                                        utilidades.imp(f"La ruta  destino paso de: {rutaDestinoVieja} A {destino}")
                                        if categoria != None:
                                            utilidades.imp(f"la categoria del archivo paso de: {categoriaVieja} A {categoria}")

                                        break
                                
                                    case _:
                                        utilidades.imp("Opción invalida, por favor ingrese una opción que se encuentre en el menú de opciones")

                            if things.mod_otro_proceso() == False:
                                break
                    else:
                        utilidades.imp(f"El número de proceso que ingresaste({busProceso}) NO tiene asignado ningún proceso existente, por favor intente nuevamente.\n")

            case 4:
                utilidades.imp("\tMODO AUTOMÁTICO\n")
                things.menu_modo_automatico()

            case 5:
                utilidades.imp("\tCATEGORIAS\n")
                things.menu_categorias(datos)

            case 6:
                utilidades.imp("\tHISTORIAL DE ACTIVIDAD\n")
                things.menu_historial()

            case 7:
                utilidades.imp("\tELIMINAR PROCESOS")
                things.eliminar_procesos(datos)

            case 8:
                utilidades.salir()
            case _:
                utilidades.imp("Por favor ingrese una opción que se encuentre en el menú de opciones")

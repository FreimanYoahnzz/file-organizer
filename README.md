# FILE ORGANIZER
Es un programa para Windows que sirve para pasar archivos de una carpeta a otra de forma automática.  
## Qué hace
- mueve archivos según la categoría (extensiones de archivo) a la que pertenezca
- permite crear procesos personalizados (de donde a donde se van a mover los archivos)
- permite crear categorías personalizadas
- registra los movimientos de los procesos
- permite ejecutar los procesos de forma manual o activar un modo automático con el cual no hay que estar ejecutando cada vez que se requiera mover un archivo de un lado a otro
- si un archivo tiene el mismo nombre que un archivo que ya se encontraba en la ruta de destino, este automáticamente lo renombra

## Descarga y uso

### Descarga

1. Entra a la página de [Releases](https://github.com/FreimanYoahnzz/file-organizer/releases).
2. Descarga el archivo `FileOrganizer-v1.0.zip`.
3. Extráelo en una carpeta que no vayas a mover de lugar (por ejemplo `C:\FileOrganizer`).

### Cómo empezar

1. Abre solo `FileOrganizer.exe`. El archivo `FileOrganizerAuto.exe` lo usa el programa en segundo plano para el modo automático, y tiene que estar en la misma carpeta.
2. En el primer arranque el programa crea solo, junto al exe, los archivos `config.json` y `rutas.json`. El historial (`log.txt`) se crea cuando el programa registra su primera actividad.
3. Elige la opción **2. Agregar un nuevo proceso** e ingresa la carpeta de origen, la carpeta de destino y la categoría de archivos a mover.
4. Elige la opción **1. Usar los procesos con las rutas actuales** para mover los archivos en ese momento.
5. Si quieres que se ejecute solo, entra a **4. Modo automático** y elige **1. Activar modo autoejecutar**.

### Aviso de Windows

Al abrir el programa por primera vez, Windows puede mostrar el aviso **"Windows protegió su PC"**. Aparece porque el programa no tiene firma digital, no porque tenga algún problema. Para continuar, pulsa **Más información** y luego **Ejecutar de todas formas**.

## Limitaciones conocidas

Esta es una versión beta (v1.0). Tiene estas limitaciones:

- **Solo funciona en Windows.**
- **El modo automático** revisa las carpetas cada 2 minutos. Solo funciona con tu sesión de Windows abierta. En portátiles, la tarea se pausa mientras el equipo funciona con batería y continúa cuando conectas el cargador.
- **Si mueves la carpeta del programa** después de activar el modo automático, la tarea sigue apuntando a la ubicación anterior. Para arreglarlo, entra a **4. Modo automático**, elimina la tarea y vuelve a activarla desde la nueva ubicación.
- **Una categoría que está en uso** por algún proceso no se puede eliminar. Primero cambia la categoría de ese proceso.
- **Dos procesos con la misma carpeta de origen y la misma extensión** no generan ninguna advertencia. El primero que se ejecute se queda con los archivos.
- **`FileOrganizerAuto.exe` no está pensado para abrirse a mano.** Lo ejecuta Windows en segundo plano, así que usa siempre `FileOrganizer.exe`.

## Cómo construir los .exe

Si quieres generar los ejecutables tú mismo a partir del código, necesitas Python 3.12 o superior y PyInstaller:

```
pip install pyinstaller
```

Desde la carpeta del proyecto, genera los dos ejecutables:

```
pyinstaller --onefile --clean --name FileOrganizer --icon FileOrganizer.ico program.py
pyinstaller --onefile --noconsole --clean --name FileOrganizerAuto --icon FileOrganizerAuto.ico program.py
```

Los ejecutables quedan en la carpeta `dist/`. Ambos deben estar en la misma carpeta para que el modo automático funcione.

## Próximas versiones

Mejoras que planeo para las siguientes versiones:

- Interfaz gráfica.
- Advertencia cuando dos procesos comparten la misma carpeta de origen y la misma extensión.
- Elegir qué procesos se ejecutan en el modo automático.
- Intervalo de tiempo del modo automático configurable (cada cuanto se ejecuta el modo automatico, actualmente es cada 2 min).
- Agregar y quitar extensiones de una categoría existente.
- Ver las últimas líneas del historial.
- Ver los procesos que usan una categoría sin tener que eliminarla.

## Autor y licencia

Desarrollado por **FreimanYoahnzz** (Freimhzz Studio).

Distribuido bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
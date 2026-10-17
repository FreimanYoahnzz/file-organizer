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
# Gestor de Tareas (To-Do List)

Una aplicación de escritorio para gestionar tareas diarias, desarrollada en Python con Tkinter.

## Características

- Interfaz moderna y elegante con esquema de colores azul y negro
- Creación y eliminación de tareas
- Marcado de tareas como completadas
- Filtrado de tareas (todas, pendientes, completadas)
- Contador de tareas pendientes y completadas
- Persistencia de datos (las tareas se guardan automáticamente)
- Fecha y hora de creación de cada tarea

## Requisitos

- Python 3.6 o superior
- Tkinter (incluido en la instalación estándar de Python)

## Instalación

1. Clona o descarga este repositorio
2. Navega al directorio del proyecto:
   ```
   cd toDo
   ```
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta la aplicación:
   ```
   python app.py
   ```
2. Para agregar una tarea:
   - Escribe el texto de la tarea en el campo de entrada
   - Presiona el botón "Agregar"
3. Para marcar una tarea como completada:
   - Selecciona la tarea en la lista
   - Presiona el botón "Marcar como completada"
4. Para eliminar una tarea:
   - Selecciona la tarea en la lista
   - Presiona el botón "Eliminar"
5. Para filtrar tareas:
   - Usa los botones "Todas", "Pendientes" o "Completadas"

## Compilación a Ejecutable

Para crear un archivo ejecutable (.exe) en Windows:

1. Instala PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Compila la aplicación:
   ```
   pyinstaller --onefile --windowed app.py
   ```
3. El ejecutable se creará en la carpeta `dist`

## Estructura del Proyecto

```
toDo/
├── app.py              # Aplicación principal
├── tareas.json         # Archivo de datos (se crea automáticamente)
├── requirements.txt    # Dependencias
└── README.md          # Documentación
```

## Licencia

Este proyecto está bajo la Licencia MIT. 
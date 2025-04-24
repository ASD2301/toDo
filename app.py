import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class TodoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestor de Tareas")
        self.root.geometry("800x600")
        
        # Configurar estilos
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#0074D9')
        self.style.configure('TLabel', background='#0074D9', foreground='black', font=('Arial', 12))
        self.style.configure('TButton', background='#000000', foreground='black', font=('Arial', 12, 'bold'))
        self.style.configure('Treeview', background='white', foreground='black', fieldbackground='white', font=('Arial', 12))
        self.style.configure('Treeview.Heading', background='#0074D9', foreground='black', font=('Arial', 12, 'bold'))
        self.style.map('Treeview', background=[('selected', '#0074D9')], foreground=[('selected', 'black')])
        
        # Configurar estilo para el Entry
        self.style.configure('TEntry', fieldbackground='white', foreground='black', font=('Arial', 12))
        
        # Variables
        self.tareas = []
        self.archivo_datos = 'tareas.json'
        
        # Cargar tareas existentes
        self.cargar_tareas()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(self.main_frame, text="Gestor de Tareas", 
                 font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=3, pady=20)
        
        # Contador de tareas
        self.contador_frame = ttk.Frame(self.main_frame)
        self.contador_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.contador_pendientes = ttk.Label(self.contador_frame, text="Pendientes: 0")
        self.contador_pendientes.grid(row=0, column=0, padx=10)
        
        self.contador_completadas = ttk.Label(self.contador_frame, text="Completadas: 0")
        self.contador_completadas.grid(row=0, column=1, padx=10)
        
        # Entrada de nueva tarea
        ttk.Label(self.main_frame, text="Nueva tarea:").grid(row=2, column=0, pady=10)
        self.nueva_tarea = ttk.Entry(self.main_frame, width=40)
        self.nueva_tarea.grid(row=2, column=1, pady=10)
        
        ttk.Button(self.main_frame, text="Agregar", 
                  command=self.agregar_tarea,
                  style='TButton').grid(row=2, column=2, pady=10)
        
        # Filtros
        self.filtro_frame = ttk.Frame(self.main_frame)
        self.filtro_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(self.filtro_frame, text="Todas", 
                  command=lambda: self.filtrar_tareas("todas"),
                  style='TButton').grid(row=0, column=0, padx=5)
        
        ttk.Button(self.filtro_frame, text="Pendientes", 
                  command=lambda: self.filtrar_tareas("pendientes"),
                  style='TButton').grid(row=0, column=1, padx=5)
        
        ttk.Button(self.filtro_frame, text="Completadas", 
                  command=lambda: self.filtrar_tareas("completadas"),
                  style='TButton').grid(row=0, column=2, padx=5)
        
        # Lista de tareas
        self.lista_frame = ttk.Frame(self.main_frame)
        self.lista_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.tree = ttk.Treeview(self.lista_frame, columns=('ID', 'Tarea', 'Estado', 'Fecha'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tarea', text='Tarea')
        self.tree.heading('Estado', text='Estado')
        self.tree.heading('Fecha', text='Fecha')
        
        self.tree.column('ID', width=50)
        self.tree.column('Tarea', width=400)
        self.tree.column('Estado', width=100)
        self.tree.column('Fecha', width=150)
        
        # Configurar el estilo para las tareas completadas
        self.tree.tag_configure('completada', background='#90EE90')  # Verde claro
        
        self.tree.grid(row=0, column=0)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.lista_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Botones de acción
        self.acciones_frame = ttk.Frame(self.main_frame)
        self.acciones_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        ttk.Button(self.acciones_frame, text="Marcar como completada", 
                  command=self.marcar_completada,
                  style='TButton').grid(row=0, column=0, padx=5)
        
        ttk.Button(self.acciones_frame, text="Eliminar", 
                  command=self.eliminar_tarea,
                  style='TButton').grid(row=0, column=1, padx=5)
        
        ttk.Button(self.acciones_frame, text="Editar", 
                  command=self.editar_tarea,
                  style='TButton').grid(row=0, column=2, padx=5)
        
        # Actualizar lista
        self.actualizar_lista()
        
    def cargar_tareas(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r') as f:
                    self.tareas = json.load(f)
                    # Asegurar que los IDs sean consecutivos
                    for i, tarea in enumerate(self.tareas, 1):
                        tarea['id'] = i
                    # Guardar las tareas actualizadas
                    self.guardar_tareas()
            except:
                self.tareas = []
        else:
            self.tareas = []
            
    def guardar_tareas(self):
        with open(self.archivo_datos, 'w') as f:
            json.dump(self.tareas, f)
            
    def agregar_tarea(self):
        texto = self.nueva_tarea.get().strip()
        if texto:
            tarea = {
                'id': len(self.tareas) + 1,  # ID único basado en la posición + 1 para empezar desde 1
                'texto': texto,
                'completada': False,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            self.tareas.append(tarea)
            self.nueva_tarea.delete(0, tk.END)
            self.guardar_tareas()
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese una tarea")
            
    def marcar_completada(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            tarea_id = item['values'][0]  # El ID está en la primera columna
            for tarea in self.tareas:
                if tarea['id'] == tarea_id:
                    tarea['completada'] = not tarea['completada']
                    break
            self.guardar_tareas()
            self.actualizar_lista()
            
    def eliminar_tarea(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            tarea_id = item['values'][0]  # El ID está en la primera columna
            # Eliminar la tarea
            self.tareas = [t for t in self.tareas if t['id'] != tarea_id]
            # Reordenar los IDs de manera consecutiva
            for i, tarea in enumerate(self.tareas, 1):
                tarea['id'] = i
            # Guardar los cambios
            self.guardar_tareas()
            # Actualizar la lista
            self.actualizar_lista()
            
    def actualizar_lista(self):
        # Limpiar lista
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Agregar tareas
        for tarea in self.tareas:
            estado = "Completada" if tarea['completada'] else "Pendiente"
            item = self.tree.insert('', 'end', values=(
                tarea['id'],
                tarea['texto'],
                estado,
                tarea['fecha']
            ))
            # Agregar fondo verde claro para tareas completadas
            if tarea['completada']:
                self.tree.item(item, tags=('completada',))
            
        # Actualizar contadores
        completadas = sum(1 for t in self.tareas if t['completada'])
        pendientes = len(self.tareas) - completadas
        
        self.contador_completadas.config(text=f"Completadas: {completadas}")
        self.contador_pendientes.config(text=f"Pendientes: {pendientes}")
        
    def filtrar_tareas(self, filtro):
        # Limpiar lista
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Filtrar y agregar tareas
        for tarea in self.tareas:
            if (filtro == "todas" or
                (filtro == "pendientes" and not tarea['completada']) or
                (filtro == "completadas" and tarea['completada'])):
                estado = "Completada" if tarea['completada'] else "Pendiente"
                item = self.tree.insert('', 'end', values=(
                    tarea['id'],
                    tarea['texto'],
                    estado,
                    tarea['fecha']
                ))
                # Agregar fondo verde claro para tareas completadas
                if tarea['completada']:
                    self.tree.item(item, tags=('completada',))
                    
    def editar_tarea(self):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            tarea_id = item['values'][0]  # El ID está en la primera columna
            texto_actual = item['values'][1]  # El texto actual está en la segunda columna
            
            # Crear ventana de edición
            ventana_edicion = tk.Toplevel(self.root)
            ventana_edicion.title("Editar Tarea")
            ventana_edicion.geometry("400x100")
            
            # Frame para la edición
            frame_edicion = ttk.Frame(ventana_edicion, padding="10")
            frame_edicion.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Label y Entry para editar
            ttk.Label(frame_edicion, text="Nuevo nombre de la tarea:").grid(row=0, column=0, pady=5)
            nuevo_texto = ttk.Entry(frame_edicion, width=40)
            nuevo_texto.grid(row=0, column=1, pady=5)
            nuevo_texto.insert(0, texto_actual)
            
            def guardar_edicion():
                nuevo_nombre = nuevo_texto.get().strip()
                if nuevo_nombre:
                    # Actualizar la tarea en la lista
                    for tarea in self.tareas:
                        if tarea['id'] == tarea_id:
                            tarea['texto'] = nuevo_nombre
                            break
                    # Guardar cambios
                    self.guardar_tareas()
                    # Actualizar la lista
                    self.actualizar_lista()
                    # Cerrar ventana
                    ventana_edicion.destroy()
                else:
                    messagebox.showwarning("Advertencia", "El nombre de la tarea no puede estar vacío")
            
            # Botón para guardar
            ttk.Button(frame_edicion, text="Guardar", 
                      command=guardar_edicion,
                      style='TButton').grid(row=1, column=0, columnspan=2, pady=10)
            
            # Centrar la ventana
            ventana_edicion.transient(self.root)
            ventana_edicion.grab_set()
            self.root.wait_window(ventana_edicion)
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione una tarea para editar")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TodoApp()
    app.run() 
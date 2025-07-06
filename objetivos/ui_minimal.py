# objetivos/ui_minimal.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date
import threading
import time

from objetivos.gestor_objetivos import GestorObjetivos
from utils.helpers import formatear_tiempo

class ObjetivosUI:
    def __init__(self):
        self.gestor = GestorObjetivos()
        self.root = None
        self.frame_objetivos = None
        self.objetivos_widgets = {}
        
    def crear_ventana(self):
        """Crea la ventana principal de objetivos"""
        self.root = tk.Tk()
        self.root.title("🎯 Objetivos Diarios")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        
        # Hacer que la ventana se mantenga al frente
        self.root.attributes('-topmost', True)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="🎯 OBJETIVOS DE HOY", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Botones de acción
        frame_botones = ttk.Frame(main_frame)
        frame_botones.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky='ew')
        
        ttk.Button(frame_botones, text="➕ Nuevo Objetivo", 
                  command=self.crear_objetivo).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(frame_botones, text="🔄 Actualizar", 
                  command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="📊 Resumen", 
                  command=self.mostrar_resumen).pack(side=tk.LEFT, padx=5)
        
        # Botón de personalización
        ttk.Button(frame_botones, text="🎨 Personalizar", 
                  command=self.abrir_personalizacion).pack(side=tk.RIGHT)
        
        # Frame para objetivos con scroll
        self.crear_area_objetivos(main_frame)
        
        # Configurar redimensionamiento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Cargar objetivos iniciales
        self.actualizar_lista()
        
        return self.root
    
    def crear_area_objetivos(self, parent):
        """Crea el área scrolleable para mostrar objetivos"""
        # Canvas y scrollbar para scroll
        canvas = tk.Canvas(parent, bg='white', height=250)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.frame_objetivos = ttk.Frame(canvas)
        
        # Configurar scroll
        self.frame_objetivos.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.frame_objetivos, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        canvas.grid(row=2, column=0, columnspan=2, sticky='nsew', pady=(0, 10))
        scrollbar.grid(row=2, column=2, sticky='ns', pady=(0, 10))
        
        parent.rowconfigure(2, weight=1)
    
    def actualizar_lista(self):
        """Actualiza la lista de objetivos mostrada"""
        # Limpiar widgets existentes
        for widget in self.frame_objetivos.winfo_children():
            widget.destroy()
        self.objetivos_widgets.clear()
        
        # Obtener objetivos actuales
        objetivos = self.gestor.obtener_objetivos_hoy()
        
        if not objetivos:
            # Mostrar mensaje si no hay objetivos
            label_vacio = ttk.Label(self.frame_objetivos, 
                                   text="📝 No hay objetivos para hoy.\n¡Crea algunos para empezar!",
                                   font=('Arial', 12),
                                   foreground='gray')
            label_vacio.pack(pady=20)
            return
        
        # Mostrar cada objetivo
        for objetivo in objetivos:
            self.crear_widget_objetivo(objetivo)
    
    def crear_widget_objetivo(self, objetivo):
        """Crea un widget para mostrar un objetivo individual"""
        # Frame contenedor para el objetivo
        frame_obj = ttk.LabelFrame(self.frame_objetivos, 
                                  text=f"Objetivo #{objetivo['id']}", 
                                  padding="10")
        frame_obj.pack(fill='x', pady=5, padx=5)
        
        # Estado del objetivo (emoji y color)
        estado_emoji = "✅" if objetivo['completado'] else "⏳"
        color_estado = "green" if objetivo['completado'] else "orange"
        
        # Descripción del objetivo
        label_desc = ttk.Label(frame_obj, 
                              text=f"{estado_emoji} {objetivo['descripcion']}",
                              font=('Arial', 11, 'bold'))
        label_desc.grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 5))
        
        # Barra de progreso
        progreso_pct = (objetivo['progreso'] / objetivo['meta']) * 100
        
        progress_frame = ttk.Frame(frame_obj)
        progress_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 5))
        
        progress_bar = ttk.Progressbar(progress_frame, 
                                      value=progreso_pct, 
                                      maximum=100,
                                      length=200)
        progress_bar.pack(side=tk.LEFT, fill='x', expand=True)
        
        # Etiqueta de progreso
        label_progreso = ttk.Label(progress_frame, 
                                  text=f"{objetivo['progreso']}/{objetivo['meta']} ({progreso_pct:.0f}%)")
        label_progreso.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Botones de acción
        frame_botones = ttk.Frame(frame_obj)
        frame_botones.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(5, 0))
        
        if not objetivo['completado']:
            # Botón para avanzar (+1)
            btn_avanzar = ttk.Button(frame_botones, 
                                   text="↗️ +1",
                                   width=8,
                                   command=lambda oid=objetivo['id']: self.avanzar_objetivo(oid, 1))
            btn_avanzar.pack(side=tk.LEFT, padx=(0, 5))
            
            # Botón para completar
            btn_completar = ttk.Button(frame_botones, 
                                     text="✅ Completar",
                                     command=lambda oid=objetivo['id']: self.completar_objetivo(oid))
            btn_completar.pack(side=tk.LEFT, padx=5)
        
        # Botón para eliminar
        btn_eliminar = ttk.Button(frame_botones, 
                                text="🗑️ Eliminar",
                                command=lambda oid=objetivo['id']: self.eliminar_objetivo(oid))
        btn_eliminar.pack(side=tk.RIGHT)
        
        # Configurar expansión de columnas
        frame_obj.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        
        # Guardar referencia del widget
        self.objetivos_widgets[objetivo['id']] = frame_obj
    
    def crear_objetivo(self):
        """Muestra diálogo para crear un nuevo objetivo"""
        dialog = ObjetivoDialog(self.root)
        resultado = dialog.resultado
        
        if resultado:
            descripcion, meta = resultado
            self.gestor.crear_objetivo_diario(descripcion, meta)
            self.actualizar_lista()
            messagebox.showinfo("✅", f"Objetivo creado: {descripcion}")
    
    def avanzar_objetivo(self, objetivo_id, incremento=1):
        """Avanza el progreso de un objetivo"""
        if self.gestor.avanzar_objetivo(objetivo_id, incremento):
            self.actualizar_lista()
        else:
            messagebox.showerror("❌", "Error al avanzar objetivo")
    
    def completar_objetivo(self, objetivo_id):
        """Marca un objetivo como completado"""
        if self.gestor.marcar_objetivo_completado(objetivo_id):
            self.actualizar_lista()
            messagebox.showinfo("🎉", "¡Objetivo completado!")
        else:
            messagebox.showerror("❌", "Error al completar objetivo")
    
    def eliminar_objetivo(self, objetivo_id):
        """Elimina un objetivo después de confirmación"""
        if messagebox.askyesno("🗑️ Confirmar", "¿Estás seguro de eliminar este objetivo?"):
            if self.gestor.eliminar_objetivo(objetivo_id):
                self.actualizar_lista()
                messagebox.showinfo("✅", "Objetivo eliminado")
            else:
                messagebox.showerror("❌", "Error al eliminar objetivo")
    
    def mostrar_resumen(self):
        """Muestra el resumen del día"""
        resumen = self.gestor.obtener_resumen_diario()
        
        mensaje = f"""📊 RESUMEN DEL DÍA
        
Fecha: {resumen['fecha']}
Total de objetivos: {resumen['total_objetivos']}
Objetivos completados: {resumen['objetivos_completados']}
Porcentaje completado: {resumen['porcentaje_completado']:.1f}%

{"🎉 ¡Excelente trabajo!" if resumen['porcentaje_completado'] >= 100 else "💪 ¡Sigue así!" if resumen['porcentaje_completado'] >= 50 else "🚀 ¡Puedes hacerlo mejor!"}"""
        
        messagebox.showinfo("📊 Resumen", mensaje)
    
    def abrir_personalizacion(self):
        """Abre la ventana de personalización"""
        try:
            from personalizacion import abrir_ui_personalizacion
            
            # Crear ventana de personalización como hijo de la ventana actual
            ui_personalizacion = abrir_ui_personalizacion(self.root)
            
            # Centrar la ventana
            ui_personalizacion.ventana.update_idletasks()
            x = (ui_personalizacion.ventana.winfo_screenwidth() // 2) - (800 // 2)
            y = (ui_personalizacion.ventana.winfo_screenheight() // 2) - (600 // 2)
            ui_personalizacion.ventana.geometry(f"800x600+{x}+{y}")
            
            # Foco en la nueva ventana
            ui_personalizacion.ventana.focus_force()
            
        except ImportError as e:
            messagebox.showerror("❌ Error", 
                               "El módulo de personalización no está disponible.\n"
                               "Asegúrate de que todos los archivos estén instalados correctamente.")
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo abrir la personalización:\n{e}")

    def ejecutar(self):
        """Ejecuta la interfaz gráfica"""
        ventana = self.crear_ventana()
        ventana.mainloop()

class ObjetivoDialog:
    def __init__(self, parent):
        self.resultado = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("➕ Crear Nuevo Objetivo")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        
        # Hacer modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar en pantalla
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.crear_formulario()
    
    def crear_formulario(self):
        """Crea el formulario para el nuevo objetivo"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Campo descripción
        ttk.Label(main_frame, text="📝 Descripción del objetivo:").pack(anchor='w', pady=(0, 5))
        self.entry_descripcion = ttk.Entry(main_frame, width=40, font=('Arial', 11))
        self.entry_descripcion.pack(fill='x', pady=(0, 15))
        self.entry_descripcion.focus()
        
        # Campo meta numérica
        ttk.Label(main_frame, text="🎯 Meta numérica (opcional):").pack(anchor='w', pady=(0, 5))
        self.entry_meta = ttk.Entry(main_frame, width=15)
        self.entry_meta.pack(anchor='w', pady=(0, 20))
        self.entry_meta.insert(0, "1")
        
        # Botones
        frame_botones = ttk.Frame(main_frame)
        frame_botones.pack(fill='x')
        
        ttk.Button(frame_botones, text="✅ Crear", command=self.crear).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(frame_botones, text="❌ Cancelar", command=self.cancelar).pack(side=tk.RIGHT)
        
        # Bind Enter para crear
        self.dialog.bind('<Return>', lambda e: self.crear())
        self.dialog.bind('<Escape>', lambda e: self.cancelar())
    
    def crear(self):
        """Procesa la creación del objetivo"""
        descripcion = self.entry_descripcion.get().strip()
        meta_text = self.entry_meta.get().strip()
        
        if not descripcion:
            messagebox.showerror("❌", "La descripción es obligatoria")
            return
        
        try:
            meta = int(meta_text) if meta_text else 1
            if meta <= 0:
                raise ValueError("La meta debe ser mayor a 0")
        except ValueError:
            messagebox.showerror("❌", "La meta debe ser un número entero positivo")
            return
        
        self.resultado = (descripcion, meta)
        self.dialog.destroy()
    
    def cancelar(self):
        """Cancela la creación del objetivo"""
        self.dialog.destroy()

def crear_ventana_flotante():
    """Crea una ventana flotante minimalista para objetivos"""
    # Esta función puede expandirse para crear una ventana pequeña
    # que permanezca visible durante el trabajo
    pass

def main():
    """Función principal para ejecutar la UI de objetivos"""
    try:
        app = ObjetivosUI()
        app.ejecutar()
    except Exception as e:
        print(f"❌ Error en UI de objetivos: {e}")

if __name__ == "__main__":
    main()

# personalizacion/ui_personalizacion.py - Interfaz para gestionar personalización

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
from .frases_motivadoras import sistema_frases
from .musica_motivacional import sistema_musica
from .temas_visuales import sistema_temas

class UIPersonalizacion:
    def __init__(self, parent=None):
        self.ventana = tk.Toplevel(parent) if parent else tk.Tk()
        self.ventana.title("🎨 Personalización - Timer Work")
        self.ventana.geometry("800x600")
        self.ventana.resizable(True, True)
        
        # Aplicar tema actual
        self.aplicar_tema()
        
        self.crear_interfaz()
        
    def aplicar_tema(self):
        """Aplica el tema visual actual a la ventana"""
        estilo = sistema_temas.obtener_estilo_tkinter()
        self.ventana.configure(bg=estilo['bg'])
        
        # Configurar colores de la ventana
        self.colores = {
            'fondo': estilo['bg'],
            'texto': estilo['fg'],
            'primario': sistema_temas.obtener_color('primario'),
            'secundario': sistema_temas.obtener_color('secundario'),
            'acento': sistema_temas.obtener_color('acento'),
            'exito': sistema_temas.obtener_color('exito'),
            'error': sistema_temas.obtener_color('error')
        }
        
    def crear_interfaz(self):
        """Crea la interfaz principal de personalización"""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestañas
        self.crear_pestaña_temas()
        self.crear_pestaña_frases()
        self.crear_pestaña_musica()
        self.crear_pestaña_recursos()
        
        # Botones inferiores
        self.crear_botones_principales()
        
    def crear_pestaña_temas(self):
        """Crea la pestaña de gestión de temas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎨 Temas Visuales")
        
        # Título
        titulo = tk.Label(frame, text="🎨 Personalización Visual", 
                         font=('Arial', 16, 'bold'),
                         bg=self.colores['fondo'],
                         fg=self.colores['primario'])
        titulo.pack(pady=10)
        
        # Frame para selección de tema
        frame_seleccion = tk.Frame(frame, bg=self.colores['fondo'])
        frame_seleccion.pack(fill='x', padx=20, pady=10)
        
        tk.Label(frame_seleccion, text="Tema actual:", 
                bg=self.colores['fondo'], fg=self.colores['texto']).pack(side='left')
        
        # Combobox para seleccionar tema
        self.combo_temas = ttk.Combobox(frame_seleccion, state='readonly')
        self.combo_temas.pack(side='left', padx=(10, 0), fill='x', expand=True)
        self.actualizar_lista_temas()
        self.combo_temas.bind('<<ComboboxSelected>>', self.cambiar_tema_seleccionado)
        
        # Vista previa del tema
        self.crear_vista_previa_tema(frame)
        
        # Botones de tema
        frame_botones_tema = tk.Frame(frame, bg=self.colores['fondo'])
        frame_botones_tema.pack(fill='x', padx=20, pady=10)
        
        btn_aplicar = tk.Button(frame_botones_tema, text="✅ Aplicar Tema",
                               command=self.aplicar_tema_seleccionado,
                               **sistema_temas.obtener_estilo_boton('exito'))
        btn_aplicar.pack(side='left', padx=(0, 5))
        
        btn_crear = tk.Button(frame_botones_tema, text="➕ Crear Tema Personalizado",
                             command=self.abrir_creador_tema,
                             **sistema_temas.obtener_estilo_boton())
        btn_crear.pack(side='left', padx=5)
        
    def crear_vista_previa_tema(self, parent):
        """Crea una vista previa del tema seleccionado"""
        frame_preview = tk.LabelFrame(parent, text="Vista Previa", 
                                     bg=self.colores['fondo'], 
                                     fg=self.colores['texto'])
        frame_preview.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Canvas para mostrar colores
        self.canvas_colores = tk.Canvas(frame_preview, height=100, 
                                       bg=self.colores['fondo'])
        self.canvas_colores.pack(fill='x', padx=10, pady=10)
        
        self.dibujar_preview_colores()
        
    def dibujar_preview_colores(self):
        """Dibuja los colores del tema en el canvas"""
        self.canvas_colores.delete("all")
        tema = sistema_temas.obtener_tema_actual()
        colores = tema['colores']
        
        x = 10
        width = 80
        height = 30
        
        for nombre, color in colores.items():
            # Rectángulo de color
            self.canvas_colores.create_rectangle(x, 10, x + width, 10 + height,
                                               fill=color, outline='black')
            # Etiqueta
            self.canvas_colores.create_text(x + width//2, 10 + height + 15,
                                          text=nombre, font=('Arial', 8))
            x += width + 10
        
    def crear_pestaña_frases(self):
        """Crea la pestaña de gestión de frases"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💬 Frases Motivadoras")
        
        # Título
        titulo = tk.Label(frame, text="💬 Gestión de Frases Motivadoras", 
                         font=('Arial', 16, 'bold'),
                         bg=self.colores['fondo'],
                         fg=self.colores['primario'])
        titulo.pack(pady=10)
        
        # Frame superior para controles
        frame_controles = tk.Frame(frame, bg=self.colores['fondo'])
        frame_controles.pack(fill='x', padx=20, pady=10)
        
        # Selector de categoría
        tk.Label(frame_controles, text="Categoría:", 
                bg=self.colores['fondo'], fg=self.colores['texto']).pack(side='left')
        
        self.combo_categorias = ttk.Combobox(frame_controles, state='readonly')
        self.combo_categorias.pack(side='left', padx=(5, 10))
        self.actualizar_categorias_frases()
        self.combo_categorias.bind('<<ComboboxSelected>>', self.mostrar_frases_categoria)
        
        # Botón probar frase
        btn_probar = tk.Button(frame_controles, text="🎲 Frase Aleatoria",
                              command=self.mostrar_frase_aleatoria,
                              **sistema_temas.obtener_estilo_boton())
        btn_probar.pack(side='right')
        
        # Lista de frases
        frame_lista = tk.LabelFrame(frame, text="Frases Existentes",
                                   bg=self.colores['fondo'], 
                                   fg=self.colores['texto'])
        frame_lista.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.lista_frases = scrolledtext.ScrolledText(frame_lista, height=10,
                                                     bg=self.colores['fondo'],
                                                     fg=self.colores['texto'])
        self.lista_frases.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame para agregar nueva frase
        frame_nueva = tk.LabelFrame(frame, text="Agregar Nueva Frase",
                                   bg=self.colores['fondo'], 
                                   fg=self.colores['texto'])
        frame_nueva.pack(fill='x', padx=20, pady=10)
        
        self.entry_nueva_frase = tk.Text(frame_nueva, height=3,
                                        bg=self.colores['fondo'],
                                        fg=self.colores['texto'])
        self.entry_nueva_frase.pack(fill='x', padx=10, pady=5)
        
        btn_agregar = tk.Button(frame_nueva, text="➕ Agregar Frase",
                               command=self.agregar_nueva_frase,
                               **sistema_temas.obtener_estilo_boton('exito'))
        btn_agregar.pack(pady=5)
        
    def crear_pestaña_musica(self):
        """Crea la pestaña de gestión de música"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎵 Música & Audio")
        
        # Título
        titulo = tk.Label(frame, text="🎵 Recursos de Audio y Música", 
                         font=('Arial', 16, 'bold'),
                         bg=self.colores['fondo'],
                         fg=self.colores['primario'])
        titulo.pack(pady=10)
        
        # Frame para categorías de música
        frame_cat_musica = tk.Frame(frame, bg=self.colores['fondo'])
        frame_cat_musica.pack(fill='x', padx=20, pady=10)
        
        tk.Label(frame_cat_musica, text="Tipo de música:", 
                bg=self.colores['fondo'], fg=self.colores['texto']).pack(side='left')
        
        self.combo_musica = ttk.Combobox(frame_cat_musica, state='readonly')
        self.combo_musica.pack(side='left', padx=(5, 10))
        self.actualizar_categorias_musica()
        self.combo_musica.bind('<<ComboboxSelected>>', self.mostrar_recursos_musica)
        
        # Botón de reproducción aleatoria
        btn_random = tk.Button(frame_cat_musica, text="🎲 Sorpréndeme",
                              command=self.reproducir_musica_aleatoria,
                              **sistema_temas.obtener_estilo_boton())
        btn_random.pack(side='right')
        
        # Lista de recursos musicales
        frame_lista_musica = tk.LabelFrame(frame, text="Recursos Disponibles",
                                          bg=self.colores['fondo'], 
                                          fg=self.colores['texto'])
        frame_lista_musica.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview para mostrar recursos con botones
        self.tree_musica = ttk.Treeview(frame_lista_musica, 
                                       columns=('Tipo', 'Descripción'), 
                                       show='tree headings')
        self.tree_musica.heading('#0', text='Nombre')
        self.tree_musica.heading('Tipo', text='Tipo')
        self.tree_musica.heading('Descripción', text='Descripción')
        self.tree_musica.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botones para recursos
        frame_btn_musica = tk.Frame(frame_lista_musica, bg=self.colores['fondo'])
        frame_btn_musica.pack(fill='x', padx=10, pady=5)
        
        btn_abrir = tk.Button(frame_btn_musica, text="🔗 Abrir Seleccionado",
                             command=self.abrir_recurso_seleccionado,
                             **sistema_temas.obtener_estilo_boton('exito'))
        btn_abrir.pack(side='left', padx=(0, 5))
        
        btn_agregar_recurso = tk.Button(frame_btn_musica, text="➕ Agregar Recurso",
                                       command=self.abrir_dialogo_agregar_recurso,
                                       **sistema_temas.obtener_estilo_boton())
        btn_agregar_recurso.pack(side='left')
        
    def crear_pestaña_recursos(self):
        """Crea la pestaña de recursos adicionales"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📚 Recursos")
        
        # Título
        titulo = tk.Label(frame, text="📚 Recursos de Productividad", 
                         font=('Arial', 16, 'bold'),
                         bg=self.colores['fondo'],
                         fg=self.colores['primario'])
        titulo.pack(pady=10)
        
        # Información de uso
        info_text = """
🎯 ¿Cómo usar la personalización?

• Temas: Cambia la apariencia visual de toda la aplicación
• Frases: Personaliza los mensajes motivacionales que recibes
• Música: Agrega tus enlaces favoritos para concentración y motivación
• Recursos: Enlaces útiles para mejorar tu productividad

💡 Consejos:
• Las frases personalizadas tienen prioridad sobre las predeterminadas
• Puedes agregar enlaces de YouTube, Spotify, podcasts, etc.
• Los temas se aplican inmediatamente a toda la aplicación
• Tus configuraciones se guardan automáticamente
        """
        
        text_info = scrolledtext.ScrolledText(frame, height=15, wrap='word',
                                             bg=self.colores['fondo'],
                                             fg=self.colores['texto'])
        text_info.pack(fill='both', expand=True, padx=20, pady=10)
        text_info.insert('1.0', info_text)
        text_info.config(state='disabled')
        
        # Enlaces útiles
        frame_enlaces = tk.LabelFrame(frame, text="Enlaces Útiles",
                                     bg=self.colores['fondo'], 
                                     fg=self.colores['texto'])
        frame_enlaces.pack(fill='x', padx=20, pady=10)
        
        enlaces = [
            ("📖 Getting Things Done", "https://gettingthingsdone.com/"),
            ("🎵 YouTube Music", "https://music.youtube.com/"),
            ("📊 Notion Templates", "https://www.notion.so/templates"),
            ("⏱️ Técnica Pomodoro", "https://en.wikipedia.org/wiki/Pomodoro_Technique")
        ]
        
        for nombre, url in enlaces:
            btn = tk.Button(frame_enlaces, text=nombre,
                           command=lambda u=url: webbrowser.open(u),
                           **sistema_temas.obtener_estilo_boton())
            btn.pack(side='left', padx=5, pady=5)
        
    def crear_botones_principales(self):
        """Crea los botones principales de la ventana"""
        frame_botones = tk.Frame(self.ventana, bg=self.colores['fondo'])
        frame_botones.pack(fill='x', padx=10, pady=10)
        
        btn_cerrar = tk.Button(frame_botones, text="❌ Cerrar",
                              command=self.ventana.destroy,
                              **sistema_temas.obtener_estilo_boton('error'))
        btn_cerrar.pack(side='right', padx=(5, 0))
        
        btn_aplicar = tk.Button(frame_botones, text="✅ Aplicar Cambios",
                               command=self.aplicar_todos_los_cambios,
                               **sistema_temas.obtener_estilo_boton('exito'))
        btn_aplicar.pack(side='right', padx=5)
    
    # Métodos auxiliares para funcionalidad
    def actualizar_lista_temas(self):
        """Actualiza la lista de temas disponibles"""
        temas = sistema_temas.obtener_todos_los_temas()
        nombres = [f"{tema['nombre']}" for tema in temas.values()]
        self.combo_temas['values'] = nombres
        
        # Seleccionar tema actual
        tema_actual = sistema_temas.obtener_tema_actual()
        self.combo_temas.set(tema_actual['nombre'])
    
    def cambiar_tema_seleccionado(self, event=None):
        """Cambia la vista previa del tema seleccionado"""
        self.dibujar_preview_colores()
    
    def aplicar_tema_seleccionado(self):
        """Aplica el tema seleccionado"""
        # Encontrar el tema por nombre
        temas = sistema_temas.obtener_todos_los_temas()
        nombre_seleccionado = self.combo_temas.get()
        
        for id_tema, config_tema in temas.items():
            if config_tema['nombre'] == nombre_seleccionado:
                if sistema_temas.cambiar_tema(id_tema):
                    messagebox.showinfo("✅ Éxito", "Tema aplicado correctamente")
                    self.aplicar_tema()
                    self.recrear_interfaz()
                else:
                    messagebox.showerror("❌ Error", "No se pudo aplicar el tema")
                break
    
    def actualizar_categorias_frases(self):
        """Actualiza las categorías de frases disponibles"""
        categorias = sistema_frases.obtener_todas_las_categorias()
        self.combo_categorias['values'] = categorias
        if categorias:
            self.combo_categorias.set(categorias[0])
            self.mostrar_frases_categoria()
    
    def mostrar_frases_categoria(self, event=None):
        """Muestra las frases de la categoría seleccionada"""
        categoria = self.combo_categorias.get()
        if categoria:
            frases = sistema_frases.obtener_frases_de_categoria(categoria)
            
            texto = f"=== FRASES DE '{categoria.upper()}' ===\n\n"
            texto += "📝 Frases por defecto:\n"
            for i, frase in enumerate(frases['default'], 1):
                texto += f"{i}. {frase}\n"
            
            if frases['personalizadas']:
                texto += "\n💖 Tus frases personalizadas:\n"
                for i, frase in enumerate(frases['personalizadas'], 1):
                    texto += f"{i}. {frase}\n"
            
            self.lista_frases.delete('1.0', tk.END)
            self.lista_frases.insert('1.0', texto)
    
    def mostrar_frase_aleatoria(self):
        """Muestra una frase aleatoria de la categoría seleccionada"""
        categoria = self.combo_categorias.get()
        if categoria:
            frase = sistema_frases.obtener_frase(categoria)
            messagebox.showinfo("🎲 Frase Aleatoria", frase)
    
    def agregar_nueva_frase(self):
        """Agrega una nueva frase personalizada"""
        categoria = self.combo_categorias.get()
        nueva_frase = self.entry_nueva_frase.get('1.0', tk.END).strip()
        
        if categoria and nueva_frase:
            if sistema_frases.agregar_frase_personalizada(categoria, nueva_frase):
                messagebox.showinfo("✅ Éxito", "Frase agregada correctamente")
                self.entry_nueva_frase.delete('1.0', tk.END)
                self.mostrar_frases_categoria()
            else:
                messagebox.showwarning("⚠️ Advertencia", "Esta frase ya existe")
        else:
            messagebox.showerror("❌ Error", "Selecciona una categoría y escribe una frase")
    
    def actualizar_categorias_musica(self):
        """Actualiza las categorías de música disponibles"""
        categorias = sistema_musica.obtener_todas_las_categorias()
        self.combo_musica['values'] = categorias
        if categorias:
            self.combo_musica.set(categorias[0])
            self.mostrar_recursos_musica()
    
    def mostrar_recursos_musica(self, event=None):
        """Muestra los recursos de música de la categoría seleccionada"""
        categoria = self.combo_musica.get()
        if categoria:
            # Limpiar tree
            for item in self.tree_musica.get_children():
                self.tree_musica.delete(item)
            
            recursos = sistema_musica.obtener_recursos_de_categoria(categoria)
            
            # Agregar recursos por defecto
            for recurso in recursos['default']:
                self.tree_musica.insert('', 'end', 
                                      text=recurso['nombre'],
                                      values=(recurso['tipo'], recurso['descripcion']))
            
            # Agregar recursos personalizados
            for recurso in recursos['personalizados']:
                self.tree_musica.insert('', 'end', 
                                      text=f"👤 {recurso['nombre']}",
                                      values=(recurso['tipo'], recurso['descripcion']))
    
    def reproducir_musica_aleatoria(self):
        """Reproduce un recurso musical aleatorio"""
        categoria = self.combo_musica.get()
        if categoria:
            recurso = sistema_musica.obtener_recurso_aleatorio(categoria)
            if recurso:
                if sistema_musica.abrir_recurso(recurso):
                    messagebox.showinfo("🎵 Reproduciendo", 
                                      f"Abriendo: {recurso['nombre']}")
                else:
                    messagebox.showerror("❌ Error", "No se pudo abrir el recurso")
    
    def abrir_recurso_seleccionado(self):
        """Abre el recurso seleccionado en el tree"""
        seleccion = self.tree_musica.selection()
        if seleccion:
            item = self.tree_musica.item(seleccion[0])
            nombre = item['text'].replace('👤 ', '')
            
            # Buscar el recurso completo
            categoria = self.combo_musica.get()
            recursos = sistema_musica.obtener_recursos_de_categoria(categoria)
            
            for recurso in recursos['default'] + recursos['personalizados']:
                if recurso['nombre'] == nombre:
                    if sistema_musica.abrir_recurso(recurso):
                        messagebox.showinfo("🔗 Abriendo", f"Abriendo: {nombre}")
                    else:
                        messagebox.showerror("❌ Error", "No se pudo abrir el recurso")
                    break
        else:
            messagebox.showwarning("⚠️ Advertencia", "Selecciona un recurso primero")
    
    def abrir_dialogo_agregar_recurso(self):
        """Abre diálogo para agregar nuevo recurso musical"""
        DialogoAgregarRecurso(self.ventana, self.combo_musica.get(), 
                             self.mostrar_recursos_musica)
    
    def abrir_creador_tema(self):
        """Abre el creador de temas personalizados"""
        CreadorTemas(self.ventana, self.actualizar_lista_temas)
    
    def aplicar_todos_los_cambios(self):
        """Aplica todos los cambios realizados"""
        messagebox.showinfo("✅ Cambios Aplicados", 
                          "Todos los cambios han sido guardados correctamente")
    
    def recrear_interfaz(self):
        """Recrea la interfaz con el nuevo tema"""
        # Destruir la interfaz actual y recrearla
        for widget in self.ventana.winfo_children():
            widget.destroy()
        
        self.aplicar_tema()
        self.crear_interfaz()


class DialogoAgregarRecurso:
    """Diálogo para agregar nuevos recursos musicales"""
    def __init__(self, parent, categoria, callback_refresh):
        self.categoria = categoria
        self.callback_refresh = callback_refresh
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("➕ Agregar Nuevo Recurso")
        self.ventana.geometry("500x400")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Campos del formulario
        tk.Label(self.ventana, text="Nombre del recurso:").pack(pady=5)
        self.entry_nombre = tk.Entry(self.ventana, width=50)
        self.entry_nombre.pack(pady=5)
        
        tk.Label(self.ventana, text="URL del recurso:").pack(pady=5)
        self.entry_url = tk.Entry(self.ventana, width=50)
        self.entry_url.pack(pady=5)
        
        tk.Label(self.ventana, text="Tipo:").pack(pady=5)
        self.combo_tipo = ttk.Combobox(self.ventana, 
                                      values=['youtube', 'spotify', 'podcast', 'web'],
                                      state='readonly')
        self.combo_tipo.pack(pady=5)
        self.combo_tipo.set('youtube')
        
        tk.Label(self.ventana, text="Descripción:").pack(pady=5)
        self.text_descripcion = tk.Text(self.ventana, height=4, width=50)
        self.text_descripcion.pack(pady=5)
        
        # Botones
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="✅ Agregar",
                 command=self.agregar_recurso).pack(side='left', padx=5)
        tk.Button(frame_botones, text="❌ Cancelar",
                 command=self.ventana.destroy).pack(side='left', padx=5)
    
    def agregar_recurso(self):
        nombre = self.entry_nombre.get().strip()
        url = self.entry_url.get().strip()
        tipo = self.combo_tipo.get()
        descripcion = self.text_descripcion.get('1.0', tk.END).strip()
        
        if nombre and url:
            if sistema_musica.agregar_recurso_personalizado(
                self.categoria, nombre, url, tipo, descripcion):
                messagebox.showinfo("✅ Éxito", "Recurso agregado correctamente")
                self.callback_refresh()
                self.ventana.destroy()
            else:
                messagebox.showerror("❌ Error", "No se pudo agregar el recurso")
        else:
            messagebox.showerror("❌ Error", "Completa al menos el nombre y la URL")


class CreadorTemas:
    """Creador de temas personalizados"""
    def __init__(self, parent, callback_refresh):
        self.callback_refresh = callback_refresh
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("🎨 Crear Tema Personalizado")
        self.ventana.geometry("600x500")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        messagebox.showinfo("🚧 En Desarrollo", 
                          "El creador de temas personalizados estará disponible en una futura actualización.")
        self.ventana.destroy()


def abrir_ui_personalizacion(parent=None):
    """Función para abrir la UI de personalización"""
    return UIPersonalizacion(parent)

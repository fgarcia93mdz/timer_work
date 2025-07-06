# setup_inicial.py - Configuración inicial para primer uso

import tkinter as tk
from tkinter import ttk, messagebox
from config import config_sistema

class ConfiguracionInicial:
    def __init__(self):
        self.root = None
        self.nombre_usuario = ""
        self.configuracion_completada = False
    
    def mostrar_bienvenida(self):
        """Muestra la ventana de configuración inicial"""
        self.root = tk.Tk()
        self.root.title("🚀 Bienvenido al Sistema de Productividad")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.root.eval('tk::PlaceWindow . center')
        
        # Hacer que la ventana esté siempre al frente
        self.root.attributes('-topmost', True)
        
        self.crear_interfaz_bienvenida()
        
        # Ejecutar la ventana
        self.root.mainloop()
        
        return self.configuracion_completada
    
    def crear_interfaz_bienvenida(self):
        """Crea la interfaz de bienvenida"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill='both', expand=True)
        
        # Título principal
        titulo = tk.Label(main_frame, 
                         text="🚀 Sistema de Productividad Personal",
                         font=('Arial', 18, 'bold'),
                         fg='#2E86AB')
        titulo.pack(pady=(0, 20))
        
        # Subtítulo
        subtitulo = tk.Label(main_frame,
                           text="Tu compañero personal para mejorar la productividad",
                           font=('Arial', 12),
                           fg='#666666')
        subtitulo.pack(pady=(0, 30))
        
        # Descripción del sistema
        descripcion_frame = ttk.LabelFrame(main_frame, text="¿Qué hace este sistema?", padding="15")
        descripcion_frame.pack(fill='x', pady=(0, 20))
        
        caracteristicas = [
            "📊 Monitorea tu actividad de forma privada y respetuosa",
            "🍅 Te ayuda con ciclos Pomodoro para mejor concentración",
            "🎯 Te permite definir y seguir objetivos diarios",
            "📈 Genera reportes para que veas tu progreso",
            "💪 Te motiva con mensajes personalizados"
        ]
        
        for caracteristica in caracteristicas:
            label_car = tk.Label(descripcion_frame, 
                               text=caracteristica,
                               font=('Arial', 10),
                               anchor='w')
            label_car.pack(fill='x', pady=2)
        
        # Sección de configuración personal
        config_frame = ttk.LabelFrame(main_frame, text="Configuración Personal", padding="15")
        config_frame.pack(fill='x', pady=(0, 20))
        
        # Campo nombre
        tk.Label(config_frame, 
                text="👤 ¿Cómo te gustaría que te llame?",
                font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 5))
        
        tk.Label(config_frame,
                text="(Este nombre se usará para personalizar los mensajes)",
                font=('Arial', 9),
                fg='#666666').pack(anchor='w', pady=(0, 10))
        
        self.entry_nombre = ttk.Entry(config_frame, 
                                    font=('Arial', 12),
                                    width=30)
        self.entry_nombre.pack(anchor='w', pady=(0, 10))
        self.entry_nombre.focus()
        
        # Configuraciones opcionales
        tk.Label(config_frame,
                text="⚙️ Configuraciones iniciales:",
                font=('Arial', 11, 'bold')).pack(anchor='w', pady=(15, 5))
        
        # Checkboxes para configuraciones
        self.var_notificaciones = tk.BooleanVar(value=True)
        self.var_sonidos = tk.BooleanVar(value=True)
        self.var_inicio_windows = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(config_frame,
                       text="🔔 Activar notificaciones Pomodoro",
                       variable=self.var_notificaciones).pack(anchor='w', pady=2)
        
        ttk.Checkbutton(config_frame,
                       text="🔊 Activar sonidos de alerta",
                       variable=self.var_sonidos).pack(anchor='w', pady=2)
        
        ttk.Checkbutton(config_frame,
                       text="🚀 Iniciar automáticamente con Windows",
                       variable=self.var_inicio_windows).pack(anchor='w', pady=2)
        
        # Información de privacidad
        privacidad_frame = ttk.LabelFrame(main_frame, text="🔒 Privacidad", padding="10")
        privacidad_frame.pack(fill='x', pady=(0, 20))
        
        privacidad_texto = """✅ Todos los datos se almacenan SOLO en tu computadora
✅ No se envía información personal a internet
✅ Tú controlas completamente tus datos
✅ Puedes desinstalar el sistema cuando quieras"""
        
        tk.Label(privacidad_frame,
                text=privacidad_texto,
                font=('Arial', 9),
                fg='#2E7D32',
                justify='left').pack(anchor='w')
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(botones_frame,
                  text="🚀 ¡Comenzar a usar el sistema!",
                  command=self.iniciar_sistema,
                  style='Accent.TButton').pack(side='right', padx=(10, 0))
        
        ttk.Button(botones_frame,
                  text="❌ Cancelar",
                  command=self.cancelar).pack(side='right')
        
        # Bind Enter para iniciar
        self.root.bind('<Return>', lambda e: self.iniciar_sistema())
        
    def iniciar_sistema(self):
        """Procesa la configuración inicial y inicia el sistema"""
        nombre = self.entry_nombre.get().strip()
        
        if not nombre:
            messagebox.showerror("❌ Error", "Por favor, ingresa tu nombre para continuar")
            self.entry_nombre.focus()
            return
        
        if len(nombre) < 2:
            messagebox.showerror("❌ Error", "El nombre debe tener al menos 2 caracteres")
            self.entry_nombre.focus()
            return
        
        # Confirmar configuración
        mensaje_confirmacion = f"""¿Confirmas la configuración?

👤 Nombre: {nombre}
🔔 Notificaciones: {'Sí' if self.var_notificaciones.get() else 'No'}
🔊 Sonidos: {'Sí' if self.var_sonidos.get() else 'No'}
🚀 Inicio automático: {'Sí' if self.var_inicio_windows.get() else 'No'}

Esta configuración se puede cambiar después."""
        
        if not messagebox.askyesno("✅ Confirmar Configuración", mensaje_confirmacion):
            return
        
        # Guardar configuración
        try:
            config_sistema.configurar_primer_uso(nombre)
            
            # Aplicar configuraciones adicionales
            config_sistema.actualizar_configuracion('pomodoro', 'notificaciones_activas', self.var_notificaciones.get())
            config_sistema.actualizar_configuracion('pomodoro', 'sonidos_activos', self.var_sonidos.get())
            
            # Si se seleccionó inicio automático, configurarlo
            if self.var_inicio_windows.get():
                self.configurar_inicio_automatico()
            
            self.configuracion_completada = True
            
            messagebox.showinfo("🎉 ¡Listo!", 
                              f"¡Bienvenido/a {nombre}!\n\n"
                              "El sistema está configurado y listo para usar.\n"
                              "Se abrirá la interfaz principal para que puedas:\n\n"
                              "• Definir tu objetivo del día\n"
                              "• Comenzar con el monitoreo\n"
                              "• Usar el Pomodoro Timer\n\n"
                              "¡Que tengas un día productivo! 🚀")
            
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar configuración:\n{e}")
    
    def configurar_inicio_automatico(self):
        """Configura el sistema para iniciarse automáticamente con Windows"""
        try:
            import winreg
            import sys
            import os
            
            # Ruta del registro para inicio automático
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            app_name = "ProductividadPersonal"
            
            # Ruta del ejecutable (o script Python)
            if getattr(sys, 'frozen', False):
                # Si es un ejecutable compilado
                app_path = sys.executable
            else:
                # Si es script Python
                python_exe = sys.executable
                script_path = os.path.abspath("main.py")
                app_path = f'"{python_exe}" "{script_path}"'
            
            # Abrir clave del registro
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            
            print("✅ Inicio automático configurado")
            
        except Exception as e:
            print(f"⚠️ No se pudo configurar inicio automático: {e}")
    
    def cancelar(self):
        """Cancela la configuración inicial"""
        if messagebox.askyesno("❌ Cancelar", 
                              "¿Estás seguro de que quieres cancelar?\n"
                              "El sistema no se configurará."):
            self.root.quit()
            self.root.destroy()

def verificar_y_configurar_primer_uso():
    """Verifica si es primer uso y muestra la configuración inicial"""
    if config_sistema.es_primer_uso():
        print("🔧 Primer uso detectado. Mostrando configuración inicial...")
        configurador = ConfiguracionInicial()
        return configurador.mostrar_bienvenida()
    else:
        nombre = config_sistema.obtener_nombre_usuario()
        print(f"👋 ¡Hola de nuevo, {nombre}!")
        return True

if __name__ == "__main__":
    # Prueba de la configuración inicial
    verificar_y_configurar_primer_uso()

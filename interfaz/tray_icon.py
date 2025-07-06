# interfaz/tray_icon.py - Sistema de icono en bandeja del sistema

import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from config import config_sistema
from objetivos.gestor_objetivos import GestorObjetivos
from reportes.resumen_diario import ResumenDiario

class TrayIcon:
    def __init__(self, sistema_principal):
        self.sistema_principal = sistema_principal
        self.icon = None
        self.gestor_objetivos = GestorObjetivos()
        self.resumen_diario = ResumenDiario()
        self.nombre_usuario = config_sistema.obtener_nombre_usuario()
        
    def crear_imagen_icono(self):
        """Crea la imagen del icono para la bandeja"""
        try:
            # Crear una imagen simple para el icono
            width = 64
            height = 64
            image = Image.new('RGB', (width, height), color='white')
            dc = ImageDraw.Draw(image)
            
            # Dibujar un círculo verde (productividad)
            dc.ellipse([width//4, height//4, 3*width//4, 3*height//4], fill='#4CAF50', outline='#2E7D32')
            
            # Dibujar una "P" de productividad
            dc.text((width//2-8, height//2-8), "P", fill='white')
            
            return image
        except Exception:
            # Si falla, crear imagen básica
            return Image.new('RGB', (64, 64), color='#4CAF50')
    
    def crear_menu(self):
        """Crea el menú contextual del tray icon"""
        return pystray.Menu(
            item(f"👋 Hola, {self.nombre_usuario}", self.mostrar_saludo, enabled=False),
            pystray.Menu.SEPARATOR,
            item("📊 Estado del Sistema", self.mostrar_estado),
            item("🎯 Gestionar Objetivos", self.abrir_objetivos),
            item("🍅 Estado Pomodoro", self.mostrar_estado_pomodoro),
            pystray.Menu.SEPARATOR,
            item("📈 Resumen del Día", self.mostrar_resumen_dia),
            item("📋 Estadísticas Rápidas", self.mostrar_estadisticas),
            pystray.Menu.SEPARATOR,
            item("🎨 Personalización", self.abrir_personalizacion),
            item("⚙️ Configuración", self.abrir_configuracion),
            item("❓ Ayuda", self.mostrar_ayuda),
            pystray.Menu.SEPARATOR,
            item("🔄 Reiniciar", self.reiniciar_sistema),
            item("❌ Salir", self.salir_aplicacion)
        )
    
    def inicializar_tray(self):
        """Inicializa el icono en la bandeja del sistema"""
        try:
            imagen = self.crear_imagen_icono()
            menu = self.crear_menu()
            
            self.icon = pystray.Icon(
                name="ProductividadPersonal",
                icon=imagen,
                title=f"Sistema de Productividad - {self.nombre_usuario}",
                menu=menu
            )
            
            # Ejecutar en hilo separado
            hilo_tray = threading.Thread(target=self.icon.run, daemon=True)
            hilo_tray.start()
            
            print("🖥️ Icono de bandeja inicializado")
            return True
            
        except Exception as e:
            print(f"❌ Error al inicializar tray icon: {e}")
            return False
    
    def mostrar_saludo(self, icon, item):
        """Muestra saludo personalizado"""
        pass  # Este item está deshabilitado, solo es informativo
    
    def mostrar_estado(self, icon, item):
        """Muestra el estado actual del sistema"""
        try:
            estado_pomodoro = self.sistema_principal.pomodoro.obtener_estado() if hasattr(self.sistema_principal, 'pomodoro') else None
            objetivos_hoy = len(self.gestor_objetivos.obtener_objetivos_hoy())
            
            mensaje = f"""🖥️ ESTADO DEL SISTEMA

👤 Usuario: {self.nombre_usuario}
⚡ Sistema: {'Activo' if self.sistema_principal.running else 'Detenido'}
🎯 Objetivos hoy: {objetivos_hoy}
🍅 Pomodoro: {'Activo' if estado_pomodoro and estado_pomodoro['activo'] else 'Inactivo'}

📅 Fecha: {self.obtener_fecha_actual()}
⏰ Funcionando desde el inicio del día"""
            
            self.mostrar_mensaje_info("Estado del Sistema", mensaje)
            
        except Exception as e:
            self.mostrar_mensaje_error("Error", f"Error al obtener estado: {e}")
    
    def abrir_objetivos(self, icon, item):
        """Abre la interfaz de gestión de objetivos"""
        try:
            from objetivos.ui_minimal import ObjetivosUI
            
            def ejecutar_objetivos():
                app = ObjetivosUI()
                app.ejecutar()
            
            # Ejecutar en hilo separado para no bloquear
            hilo_objetivos = threading.Thread(target=ejecutar_objetivos, daemon=True)
            hilo_objetivos.start()
            
        except Exception as e:
            self.mostrar_mensaje_error("Error", f"Error al abrir objetivos: {e}")
    
    def mostrar_estado_pomodoro(self, icon, item):
        """Muestra información del estado del Pomodoro"""
        try:
            if hasattr(self.sistema_principal, 'pomodoro'):
                estado = self.sistema_principal.pomodoro.obtener_estado()
                
                if estado['activo']:
                    fase = "Trabajo" if estado['fase'] == "trabajo" else "Descanso"
                    mensaje = f"""🍅 POMODORO ACTIVO

📊 Estado: {fase}
🔢 Ciclo: {estado['ciclo']}
⏱️ Tiempo restante: {estado.get('tiempo_restante', 'N/A')}
⏸️ Pausado: {'Sí' if estado.get('pausado', False) else 'No'}

💡 El Pomodoro te ayuda a mantener el foco
   con ciclos de trabajo y descanso programados."""
                else:
                    mensaje = f"""🍅 POMODORO INACTIVO

El temporizador Pomodoro no está funcionando.

💡 ¿Sabías que usar Pomodoro puede mejorar
   tu concentración hasta un 25%?
   
🚀 Se iniciará automáticamente con el sistema."""
                
                self.mostrar_mensaje_info("Estado Pomodoro", mensaje)
            else:
                self.mostrar_mensaje_info("Pomodoro", "Sistema Pomodoro no disponible")
                
        except Exception as e:
            self.mostrar_mensaje_error("Error", f"Error al obtener estado Pomodoro: {e}")
    
    def mostrar_resumen_dia(self, icon, item):
        """Muestra el resumen del día actual"""
        try:
            # Ejecutar en hilo separado
            def generar_resumen():
                self.resumen_diario.mostrar_resumen_ventana()
            
            hilo_resumen = threading.Thread(target=generar_resumen, daemon=True)
            hilo_resumen.start()
            
        except Exception as e:
            self.mostrar_mensaje_error("Error", f"Error al generar resumen: {e}")
    
    def mostrar_estadisticas(self, icon, item):
        """Muestra estadísticas rápidas"""
        try:
            resumen = self.resumen_diario.generar_resumen_completo()
            
            if resumen:
                mensaje = f"""📊 ESTADÍSTICAS RÁPIDAS

⏰ Tiempo activo: {resumen['metricas']['tiempo_activo_horas']} horas
🍅 Pomodoros: {resumen['metricas']['pomodoros_completados']}
🎯 Objetivos: {resumen['objetivos']['objetivos_completados']}/{resumen['objetivos']['total_objetivos']}
💻 App principal: {resumen['metricas']['aplicacion_principal']}

📈 Progreso objetivos: {resumen['objetivos']['porcentaje_completado']}%"""
            else:
                mensaje = "📊 Aún no hay estadísticas disponibles para hoy.\n\n💡 Las estadísticas se generan conforme uses el sistema."
            
            self.mostrar_mensaje_info("Estadísticas del Día", mensaje)
            
        except Exception as e:
            self.mostrar_mensaje_error("Error", f"Error al obtener estadísticas: {e}")
    
    def abrir_configuracion(self, icon, item):
        """Abre la ventana de configuración"""
        try:
            def mostrar_config():
                ventana = tk.Tk()
                ventana.title("⚙️ Configuración del Sistema")
                ventana.geometry("500x400")
                
                # Contenido básico de configuración
                frame_main = tk.Frame(ventana, padx=20, pady=20)
                frame_main.pack(fill='both', expand=True)
                
                tk.Label(frame_main, 
                        text="⚙️ Configuración del Sistema",
                        font=('Arial', 16, 'bold')).pack(pady=(0, 20))
                
                config_texto = f"""👤 Usuario: {self.nombre_usuario}

⚙️ CONFIGURACIONES ACTUALES:
📊 Monitoreo cada: 60 segundos
💤 Inactividad tras: 10 minutos
🍅 Pomodoro: 25/5/15 minutos
🔔 Notificaciones: Activas

💾 Archivos de datos:
• Logs: storage/log_actividad.csv
• Base de datos: storage/actividad.db
• Configuración: storage/config.json

💡 Para cambios avanzados, edita el archivo config.py"""
                
                tk.Label(frame_main, text=config_texto, justify='left').pack()
                
                tk.Button(frame_main, text="Cerrar", command=ventana.destroy).pack(pady=20)
                
                ventana.mainloop()
            
            hilo_config = threading.Thread(target=mostrar_config, daemon=True)
            hilo_config.start()
            
        except Exception as e:
            self.mostrar_mensaje_error("Error", f"Error al abrir configuración: {e}")
    
    def mostrar_ayuda(self, icon, item):
        """Muestra información de ayuda"""
        mensaje = f"""❓ AYUDA DEL SISTEMA

🖥️ SISTEMA DE PRODUCTIVIDAD PERSONAL

¿Qué hace?
• Monitorea tu actividad de forma privada
• Te ayuda con ciclos Pomodoro
• Gestiona tus objetivos diarios
• Genera reportes motivadores

🎯 Cómo usar:
• Define objetivos al inicio del día
• Deja que el sistema monitoree tu trabajo
• Usa el Pomodoro para mantener foco
• Revisa tu progreso cuando quieras

📞 Funciones disponibles:
• Clic derecho en este icono → Ver opciones
• "Gestionar Objetivos" → Agregar/editar objetivos
• "Resumen del Día" → Ver tu progreso
• "Estado Pomodoro" → Info del temporizador

🔒 Privacidad:
Todos los datos se guardan SOLO en tu computadora.
Nada se envía a internet sin tu autorización.

📁 Archivos del sistema en: {os.getcwd()}"""
        
        self.mostrar_mensaje_info("Ayuda del Sistema", mensaje)
    
    def reiniciar_sistema(self, icon, item):
        """Reinicia el sistema completo"""
        try:
            respuesta = messagebox.askyesno(
                "🔄 Reiniciar Sistema",
                "¿Estás seguro de que quieres reiniciar el sistema?\n\n"
                "Se cerrará y volverá a iniciar automáticamente."
            )
            
            if respuesta:
                # Detener sistema actual
                self.sistema_principal.detener_sistema()
                
                # Ejecutar nuevo proceso
                if getattr(sys, 'frozen', False):
                    # Si es ejecutable
                    os.execv(sys.executable, [sys.executable])
                else:
                    # Si es script Python
                    os.execv(sys.executable, [sys.executable, "main.py"])
                    
        except Exception as e:
            self.mostrar_mensaje_error("Error", f"Error al reiniciar: {e}")
    
    def salir_aplicacion(self, icon, item):
        """Sale de la aplicación completamente"""
        try:
            respuesta = messagebox.askyesno(
                "❌ Salir del Sistema",
                f"¿Estás seguro de que quieres salir, {self.nombre_usuario}?\n\n"
                "Se detendrá el monitoreo y el Pomodoro Timer.\n"
                "Tus datos se mantendrán guardados."
            )
            
            if respuesta:
                print(f"👋 ¡Hasta luego, {self.nombre_usuario}!")
                
                # Generar resumen final si hay actividad
                try:
                    self.resumen_diario.procesar_resumen_diario()
                except:
                    pass
                
                # Detener sistema
                self.sistema_principal.detener_sistema()
                
                # Detener tray icon
                if self.icon:
                    self.icon.stop()
                
                # Salir completamente
                sys.exit(0)
                
        except Exception as e:
            print(f"❌ Error al salir: {e}")
            sys.exit(1)
    
    def obtener_fecha_actual(self):
        """Obtiene la fecha actual formateada"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y")
    
    def mostrar_mensaje_info(self, titulo, mensaje):
        """Muestra un mensaje informativo"""
        def mostrar():
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            messagebox.showinfo(titulo, mensaje)
            root.destroy()
        
        hilo_mensaje = threading.Thread(target=mostrar, daemon=True)
        hilo_mensaje.start()
    
    def mostrar_mensaje_error(self, titulo, mensaje):
        """Muestra un mensaje de error"""
        def mostrar():
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            messagebox.showerror(titulo, mensaje)
            root.destroy()
        
        hilo_mensaje = threading.Thread(target=mostrar, daemon=True)
        hilo_mensaje.start()
    
    def actualizar_tooltip(self, mensaje):
        """Actualiza el tooltip del icono de bandeja"""
        if self.icon:
            try:
                self.icon.title = f"Sistema de Productividad - {mensaje}"
            except:
                pass
    
    def detener(self):
        """Detiene el icono de bandeja"""
        if self.icon:
            self.icon.stop()

    def abrir_personalizacion(self, icon, item):
        """Abre la interfaz de personalización"""
        try:
            def mostrar():
                from personalizacion import abrir_ui_personalizacion
                root = tk.Tk()
                root.withdraw()  # Ocultar ventana principal
                
                ui_personalizacion = abrir_ui_personalizacion(root)
                
                # Centrar la ventana
                ui_personalizacion.ventana.update_idletasks()
                x = (ui_personalizacion.ventana.winfo_screenwidth() // 2) - (800 // 2)
                y = (ui_personalizacion.ventana.winfo_screenheight() // 2) - (600 // 2)
                ui_personalizacion.ventana.geometry(f"800x600+{x}+{y}")
                
                root.wait_window(ui_personalizacion.ventana)
                root.destroy()
            
            hilo_personalizacion = threading.Thread(target=mostrar, daemon=True)
            hilo_personalizacion.start()
            
        except Exception as e:
            print(f"❌ Error abriendo personalización: {e}")
            self.mostrar_mensaje_error("Error", f"No se pudo abrir la personalización:\n{e}")

if __name__ == "__main__":
    # Prueba del tray icon
    print("🧪 Probando tray icon...")
    
    class SistemaFake:
        def __init__(self):
            self.running = True
        def detener_sistema(self):
            pass
    
    sistema_fake = SistemaFake()
    tray = TrayIcon(sistema_fake)
    
    if tray.inicializar_tray():
        print("✅ Tray icon iniciado. Revisa la bandeja del sistema.")
        print("❌ Presiona Ctrl+C para detener la prueba")
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo prueba...")
            tray.detener()
    else:
        print("❌ No se pudo inicializar el tray icon")

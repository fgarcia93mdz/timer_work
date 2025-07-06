# main.py - Controlador principal del sistema de monitoreo

import threading
import time
import sys
import os
from datetime import datetime

# Verificar primer uso y configurar sistema
print("🔧 Verificando configuración del sistema...")
from setup_inicial import verificar_y_configurar_primer_uso
from config import config_sistema

# Si es primer uso, mostrar configuración inicial
if not verificar_y_configurar_primer_uso():
    print("❌ Configuración inicial cancelada. Saliendo...")
    sys.exit(0)

# Importar módulos del sistema después de la configuración
from monitor.logger import inicializar_log, registrar_evento
from monitor.inactividad import iniciar_monitoreo_inactividad
from monitor.ventana_activa import MonitorVentanas
from pomodoro.temporizador import PomodoroTimer
from pomodoro.notificador import NotificadorPomodoro
from objetivos.gestor_objetivos import GestorObjetivos
from storage.database import inicializar_db
from reportes.resumen_diario import ResumenDiario, programar_resumen_automatico
from interfaz.tray_icon import TrayIcon

class SistemaMonitoreo:
    def __init__(self):
        self.running = False
        self.monitor_ventanas = None
        self.pomodoro = None
        self.gestor_objetivos = None
        self.resumen_diario = None
        self.tray_icon = None
        self.nombre_usuario = config_sistema.obtener_nombre_usuario()
        
    def inicializar_sistema(self):
        """Inicializa todos los componentes del sistema"""
        print(f"🚀 Iniciando Sistema de Productividad Personal para {self.nombre_usuario}...")
        
        try:
            # Inicializar base de datos y logs
            inicializar_db()
            inicializar_log()
            
            # Inicializar componentes principales
            self.monitor_ventanas = MonitorVentanas()
            self.pomodoro = PomodoroTimer()
            self.gestor_objetivos = GestorObjetivos()
            self.resumen_diario = ResumenDiario()
            
            # Configurar Pomodoro según preferencias del usuario
            config_pomodoro = config_sistema.obtener_configuracion('pomodoro')
            if config_pomodoro:
                self.pomodoro.configurar_tiempos(
                    trabajo=config_pomodoro.get('tiempo_trabajo_minutos', 25),
                    descanso_corto=config_pomodoro.get('tiempo_descanso_corto_minutos', 5),
                    descanso_largo=config_pomodoro.get('tiempo_descanso_largo_minutos', 15)
                )
            
            # Inicializar tray icon si está habilitado
            if config_sistema.obtener_configuracion('interfaz', 'modo_tray'):
                self.tray_icon = TrayIcon(self)
                if not self.tray_icon.inicializar_tray():
                    print("⚠️ No se pudo inicializar el icono de bandeja, continuando sin él")
            
            # Programar resumen automático
            programar_resumen_automatico()
            
            registrar_evento(f"Sistema iniciado para {self.nombre_usuario}", "sistema")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al inicializar sistema: {e}")
            return False
        
    def mostrar_objetivos_inicio_dia(self):
        """Muestra la interfaz de objetivos al inicio del día si está habilitado"""
        try:
            if config_sistema.obtener_configuracion('objetivos', 'recordatorio_inicio_dia'):
                objetivos_hoy = self.gestor_objetivos.obtener_objetivos_hoy()
                
                if len(objetivos_hoy) == 0:
                    print("\n🎯 ¡Es hora de definir tus objetivos del día!")
                    print("💡 Tip: Define objetivos específicos y medibles")
                    print("📝 Ejemplo: 'Contactar 10 clientes' o 'Completar 3 tareas del proyecto'")
                    
                    respuesta = input("\n¿Quieres abrir la interfaz de objetivos ahora? (s/N): ")
                    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                        from objetivos.ui_minimal import ObjetivosUI
                        
                        def ejecutar_objetivos():
                            app = ObjetivosUI()
                            app.ejecutar()
                        
                        hilo_objetivos = threading.Thread(target=ejecutar_objetivos, daemon=True)
                        hilo_objetivos.start()
                        time.sleep(2)  # Dar tiempo para que se abra la ventana
                else:
                    print(f"\n🎯 Tienes {len(objetivos_hoy)} objetivo(s) definido(s) para hoy")
                    self.gestor_objetivos.mostrar_objetivos_hoy()
                    
        except Exception as e:
            print(f"⚠️ Error al mostrar objetivos de inicio: {e}")
        
    def iniciar_monitoreo(self):
        """Inicia todos los hilos de monitoreo"""
        self.running = True
        
        try:
            # Mostrar objetivos del día
            self.mostrar_objetivos_inicio_dia()
            
            print("\n" + "="*60)
            print(f"🎉 ¡BIENVENIDO/A DE NUEVO, {self.nombre_usuario.upper()}!")
            print("="*60)
            
            # Hilo para monitoreo de inactividad
            hilo_inactividad = threading.Thread(
                target=self._ejecutar_monitoreo_inactividad, 
                daemon=True
            )
            hilo_inactividad.start()
            
            # Hilo para monitoreo de ventanas
            hilo_ventanas = threading.Thread(
                target=self.monitor_ventanas.iniciar_monitoreo, 
                daemon=True
            )
            hilo_ventanas.start()
            
            # Hilo para Pomodoro
            hilo_pomodoro = threading.Thread(
                target=self.pomodoro.iniciar, 
                daemon=True
            )
            hilo_pomodoro.start()
            
            print("\n✅ SISTEMA COMPLETAMENTE OPERATIVO")
            print("📊 Monitoreo de actividad: ACTIVO")
            print("🍅 Pomodoro Timer: ACTIVO")  
            print("🎯 Gestión de objetivos: DISPONIBLE")
            print("🖥️ Icono en bandeja: " + ("ACTIVO" if self.tray_icon else "NO DISPONIBLE"))
            
            print(f"\n� CONSEJOS PARA {self.nombre_usuario}:")
            print("• El sistema funciona en segundo plano automáticamente")
            print("• Revisa el icono de la bandeja del sistema (abajo a la derecha)")
            print("• Haz clic derecho en el icono para ver opciones")
            print("• El Pomodoro te ayudará a mantener el foco")
            print("• Al final del día recibirás un resumen personalizado")
            
            print("\n🔄 El sistema se ejecuta continuamente...")
            print("⚡ Presiona Ctrl+C cuando quieras ver el resumen del día y salir")
            print("="*60)
            
            # Mantener el programa ejecutándose
            while self.running:
                time.sleep(5)
                
                # Actualizar tooltip del tray icon si está disponible
                if self.tray_icon:
                    try:
                        estado_pomodoro = self.pomodoro.obtener_estado()
                        if estado_pomodoro['activo']:
                            fase = "Trabajo" if estado_pomodoro['fase'] == "trabajo" else "Descanso"
                            tiempo = estado_pomodoro.get('tiempo_restante', '')
                            mensaje = f"Pomodoro: {fase} {tiempo}"
                        else:
                            objetivos = len(self.gestor_objetivos.obtener_objetivos_hoy())
                            mensaje = f"Activo - {objetivos} objetivos hoy"
                        
                        self.tray_icon.actualizar_tooltip(mensaje)
                    except:
                        pass
                
        except KeyboardInterrupt:
            self.detener_sistema()
            
    def _ejecutar_monitoreo_inactividad(self):
        """Ejecuta el monitoreo de inactividad en un hilo separado"""
        try:
            iniciar_monitoreo_inactividad()
        except Exception as e:
            print(f"❌ Error en monitoreo de inactividad: {e}")
            registrar_evento(f"Error en monitoreo de inactividad: {e}", "error")
        
    def detener_sistema(self):
        """Detiene el sistema de monitoreo"""
        print(f"\n🛑 Deteniendo sistema para {self.nombre_usuario}...")
        self.running = False
        
        try:
            # Generar resumen final del día
            print("📊 Generando resumen final del día...")
            self.resumen_diario.procesar_resumen_diario()
            
        except Exception as e:
            print(f"⚠️ Error al generar resumen final: {e}")
        
        try:
            # Detener tray icon
            if self.tray_icon:
                self.tray_icon.detener()
                
            registrar_evento(f"Sistema detenido por {self.nombre_usuario}", "sistema")
            
        except Exception as e:
            print(f"⚠️ Error al detener componentes: {e}")
        
        print(f"✅ ¡Hasta luego, {self.nombre_usuario}! Sistema detenido correctamente")
        print("💾 Todos tus datos han sido guardados")
        print("🚀 La próxima vez que ejecutes el sistema, continuará desde donde lo dejaste")
        
        sys.exit(0)

def main():
    """Función principal para ejecutar el sistema"""
    try:
        print("=" * 60)
        print("🖥️  SISTEMA DE PRODUCTIVIDAD PERSONAL")
        print("   Tu compañero para mejorar la productividad")
        print("=" * 60)
        
        # Verificar dependencias críticas
        try:
            from utils.helpers import validar_configuracion
            if not validar_configuracion():
                print("\n❌ Faltan dependencias críticas. Ejecuta:")
                print("   pip install -r requirements.txt")
                sys.exit(1)
        except Exception as e:
            print(f"⚠️ No se pudo verificar dependencias: {e}")
        
        # Inicializar y ejecutar sistema
        sistema = SistemaMonitoreo()
        
        if sistema.inicializar_sistema():
            sistema.iniciar_monitoreo()
        else:
            print("❌ No se pudo inicializar el sistema")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error crítico en el sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

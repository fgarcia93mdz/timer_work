# reportes/resumen_diario.py - Sistema de resumen diario con mensajes motivadores

import json
import requests
from datetime import datetime, date
from config import config_sistema
from storage.database import obtener_estadisticas_diarias
from objetivos.gestor_objetivos import GestorObjetivos
from monitor.logger import registrar_evento

class ResumenDiario:
    def __init__(self):
        self.gestor_objetivos = GestorObjetivos()
        self.nombre_usuario = config_sistema.obtener_nombre_usuario()
        
    def generar_resumen_completo(self, fecha=None):
        """Genera un resumen completo del día"""
        if fecha is None:
            fecha = date.today().isoformat()
        
        try:
            # Obtener datos del día
            estadisticas = obtener_estadisticas_diarias(fecha)
            resumen_objetivos = self.gestor_objetivos.obtener_resumen_diario(fecha)
            
            # Calcular métricas
            tiempo_activo_horas = 0
            aplicacion_principal = "Ninguna"
            tiempo_app_principal = 0
            pomodoros_completados = 0
            
            if estadisticas and estadisticas['estadisticas_generales']:
                data = estadisticas['estadisticas_generales']
                tiempo_activo_horas = (data[2] or 0) / 3600  # Convertir a horas
                pomodoros_completados = data[5] or 0
                aplicacion_principal = data[7] or "Ninguna"
                tiempo_app_principal = (data[8] or 0) / 60  # Convertir a minutos
            
            # Crear resumen estructurado
            resumen = {
                'fecha': fecha,
                'usuario': self.nombre_usuario,
                'timestamp_generacion': datetime.now().isoformat(),
                'metricas': {
                    'tiempo_activo_horas': round(tiempo_activo_horas, 2),
                    'pomodoros_completados': pomodoros_completados,
                    'aplicacion_principal': aplicacion_principal,
                    'tiempo_app_principal_minutos': round(tiempo_app_principal, 1)
                },
                'objetivos': {
                    'total_objetivos': resumen_objetivos['total_objetivos'],
                    'objetivos_completados': resumen_objetivos['objetivos_completados'],
                    'porcentaje_completado': round(resumen_objetivos['porcentaje_completado'], 1),
                    'detalle_objetivos': [
                        {
                            'descripcion': obj['descripcion'],
                            'completado': obj['completado'],
                            'progreso': obj['progreso'],
                            'meta': obj['meta']
                        }
                        for obj in resumen_objetivos['objetivos']
                    ]
                },
                'aplicaciones_tiempo': []
            }
            
            # Agregar tiempo por aplicaciones si está disponible
            if estadisticas and estadisticas['tiempo_aplicaciones']:
                resumen['aplicaciones_tiempo'] = [
                    {
                        'aplicacion': app[0],
                        'tiempo_minutos': round(app[1] / 60, 1),
                        'sesiones': app[2]
                    }
                    for app in estadisticas['tiempo_aplicaciones'][:10]  # Top 10
                ]
            
            return resumen
            
        except Exception as e:
            print(f"❌ Error al generar resumen: {e}")
            return None
    
    def generar_mensaje_motivador(self, resumen):
        """Genera un mensaje motivador personalizado basado en el desempeño"""
        if not resumen:
            try:
                from personalizacion import sistema_frases
                return sistema_frases.obtener_frase('fin_dia')
            except ImportError:
                return f"¡Hasta mañana, {self.nombre_usuario}! 🌙"
        
        nombre = self.nombre_usuario
        objetivos_completados = resumen['objetivos']['objetivos_completados']
        total_objetivos = resumen['objetivos']['total_objetivos']
        porcentaje_objetivos = resumen['objetivos']['porcentaje_completado']
        pomodoros = resumen['metricas']['pomodoros_completados']
        tiempo_activo = resumen['metricas']['tiempo_activo_horas']
        
        # Mensajes según desempeño de objetivos
        if total_objetivos == 0:
            mensaje_objetivos = "💡 Para mañana, considera definir algunos objetivos específicos. ¡Te ayudarán a mantener el foco!"
        elif porcentaje_objetivos >= 100:
            try:
                from personalizacion import sistema_frases
                frase_objetivo = sistema_frases.obtener_frase('objetivo_completado')
                mensaje_objetivos = f"🎉 {frase_objetivo}"
            except ImportError:
                mensaje_objetivos = f"🎉 ¡Increíble, {nombre}! Completaste todos tus objetivos del día. ¡Eres imparable!"
        elif porcentaje_objetivos >= 80:
            mensaje_objetivos = f"💪 ¡Muy bien, {nombre}! Casi todos los objetivos completados ({porcentaje_objetivos:.0f}%). ¡Estás en gran forma!"
        elif porcentaje_objetivos >= 50:
            mensaje_objetivos = f"👍 Buen trabajo, {nombre}. Completaste {porcentaje_objetivos:.0f}% de tus objetivos. ¡Mañana puedes llegar al 100%!"
        elif porcentaje_objetivos >= 25:
            mensaje_objetivos = f"💭 {nombre}, completaste {porcentaje_objetivos:.0f}% de tus objetivos. ¡Estuviste cerca! Mañana lo lográs 💪"
        else:
            mensaje_objetivos = f"🌱 {nombre}, fue un día para aprender. Mañana es una nueva oportunidad para brillar ✨"
        
        # Mensaje sobre Pomodoros
        if pomodoros >= 8:
            mensaje_pomodoro = f"🍅 ¡{pomodoros} Pomodoros completados! Tu concentración fue excepcional."
        elif pomodoros >= 4:
            mensaje_pomodoro = f"🍅 {pomodoros} Pomodoros realizados. ¡Buena disciplina de trabajo!"
        elif pomodoros >= 1:
            mensaje_pomodoro = f"🍅 {pomodoros} Pomodoro{'s' if pomodoros > 1 else ''} completado{'s' if pomodoros > 1 else ''}. ¡Cada sesión cuenta!"
        else:
            mensaje_pomodoro = "🍅 Mañana prueba usar el Pomodoro Timer. ¡Te ayudará a concentrarte mejor!"
        
        # Mensaje sobre tiempo activo
        if tiempo_activo >= 8:
            mensaje_tiempo = f"⏰ {tiempo_activo:.1f} horas de actividad. ¡Día muy productivo!"
        elif tiempo_activo >= 6:
            mensaje_tiempo = f"⏰ {tiempo_activo:.1f} horas de actividad. ¡Sólido día de trabajo!"
        elif tiempo_activo >= 4:
            mensaje_tiempo = f"⏰ {tiempo_activo:.1f} horas de actividad. ¡Buen ritmo de trabajo!"
        elif tiempo_activo >= 2:
            mensaje_tiempo = f"⏰ {tiempo_activo:.1f} horas de actividad. Considera períodos más largos de concentración."
        else:
            mensaje_tiempo = "⏰ Poco tiempo de actividad registrado. ¿Quizás trabajaste offline?"
        
        # Consejo para mañana
        consejos_manana = [
            "🌅 Mañana define tus objetivos apenas comiences el día.",
            "📋 Para mañana, prueba dividir tareas grandes en objetivos más pequeños.",
            "🎯 Mañana enfócate en 2-3 objetivos principales en lugar de muchos pequeños.",
            "⚡ Considera usar más el Pomodoro Timer mañana para mantener el foco.",
            "🌟 Mañana comienza con tu tarea más importante del día."
        ]
        
        # Construir mensaje final
        consejo = consejos_manana[hash(nombre) % len(consejos_manana)]
        
        mensaje_final = f"""
📊 RESUMEN DE TU DÍA, {nombre.upper()}:

{mensaje_objetivos}

{mensaje_pomodoro}

{mensaje_tiempo}

{consejo}
        """.strip()
        
        # Agregar sugerencia de música para mañana
        try:
            from personalizacion import sistema_musica
            sugerencia_musica = sistema_musica.obtener_sugerencia_contextual('fin_dia')
            
            if sugerencia_musica:
                mensaje_final += f"\n\n{sugerencia_musica['mensaje']}\n🔗 {sugerencia_musica['recurso']['nombre']}"
        except ImportError:
            pass  # El módulo de personalización no está disponible
        
        # Mensaje de cierre usando frases personalizadas
        try:
            from personalizacion import sistema_frases
            frase_cierre = sistema_frases.obtener_frase('fin_dia')
            mensaje_final += f"\n\n{frase_cierre}"
        except ImportError:
            mensaje_final += "\n\n¡Que descanses bien! Mañana será un gran día 🌙✨"
        
        return mensaje_final
    
    def enviar_resumen_a_api(self, resumen):
        """Envía el resumen a una API externa si está configurado"""
        try:
            url_api = config_sistema.config['reportes']['url_api']
            enviar_api = config_sistema.config['reportes']['enviar_a_api']
            
            if not enviar_api or not url_api:
                print("📡 Envío a API desactivado o no configurado")
                return False
            
            # Preparar datos para envío
            datos_envio = {
                'tipo': 'resumen_diario',
                'version': '1.0',
                'resumen': resumen
            }
            
            # Realizar petición POST
            response = requests.post(
                url_api,
                json=datos_envio,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Resumen enviado exitosamente a la API")
                registrar_evento("Resumen diario enviado a API", "sistema")
                return True
            else:
                print(f"⚠️ Error al enviar a API: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Error de conexión con API: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado al enviar a API: {e}")
            return False
    
    def guardar_resumen_local(self, resumen, mensaje_motivador):
        """Guarda el resumen localmente en archivos JSON y texto"""
        try:
            fecha = resumen['fecha']
            
            # Guardar resumen JSON
            archivo_json = f"storage/resumenes/resumen_{fecha}.json"
            import os
            os.makedirs(os.path.dirname(archivo_json), exist_ok=True)
            
            with open(archivo_json, 'w', encoding='utf-8') as f:
                json.dump(resumen, f, indent=2, ensure_ascii=False)
            
            # Guardar mensaje motivador
            archivo_mensaje = f"storage/resumenes/mensaje_{fecha}.txt"
            with open(archivo_mensaje, 'w', encoding='utf-8') as f:
                f.write(mensaje_motivador)
            
            print(f"💾 Resumen guardado localmente: {archivo_json}")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar resumen local: {e}")
            return False
    
    def procesar_resumen_diario(self):
        """Procesa el resumen diario completo"""
        try:
            print(f"📊 Generando resumen diario para {self.nombre_usuario}...")
            
            # Generar resumen
            resumen = self.generar_resumen_completo()
            if not resumen:
                print("❌ No se pudo generar el resumen")
                return False
            
            # Generar mensaje motivador
            mensaje_motivador = self.generar_mensaje_motivador(resumen)
            
            # Mostrar mensaje al usuario
            print("\n" + "="*60)
            print(mensaje_motivador)
            print("="*60)
            
            # Guardar localmente si está habilitado
            if config_sistema.config['reportes']['guardar_local']:
                self.guardar_resumen_local(resumen, mensaje_motivador)
            
            # Enviar a API si está habilitado
            if config_sistema.config['reportes']['enviar_a_api']:
                self.enviar_resumen_a_api(resumen)
            
            registrar_evento("Resumen diario generado", "sistema", {
                'objetivos_completados': resumen['objetivos']['objetivos_completados'],
                'tiempo_activo': resumen['metricas']['tiempo_activo_horas'],
                'pomodoros': resumen['metricas']['pomodoros_completados']
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Error al procesar resumen diario: {e}")
            return False
    
    def mostrar_resumen_ventana(self):
        """Muestra el resumen en una ventana gráfica"""
        try:
            import tkinter as tk
            from tkinter import ttk, messagebox
            
            resumen = self.generar_resumen_completo()
            if not resumen:
                messagebox.showerror("Error", "No se pudo generar el resumen")
                return
            
            mensaje = self.generar_mensaje_motivador(resumen)
            
            # Crear ventana
            ventana = tk.Toplevel()
            ventana.title(f"📊 Resumen del Día - {resumen['fecha']}")
            ventana.geometry("600x500")
            ventana.resizable(True, True)
            
            # Frame principal con scroll
            main_frame = ttk.Frame(ventana, padding="20")
            main_frame.pack(fill='both', expand=True)
            
            # Título
            titulo = tk.Label(main_frame, 
                            text=f"📊 Tu Día en Números, {self.nombre_usuario}",
                            font=('Arial', 16, 'bold'))
            titulo.pack(pady=(0, 20))
            
            # Métricas principales
            metricas_frame = ttk.LabelFrame(main_frame, text="📈 Métricas del Día", padding="10")
            metricas_frame.pack(fill='x', pady=(0, 15))
            
            metricas_text = f"""⏰ Tiempo activo: {resumen['metricas']['tiempo_activo_horas']} horas
🍅 Pomodoros completados: {resumen['metricas']['pomodoros_completados']}
🎯 Objetivos: {resumen['objetivos']['objetivos_completados']}/{resumen['objetivos']['total_objetivos']} ({resumen['objetivos']['porcentaje_completado']}%)
💻 App principal: {resumen['metricas']['aplicacion_principal']}"""
            
            tk.Label(metricas_frame, text=metricas_text, justify='left', font=('Arial', 10)).pack()
            
            # Mensaje motivador
            mensaje_frame = ttk.LabelFrame(main_frame, text="💭 Mensaje Personal", padding="10")
            mensaje_frame.pack(fill='both', expand=True, pady=(0, 15))
            
            text_widget = tk.Text(mensaje_frame, wrap='word', height=10, font=('Arial', 10))
            text_widget.pack(fill='both', expand=True)
            text_widget.insert('1.0', mensaje)
            text_widget.config(state='disabled')
            
            # Botón cerrar
            ttk.Button(main_frame, text="Cerrar", command=ventana.destroy).pack()
            
        except Exception as e:
            print(f"❌ Error al mostrar resumen en ventana: {e}")

def programar_resumen_automatico():
    """Programa el resumen automático al final del día"""
    import schedule
    import time
    import threading
    
    def ejecutar_resumen():
        resumen_diario = ResumenDiario()
        resumen_diario.procesar_resumen_diario()
    
    # Programar para las 18:00 por defecto
    hora_resumen = config_sistema.config['reportes']['hora_resumen_diario']
    schedule.every().day.at(hora_resumen).do(ejecutar_resumen)
    
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    hilo_schedule = threading.Thread(target=run_schedule, daemon=True)
    hilo_schedule.start()
    print(f"⏰ Resumen automático programado para las {hora_resumen}")

if __name__ == "__main__":
    # Prueba del sistema de resumen
    print("🧪 Probando sistema de resumen diario...")
    
    resumen = ResumenDiario()
    exito = resumen.procesar_resumen_diario()
    
    if exito:
        print("✅ Resumen generado exitosamente")
    else:
        print("❌ Error al generar resumen")

# pomodoro/notificador.py

from plyer import notification
import os
import threading
import time

class NotificadorPomodoro:
    def __init__(self):
        self.sonidos_activados = True
        self.icono_path = self._obtener_icono()
        
    def _obtener_icono(self):
        """Obtiene la ruta del icono para las notificaciones"""
        # Por ahora usamos None, podrías agregar un icono personalizado
        return None
    
    def _mostrar_notificacion(self, titulo, mensaje, duracion=10):
        """Muestra una notificación del sistema"""
        try:
            notification.notify(
                title=titulo,
                message=mensaje,
                app_name="Pomodoro Timer",
                timeout=duracion,
                app_icon=self.icono_path
            )
        except Exception as e:
            # Si falla la notificación, mostrar en consola
            print(f"🔔 {titulo}: {mensaje}")
            print(f"Error de notificación: {e}")
    
    def _reproducir_sonido_sistema(self):
        """Reproduce un sonido del sistema (beep)"""
        if self.sonidos_activados:
            try:
                import winsound
                winsound.Beep(800, 200)  # Frecuencia 800Hz, duración 200ms
            except:
                # Alternativa si winsound no está disponible
                print('\a')  # Beep del sistema
    
    def mostrar_inicio_trabajo(self, ciclo):
        """Notificación al iniciar una sesión de trabajo"""
        titulo = f"🍅 Pomodoro {ciclo}"
        mensaje = "¡Es hora de trabajar! Concentrate por 25 minutos."
        
        self._mostrar_notificacion(titulo, mensaje, duracion=5)
        self._reproducir_sonido_sistema()
        print(f"🍅 Iniciando Pomodoro {ciclo} - ¡A trabajar!")
    
    def mostrar_fin_trabajo(self):
        """Notificación al finalizar una sesión de trabajo"""
        titulo = "✅ ¡Pomodoro Completado!"
        mensaje = "¡Excelente trabajo! Es hora de tomar un descanso."
        
        self._mostrar_notificacion(titulo, mensaje, duracion=8)
        self._reproducir_sonido_sistema()
        print("✅ ¡Pomodoro completado! Tiempo de descansar.")
    
    def mostrar_inicio_descanso_corto(self):
        """Notificación al iniciar un descanso corto"""
        titulo = "☕ Descanso Corto"
        mensaje = "Tomate 5 minutos para relajarte. ¡Te lo merecés!"
        
        self._mostrar_notificacion(titulo, mensaje, duracion=5)
        print("☕ Descanso corto - 5 minutos para relajarte")
    
    def mostrar_inicio_descanso_largo(self):
        """Notificación al iniciar un descanso largo"""
        titulo = "🌴 Descanso Largo"
        mensaje = "¡Excelente! Tomate 15 minutos para recargar energías."
        
        self._mostrar_notificacion(titulo, mensaje, duracion=5)
        print("🌴 Descanso largo - 15 minutos para recargar")
    
    def mostrar_fin_descanso(self):
        """Notificación al finalizar cualquier descanso"""
        titulo = "🔄 Fin del Descanso"
        mensaje = "¡Descansaste bien! Es hora de volver al trabajo."
        
        self._mostrar_notificacion(titulo, mensaje, duracion=8)
        self._reproducir_sonido_sistema()
        print("🔄 Fin del descanso - ¡Volvamos al trabajo!")
    
    def mostrar_pausado(self):
        """Notificación cuando se pausa el Pomodoro"""
        titulo = "⏸️ Pomodoro Pausado"
        mensaje = "Temporizador pausado. Presiona reanudar cuando estés listo."
        
        self._mostrar_notificacion(titulo, mensaje, duracion=3)
        print("⏸️ Pomodoro pausado")
    
    def mostrar_reanudado(self):
        """Notificación cuando se reanuda el Pomodoro"""
        titulo = "▶️ Pomodoro Reanudado"
        mensaje = "¡Continuemos donde lo dejamos!"
        
        self._mostrar_notificacion(titulo, mensaje, duracion=3)
        print("▶️ Pomodoro reanudado")
    
    def mostrar_objetivo_completado(self, objetivo):
        """Notificación cuando se completa un objetivo"""
        titulo = "🎯 ¡Objetivo Completado!"
        mensaje = f"¡Felicitaciones! Completaste: {objetivo}"
        
        self._mostrar_notificacion(titulo, mensaje, duracion=10)
        self._reproducir_sonido_sistema()
        print(f"🎯 ¡Objetivo completado!: {objetivo}")
    
    def mostrar_progreso_objetivo(self, objetivo, progreso, total):
        """Notificación de progreso en un objetivo"""
        titulo = "📈 Progreso del Objetivo"
        mensaje = f"{objetivo}: {progreso}/{total} completado"
        
        if progreso % 3 == 0:  # Mostrar solo cada 3 avances para no saturar
            self._mostrar_notificacion(titulo, mensaje, duracion=5)
        
        print(f"📈 Progreso: {objetivo} ({progreso}/{total})")
    
    def configurar_sonidos(self, activar=True):
        """Activa o desactiva los sonidos"""
        self.sonidos_activados = activar
        estado = "activados" if activar else "desactivados"
        print(f"🔊 Sonidos {estado}")
    
    def mostrar_notificacion_personalizada(self, titulo, mensaje, duracion=5):
        """Permite mostrar notificaciones personalizadas"""
        self._mostrar_notificacion(titulo, mensaje, duracion)

# Función de prueba
def test_notificaciones():
    """Prueba todas las notificaciones"""
    notificador = NotificadorPomodoro()
    
    print("Probando notificaciones...")
    
    notificador.mostrar_inicio_trabajo(1)
    time.sleep(3)
    
    notificador.mostrar_fin_trabajo()
    time.sleep(3)
    
    notificador.mostrar_inicio_descanso_corto()
    time.sleep(3)
    
    notificador.mostrar_fin_descanso()
    time.sleep(3)
    
    notificador.mostrar_objetivo_completado("Contactar 10 clientes")
    
    print("Prueba de notificaciones completada")

if __name__ == "__main__":
    test_notificaciones()

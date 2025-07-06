# pomodoro/temporizador.py

import time
import threading
from datetime import datetime, timedelta
from pomodoro.notificador import NotificadorPomodoro
from monitor.logger import registrar_evento

class PomodoroTimer:
    def __init__(self):
        self.notificador = NotificadorPomodoro()
        self.activo = False
        self.pausado = False
        self.ciclo_actual = 1
        self.en_descanso = False
        
        # Configuración de tiempos (en minutos)
        self.tiempo_trabajo = 25
        self.tiempo_descanso_corto = 5
        self.tiempo_descanso_largo = 15
        self.ciclos_hasta_descanso_largo = 4
        
        # Estado interno
        self.tiempo_inicio = None
        self.tiempo_restante = 0
        
    def iniciar(self):
        """Inicia el ciclo Pomodoro"""
        self.activo = True
        registrar_evento("🍅 Pomodoro Timer iniciado")
        
        while self.activo:
            try:
                self._ejecutar_ciclo_completo()
            except Exception as e:
                print(f"Error en Pomodoro Timer: {e}")
                time.sleep(10)
    
    def _ejecutar_ciclo_completo(self):
        """Ejecuta un ciclo completo de Pomodoro"""
        # Fase de trabajo
        self._iniciar_fase_trabajo()
        
        if not self.activo:
            return
            
        # Determinar tipo de descanso
        if self.ciclo_actual % self.ciclos_hasta_descanso_largo == 0:
            self._iniciar_descanso_largo()
        else:
            self._iniciar_descanso_corto()
            
        self.ciclo_actual += 1
    
    def _iniciar_fase_trabajo(self):
        """Inicia una fase de trabajo de 25 minutos"""
        self.en_descanso = False
        duracion = self.tiempo_trabajo * 60  # Convertir a segundos
        
        self.notificador.mostrar_inicio_trabajo(self.ciclo_actual)
        registrar_evento(f"🍅 Iniciando Pomodoro {self.ciclo_actual} - Trabajo ({self.tiempo_trabajo} min)")
        
        self._ejecutar_temporizador(duracion, "trabajo")
        
        if self.activo:
            self.notificador.mostrar_fin_trabajo()
            registrar_evento(f"✅ Pomodoro {self.ciclo_actual} completado")
    
    def _iniciar_descanso_corto(self):
        """Inicia un descanso corto de 5 minutos"""
        self.en_descanso = True
        duracion = self.tiempo_descanso_corto * 60
        
        self.notificador.mostrar_inicio_descanso_corto()
        registrar_evento(f"☕ Iniciando descanso corto ({self.tiempo_descanso_corto} min)")
        
        self._ejecutar_temporizador(duracion, "descanso_corto")
        
        if self.activo:
            self.notificador.mostrar_fin_descanso()
            registrar_evento("🔄 Fin del descanso corto")
    
    def _iniciar_descanso_largo(self):
        """Inicia un descanso largo de 15 minutos"""
        self.en_descanso = True
        duracion = self.tiempo_descanso_largo * 60
        
        self.notificador.mostrar_inicio_descanso_largo()
        registrar_evento(f"🌴 Iniciando descanso largo ({self.tiempo_descanso_largo} min)")
        
        self._ejecutar_temporizador(duracion, "descanso_largo")
        
        if self.activo:
            self.notificador.mostrar_fin_descanso()
            registrar_evento("🔄 Fin del descanso largo")
    
    def _ejecutar_temporizador(self, duracion_segundos, tipo_fase):
        """Ejecuta el temporizador para una fase específica"""
        self.tiempo_inicio = time.time()
        tiempo_objetivo = self.tiempo_inicio + duracion_segundos
        
        while time.time() < tiempo_objetivo and self.activo:
            if not self.pausado:
                self.tiempo_restante = tiempo_objetivo - time.time()
                time.sleep(1)
            else:
                # Si está pausado, ajustar el tiempo objetivo
                tiempo_objetivo += 1
                time.sleep(1)
    
    def pausar(self):
        """Pausa el temporizador actual"""
        if self.activo and not self.pausado:
            self.pausado = True
            self.notificador.mostrar_pausado()
            registrar_evento("⏸️ Pomodoro pausado")
    
    def reanudar(self):
        """Reanuda el temporizador pausado"""
        if self.activo and self.pausado:
            self.pausado = False
            self.notificador.mostrar_reanudado()
            registrar_evento("▶️ Pomodoro reanudado")
    
    def detener(self):
        """Detiene completamente el Pomodoro"""
        self.activo = False
        self.pausado = False
        registrar_evento("🛑 Pomodoro Timer detenido")
    
    def obtener_estado(self):
        """Retorna el estado actual del Pomodoro"""
        if not self.activo:
            return {
                'activo': False,
                'ciclo': self.ciclo_actual,
                'fase': 'detenido'
            }
        
        fase = "descanso" if self.en_descanso else "trabajo"
        tiempo_restante_min = int(self.tiempo_restante / 60)
        tiempo_restante_seg = int(self.tiempo_restante % 60)
        
        return {
            'activo': True,
            'pausado': self.pausado,
            'ciclo': self.ciclo_actual,
            'fase': fase,
            'tiempo_restante': f"{tiempo_restante_min:02d}:{tiempo_restante_seg:02d}"
        }
    
    def configurar_tiempos(self, trabajo=None, descanso_corto=None, descanso_largo=None):
        """Permite configurar los tiempos del Pomodoro"""
        if trabajo:
            self.tiempo_trabajo = trabajo
        if descanso_corto:
            self.tiempo_descanso_corto = descanso_corto
        if descanso_largo:
            self.tiempo_descanso_largo = descanso_largo
            
        registrar_evento(f"⚙️ Tiempos configurados: {self.tiempo_trabajo}/{self.tiempo_descanso_corto}/{self.tiempo_descanso_largo}")

if __name__ == "__main__":
    # Prueba del temporizador
    pomodoro = PomodoroTimer()
    pomodoro.configurar_tiempos(trabajo=1, descanso_corto=1, descanso_largo=2)  # Tiempos cortos para prueba
    pomodoro.iniciar()

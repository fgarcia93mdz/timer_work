# monitor/ventana_activa.py

import win32gui
import time
import psutil
from monitor.logger import registrar_evento

class MonitorVentanas:
    def __init__(self):
        self.ventana_anterior = ""
        self.tiempo_inicio_ventana = time.time()
        self.tiempos_por_aplicacion = {}
        
    def get_active_window(self):
        """Obtiene el título de la ventana activa"""
        try:
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except:
            return "Desconocida"
    
    def get_process_name(self):
        """Obtiene el nombre del proceso de la ventana activa"""
        try:
            window = win32gui.GetForegroundWindow()
            _, pid = win32gui.GetWindowThreadProcessId(window)
            process = psutil.Process(pid)
            return process.name()
        except:
            return "proceso_desconocido"
    
    def actualizar_tiempo_aplicacion(self, aplicacion, tiempo_usado):
        """Actualiza el tiempo acumulado por aplicación"""
        if aplicacion in self.tiempos_por_aplicacion:
            self.tiempos_por_aplicacion[aplicacion] += tiempo_usado
        else:
            self.tiempos_por_aplicacion[aplicacion] = tiempo_usado
    
    def iniciar_monitoreo(self):
        """Inicia el monitoreo continuo de ventanas"""
        print("🪟 Iniciando monitoreo de ventanas activas...")
        
        while True:
            try:
                ventana_actual = self.get_active_window()
                proceso_actual = self.get_process_name()
                
                if ventana_actual != self.ventana_anterior and ventana_actual:
                    # Calcular tiempo en la ventana anterior
                    if self.ventana_anterior:
                        tiempo_usado = time.time() - self.tiempo_inicio_ventana
                        self.actualizar_tiempo_aplicacion(self.ventana_anterior, tiempo_usado)
                        
                        if tiempo_usado > 30:  # Solo registrar si estuvo más de 30 segundos
                            registrar_evento(f"Cambio de aplicación: {self.ventana_anterior} -> {ventana_actual} (tiempo: {tiempo_usado:.1f}s)")
                    
                    # Registrar nueva ventana
                    registrar_evento(f"Ventana activa: {ventana_actual} ({proceso_actual})")
                    self.ventana_anterior = ventana_actual
                    self.tiempo_inicio_ventana = time.time()
                
                time.sleep(60)  # Verificar cada 60 segundos según especificación
                
            except Exception as e:
                print(f"Error en monitoreo de ventanas: {e}")
                time.sleep(5)
    
    def obtener_estadisticas(self):
        """Retorna las estadísticas de tiempo por aplicación"""
        # Actualizar tiempo de la aplicación actual
        if self.ventana_anterior:
            tiempo_actual = time.time() - self.tiempo_inicio_ventana
            self.actualizar_tiempo_aplicacion(self.ventana_anterior, tiempo_actual)
        
        return self.tiempos_por_aplicacion

def test_ventana_activa():
    monitor = MonitorVentanas()
    monitor.iniciar_monitoreo()

# Si querés probar directamente este archivo
if __name__ == "__main__":
    test_ventana_activa()

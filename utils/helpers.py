# utils/helpers.py

import os
import sys
import json
import time
from datetime import datetime, timedelta
import threading

def formatear_tiempo(segundos):
    """Convierte segundos a formato legible (ej: 2h 30m 15s)"""
    if segundos < 60:
        return f"{segundos:.0f}s"
    elif segundos < 3600:
        minutos = segundos / 60
        return f"{minutos:.1f}m"
    else:
        horas = segundos / 3600
        minutos_restantes = (segundos % 3600) / 60
        if minutos_restantes < 1:
            return f"{horas:.1f}h"
        else:
            return f"{int(horas)}h {int(minutos_restantes)}m"

def formatear_tiempo_detallado(segundos):
    """Convierte segundos a formato HH:MM:SS"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos_restantes = int(segundos % 60)
    return f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"

def obtener_fecha_formateada(fecha=None):
    """Retorna una fecha en formato español legible"""
    if fecha is None:
        fecha = datetime.now()
    elif isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    
    meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    dias = [
        'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'
    ]
    
    dia_semana = dias[fecha.weekday()]
    dia = fecha.day
    mes = meses[fecha.month - 1]
    año = fecha.year
    
    return f"{dia_semana} {dia} de {mes} de {año}"

def es_horario_laboral(hora=None):
    """Determina si una hora está dentro del horario laboral típico"""
    if hora is None:
        hora = datetime.now().hour
    
    return 9 <= hora <= 18

def calcular_productividad(tiempo_activo, tiempo_total):
    """Calcula un porcentaje de productividad"""
    if tiempo_total == 0:
        return 0
    return (tiempo_activo / tiempo_total) * 100

def limpiar_nombre_aplicacion(nombre_ventana):
    """Limpia y normaliza el nombre de una aplicación"""
    if not nombre_ventana:
        return "Aplicación Desconocida"
    
    # Remover sufijos comunes de ventanas
    sufijos_remover = [
        " - Google Chrome",
        " - Mozilla Firefox",
        " - Microsoft Edge",
        " - Visual Studio Code",
        " - Notepad++",
        " - Word",
        " - Excel",
        " - PowerPoint"
    ]
    
    nombre_limpio = nombre_ventana
    for sufijo in sufijos_remover:
        if nombre_limpio.endswith(sufijo):
            nombre_limpio = nombre_limpio[:-len(sufijo)]
            break
    
    # Truncar si es muy largo
    if len(nombre_limpio) > 50:
        nombre_limpio = nombre_limpio[:47] + "..."
    
    return nombre_limpio

def categorizar_aplicacion(nombre_proceso):
    """Categoriza una aplicación según su tipo"""
    nombre_proceso = nombre_proceso.lower()
    
    categorias = {
        'navegador': ['chrome', 'firefox', 'edge', 'safari', 'opera', 'brave'],
        'desarrollo': ['code', 'pycharm', 'intellij', 'eclipse', 'atom', 'sublime'],
        'oficina': ['winword', 'excel', 'powerpnt', 'outlook', 'notepad'],
        'comunicacion': ['teams', 'zoom', 'skype', 'slack', 'discord', 'whatsapp'],
        'multimedia': ['vlc', 'spotify', 'iTunes', 'photoshop', 'premiere'],
        'juegos': ['steam', 'origin', 'epicgames', 'minecraft'],
        'sistema': ['explorer', 'taskmgr', 'settings', 'control'],
    }
    
    for categoria, procesos in categorias.items():
        if any(proceso in nombre_proceso for proceso in procesos):
            return categoria
    
    return 'otros'

def validar_configuracion():
    """Valida que todas las dependencias estén instaladas"""
    dependencias = [
        'pynput',
        'pywin32', 
        'schedule',
        'plyer',
        'psutil',
        'reportlab'
    ]
    
    faltantes = []
    
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltantes.append(dep)
    
    if faltantes:
        print("❌ Dependencias faltantes:")
        for dep in faltantes:
            print(f"   - {dep}")
        print("\n💡 Instala con: pip install " + " ".join(faltantes))
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def crear_backup_configuracion():
    """Crea un backup de la configuración actual"""
    try:
        backup_dir = 'storage/backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archivo_backup = f"{backup_dir}/backup_{timestamp}.json"
        
        configuracion = {
            'fecha_backup': datetime.now().isoformat(),
            'version': '1.0',
            # Aquí podrías agregar más datos de configuración
        }
        
        with open(archivo_backup, 'w', encoding='utf-8') as f:
            json.dump(configuracion, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Backup creado: {archivo_backup}")
        return archivo_backup
        
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return None

def monitorear_memoria():
    """Monitorea el uso de memoria del proceso actual"""
    try:
        import psutil
        proceso = psutil.Process()
        memoria_mb = proceso.memory_info().rss / 1024 / 1024
        return memoria_mb
    except:
        return 0

def configurar_logging():
    """Configura el sistema de logging avanzado"""
    import logging
    
    # Crear directorio de logs
    os.makedirs('storage/logs', exist_ok=True)
    
    # Configurar formato
    formato = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Archivo de log con rotación diaria
    archivo_log = f"storage/logs/actividad_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format=formato,
        handlers=[
            logging.FileHandler(archivo_log, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

class TemporizadorPersonalizado:
    """Clase para crear temporizadores personalizados"""
    
    def __init__(self, duracion_segundos, callback=None):
        self.duracion = duracion_segundos
        self.callback = callback
        self.activo = False
        self.hilo = None
    
    def iniciar(self):
        """Inicia el temporizador"""
        if not self.activo:
            self.activo = True
            self.hilo = threading.Thread(target=self._ejecutar, daemon=True)
            self.hilo.start()
    
    def detener(self):
        """Detiene el temporizador"""
        self.activo = False
    
    def _ejecutar(self):
        """Ejecuta el temporizador"""
        time.sleep(self.duracion)
        if self.activo and self.callback:
            self.callback()

def verificar_permisos_admin():
    """Verifica si el script tiene permisos de administrador (necesario para ciertos monitoreos)"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def obtener_informacion_sistema():
    """Obtiene información básica del sistema"""
    try:
        import platform
        import psutil
        
        info = {
            'sistema_operativo': platform.system(),
            'version_os': platform.version(),
            'arquitectura': platform.architecture()[0],
            'procesador': platform.processor(),
            'memoria_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'python_version': platform.python_version()
        }
        
        return info
    except:
        return {}

def generar_estadisticas_rapidas():
    """Genera estadísticas rápidas para mostrar en consola"""
    try:
        from storage.database import obtener_estadisticas_diarias
        from datetime import date
        
        stats = obtener_estadisticas_diarias(date.today().isoformat())
        
        if stats and stats['estadisticas_generales']:
            data = stats['estadisticas_generales']
            print("\n📊 ESTADÍSTICAS RÁPIDAS DE HOY:")
            print("=" * 40)
            print(f"⏱️  Tiempo activo: {formatear_tiempo(data[2] or 0)}")
            print(f"🍅 Pomodoros: {data[5] or 0}")
            print(f"🎯 Objetivos completados: {data[6] or 0}")
            print(f"💻 App principal: {data[7] or 'N/A'}")
            print("=" * 40)
        else:
            print("📊 No hay estadísticas disponibles aún")
            
    except Exception as e:
        print(f"❌ Error al generar estadísticas: {e}")

if __name__ == "__main__":
    # Pruebas de las funciones
    print("🧪 Probando funciones helper...")
    
    print(f"Tiempo formateado: {formatear_tiempo(7325)}")
    print(f"Fecha: {obtener_fecha_formateada()}")
    print(f"Horario laboral: {es_horario_laboral()}")
    print(f"Categoría Chrome: {categorizar_aplicacion('chrome.exe')}")
    
    validar_configuracion()
    generar_estadisticas_rapidas()

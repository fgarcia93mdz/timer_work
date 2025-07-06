# monitor/logger.py

import csv
import os
from datetime import datetime
import threading

# Importar base de datos si está disponible
try:
    from storage.database import registrar_evento_db
    DATABASE_DISPONIBLE = True
except ImportError:
    DATABASE_DISPONIBLE = False

LOG_FILE = 'storage/log_actividad.csv'

# Lock para escritura thread-safe
log_lock = threading.Lock()

def inicializar_log():
    """Inicializa el archivo de log CSV"""
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        existe = os.path.exists(LOG_FILE)
        if not existe:
            with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(['timestamp', 'evento', 'tipo_evento', 'datos_adicionales'])
            print(f"✅ Archivo de log creado: {LOG_FILE}")
        else:
            print(f"✅ Archivo de log encontrado: {LOG_FILE}")
            
    except Exception as e:
        print(f"❌ Error al inicializar log: {e}")

def registrar_evento(evento, tipo_evento="general", datos_adicionales=None, mostrar_consola=True):
    """
    Registra un evento en el log CSV y opcionalmente en la base de datos
    
    Args:
        evento (str): Descripción del evento
        tipo_evento (str): Categoría del evento (general, actividad, pomodoro, objetivo, etc.)
        datos_adicionales (dict): Datos adicionales del evento
        mostrar_consola (bool): Si mostrar el evento en consola
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with log_lock:
            # Registrar en CSV
            with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                datos_str = str(datos_adicionales) if datos_adicionales else ""
                writer.writerow([timestamp, evento, tipo_evento, datos_str])
            
            # Registrar en base de datos si está disponible
            if DATABASE_DISPONIBLE:
                try:
                    registrar_evento_db(tipo_evento, evento, datos_adicionales)
                except Exception as e:
                    if mostrar_consola:
                        print(f"⚠️ Error al registrar en BD (usando solo CSV): {e}")
            
            # Mostrar en consola si está habilitado
            if mostrar_consola:
                emoji_por_tipo = {
                    "general": "📝",
                    "actividad": "👁️",
                    "pomodoro": "🍅",
                    "objetivo": "🎯",
                    "sistema": "⚙️",
                    "error": "❌",
                    "ventana": "🪟",
                    "inactividad": "💤"
                }
                
                emoji = emoji_por_tipo.get(tipo_evento, "📝")
                print(f"[{timestamp}] {emoji} {evento}")
                
    except Exception as e:
        # En caso de error, al menos mostrar en consola
        if mostrar_consola:
            print(f"[{timestamp}] ❌ ERROR LOG: {evento} (Error: {e})")

def registrar_actividad(evento, datos_adicionales=None):
    """Registra un evento específico de actividad"""
    registrar_evento(evento, "actividad", datos_adicionales)

def registrar_pomodoro(evento, datos_adicionales=None):
    """Registra un evento específico del Pomodoro"""
    registrar_evento(evento, "pomodoro", datos_adicionales)

def registrar_objetivo(evento, datos_adicionales=None):
    """Registra un evento específico de objetivos"""
    registrar_evento(evento, "objetivo", datos_adicionales)

def registrar_ventana(evento, datos_adicionales=None):
    """Registra un evento específico de cambio de ventana"""
    registrar_evento(evento, "ventana", datos_adicionales, mostrar_consola=False)

def registrar_inactividad(evento, datos_adicionales=None):
    """Registra un evento específico de inactividad"""
    registrar_evento(evento, "inactividad", datos_adicionales)

def registrar_error(evento, datos_adicionales=None):
    """Registra un evento de error"""
    registrar_evento(evento, "error", datos_adicionales)

def obtener_eventos_recientes(limite=50, tipo_evento=None):
    """
    Obtiene los eventos más recientes del log
    
    Args:
        limite (int): Número máximo de eventos a retornar
        tipo_evento (str): Filtrar por tipo de evento específico
    
    Returns:
        list: Lista de eventos recientes
    """
    try:
        if not os.path.exists(LOG_FILE):
            return []
        
        eventos = []
        with open(LOG_FILE, mode='r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                if tipo_evento is None or fila.get('tipo_evento') == tipo_evento:
                    eventos.append(fila)
        
        # Retornar los más recientes
        return eventos[-limite:] if limite > 0 else eventos
        
    except Exception as e:
        print(f"❌ Error al leer eventos: {e}")
        return []

def limpiar_log_antiguo(dias_mantener=7):
    """
    Elimina eventos más antiguos que el número de días especificado
    
    Args:
        dias_mantener (int): Número de días de eventos a mantener
    """
    try:
        if not os.path.exists(LOG_FILE):
            return
        
        from datetime import timedelta
        fecha_limite = datetime.now() - timedelta(days=dias_mantener)
        
        eventos_mantener = []
        with open(LOG_FILE, mode='r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                try:
                    fecha_evento = datetime.strptime(fila['timestamp'], '%Y-%m-%d %H:%M:%S')
                    if fecha_evento >= fecha_limite:
                        eventos_mantener.append(fila)
                except ValueError:
                    # Mantener eventos con formato de fecha inválido
                    eventos_mantener.append(fila)
        
        # Reescribir archivo con eventos filtrados
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as archivo:
            if eventos_mantener:
                fieldnames = eventos_mantener[0].keys()
                writer = csv.DictWriter(archivo, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(eventos_mantener)
            else:
                # Si no hay eventos, crear encabezados básicos
                writer = csv.writer(archivo)
                writer.writerow(['timestamp', 'evento', 'tipo_evento', 'datos_adicionales'])
        
        eventos_eliminados = len(eventos_mantener)
        print(f"✅ Log limpiado. Eventos mantenidos: {eventos_eliminados}")
        
    except Exception as e:
        print(f"❌ Error al limpiar log: {e}")

def generar_resumen_log():
    """Genera un resumen rápido de la actividad del día"""
    try:
        eventos_hoy = obtener_eventos_recientes(limite=0)  # Todos los eventos
        
        if not eventos_hoy:
            print("📊 No hay eventos registrados")
            return
        
        # Filtrar eventos de hoy
        hoy = datetime.now().strftime('%Y-%m-%d')
        eventos_hoy_filtrados = [
            evento for evento in eventos_hoy 
            if evento['timestamp'].startswith(hoy)
        ]
        
        if not eventos_hoy_filtrados:
            print(f"📊 No hay eventos registrados para hoy ({hoy})")
            return
        
        # Contar por tipo
        conteo_tipos = {}
        for evento in eventos_hoy_filtrados:
            tipo = evento.get('tipo_evento', 'general')
            conteo_tipos[tipo] = conteo_tipos.get(tipo, 0) + 1
        
        print(f"\n📊 RESUMEN DE ACTIVIDAD ({hoy}):")
        print("=" * 40)
        for tipo, cantidad in sorted(conteo_tipos.items()):
            emoji_por_tipo = {
                "actividad": "👁️",
                "pomodoro": "🍅",
                "objetivo": "🎯",
                "ventana": "🪟",
                "inactividad": "💤",
                "general": "📝"
            }
            emoji = emoji_por_tipo.get(tipo, "📝")
            print(f"{emoji} {tipo.capitalize()}: {cantidad} eventos")
        
        print(f"\n📈 Total de eventos: {len(eventos_hoy_filtrados)}")
        print("=" * 40)
        
    except Exception as e:
        print(f"❌ Error al generar resumen: {e}")

# Funciones de compatibilidad hacia atrás
def registrar_evento_simple(evento):
    """Función de compatibilidad para el código existente"""
    registrar_evento(evento, "general")

if __name__ == "__main__":
    # Pruebas del sistema de logging
    print("🧪 Probando sistema de logging...")
    
    inicializar_log()
    
    # Probar diferentes tipos de eventos
    registrar_evento("Sistema de prueba iniciado", "sistema")
    registrar_actividad("Usuario activo detectado")
    registrar_pomodoro("Pomodoro iniciado")
    registrar_objetivo("Objetivo creado: Prueba")
    registrar_ventana("Cambio a Visual Studio Code")
    registrar_inactividad("Usuario inactivo")
    
    # Mostrar resumen
    generar_resumen_log()
    
    # Mostrar eventos recientes
    eventos = obtener_eventos_recientes(5)
    print(f"\n🔍 Últimos 5 eventos:")
    for evento in eventos:
        print(f"  {evento['timestamp']} - {evento['evento']}")
    
    print("\n✅ Prueba del sistema de logging completada")

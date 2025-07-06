# storage/database.py

import sqlite3
import os
from datetime import datetime, date
import json

DATABASE_PATH = 'storage/actividad.db'

def inicializar_db():
    """Inicializa la base de datos SQLite con todas las tablas necesarias"""
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Tabla de eventos de actividad
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos_actividad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                tipo_evento TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                datos_adicionales TEXT,
                fecha DATE DEFAULT (date('now'))
            )
        ''')
        
        # Tabla de tiempo por aplicación
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tiempo_aplicaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE DEFAULT (date('now')),
                aplicacion TEXT NOT NULL,
                proceso TEXT,
                tiempo_segundos INTEGER DEFAULT 0,
                sesiones INTEGER DEFAULT 1,
                UNIQUE(fecha, aplicacion)
            )
        ''')
        
        # Tabla de sesiones Pomodoro
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesiones_pomodoro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE DEFAULT (date('now')),
                numero_sesion INTEGER,
                tipo TEXT CHECK(tipo IN ('trabajo', 'descanso_corto', 'descanso_largo')),
                inicio DATETIME,
                fin DATETIME,
                completada BOOLEAN DEFAULT FALSE,
                interrumpida BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Tabla de objetivos diarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS objetivos_diarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE DEFAULT (date('now')),
                descripcion TEXT NOT NULL,
                tipo TEXT DEFAULT 'contador',
                meta INTEGER DEFAULT 1,
                progreso INTEGER DEFAULT 0,
                completado BOOLEAN DEFAULT FALSE,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                fecha_completado DATETIME
            )
        ''')
        
        # Tabla de estadísticas diarias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estadisticas_diarias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE UNIQUE DEFAULT (date('now')),
                tiempo_activo_segundos INTEGER DEFAULT 0,
                tiempo_inactivo_segundos INTEGER DEFAULT 0,
                clicks_totales INTEGER DEFAULT 0,
                teclas_totales INTEGER DEFAULT 0,
                pomodoros_completados INTEGER DEFAULT 0,
                objetivos_completados INTEGER DEFAULT 0,
                aplicacion_mas_usada TEXT,
                tiempo_aplicacion_principal INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")

def registrar_evento_db(tipo_evento, descripcion, datos_adicionales=None):
    """Registra un evento en la base de datos"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        datos_json = json.dumps(datos_adicionales) if datos_adicionales else None
        
        cursor.execute('''
            INSERT INTO eventos_actividad (tipo_evento, descripcion, datos_adicionales)
            VALUES (?, ?, ?)
        ''', (tipo_evento, descripcion, datos_json))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error al registrar evento en BD: {e}")

def actualizar_tiempo_aplicacion(aplicacion, proceso, tiempo_segundos):
    """Actualiza el tiempo usado en una aplicación específica"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        fecha_hoy = date.today().isoformat()
        
        # Verificar si ya existe registro para hoy
        cursor.execute('''
            SELECT tiempo_segundos, sesiones FROM tiempo_aplicaciones 
            WHERE fecha = ? AND aplicacion = ?
        ''', (fecha_hoy, aplicacion))
        
        resultado = cursor.fetchone()
        
        if resultado:
            # Actualizar registro existente
            nuevo_tiempo = resultado[0] + tiempo_segundos
            nuevas_sesiones = resultado[1] + 1
            
            cursor.execute('''
                UPDATE tiempo_aplicaciones 
                SET tiempo_segundos = ?, sesiones = ?, proceso = ?
                WHERE fecha = ? AND aplicacion = ?
            ''', (nuevo_tiempo, nuevas_sesiones, proceso, fecha_hoy, aplicacion))
        else:
            # Crear nuevo registro
            cursor.execute('''
                INSERT INTO tiempo_aplicaciones 
                (fecha, aplicacion, proceso, tiempo_segundos, sesiones)
                VALUES (?, ?, ?, ?, 1)
            ''', (fecha_hoy, aplicacion, proceso, tiempo_segundos))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error al actualizar tiempo de aplicación: {e}")

def registrar_sesion_pomodoro(numero_sesion, tipo, completada=True, interrumpida=False):
    """Registra una sesión de Pomodoro en la base de datos"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sesiones_pomodoro 
            (numero_sesion, tipo, inicio, fin, completada, interrumpida)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (numero_sesion, tipo, datetime.now(), datetime.now(), completada, interrumpida))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error al registrar sesión Pomodoro: {e}")

def obtener_estadisticas_diarias(fecha=None):
    """Obtiene las estadísticas de un día específico"""
    if fecha is None:
        fecha = date.today().isoformat()
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Estadísticas básicas
        cursor.execute('''
            SELECT * FROM estadisticas_diarias WHERE fecha = ?
        ''', (fecha,))
        
        estadisticas = cursor.fetchone()
        
        # Tiempo por aplicaciones
        cursor.execute('''
            SELECT aplicacion, tiempo_segundos, sesiones 
            FROM tiempo_aplicaciones 
            WHERE fecha = ?
            ORDER BY tiempo_segundos DESC
        ''', (fecha,))
        
        aplicaciones = cursor.fetchall()
        
        # Sesiones Pomodoro
        cursor.execute('''
            SELECT tipo, COUNT(*), AVG(CASE WHEN completada THEN 1 ELSE 0 END)
            FROM sesiones_pomodoro 
            WHERE date(inicio) = ?
            GROUP BY tipo
        ''', (fecha,))
        
        pomodoros = cursor.fetchall()
        
        # Objetivos del día
        cursor.execute('''
            SELECT COUNT(*), 
                   SUM(CASE WHEN completado THEN 1 ELSE 0 END),
                   AVG(progreso * 100.0 / meta)
            FROM objetivos_diarios 
            WHERE fecha = ?
        ''', (fecha,))
        
        objetivos = cursor.fetchone()
        
        conn.close()
        
        return {
            'estadisticas_generales': estadisticas,
            'tiempo_aplicaciones': aplicaciones,
            'sesiones_pomodoro': pomodoros,
            'objetivos': objetivos
        }
        
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return None

def actualizar_estadisticas_diarias():
    """Actualiza las estadísticas del día actual"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        fecha_hoy = date.today().isoformat()
        
        # Calcular tiempo total por aplicaciones
        cursor.execute('''
            SELECT SUM(tiempo_segundos), COUNT(DISTINCT aplicacion)
            FROM tiempo_aplicaciones 
            WHERE fecha = ?
        ''', (fecha_hoy,))
        
        resultado_apps = cursor.fetchone()
        tiempo_total = resultado_apps[0] or 0
        
        # Aplicación más usada
        cursor.execute('''
            SELECT aplicacion, tiempo_segundos 
            FROM tiempo_aplicaciones 
            WHERE fecha = ?
            ORDER BY tiempo_segundos DESC 
            LIMIT 1
        ''', (fecha_hoy,))
        
        app_principal = cursor.fetchone()
        
        # Contar Pomodoros completados
        cursor.execute('''
            SELECT COUNT(*) FROM sesiones_pomodoro 
            WHERE date(inicio) = ? AND completada = TRUE AND tipo = 'trabajo'
        ''', (fecha_hoy,))
        
        pomodoros_completados = cursor.fetchone()[0]
        
        # Contar objetivos completados
        cursor.execute('''
            SELECT COUNT(*) FROM objetivos_diarios 
            WHERE fecha = ? AND completado = TRUE
        ''', (fecha_hoy,))
        
        objetivos_completados = cursor.fetchone()[0]
        
        # Insertar o actualizar estadísticas
        cursor.execute('''
            INSERT OR REPLACE INTO estadisticas_diarias 
            (fecha, tiempo_activo_segundos, pomodoros_completados, objetivos_completados,
             aplicacion_mas_usada, tiempo_aplicacion_principal)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (fecha_hoy, tiempo_total, pomodoros_completados, objetivos_completados,
              app_principal[0] if app_principal else None,
              app_principal[1] if app_principal else 0))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error al actualizar estadísticas diarias: {e}")

def obtener_resumen_semanal():
    """Obtiene un resumen de la actividad de los últimos 7 días"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT fecha, tiempo_activo_segundos, pomodoros_completados, 
                   objetivos_completados, aplicacion_mas_usada
            FROM estadisticas_diarias 
            WHERE fecha >= date('now', '-7 days')
            ORDER BY fecha DESC
        ''', )
        
        datos = cursor.fetchall()
        conn.close()
        
        return datos
        
    except Exception as e:
        print(f"Error al obtener resumen semanal: {e}")
        return []

def limpiar_datos_antiguos(dias_a_mantener=30):
    """Elimina datos más antiguos que el número de días especificado"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        fecha_limite = f"date('now', '-{dias_a_mantener} days')"
        
        # Limpiar eventos antiguos
        cursor.execute(f'''
            DELETE FROM eventos_actividad 
            WHERE fecha < {fecha_limite}
        ''')
        
        # Limpiar datos de aplicaciones antiguos
        cursor.execute(f'''
            DELETE FROM tiempo_aplicaciones 
            WHERE fecha < {fecha_limite}
        ''')
        
        conn.commit()
        conn.close()
        
        print(f"✅ Datos antiguos eliminados (manteniendo últimos {dias_a_mantener} días)")
        
    except Exception as e:
        print(f"Error al limpiar datos antiguos: {e}")

if __name__ == "__main__":
    # Prueba de la base de datos
    inicializar_db()
    registrar_evento_db("prueba", "Evento de prueba", {"test": True})
    stats = obtener_estadisticas_diarias()
    print("Estadísticas:", stats)

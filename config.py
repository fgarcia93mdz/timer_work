# config.py - Configuración centralizada del sistema

import os
import json
from datetime import datetime

CONFIG_FILE = 'storage/config.json'

class ConfiguracionSistema:
    def __init__(self):
        self.config_default = {
            'usuario': {
                'nombre': '',
                'primer_uso': True,
                'fecha_registro': None
            },
            'monitoreo': {
                'intervalo_ventana_segundos': 60,  # Cada 60 segundos como solicitaste
                'tiempo_inactividad_minutos': 10,  # 10 minutos para marcar inactividad
                'registro_detallado': True
            },
            'pomodoro': {
                'tiempo_trabajo_minutos': 25,
                'tiempo_descanso_corto_minutos': 5,
                'tiempo_descanso_largo_minutos': 15,
                'ciclos_hasta_descanso_largo': 4,
                'notificaciones_activas': True,
                'sonidos_activos': True
            },
            'objetivos': {
                'recordatorio_inicio_dia': True,
                'mostrar_progreso_continuo': True
            },
            'reportes': {
                'enviar_a_api': False,
                'url_api': '',
                'guardar_local': True,
                'hora_resumen_diario': '18:00'
            },
            'interfaz': {
                'modo_tray': True,
                'ventana_siempre_visible': False,
                'tema': 'claro'
            }
        }
        self.config = self.cargar_configuracion()
    
    def cargar_configuracion(self):
        """Carga la configuración desde el archivo JSON"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config_cargada = json.load(f)
                    # Fusionar con config default para nuevas opciones
                    return self._fusionar_config(self.config_default, config_cargada)
            else:
                return self.config_default.copy()
        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
            return self.config_default.copy()
    
    def _fusionar_config(self, default, cargada):
        """Fusiona configuración cargada con valores por defecto"""
        resultado = default.copy()
        for seccion, valores in cargada.items():
            if seccion in resultado and isinstance(valores, dict):
                resultado[seccion].update(valores)
            else:
                resultado[seccion] = valores
        return resultado
    
    def guardar_configuracion(self):
        """Guarda la configuración actual en el archivo"""
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")
    
    def configurar_primer_uso(self, nombre_usuario):
        """Configura el sistema para el primer uso"""
        self.config['usuario']['nombre'] = nombre_usuario
        self.config['usuario']['primer_uso'] = False
        self.config['usuario']['fecha_registro'] = datetime.now().isoformat()
        self.guardar_configuracion()
        print(f"✅ Sistema configurado para {nombre_usuario}")
    
    def es_primer_uso(self):
        """Verifica si es el primer uso del sistema"""
        return self.config['usuario']['primer_uso']
    
    def obtener_nombre_usuario(self):
        """Obtiene el nombre del usuario configurado"""
        return self.config['usuario']['nombre']
    
    def actualizar_configuracion(self, seccion, clave, valor):
        """Actualiza una configuración específica"""
        if seccion in self.config and isinstance(self.config[seccion], dict):
            self.config[seccion][clave] = valor
            self.guardar_configuracion()
            return True
        return False
    
    def obtener_configuracion(self, seccion, clave=None):
        """Obtiene una configuración específica"""
        if seccion in self.config:
            if clave is None:
                return self.config[seccion]
            elif clave in self.config[seccion]:
                return self.config[seccion][clave]
        return None

# Instancia global de configuración
config_sistema = ConfiguracionSistema()

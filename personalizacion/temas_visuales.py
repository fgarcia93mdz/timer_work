# personalizacion/temas_visuales.py - Sistema de temas y personalización visual

import json
import os
from datetime import datetime

TEMAS_FILE = 'storage/temas_personalizados.json'

class SistemaTemasVisuales:
    def __init__(self):
        self.temas_predefinidos = {
            'productivo': {
                'nombre': '🎯 Tema Productivo',
                'colores': {
                    'primario': '#2E8B57',      # Verde bosque
                    'secundario': '#98FB98',    # Verde claro
                    'acento': '#FF6B35',        # Naranja energético
                    'fondo': '#F0F8FF',         # Azul muy claro
                    'texto': '#2F4F4F',         # Gris oscuro
                    'error': '#DC143C',         # Rojo carmesí
                    'exito': '#32CD32',         # Verde lima
                    'advertencia': '#FFD700'    # Dorado
                },
                'fuentes': {
                    'principal': 'Segoe UI',
                    'tamaño_normal': 10,
                    'tamaño_titulo': 14,
                    'tamaño_grande': 16
                },
                'efectos': {
                    'sombras': True,
                    'bordes_redondeados': True,
                    'animaciones': True
                }
            },
            'zen': {
                'nombre': '🧘‍♀️ Tema Zen',
                'colores': {
                    'primario': '#8FBC8F',      # Verde grisáceo
                    'secundario': '#F5F5DC',    # Beige
                    'acento': '#DDA0DD',        # Ciruela
                    'fondo': '#F8F8FF',         # Blanco fantasma
                    'texto': '#696969',         # Gris tenue
                    'error': '#CD5C5C',         # Rojo indio
                    'exito': '#9ACD32',         # Verde amarillo
                    'advertencia': '#F0E68C'    # Caqui
                },
                'fuentes': {
                    'principal': 'Calibri',
                    'tamaño_normal': 10,
                    'tamaño_titulo': 13,
                    'tamaño_grande': 15
                },
                'efectos': {
                    'sombras': False,
                    'bordes_redondeados': True,
                    'animaciones': False
                }
            },
            'energia': {
                'nombre': '⚡ Tema Energía',
                'colores': {
                    'primario': '#FF4500',      # Rojo naranja
                    'secundario': '#FFA500',    # Naranja
                    'acento': '#FFD700',        # Dorado
                    'fondo': '#FFFACD',         # Amarillo claro
                    'texto': '#8B0000',         # Rojo oscuro
                    'error': '#B22222',         # Rojo ladrillo
                    'exito': '#228B22',         # Verde bosque
                    'advertencia': '#FF8C00'    # Naranja oscuro
                },
                'fuentes': {
                    'principal': 'Arial',
                    'tamaño_normal': 10,
                    'tamaño_titulo': 14,
                    'tamaño_grande': 16
                },
                'efectos': {
                    'sombras': True,
                    'bordes_redondeados': False,
                    'animaciones': True
                }
            },
            'nocturno': {
                'nombre': '🌙 Tema Nocturno',
                'colores': {
                    'primario': '#4169E1',      # Azul real
                    'secundario': '#191970',    # Azul medianoche
                    'acento': '#00CED1',        # Turquesa oscuro
                    'fondo': '#2F2F2F',         # Gris muy oscuro
                    'texto': '#E0E0E0',         # Gris claro
                    'error': '#FF6347',         # Tomate
                    'exito': '#00FF7F',         # Verde primavera
                    'advertencia': '#FFB347'    # Naranja claro
                },
                'fuentes': {
                    'principal': 'Consolas',
                    'tamaño_normal': 10,
                    'tamaño_titulo': 13,
                    'tamaño_grande': 15
                },
                'efectos': {
                    'sombras': True,
                    'bordes_redondeados': True,
                    'animaciones': False
                }
            },
            'minimalista': {
                'nombre': '⚪ Tema Minimalista',
                'colores': {
                    'primario': '#708090',      # Gris pizarra
                    'secundario': '#D3D3D3',    # Gris claro
                    'acento': '#4682B4',        # Azul acero
                    'fondo': '#FFFFFF',         # Blanco
                    'texto': '#2F4F4F',         # Gris oscuro
                    'error': '#A0522D',         # Marrón silla
                    'exito': '#556B2F',         # Verde olivo oscuro
                    'advertencia': '#B8860B'    # Vara dorada oscura
                },
                'fuentes': {
                    'principal': 'Helvetica',
                    'tamaño_normal': 9,
                    'tamaño_titulo': 12,
                    'tamaño_grande': 14
                },
                'efectos': {
                    'sombras': False,
                    'bordes_redondeados': False,
                    'animaciones': False
                }
            }
        }
        self.tema_actual = 'productivo'
        self.temas_personalizados = self.cargar_temas_personalizados()
    
    def cargar_temas_personalizados(self):
        """Carga temas personalizados del usuario"""
        try:
            if os.path.exists(TEMAS_FILE):
                with open(TEMAS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tema_actual = data.get('tema_actual', 'productivo')
                    return data.get('temas_personalizados', {})
            else:
                return {}
        except Exception as e:
            print(f"❌ Error cargando temas personalizados: {e}")
            return {}
    
    def guardar_temas_personalizados(self):
        """Guarda los temas personalizados en archivo"""
        try:
            os.makedirs(os.path.dirname(TEMAS_FILE), exist_ok=True)
            data = {
                'tema_actual': self.tema_actual,
                'temas_personalizados': self.temas_personalizados,
                'ultima_actualizacion': datetime.now().isoformat()
            }
            with open(TEMAS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando temas personalizados: {e}")
    
    def obtener_tema_actual(self):
        """Obtiene la configuración del tema actual"""
        if self.tema_actual in self.temas_personalizados:
            return self.temas_personalizados[self.tema_actual]
        elif self.tema_actual in self.temas_predefinidos:
            return self.temas_predefinidos[self.tema_actual]
        else:
            return self.temas_predefinidos['productivo']
    
    def cambiar_tema(self, nombre_tema):
        """Cambia el tema actual"""
        if (nombre_tema in self.temas_predefinidos or 
            nombre_tema in self.temas_personalizados):
            self.tema_actual = nombre_tema
            self.guardar_temas_personalizados()
            return True
        return False
    
    def obtener_color(self, tipo_color):
        """Obtiene un color específico del tema actual"""
        tema = self.obtener_tema_actual()
        return tema['colores'].get(tipo_color, '#000000')
    
    def obtener_fuente(self, tipo_fuente='principal'):
        """Obtiene configuración de fuente del tema actual"""
        tema = self.obtener_tema_actual()
        return tema['fuentes'].get(tipo_fuente, 'Arial')
    
    def obtener_todos_los_temas(self):
        """Obtiene lista de todos los temas disponibles"""
        temas = {}
        temas.update(self.temas_predefinidos)
        temas.update(self.temas_personalizados)
        return temas
    
    def crear_tema_personalizado(self, nombre, configuracion):
        """Crea un nuevo tema personalizado"""
        self.temas_personalizados[nombre] = configuracion
        self.guardar_temas_personalizados()
        return True
    
    def obtener_estilo_tkinter(self):
        """Genera configuración de estilo para Tkinter"""
        tema = self.obtener_tema_actual()
        colores = tema['colores']
        fuentes = tema['fuentes']
        
        return {
            'bg': colores['fondo'],
            'fg': colores['texto'],
            'font': (fuentes['principal'], fuentes['tamaño_normal']),
            'selectbackground': colores['secundario'],
            'selectforeground': colores['texto'],
            'insertbackground': colores['texto'],
            'highlightbackground': colores['primario'],
            'highlightcolor': colores['acento'],
            'activebackground': colores['secundario'],
            'activeforeground': colores['texto'],
            'relief': 'flat' if not tema['efectos']['bordes_redondeados'] else 'raised'
        }
    
    def obtener_estilo_boton(self, tipo='normal'):
        """Genera estilo específico para botones"""
        tema = self.obtener_tema_actual()
        colores = tema['colores']
        fuentes = tema['fuentes']
        
        estilos = {
            'normal': {
                'bg': colores['primario'],
                'fg': colores['fondo'],
                'font': (fuentes['principal'], fuentes['tamaño_normal'], 'bold'),
                'activebackground': colores['acento'],
                'activeforeground': colores['fondo']
            },
            'exito': {
                'bg': colores['exito'],
                'fg': colores['fondo'],
                'font': (fuentes['principal'], fuentes['tamaño_normal'], 'bold')
            },
            'error': {
                'bg': colores['error'],
                'fg': colores['fondo'],
                'font': (fuentes['principal'], fuentes['tamaño_normal'], 'bold')
            },
            'advertencia': {
                'bg': colores['advertencia'],
                'fg': colores['texto'],
                'font': (fuentes['principal'], fuentes['tamaño_normal'], 'bold')
            }
        }
        
        return estilos.get(tipo, estilos['normal'])
    
    def generar_gradiente_color(self, color_inicio, color_fin, pasos=10):
        """Genera una lista de colores en gradiente (para futuras animaciones)"""
        # Convertir hex a RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        inicio_rgb = hex_to_rgb(color_inicio)
        fin_rgb = hex_to_rgb(color_fin)
        
        gradiente = []
        for i in range(pasos):
            factor = i / (pasos - 1)
            r = inicio_rgb[0] + (fin_rgb[0] - inicio_rgb[0]) * factor
            g = inicio_rgb[1] + (fin_rgb[1] - inicio_rgb[1]) * factor
            b = inicio_rgb[2] + (fin_rgb[2] - inicio_rgb[2]) * factor
            gradiente.append(rgb_to_hex((r, g, b)))
        
        return gradiente

# Instancia global
sistema_temas = SistemaTemasVisuales()

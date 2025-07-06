# personalizacion/musica_motivacional.py - Sistema de música y recursos motivacionales

import json
import os
import webbrowser
import random
from datetime import datetime

MUSICA_FILE = 'storage/musica_recursos.json'

class SistemaMusicaMotivacional:
    def __init__(self):
        self.recursos_default = {
            'musica_focus': [
                {
                    'nombre': '🎵 Lofi Hip Hop - Deep Focus',
                    'url': 'https://www.youtube.com/watch?v=jfKfPfyJRdk',
                    'tipo': 'youtube',
                    'descripcion': 'Música relajante para concentración profunda'
                },
                {
                    'nombre': '🎼 Classical Music for Studying',
                    'url': 'https://www.youtube.com/watch?v=YE2iyBvzZbw',
                    'tipo': 'youtube',
                    'descripcion': 'Música clásica ideal para estudiar'
                },
                {
                    'nombre': '🌊 Nature Sounds - Forest Rain',
                    'url': 'https://www.youtube.com/watch?v=nDq6TstdEi8',
                    'tipo': 'youtube',
                    'descripcion': 'Sonidos de la naturaleza para relajación'
                },
                {
                    'nombre': '⚡ Binaural Beats - Focus 40Hz',
                    'url': 'https://www.youtube.com/watch?v=GpWyF4FrOYU',
                    'tipo': 'youtube',
                    'descripcion': 'Ondas binaurales para concentración'
                }
            ],
            'musica_energia': [
                {
                    'nombre': '🔥 Epic Motivation Music',
                    'url': 'https://www.youtube.com/watch?v=XULUBg_ZcAU',
                    'tipo': 'youtube',
                    'descripcion': 'Música épica para máxima motivación'
                },
                {
                    'nombre': '⚡ High Energy Workout Mix',
                    'url': 'https://www.youtube.com/watch?v=fBYVlFXsEME',
                    'tipo': 'youtube',
                    'descripcion': 'Mix energético para activarse'
                },
                {
                    'nombre': '🎯 Productivity Power Hour',
                    'url': 'https://www.youtube.com/watch?v=BeOdBkHBGUs',
                    'tipo': 'youtube',
                    'descripcion': 'Una hora de música ultra productiva'
                }
            ],
            'descanso': [
                {
                    'nombre': '🧘‍♀️ Meditation Music - 5 min',
                    'url': 'https://www.youtube.com/watch?v=1ZYbU82GVz4',
                    'tipo': 'youtube',
                    'descripcion': 'Música de meditación para descansos'
                },
                {
                    'nombre': '☕ Café Jazz - Relaxing',
                    'url': 'https://www.youtube.com/watch?v=Dx5qFachd3A',
                    'tipo': 'youtube',
                    'descripcion': 'Jazz suave para descansar'
                },
                {
                    'nombre': '🌅 Morning Ambient Music',
                    'url': 'https://www.youtube.com/watch?v=5qap5aO4i9A',
                    'tipo': 'youtube',
                    'descripcion': 'Música ambiente para relajarse'
                }
            ],
            'podcasts_motivacion': [
                {
                    'nombre': '🎙️ The Tim Ferriss Show',
                    'url': 'https://tim.blog/podcast/',
                    'tipo': 'podcast',
                    'descripcion': 'Entrevistas con personas de alto rendimiento'
                },
                {
                    'nombre': '💪 The Tony Robbins Podcast',
                    'url': 'https://www.tonyrobbins.com/podcasts/',
                    'tipo': 'podcast',
                    'descripcion': 'Desarrollo personal y motivación'
                }
            ],
            'recursos_productividad': [
                {
                    'nombre': '📖 Getting Things Done (GTD)',
                    'url': 'https://gettingthingsdone.com/',
                    'tipo': 'web',
                    'descripcion': 'Metodología de productividad personal'
                },
                {
                    'nombre': '🎯 Notion Templates',
                    'url': 'https://www.notion.so/templates',
                    'tipo': 'web',
                    'descripcion': 'Plantillas para organización'
                }
            ]
        }
        self.recursos_personalizados = self.cargar_recursos_personalizados()
    
    def cargar_recursos_personalizados(self):
        """Carga recursos personalizados del usuario"""
        try:
            if os.path.exists(MUSICA_FILE):
                with open(MUSICA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"❌ Error cargando recursos personalizados: {e}")
            return {}
    
    def guardar_recursos_personalizados(self):
        """Guarda los recursos personalizados en archivo"""
        try:
            os.makedirs(os.path.dirname(MUSICA_FILE), exist_ok=True)
            with open(MUSICA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.recursos_personalizados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando recursos personalizados: {e}")
    
    def obtener_recurso_aleatorio(self, categoria):
        """Obtiene un recurso aleatorio de la categoría especificada"""
        recursos_disponibles = []
        
        # Agregar recursos personalizados
        if categoria in self.recursos_personalizados:
            recursos_disponibles.extend(self.recursos_personalizados[categoria])
        
        # Agregar recursos por defecto
        if categoria in self.recursos_default:
            recursos_disponibles.extend(self.recursos_default[categoria])
        
        if not recursos_disponibles:
            return None
        
        return random.choice(recursos_disponibles)
    
    def agregar_recurso_personalizado(self, categoria, nombre, url, tipo, descripcion=""):
        """Agrega un recurso personalizado"""
        if categoria not in self.recursos_personalizados:
            self.recursos_personalizados[categoria] = []
        
        nuevo_recurso = {
            'nombre': nombre,
            'url': url,
            'tipo': tipo,
            'descripcion': descripcion,
            'fecha_agregado': datetime.now().isoformat()
        }
        
        self.recursos_personalizados[categoria].append(nuevo_recurso)
        self.guardar_recursos_personalizados()
        return True
    
    def abrir_recurso(self, recurso):
        """Abre un recurso en el navegador"""
        try:
            webbrowser.open(recurso['url'])
            return True
        except Exception as e:
            print(f"❌ Error abriendo recurso: {e}")
            return False
    
    def obtener_sugerencia_contextual(self, contexto):
        """Obtiene sugerencia de música/recurso según el contexto"""
        sugerencias = {
            'inicio_pomodoro': {
                'categoria': 'musica_focus',
                'mensaje': '🎵 ¿Te ayudo a concentrarte? Aquí tienes música perfecta para el focus:'
            },
            'descanso_pomodoro': {
                'categoria': 'descanso',
                'mensaje': '☕ Tiempo de relajarte. ¿Qué tal un poco de música suave?'
            },
            'inicio_dia': {
                'categoria': 'musica_energia',
                'mensaje': '⚡ ¡Actívate! Música energética para empezar el día:'
            },
            'objetivo_completado': {
                'categoria': 'musica_energia',
                'mensaje': '🎉 ¡Celebremos! Música motivacional para seguir la racha:'
            }
        }
        
        if contexto in sugerencias:
            info = sugerencias[contexto]
            recurso = self.obtener_recurso_aleatorio(info['categoria'])
            if recurso:
                return {
                    'mensaje': info['mensaje'],
                    'recurso': recurso
                }
        
        return None
    
    def obtener_todas_las_categorias(self):
        """Obtiene todas las categorías de recursos disponibles"""
        categorias = set(self.recursos_default.keys())
        categorias.update(self.recursos_personalizados.keys())
        return list(categorias)
    
    def obtener_recursos_de_categoria(self, categoria):
        """Obtiene todos los recursos de una categoría"""
        recursos = {
            'default': self.recursos_default.get(categoria, []),
            'personalizados': self.recursos_personalizados.get(categoria, [])
        }
        return recursos

# Instancia global
sistema_musica = SistemaMusicaMotivacional()

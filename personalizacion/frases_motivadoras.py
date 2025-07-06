# personalizacion/frases_motivadoras.py - Sistema de frases motivadoras personalizable

import random
import json
import os
from datetime import datetime, time

FRASES_FILE = 'storage/frases_personalizadas.json'

class SistemaFrasesMotivadoras:
    def __init__(self):
        self.frases_default = {
            'inicio_dia': [
                "🌅 ¡Buenos días! Hoy es un gran día para ser productivo",
                "☀️ Cada día es una nueva oportunidad para brillar",
                "🎯 Enfócate en tus objetivos, ¡tú puedes lograrlo!",
                "💪 La disciplina es el puente entre metas y logros",
                "🚀 ¡Despega hacia un día productivo!",
                "⭐ Haz que hoy cuente, el futuro te lo agradecerá"
            ],
            'inicio_pomodoro': [
                "🍅 ¡Es hora de concentrarse! 25 minutos de productividad pura",
                "⏰ Deep focus activated! Deja que la magia suceda",
                "🎯 Enfoque láser activado. ¡A por esos objetivos!",
                "💎 Los diamantes se forman bajo presión. ¡Presiona play!",
                "🔥 Flow state: ON. Distracciones: OFF",
                "⚡ Tu próximo nivel te está esperando. ¡Comencemos!"
            ],
            'descanso': [
                "☕ Momento de recargar energías. ¡Te lo has ganado!",
                "🌱 Los descansos son parte del crecimiento",
                "🧘‍♀️ Respira profundo, estás haciendo un gran trabajo",
                "💆‍♂️ Tu cerebro necesita este descanso para rendir mejor",
                "🎵 Tiempo de relajación. ¡Disfruta estos minutos!",
                "🌈 Cada descanso te acerca más a tus metas"
            ],
            'objetivo_completado': [
                "🎉 ¡OBJETIVO COMPLETADO! Eres imparable",
                "⭐ ¡Increíble! Otro objetivo conquistado",
                "🏆 Champion mindset activated! ¡Sigue así!",
                "💪 Disciplina + Constancia = Éxito garantizado",
                "🎯 Bullseye! Directo al objetivo",
                "🔥 Estás en racha! El éxito llama al éxito"
            ],
            'fin_dia': [
                "🌙 Día completado. Reflexiona sobre tus logros de hoy",
                "✨ Cada día productivo te acerca a tus sueños",
                "🏁 Misión del día cumplida. ¡Descansa y prepárate para mañana!",
                "📈 Progreso constante = Resultados extraordinarios",
                "💫 Hoy plantaste semillas de éxito para el futuro",
                "🎊 ¡Felicidades por otro día de crecimiento!"
            ],
            'motivacion_general': [
                "🌟 El éxito es la suma de pequeños esfuerzos repetidos",
                "⚡ Tu única competencia eres tú mismo de ayer",
                "🎯 Enfócate en el progreso, no en la perfección",
                "💡 Las ideas sin acción quedan en sueños",
                "🔥 La consistencia vence al talento cuando el talento no es consistente",
                "🚀 No esperes la motivación, crea el hábito"
            ]
        }
        self.frases_personalizadas = self.cargar_frases_personalizadas()
    
    def cargar_frases_personalizadas(self):
        """Carga frases personalizadas del usuario"""
        try:
            if os.path.exists(FRASES_FILE):
                with open(FRASES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"❌ Error cargando frases personalizadas: {e}")
            return {}
    
    def guardar_frases_personalizadas(self):
        """Guarda las frases personalizadas en archivo"""
        try:
            os.makedirs(os.path.dirname(FRASES_FILE), exist_ok=True)
            with open(FRASES_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.frases_personalizadas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando frases personalizadas: {e}")
    
    def obtener_frase(self, categoria, personalizada_primero=True):
        """Obtiene una frase aleatoria de la categoría especificada"""
        frases_disponibles = []
        
        # Priorizar frases personalizadas si existe la preferencia
        if personalizada_primero and categoria in self.frases_personalizadas:
            frases_disponibles.extend(self.frases_personalizadas[categoria])
        
        # Agregar frases por defecto
        if categoria in self.frases_default:
            frases_disponibles.extend(self.frases_default[categoria])
        
        # Si no hay frases, devolver una por defecto
        if not frases_disponibles:
            return "🌟 ¡Sigue adelante, estás haciendo un gran trabajo!"
        
        return random.choice(frases_disponibles)
    
    def agregar_frase_personalizada(self, categoria, frase):
        """Agrega una frase personalizada a una categoría"""
        if categoria not in self.frases_personalizadas:
            self.frases_personalizadas[categoria] = []
        
        if frase not in self.frases_personalizadas[categoria]:
            self.frases_personalizadas[categoria].append(frase)
            self.guardar_frases_personalizadas()
            return True
        return False
    
    def eliminar_frase_personalizada(self, categoria, frase):
        """Elimina una frase personalizada"""
        if categoria in self.frases_personalizadas:
            if frase in self.frases_personalizadas[categoria]:
                self.frases_personalizadas[categoria].remove(frase)
                self.guardar_frases_personalizadas()
                return True
        return False
    
    def obtener_todas_las_categorias(self):
        """Obtiene todas las categorías disponibles"""
        categorias = set(self.frases_default.keys())
        categorias.update(self.frases_personalizadas.keys())
        return list(categorias)
    
    def obtener_frases_de_categoria(self, categoria):
        """Obtiene todas las frases de una categoría (default + personalizadas)"""
        frases = {
            'default': self.frases_default.get(categoria, []),
            'personalizadas': self.frases_personalizadas.get(categoria, [])
        }
        return frases
    
    def frase_contextual(self, hora_actual=None):
        """Obtiene una frase apropiada según el contexto temporal"""
        if hora_actual is None:
            hora_actual = datetime.now().time()
        
        # Mañana (6:00-12:00)
        if time(6, 0) <= hora_actual < time(12, 0):
            return self.obtener_frase('inicio_dia')
        
        # Tarde (12:00-18:00)
        elif time(12, 0) <= hora_actual < time(18, 0):
            return self.obtener_frase('motivacion_general')
        
        # Noche (18:00-22:00)
        elif time(18, 0) <= hora_actual < time(22, 0):
            return self.obtener_frase('fin_dia')
        
        # Madrugada (22:00-6:00)
        else:
            return self.obtener_frase('motivacion_general')

# Instancia global
sistema_frases = SistemaFrasesMotivadoras()

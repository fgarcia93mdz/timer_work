# personalizacion/__init__.py - Módulo de personalización

from .frases_motivadoras import sistema_frases
from .musica_motivacional import sistema_musica
from .temas_visuales import sistema_temas
from .ui_personalizacion import abrir_ui_personalizacion

__all__ = [
    'sistema_frases',
    'sistema_musica', 
    'sistema_temas',
    'abrir_ui_personalizacion'
]

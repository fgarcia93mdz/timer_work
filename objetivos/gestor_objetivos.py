# objetivos/gestor_objetivos.py

import json
import os
from datetime import datetime, date
from monitor.logger import registrar_evento
from pomodoro.notificador import NotificadorPomodoro

class GestorObjetivos:
    def __init__(self):
        self.archivo_objetivos = 'storage/objetivos.json'
        self.objetivos_diarios = {}
        self.notificador = NotificadorPomodoro()
        self.cargar_objetivos()
        
    def cargar_objetivos(self):
        """Carga los objetivos desde el archivo JSON"""
        try:
            if os.path.exists(self.archivo_objetivos):
                with open(self.archivo_objetivos, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.objetivos_diarios = data
            else:
                self.objetivos_diarios = {}
                self.guardar_objetivos()
        except Exception as e:
            print(f"Error al cargar objetivos: {e}")
            self.objetivos_diarios = {}
    
    def guardar_objetivos(self):
        """Guarda los objetivos en el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.archivo_objetivos), exist_ok=True)
            with open(self.archivo_objetivos, 'w', encoding='utf-8') as f:
                json.dump(self.objetivos_diarios, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar objetivos: {e}")
    
    def crear_objetivo_diario(self, descripcion, meta_numerica=None, tipo="contador"):
        """Crea un nuevo objetivo para el día actual"""
        fecha_hoy = date.today().isoformat()
        
        if fecha_hoy not in self.objetivos_diarios:
            self.objetivos_diarios[fecha_hoy] = []
        
        objetivo = {
            'id': len(self.objetivos_diarios[fecha_hoy]) + 1,
            'descripcion': descripcion,
            'tipo': tipo,  # 'contador', 'tiempo', 'boolean'
            'meta': meta_numerica or 1,
            'progreso': 0,
            'completado': False,
            'fecha_creacion': datetime.now().isoformat(),
            'fecha_completado': None
        }
        
        self.objetivos_diarios[fecha_hoy].append(objetivo)
        self.guardar_objetivos()
        
        registrar_evento(f"🎯 Nuevo objetivo creado: {descripcion}")
        print(f"✅ Objetivo creado: {descripcion} (Meta: {meta_numerica or 1})")
        
        return objetivo['id']
    
    def avanzar_objetivo(self, objetivo_id, incremento=1):
        """Avanza el progreso de un objetivo"""
        fecha_hoy = date.today().isoformat()
        
        if fecha_hoy not in self.objetivos_diarios:
            print("❌ No hay objetivos para hoy")
            return False
        
        objetivo = self._buscar_objetivo(fecha_hoy, objetivo_id)
        if not objetivo:
            print(f"❌ Objetivo {objetivo_id} no encontrado")
            return False
        
        objetivo['progreso'] += incremento
        
        # Verificar si se completó el objetivo
        if objetivo['progreso'] >= objetivo['meta'] and not objetivo['completado']:
            objetivo['completado'] = True
            objetivo['fecha_completado'] = datetime.now().isoformat()
            
            self.notificador.mostrar_objetivo_completado(objetivo['descripcion'])
            registrar_evento(f"🎯✅ Objetivo completado: {objetivo['descripcion']}")
        else:
            self.notificador.mostrar_progreso_objetivo(
                objetivo['descripcion'], 
                objetivo['progreso'], 
                objetivo['meta']
            )
            registrar_evento(f"🎯📈 Progreso: {objetivo['descripcion']} ({objetivo['progreso']}/{objetivo['meta']})")
        
        self.guardar_objetivos()
        return True
    
    def marcar_objetivo_completado(self, objetivo_id):
        """Marca un objetivo como completado directamente"""
        fecha_hoy = date.today().isoformat()
        
        if fecha_hoy not in self.objetivos_diarios:
            return False
        
        objetivo = self._buscar_objetivo(fecha_hoy, objetivo_id)
        if not objetivo:
            return False
        
        objetivo['completado'] = True
        objetivo['progreso'] = objetivo['meta']
        objetivo['fecha_completado'] = datetime.now().isoformat()
        
        self.notificador.mostrar_objetivo_completado(objetivo['descripcion'])
        registrar_evento(f"🎯✅ Objetivo marcado como completado: {objetivo['descripcion']}")
        
        self.guardar_objetivos()
        return True
    
    def _buscar_objetivo(self, fecha, objetivo_id):
        """Busca un objetivo específico por ID en una fecha"""
        for objetivo in self.objetivos_diarios[fecha]:
            if objetivo['id'] == objetivo_id:
                return objetivo
        return None
    
    def obtener_objetivos_hoy(self):
        """Retorna los objetivos del día actual"""
        fecha_hoy = date.today().isoformat()
        return self.objetivos_diarios.get(fecha_hoy, [])
    
    def obtener_resumen_diario(self, fecha=None):
        """Obtiene un resumen de los objetivos de una fecha específica"""
        if fecha is None:
            fecha = date.today().isoformat()
        
        objetivos = self.objetivos_diarios.get(fecha, [])
        total_objetivos = len(objetivos)
        objetivos_completados = len([obj for obj in objetivos if obj['completado']])
        
        porcentaje_completado = (objetivos_completados / total_objetivos * 100) if total_objetivos > 0 else 0
        
        return {
            'fecha': fecha,
            'total_objetivos': total_objetivos,
            'objetivos_completados': objetivos_completados,
            'porcentaje_completado': porcentaje_completado,
            'objetivos': objetivos
        }
    
    def mostrar_objetivos_hoy(self):
        """Muestra los objetivos del día en consola"""
        objetivos = self.obtener_objetivos_hoy()
        
        if not objetivos:
            print("📝 No hay objetivos para hoy. ¡Crea algunos!")
            return
        
        print("\n🎯 OBJETIVOS DE HOY:")
        print("=" * 40)
        
        for objetivo in objetivos:
            estado = "✅" if objetivo['completado'] else "⏳"
            progreso = f"{objetivo['progreso']}/{objetivo['meta']}"
            porcentaje = int((objetivo['progreso'] / objetivo['meta']) * 100)
            
            print(f"{estado} [{objetivo['id']}] {objetivo['descripcion']}")
            print(f"    Progreso: {progreso} ({porcentaje}%)")
            print()
    
    def eliminar_objetivo(self, objetivo_id):
        """Elimina un objetivo del día actual"""
        fecha_hoy = date.today().isoformat()
        
        if fecha_hoy not in self.objetivos_diarios:
            return False
        
        objetivos = self.objetivos_diarios[fecha_hoy]
        objetivo_eliminar = None
        
        for i, objetivo in enumerate(objetivos):
            if objetivo['id'] == objetivo_id:
                objetivo_eliminar = objetivos.pop(i)
                break
        
        if objetivo_eliminar:
            self.guardar_objetivos()
            registrar_evento(f"🗑️ Objetivo eliminado: {objetivo_eliminar['descripcion']}")
            return True
        
        return False
    
    def detectar_actividad_automatica(self, ventana_activa, proceso_activo):
        """Detecta automáticamente progreso en objetivos basado en la actividad"""
        # Esta función puede expandirse para detectar automáticamente
        # el progreso en objetivos específicos basado en las aplicaciones usadas
        
        aplicaciones_productivas = [
            'whatsapp', 'chrome', 'outlook', 'excel', 'word', 'teams',
            'zoom', 'slack', 'notion', 'trello', 'asana'
        ]
        
        if any(app in proceso_activo.lower() for app in aplicaciones_productivas):
            # Podrías implementar lógica para avanzar automáticamente ciertos objetivos
            pass

def menu_interactivo():
    """Menú interactivo para gestionar objetivos"""
    gestor = GestorObjetivos()
    
    while True:
        print("\n🎯 GESTOR DE OBJETIVOS")
        print("=" * 30)
        print("1. Ver objetivos de hoy")
        print("2. Crear nuevo objetivo")
        print("3. Avanzar objetivo")
        print("4. Marcar como completado")
        print("5. Eliminar objetivo")
        print("6. Resumen del día")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == "1":
            gestor.mostrar_objetivos_hoy()
        
        elif opcion == "2":
            descripcion = input("Descripción del objetivo: ").strip()
            meta = input("Meta numérica (opcional, presiona Enter para 1): ").strip()
            meta = int(meta) if meta.isdigit() else 1
            gestor.crear_objetivo_diario(descripcion, meta)
        
        elif opcion == "3":
            gestor.mostrar_objetivos_hoy()
            objetivo_id = input("ID del objetivo a avanzar: ").strip()
            incremento = input("Incremento (presiona Enter para 1): ").strip()
            
            objetivo_id = int(objetivo_id) if objetivo_id.isdigit() else 0
            incremento = int(incremento) if incremento.isdigit() else 1
            
            gestor.avanzar_objetivo(objetivo_id, incremento)
        
        elif opcion == "4":
            gestor.mostrar_objetivos_hoy()
            objetivo_id = input("ID del objetivo a completar: ").strip()
            objetivo_id = int(objetivo_id) if objetivo_id.isdigit() else 0
            gestor.marcar_objetivo_completado(objetivo_id)
        
        elif opcion == "5":
            gestor.mostrar_objetivos_hoy()
            objetivo_id = input("ID del objetivo a eliminar: ").strip()
            objetivo_id = int(objetivo_id) if objetivo_id.isdigit() else 0
            gestor.eliminar_objetivo(objetivo_id)
        
        elif opcion == "6":
            resumen = gestor.obtener_resumen_diario()
            print(f"\n📊 RESUMEN DEL DÍA ({resumen['fecha']})")
            print(f"Total objetivos: {resumen['total_objetivos']}")
            print(f"Completados: {resumen['objetivos_completados']}")
            print(f"Porcentaje: {resumen['porcentaje_completado']:.1f}%")
        
        elif opcion == "0":
            break
        
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    menu_interactivo()

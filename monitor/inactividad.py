# monitor/inactividad.py

from pynput import mouse, keyboard
import time
from monitor.logger import inicializar_log, registrar_evento

TIEMPO_INACTIVIDAD = 5 * 60
ultima_actividad = time.time()

def reiniciar_timer(x=None):
    global ultima_actividad
    ultima_actividad = time.time()

def esta_inactivo():
    return (time.time() - ultima_actividad) > TIEMPO_INACTIVIDAD

def iniciar_monitoreo_inactividad():
    inicializar_log()

    mouse.Listener(on_move=reiniciar_timer, on_click=reiniciar_timer, on_scroll=reiniciar_timer).start()
    keyboard.Listener(on_press=reiniciar_timer).start()

    print("Monitoreando inactividad...")

    inactivo = False

    while True:
        if not inactivo and esta_inactivo():
            registrar_evento("Usuario INACTIVO")
            inactivo = True
        elif inactivo and not esta_inactivo():
            registrar_evento("Usuario ACTIVO nuevamente")
            inactivo = False
        time.sleep(5)

if __name__ == "__main__":
    iniciar_monitoreo_inactividad()

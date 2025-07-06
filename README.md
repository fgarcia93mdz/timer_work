# 🖥️ Sistema de Monitoreo de Actividad y Productividad

Un sistema completo de monitoreo de actividad con Pomodoro integrado para mejorar la productividad durante el trabajo.

## 🚀 Características Principales

### 1. **Monitoreo en Segundo Plano**
- ⏱️ Registra tiempo activo (mouse/teclado)
- 🪟 Monitorea ventana activa y aplicaciones
- 💤 Detecta períodos de inactividad
- 📊 Guarda estadísticas en base de datos local

### 2. **Pomodoro Timer Integrado**
- 🍅 Ciclos automáticos de 25-5-25-5-15 minutos
- 🔔 Notificaciones del sistema
- ⏸️ Funciones de pausa/reanudación
- 📈 Seguimiento de sesiones completadas

### 3. **Gestión de Objetivos Diarios**
- 🎯 Crear objetivos con metas numéricas
- ✅ Seguimiento de progreso en tiempo real
- 🖥️ Interfaz gráfica minimalista
- 📊 Reportes de cumplimiento

### 4. **Reportes y Estadísticas**
- 📄 Exportación a PDF
- 📈 Resúmenes diarios y semanales
- 💻 Tiempo por aplicación
- 🎯 Análisis de productividad

## 📁 Estructura del Proyecto

```
timer_work/
│
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
│
├── monitor/               # Módulo de monitoreo
│   ├── __init__.py
│   ├── logger.py          # Sistema de logging
│   ├── inactividad.py     # Detector de inactividad
│   └── ventana_activa.py  # Monitor de ventanas activas
│
├── pomodoro/              # Sistema Pomodoro
│   ├── __init__.py
│   ├── temporizador.py    # Lógica del temporizador
│   └── notificador.py     # Sistema de notificaciones
│
├── objetivos/             # Gestión de objetivos
│   ├── __init__.py
│   ├── gestor_objetivos.py # Lógica de objetivos
│   └── ui_minimal.py      # Interfaz gráfica
│
├── storage/               # Almacenamiento de datos
│   ├── __init__.py
│   ├── database.py        # Base de datos SQLite
│   ├── actividad.db       # BD principal (se crea automáticamente)
│   └── objetivos.json     # Respaldo de objetivos
│
└── utils/                 # Utilidades generales
    ├── __init__.py
    ├── export_pdf.py      # Generación de reportes PDF
    └── helpers.py         # Funciones auxiliares
```

## 🛠️ Instalación y Configuración

### 1. **Clonar/Descargar el Proyecto**
```bash
# Si usas git
git clone <url-del-repositorio>
cd timer_work
```

### 2. **Crear Entorno Virtual (Recomendado)**
```powershell
# En PowerShell (Windows)
python -m venv venv
venv\Scripts\activate
```

### 3. **Instalar Dependencias**
```powershell
pip install -r requirements.txt
```

### 4. **Verificar Instalación**
```powershell
python -c "from utils.helpers import validar_configuracion; validar_configuracion()"
```

## 🏃‍♂️ Uso del Sistema

### **Ejecución Principal**
```powershell
python main.py
```

### **Módulos Individuales**

#### Gestión de Objetivos (UI Gráfica)
```powershell
python objetivos/ui_minimal.py
```

#### Gestión de Objetivos (Consola)
```powershell
python objetivos/gestor_objetivos.py
```

#### Solo Monitoreo de Inactividad
```powershell
python monitor/inactividad.py
```

#### Solo Monitoreo de Ventanas
```powershell
python monitor/ventana_activa.py
```

#### Prueba de Notificaciones
```powershell
python pomodoro/notificador.py
```

#### Generar Reportes PDF
```powershell
python utils/export_pdf.py
```

## 📊 Funcionalidades Detalladas

### **Sistema de Monitoreo**
- Detecta movimientos de mouse y teclas presionadas
- Registra la aplicación activa cada 3 segundos
- Marca como "inactivo" después de 5 minutos sin actividad
- Guarda todos los eventos con timestamp en base de datos

### **Pomodoro Timer**
- **25 minutos de trabajo** → **5 minutos de descanso**
- Cada 4 ciclos: **descanso largo de 15 minutos**
- Notificaciones del sistema Windows
- Sonidos de alerta opcionales
- Contador de sesiones completadas

### **Gestión de Objetivos**
- Crear objetivos con descripción y meta numérica
- Avanzar progreso manualmente (+1, +5, etc.)
- Marcar como completado
- Seguimiento de porcentaje de cumplimiento
- Interfaz gráfica intuitiva

### **Reportes y Exportación**
- **PDF diario**: Resumen de actividad, tiempo por app, Pomodoros
- **PDF semanal**: Tendencias y comparativas
- **Base de datos**: Historial completo en SQLite
- **CSV**: Exportación de datos para análisis externo

## ⚙️ Configuración Avanzada

### **Personalizar Tiempos de Pomodoro**
```python
# En main.py, modificar la configuración del PomodoroTimer
pomodoro.configurar_tiempos(
    trabajo=25,        # minutos de trabajo
    descanso_corto=5,  # descanso corto
    descanso_largo=15  # descanso largo
)
```

### **Cambiar Tiempo de Inactividad**
```python
# En monitor/inactividad.py
TIEMPO_INACTIVIDAD = 5 * 60  # 5 minutos en segundos
```

### **Ubicación de Archivos**
- **Logs**: `storage/log_actividad.csv`
- **Base de datos**: `storage/actividad.db`
- **Objetivos**: `storage/objetivos.json`
- **Reportes PDF**: `storage/reporte_*.pdf`

## 🔧 Solución de Problemas

### **Error: "No se puede resolver la importación"**
```powershell
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### **Error: "Permission denied" o problemas de monitoreo**
- Ejecutar PowerShell como Administrador
- Verificar que el antivirus no bloquee el script

### **Error: "No module named..."**
- Verificar que el entorno virtual esté activado
- Verificar que estés en el directorio correcto del proyecto

### **Las notificaciones no funcionan**
```powershell
# Verificar instalación de plyer
pip install --upgrade plyer
```

## 📋 Comandos Útiles

### **Activar entorno virtual**
```powershell
venv\Scripts\activate
```

### **Instalar dependencia individual**
```powershell
pip install pynput pywin32 schedule plyer psutil reportlab
```

### **Verificar estado del sistema**
```powershell
python -c "from utils.helpers import generar_estadisticas_rapidas; generar_estadisticas_rapidas()"
```

### **Limpiar datos antiguos**
```powershell
python -c "from storage.database import limpiar_datos_antiguos; limpiar_datos_antiguos(30)"
```

## 🎯 Casos de Uso Recomendados

### **Para Freelancers**
- Monitorear tiempo por proyecto/cliente
- Generar reportes de horas trabajadas
- Mantener disciplina con Pomodoro

### **Para Estudiantes**
- Controlar tiempo de estudio
- Objetivos de sesiones por materia
- Evitar distracciones digitales

### **Para Equipos de Trabajo**
- Reportes de productividad
- Análisis de herramientas más utilizadas
- Seguimiento de metas diarias

## 🚨 Consideraciones Importantes

- **Privacidad**: Todos los datos se almacenan localmente
- **Rendimiento**: El monitoreo consume mínimos recursos del sistema
- **Compatibilidad**: Diseñado específicamente para Windows
- **Persistencia**: Los datos se mantienen entre reinicios del sistema

# 🖥️ Sistema de Productividad Personal

**Tu compañero inteligente para maximizar la productividad en el trabajo remoto**

Un sistema completo de monitoreo privado y respetuoso que te ayuda a organizar tu jornada laboral, establecer objetivos como en un tablero Scrum personal, y recibir estadísticas motivadoras para mejorar día a día.

## 🎯 **Filosofía del Sistema**

> **No vigilamos, empoderamos.** Este sistema está diseñado para darte autonomía y control total sobre tu productividad, manteniendo tu privacidad al 100%.

## 🚀 Características Principales

### 1. **Monitoreo Inteligente y Respetuoso**
- ⏱️ Registra actividad cada 60 segundos (configurable)
- 🪟 Detecta la ventana activa sin invadir contenido
- 💤 Identifica períodos de inactividad (10+ minutos)
- 📊 Almacena todo localmente en tu computadora
- 🪶 Consume mínimos recursos del sistema

### 2. **Pomodoro Timer Integrado con Pausas Activas**
- 🍅 Ciclos automáticos: 25min trabajo → 5min descanso → 15min descanso largo
- 🔔 Notificaciones suaves que no interrumpen
- ⏸️ Pausa/reanudación cuando lo necesites
- 🖥️ Icono en bandeja del sistema (tray icon)
- 📈 Seguimiento de productividad

### 3. **Objetivos Diarios Estilo Scrum Personal**
- 🎯 Define objetivos específicos al iniciar el día
- ✅ Marca progreso incremental (+1, +5, etc.)
- 📊 Visualización de avance en tiempo real
- 🖥️ Interfaz gráfica minimalista e intuitiva
- 💪 Motivación continua con mensajes personalizados

### 4. **Personalización por Usuario**
- 👤 Configuración inicial con tu nombre/ID personal
- 💾 Datos asociados a tu perfil localmente
- ⚙️ Preferencias guardadas entre sesiones
- 🎨 Mensajes motivadores personalizados

### 5. **Resumen Diario Automático y Motivador**
- 📊 Estadísticas de tiempo activo/inactivo
- 💻 Análisis de aplicaciones más utilizadas
- 🎯 Progreso de objetivos del día
- 🚀 Mensajes motivadores inteligentes basados en tu desempeño
- 📤 Opcional: envío a API externa (POST)
- 💾 Guardado local en JSON y texto legible

### 6. **Personalización Completa 🎨**
- 🎨 **Temas visuales**: 5 temas predefinidos (Productivo, Zen, Energía, Nocturno, Minimalista)
- 💬 **Frases motivadoras**: Sistema personalizable con tus propias frases
- 🎵 **Música y recursos**: Enlaces a YouTube, Spotify, podcasts favoritos
- ⚙️ **Configuración visual**: Colores, fuentes, efectos personalizables
- 🔄 **Cambio dinámico**: Aplica cambios inmediatamente sin reiniciar

### 7. **Mensajes Motivadores Contextuales**
- ✅ Si cumpliste objetivos: *"¡Excelente trabajo hoy, seguilo así! 🚀"*
- 💪 Si estuviste cerca: *"¡Estuviste cerca! Mañana lo lográs 💪"*
- 🌱 Consejos para mejorar día a día
- 🎉 Celebración de logros

## 📁 Estructura del Proyecto

```
timer_work/
│
├── main.py                    # Punto de entrada principal
├── config.py                  # Configuración centralizada
├── setup_inicial.py           # Configuración primer uso
├── build_exe.py              # Generador de ejecutable
├── requirements.txt          # Dependencias
├── README.md                 # Esta documentación
│
├── monitor/                  # Módulo de monitoreo
│   ├── logger.py            # Sistema de logging avanzado
│   ├── inactividad.py       # Detector de inactividad  
│   └── ventana_activa.py    # Monitor de ventanas (60s)
│
├── pomodoro/                # Sistema Pomodoro
│   ├── temporizador.py      # Temporizador inteligente
│   └── notificador.py       # Notificaciones Windows
│
├── objetivos/               # Gestión de objetivos
│   ├── gestor_objetivos.py  # Lógica de objetivos
│   └── ui_minimal.py        # Interfaz gráfica
│
├── personalizacion/           # Sistema de personalización
│   ├── frases_motivadoras.py  # Frases personalizables
│   ├── musica_motivacional.py # Enlaces de música/recursos
│   ├── temas_visuales.py      # Temas y colores
│   └── ui_personalizacion.py  # Interfaz de personalización
│
├── interfaz/                # Interfaz de usuario
│   └── tray_icon.py         # Icono en bandeja del sistema
│
├── reportes/                # Sistema de reportes
│   └── resumen_diario.py    # Generador de resúmenes
│
├── storage/                 # Almacenamiento de datos
│   ├── database.py          # Base de datos SQLite
│   ├── config.json          # Configuración usuario
│   ├── actividad.db         # BD principal
│   └── resumenes/           # Reportes diarios
│
└── utils/                   # Utilidades generales
    ├── export_pdf.py        # Generación PDF
    └── helpers.py           # Funciones auxiliares
```

## 🛠️ Instalación Paso a Paso (Para Principiantes)

### **Opción 1: Instalación Automática (Recomendada)**

1. **Descargar Python** (si no lo tienes):
   - Ve a https://python.org/downloads
   - Descarga Python 3.8 o superior
   - **IMPORTANTE**: Marca "Add Python to PATH" durante la instalación

2. **Descargar el proyecto**:
   - Descarga todos los archivos en una carpeta
   - Ejemplo: `C:\ProductividadPersonal`

3. **Ejecutar instalación automática**:
   ```powershell
   # Abrir PowerShell en la carpeta del proyecto
   python setup.py
   ```
   
   La instalación automática:
   - ✅ Verifica Python
   - ✅ Crea entorno virtual
   - ✅ Instala dependencias
   - ✅ Verifica funcionamiento
   - ✅ Crea script de ejecución

### **Opción 2: Instalación Manual**

1. **Crear entorno virtual**:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Verificar instalación**:
   ```powershell
   python -c "from utils.helpers import validar_configuracion; validar_configuracion()"
   ```

## 🏃‍♂️ Cómo Usar el Sistema

### **🚀 Primera Ejecución**

1. **Ejecutar el sistema**:
   ```powershell
   # Método rápido
   iniciar_sistema.bat
   
   # O manualmente
   venv\Scripts\activate
   python main.py
   ```

2. **Configuración inicial**:
   - Se abrirá una ventana de bienvenida
   - Ingresa tu nombre (ejemplo: "María", "Juan", "Ana")
   - Configura preferencias:
     - ✅ Notificaciones Pomodoro
     - ✅ Sonidos de alerta
     - ✅ Inicio automático con Windows
   - Confirma configuración

3. **Definir objetivos del día**:
   - El sistema te preguntará si quieres definir objetivos
   - Ejemplos de objetivos:
     - "Contactar 10 clientes"
     - "Completar 3 tareas del proyecto X"
     - "Estudiar 2 horas de Python"
     - "Escribir 5 páginas del informe"

### **📊 Uso Diario**

El sistema funciona **completamente en segundo plano**:

1. **Monitoreo automático**:
   - Detecta tu actividad cada 60 segundos
   - Registra la aplicación que estás usando
   - Identifica períodos de inactividad
   - Todo se guarda localmente

2. **Pomodoro Timer**:
   - Se inicia automáticamente
   - Te notifica cuando completar 25 minutos de trabajo
   - Te recuerda tomar descansos de 5 minutos
   - Cada 4 ciclos: descanso largo de 15 minutos

3. **Gestión de objetivos**:
   - Haz clic derecho en el icono de la bandeja
   - Selecciona "Gestionar Objetivos"
   - Marca progreso cuando completes tareas
   - Ve tu avance en tiempo real

4. **Icono en bandeja del sistema**:
   - Aparece en la esquina inferior derecha
   - Clic derecho para ver todas las opciones
   - Muestra el estado actual del sistema

### **🌙 Final del Día**

Al terminar tu jornada (o presionar Ctrl+C):

1. **Resumen automático**:
   - Se genera un análisis completo del día
   - Muestra tiempo activo, aplicaciones usadas, objetivos cumplidos
   - Presenta mensaje motivador personalizado

2. **Ejemplo de mensaje motivador**:
   ```
   📊 RESUMEN DE TU DÍA, MARÍA:
   
   🎉 ¡Increíble, María! Completaste todos tus objetivos del día. ¡Eres imparable!
   
   🍅 6 Pomodoros completados! Tu concentración fue excepcional.
   
   ⏰ 7.2 horas de actividad. ¡Día muy productivo!
   
   🌅 Mañana define tus objetivos apenas comiences el día.
   
   ¡Que descanses bien! Mañana será un gran día 🌙✨
   ```

## 🖥️ Generar Ejecutable (Sin Python)

Para compartir con otros o usar sin Python instalado:

### **1. Instalar PyInstaller**:
```powershell
pip install pyinstaller
```

### **2. Generar ejecutable**:
```powershell
python build_exe.py
```

### **3. Resultado**:
- 📂 Carpeta `ProductividadPersonal_Distribucion`
- 🚀 Archivo `ProductividadPersonal.exe` (ejecutable independiente)
- 📋 Archivo `INSTRUCCIONES.txt`
- ✅ **No requiere Python instalado**
- ✅ **Funciona en cualquier PC Windows**

### **4. Distribución**:
- Comparte toda la carpeta `ProductividadPersonal_Distribucion`
- El usuario solo ejecuta `ProductividadPersonal.exe`
- Primera ejecución muestra configuración inicial

## 🖱️ Inicio Automático con Windows

### **Método 1: Durante configuración inicial**
- Marca la casilla "Iniciar automáticamente con Windows"
- El sistema se configura automáticamente

### **Método 2: Acceso directo manual**
1. Crear acceso directo a `ProductividadPersonal.exe`
2. Copiar el acceso directo
3. Presionar `Win + R`, escribir `shell:startup`
4. Pegar el acceso directo en esa carpeta

### **Método 3: Script Python**
```powershell
# Ubicar carpeta de inicio
shell:startup

# Crear archivo .bat con:
@echo off
cd "C:\ruta\a\tu\proyecto"
venv\Scripts\python.exe main.py
```

## 📊 Funcionalidades Detalladas

### **Sistema de Monitoreo No Invasivo**
- ✅ Solo registra el nombre de la aplicación activa
- ✅ NO lee contenido de pantalla ni teclas presionadas
- ✅ NO toma capturas de pantalla
- ✅ NO accede a archivos personales
- ✅ Consume menos del 1% de CPU
- ✅ Usa menos de 50MB de RAM

### **Pomodoro Inteligente**
- 🎯 **25 minutos de trabajo enfocado**
- ☕ **5 minutos de descanso activo**
- 🌴 **15 minutos de descanso largo cada 4 ciclos**
- ⏸️ **Pausa cuando necesites** (reuniones, llamadas)
- 🔊 **Sonidos opcionales** (se pueden desactivar)
- 📊 **Estadísticas de concentración**

### **Gestión de Objetivos Como Scrum Personal**
- 📝 **Objetivos específicos y medibles**
- 📈 **Progreso incremental** (+1, +2, +5, etc.)
- 🎯 **Metas numéricas** (contactar 10 clientes, escribir 5 páginas)
- ✅ **Completado manual** o automático
- 📊 **Visualización de avance** (barras de progreso)
- 🏆 **Celebración de logros**

### **Reportes y Mensajes Motivadores**
- 📊 **Métricas de productividad**:
  - Tiempo activo vs inactivo
  - Aplicaciones más utilizadas
  - Sesiones Pomodoro completadas
  - Porcentaje de objetivos cumplidos

- 💬 **Mensajes adaptativos**:
  - Si cumples 100%: "¡Eres imparable! 🚀"
  - Si cumples 80%: "¡Casi perfecto! 💪"
  - Si cumples 50%: "Buen trabajo, mañana al 100% 👍"
  - Si cumples menos: "Mañana es tu oportunidad ✨"

- 🎯 **Consejos personalizados**:
  - Mejores horarios de productividad
  - Sugerencias de aplicaciones
  - Recomendaciones de descanso

## ⚙️ Configuración Avanzada

### **Personalizar Intervalos de Monitoreo**
```python
# En config.py, sección 'monitoreo'
'intervalo_ventana_segundos': 60,  # Cambiar a 30, 120, etc.
'tiempo_inactividad_minutos': 10,  # Cambiar umbral inactividad
```

### **Personalizar Tiempos Pomodoro**
```python
# En config.py, sección 'pomodoro'  
'tiempo_trabajo_minutos': 25,        # Trabajo
'tiempo_descanso_corto_minutos': 5,  # Descanso corto
'tiempo_descanso_largo_minutos': 15, # Descanso largo
```

### **Configurar Envío a API Externa**
```python
# En config.py, sección 'reportes'
'enviar_a_api': True,
'url_api': 'https://tu-servidor.com/api/productividad'
```

### **Ubicación de Archivos de Datos**
- **Configuración**: `storage/config.json`
- **Base de datos**: `storage/actividad.db`
- **Logs CSV**: `storage/log_actividad.csv`
- **Objetivos**: `storage/objetivos.json`
- **Resúmenes**: `storage/resumenes/`

## 🔧 Solución de Problemas

### **"No se puede resolver la importación"**
```powershell
# Reinstalar dependencias
pip install --upgrade -r requirements.txt

# O instalar individualmente
pip install pynput pywin32 schedule plyer psutil reportlab pystray Pillow requests
```

### **"Permission denied" o problemas de monitoreo**
- ✅ Ejecutar PowerShell como Administrador
- ✅ Verificar que antivirus no bloquee el script
- ✅ Agregar carpeta del proyecto a exclusiones del antivirus

### **"Las notificaciones no funcionan"**
```powershell
# Verificar plyer
pip install --upgrade plyer

# Verificar notificaciones de Windows
# Configuración → Sistema → Notificaciones → Activar
```

### **"El ejecutable es muy grande"**
- Es normal: PyInstaller incluye Python completo
- Tamaño típico: 50-80 MB
- Es independiente: no requiere instalaciones

### **"Error al crear icono de bandeja"**
```powershell
# Instalar dependencias para tray
pip install pystray Pillow
```

## 📋 Comandos Útiles

### **Activar entorno virtual**
```powershell
venv\Scripts\activate
```

### **Verificar estado del sistema**
```powershell
python -c "from utils.helpers import generar_estadisticas_rapidas; generar_estadisticas_rapidas()"
```

### **Limpiar datos antiguos (30 días)**
```powershell
python -c "from storage.database import limpiar_datos_antiguos; limpiar_datos_antiguos(30)"
```

### **Ver resumen del día**
```powershell
python -c "from reportes.resumen_diario import ResumenDiario; r = ResumenDiario(); r.procesar_resumen_diario()"
```

### **Solo gestionar objetivos**
```powershell
python objetivos/ui_minimal.py
```

### **Probar notificaciones**
```powershell
python pomodoro/notificador.py
```

## 🎯 Casos de Uso Recomendados

### **Para Freelancers y Consultores**
- 📊 Monitorear tiempo por proyecto/cliente
- 📄 Generar reportes de horas trabajadas
- 🎯 Objetivos: "Facturar $2000 esta semana"
- 💼 Mantener disciplina con Pomodoro
- 📈 Analizar patrones de productividad

### **Para Estudiantes**
- ⏰ Controlar tiempo de estudio por materia
- 🎯 Objetivos: "Estudiar 3 horas de Matemáticas"
- 📱 Evitar distracciones digitales
- 🍅 Usar Pomodoro para mantener concentración
- 📊 Reportes de progreso académico

### **Para Trabajadores Remotos**
- 🏠 Estructurar la jornada en casa
- 🎯 Objetivos diarios claros
- ⏰ Respetar horarios de trabajo
- 📊 Reportes para supervisores (opcional)
- 💪 Mantener motivación con mensajes personalizados

### **Para Equipos de Trabajo**
- 📈 Análisis de productividad grupal
- 🛠️ Identificar herramientas más efectivas
- 🎯 Seguimiento de metas colaborativas
- 📊 Comparación de métricas (anonimizadas)
- 💡 Mejores prácticas compartidas

## 🚨 Consideraciones de Privacidad y Seguridad

### **🔒 Garantías de Privacidad**
- ✅ **100% Local**: Todos los datos en tu computadora
- ✅ **Sin conexión**: Funciona completamente offline
- ✅ **No invasivo**: Solo nombres de aplicaciones, no contenido
- ✅ **No screenshots**: Jamás captura pantalla
- ✅ **No keylogger**: No registra teclas presionadas
- ✅ **Tu control**: Puedes ver y borrar todos los datos

### **📁 ¿Qué datos se guardan?**
- ⏰ Timestamps de actividad e inactividad
- 🪟 Nombres de aplicaciones activas (ej: "Chrome", "Word")
- 🎯 Objetivos que TÚ defines
- 🍅 Sesiones Pomodoro completadas
- 📊 Estadísticas agregadas de productividad

### **❌ ¿Qué NO se guarda?**
- ❌ Contenido de archivos
- ❌ Capturas de pantalla
- ❌ Teclas presionadas
- ❌ URLs visitadas
- ❌ Texto escrito
- ❌ Información personal sensible

### **🌐 Comunicación Externa (Opcional)**
- El envío a API es **completamente opcional**
- Solo se envía si TÚ lo activas en configuración
- Puedes revisar exactamente qué se envía
- Se puede desactivar en cualquier momento

## 🔄 Actualizaciones y Roadmap

### **✅ Funcionalidades Actuales**
- [x] Monitoreo no invasivo cada 60 segundos
- [x] Pomodoro Timer completo con notificaciones
- [x] Gestión de objetivos con UI gráfica
- [x] Icono en bandeja del sistema (tray)
- [x] Mensajes motivadores personalizados
- [x] Resúmenes diarios automáticos
- [x] Configuración de primer uso
- [x] Generación de ejecutable independiente
- [x] Base de datos local SQLite
- [x] Reportes en PDF

### **🚧 Próximas Actualizaciones**
- [ ] Dashboard web local (HTML)
- [ ] Integración con calendarios (Google/Outlook)
- [ ] Detección automática de objetivos por actividad
- [ ] Modo "Focus" con bloqueo de aplicaciones
- [ ] Métricas avanzadas de productividad
- [ ] Sync opcional con servicios en la nube
- [ ] Plantillas de objetivos por profesión
- [ ] Análisis de patrones de productividad con IA

### **💡 Ideas para Contribuir**
- 🎨 Temas visuales personalizables
- 🌍 Soporte para otros idiomas
- 📱 Versión móvil complementaria
- 🔊 Más opciones de sonidos/alertas
- 📊 Gráficos interactivos de productividad

## 💬 Ejemplos de Mensajes Motivadores

### **Cuando cumples todos los objetivos:**
```
🎉 ¡Increíble, [Nombre]! Completaste todos tus objetivos del día. ¡Eres imparable!

🍅 8 Pomodoros completados! Tu concentración fue excepcional.

⏰ 8.3 horas de actividad. ¡Día muy productivo!

🌅 Mañana define tus objetivos apenas comiences el día.

¡Que descanses bien! Mañana será un gran día 🌙✨
```

### **Cuando completaste parcialmente:**
```
💪 Muy bien, [Nombre]! Casi todos los objetivos completados (80%). ¡Estás en gran forma!

🍅 5 Pomodoros realizados. ¡Buena disciplina de trabajo!

⏰ 6.8 horas de actividad. ¡Sólido día de trabajo!

📋 Para mañana, prueba dividir tareas grandes en objetivos más pequeños.

¡Mañana puedes llegar al 100%! 💪
```

### **Cuando fue un día difícil:**
```
🌱 [Nombre], fue un día para aprender. Mañana es una nueva oportunidad para brillar ✨

🍅 2 Pomodoros completados. ¡Cada sesión cuenta!

⏰ 4.2 horas de actividad. Considera períodos más largos de concentración.

⚡ Considera usar más el Pomodoro Timer mañana para mantener el foco.

No te desanimes, ¡mañana será mejor! 🌟
```

## 🤝 Soporte y Ayuda

### **🆘 Si algo no funciona:**
1. **Revisa la configuración**: Abre `storage/config.json`
2. **Reinstala dependencias**: `pip install -r requirements.txt`
3. **Limpia datos temporales**: Borra carpetas `build` y `dist`
4. **Ejecuta como administrador**: Clic derecho → "Ejecutar como administrador"

### **📞 Funciones de ayuda rápida:**
- **Estado del sistema**: Clic derecho en icono de bandeja → "Estado"
- **Ayuda integrada**: Clic derecho en icono → "Ayuda"
- **Configuración**: Clic derecho en icono → "Configuración"

### **📁 Archivos importantes para soporte:**
- `storage/log_actividad.csv` - Log de eventos
- `storage/config.json` - Configuración
- `storage/actividad.db` - Base de datos

---

## 🌟 **¡Desarrollado para maximizar tu productividad de forma respetuosa y privada!**

**Este sistema te acompaña, no te vigila. Te motiva, no te presiona. Te empodera, no te controla.**

### 💪 **Tu productividad, tu privacidad, tu control.**

---

*Versión: 2.0 | Última actualización: Julio 2025 | Licencia: Uso Personal*

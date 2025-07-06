# setup.py - Script de instalación y configuración automática

import os
import sys
import subprocess
import platform

def verificar_python():
    """Verifica que Python esté correctamente instalado"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def verificar_sistema():
    """Verifica que el sistema operativo sea compatible"""
    sistema = platform.system()
    if sistema != "Windows":
        print(f"⚠️  Advertencia: Este sistema está optimizado para Windows")
        print(f"   Sistema detectado: {sistema}")
        return False
    
    print(f"✅ Sistema operativo compatible: {sistema}")
    return True

def crear_entorno_virtual():
    """Crea un entorno virtual si no existe"""
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print("✅ Entorno virtual ya existe")
        return True
    
    try:
        print("🔧 Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print("✅ Entorno virtual creado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear entorno virtual: {e}")
        return False

def instalar_dependencias():
    """Instala las dependencias del proyecto"""
    # Determinar el ejecutable de pip según el sistema
    if platform.system() == "Windows":
        pip_executable = "venv\\Scripts\\pip.exe"
        python_executable = "venv\\Scripts\\python.exe"
    else:
        pip_executable = "venv/bin/pip"
        python_executable = "venv/bin/python"
    
    if not os.path.exists(pip_executable):
        print("❌ No se encontró pip en el entorno virtual")
        return False
    
    try:
        print("📦 Instalando dependencias...")
        subprocess.run([pip_executable, "install", "--upgrade", "pip"], check=True)
        subprocess.run([pip_executable, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def crear_directorios():
    """Crea los directorios necesarios para el funcionamiento"""
    directorios = [
        "storage",
        "storage/logs",
        "storage/backups"
    ]
    
    for directorio in directorios:
        try:
            os.makedirs(directorio, exist_ok=True)
            print(f"📁 Directorio creado/verificado: {directorio}")
        except Exception as e:
            print(f"❌ Error al crear directorio {directorio}: {e}")
            return False
    
    return True

def verificar_instalacion():
    """Verifica que todo esté correctamente instalado"""
    # Determinar el ejecutable de python según el sistema
    if platform.system() == "Windows":
        python_executable = "venv\\Scripts\\python.exe"
    else:
        python_executable = "venv/bin/python"
    
    try:
        print("🧪 Verificando instalación...")
        
        # Probar importaciones críticas
        test_script = '''
try:
    import pynput
    import win32gui
    import schedule
    import plyer
    import psutil
    import reportlab
    import sqlite3
    print("✅ Todas las dependencias se importaron correctamente")
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    exit(1)
'''
        
        result = subprocess.run([python_executable, "-c", test_script], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print(result.stderr.strip())
            return False
            
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def crear_script_ejecucion():
    """Crea un script para facilitar la ejecución"""
    script_content = '''@echo off
echo 🚀 Iniciando Sistema de Monitoreo de Actividad...
cd /d "%~dp0"
venv\\Scripts\\python.exe main.py
pause
'''
    
    try:
        with open("iniciar_sistema.bat", "w", encoding="utf-8") as f:
            f.write(script_content)
        print("✅ Script de ejecución creado: iniciar_sistema.bat")
        return True
    except Exception as e:
        print(f"❌ Error al crear script de ejecución: {e}")
        return False

def mostrar_instrucciones():
    """Muestra las instrucciones finales de uso"""
    print("\n" + "="*60)
    print("🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    print("="*60)
    print("\n📋 FORMAS DE EJECUTAR EL SISTEMA:")
    print("\n1. 💻 MÉTODO RÁPIDO (recomendado):")
    print("   - Hacer doble clic en: iniciar_sistema.bat")
    print("\n2. 🔧 MÉTODO MANUAL:")
    print("   - Abrir PowerShell en esta carpeta")
    print("   - Ejecutar: venv\\Scripts\\activate")
    print("   - Ejecutar: python main.py")
    print("\n3. 🎯 SOLO OBJETIVOS (interfaz gráfica):")
    print("   - venv\\Scripts\\activate")
    print("   - python objetivos/ui_minimal.py")
    print("\n📊 ARCHIVOS IMPORTANTES:")
    print("   - Logs: storage/log_actividad.csv")
    print("   - Base de datos: storage/actividad.db")
    print("   - Reportes: storage/reporte_*.pdf")
    print("\n🔧 PARA DESACTIVAR EL ENTORNO VIRTUAL:")
    print("   - En PowerShell: deactivate")
    print("\n💡 CONSEJO:")
    print("   El sistema funciona en segundo plano.")
    print("   Usa Ctrl+C para detenerlo cuando sea necesario.")
    print("\n🆘 SOPORTE:")
    print("   Si hay problemas, revisar el archivo README.md")
    print("\n" + "="*60)

def main():
    """Función principal de instalación"""
    print("🔧 INSTALADOR DEL SISTEMA DE MONITOREO DE ACTIVIDAD")
    print("="*55)
    
    # Verificaciones previas
    if not verificar_python():
        sys.exit(1)
    
    if not verificar_sistema():
        respuesta = input("\n⚠️  ¿Continuar de todos modos? (s/N): ").lower()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Instalación cancelada")
            sys.exit(1)
    
    print("\n🚀 Iniciando proceso de instalación...")
    
    # Proceso de instalación
    pasos = [
        ("Crear entorno virtual", crear_entorno_virtual),
        ("Instalar dependencias", instalar_dependencias),
        ("Crear directorios", crear_directorios),
        ("Verificar instalación", verificar_instalacion),
        ("Crear script de ejecución", crear_script_ejecucion)
    ]
    
    for paso_nombre, paso_funcion in pasos:
        print(f"\n📋 {paso_nombre}...")
        if not paso_funcion():
            print(f"\n❌ Error en: {paso_nombre}")
            print("🛑 Instalación abortada")
            sys.exit(1)
    
    # Mostrar instrucciones finales
    mostrar_instrucciones()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Instalación interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado durante la instalación: {e}")
        sys.exit(1)

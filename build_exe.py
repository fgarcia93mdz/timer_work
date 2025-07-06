# build_exe.py - Script para generar ejecutable con PyInstaller

import os
import sys
import subprocess
import shutil
from pathlib import Path

def verificar_pyinstaller():
    """Verifica si PyInstaller está instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller no está instalado")
        print("💡 Instálalo con: pip install pyinstaller")
        return False

def limpiar_build_anterior():
    """Limpia archivos de compilaciones anteriores"""
    directorios_limpiar = ['build', 'dist', '__pycache__']
    archivos_limpiar = ['*.spec']
    
    for directorio in directorios_limpiar:
        if os.path.exists(directorio):
            try:
                shutil.rmtree(directorio)
                print(f"🗑️ Eliminado directorio: {directorio}")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {directorio}: {e}")
    
    # Buscar archivos .spec
    for archivo_spec in Path('.').glob('*.spec'):
        try:
            archivo_spec.unlink()
            print(f"🗑️ Eliminado archivo: {archivo_spec}")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar {archivo_spec}: {e}")

def crear_icono():
    """Crea un icono personalizado mejorado para el ejecutable"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Crear icono con mejor diseño
        size = 256
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Fondo circular con gradiente simulado
        centro = size // 2
        radio = size // 2 - 10
        
        # Crear círculo principal (color verde productividad)
        draw.ellipse([centro-radio, centro-radio, centro+radio, centro+radio], 
                    fill='#4CAF50', outline='#2E7D32', width=4)
        
        # Agregar círculo interno para profundidad
        radio_interno = radio - 20
        draw.ellipse([centro-radio_interno, centro-radio_interno, 
                     centro+radio_interno, centro+radio_interno], 
                    fill='#66BB6A', outline='#4CAF50', width=2)
        
        # Dibujar símbolo "P" estilizado
        try:
            # Intentar usar fuente del sistema
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Usar fuente por defecto si no encuentra arial
            font = ImageFont.load_default()
        
        # Calcular posición centrada para la P
        text = "P"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = centro - text_width // 2
        text_y = centro - text_height // 2
        
        # Dibujar sombra del texto
        draw.text((text_x + 2, text_y + 2), text, font=font, fill='#1B5E20')
        # Dibujar texto principal
        draw.text((text_x, text_y), text, font=font, fill='white')
        
        # Agregar pequeños elementos decorativos (puntos)
        for i, angle in enumerate([45, 135, 225, 315]):
            import math
            x = centro + (radio - 30) * math.cos(math.radians(angle))
            y = centro + (radio - 30) * math.sin(math.radians(angle))
            draw.ellipse([x-6, y-6, x+6, y+6], fill='#81C784', outline='#4CAF50')
        
        # Guardar como ICO
        icono_path = 'productividad_icon.ico'
        # Crear múltiples tamaños para el ICO
        tamaños = [16, 32, 48, 64, 128, 256]
        iconos = []
        
        for tamaño in tamaños:
            icono_redimensionado = image.resize((tamaño, tamaño), Image.Resampling.LANCZOS)
            iconos.append(icono_redimensionado)
        
        # Guardar archivo ICO con múltiples tamaños
        iconos[0].save(icono_path, format='ICO', sizes=[(img.width, img.height) for img in iconos])
        
        print(f"✅ Icono creado: {icono_path}")
        return icono_path
        
    except Exception as e:
        print(f"⚠️ No se pudo crear icono personalizado: {e}")
        print("📝 Se usará icono por defecto")
        return None
        
        # Dibujar círculo verde
        margin = size // 8
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill='#4CAF50', outline='#2E7D32', width=8)
        
        # Dibujar "P" de productividad
        font_size = size // 3
        text_bbox = draw.textbbox((0, 0), "P")
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), "P", fill='white', anchor='mm')
        
        # Guardar como ICO
        image.save('app_icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print("✅ Icono creado: app_icon.ico")
        return True
        
    except Exception as e:
        print(f"⚠️ No se pudo crear icono: {e}")
        return False

def compilar_ejecutable():
    """Compila la aplicación usando PyInstaller"""
    try:
        print("🔧 Iniciando compilación con PyInstaller...")
        
        # Comando PyInstaller
        comando = [
            'pyinstaller',
            '--onefile',                    # Un solo archivo ejecutable
            '--windowed',                   # Sin ventana de consola
            '--name=ProductividadPersonal', # Nombre del ejecutable
            '--add-data=storage;storage',   # Incluir carpeta storage
            '--add-data=README.md;.',       # Incluir README
            '--hidden-import=pystray._win32',  # Importación necesaria para tray
            '--hidden-import=plyer.platforms.win.notification',  # Para notificaciones
            '--hidden-import=win32gui',     # Para monitoreo de ventanas
            '--hidden-import=win32api',     # APIs de Windows
            '--distpath=dist',              # Carpeta de salida
            'main.py'                       # Archivo principal
        ]
        
        # Agregar icono si existe
        if os.path.exists('app_icon.ico'):
            comando.extend(['--icon=app_icon.ico'])
        
        # Ejecutar PyInstaller
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print("✅ Compilación exitosa!")
            return True
        else:
            print("❌ Error en la compilación:")
            print(resultado.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error durante la compilación: {e}")
        return False

def crear_carpeta_distribucion():
    """Crea una carpeta de distribución con todos los archivos necesarios"""
    try:
        print("📦 Creando paquete de distribución...")
        
        # Crear carpeta de distribución
        dist_folder = "ProductividadPersonal_Distribucion"
        if os.path.exists(dist_folder):
            shutil.rmtree(dist_folder)
        
        os.makedirs(dist_folder)
        
        # Copiar ejecutable
        exe_path = "dist/ProductividadPersonal.exe"
        if os.path.exists(exe_path):
            shutil.copy2(exe_path, dist_folder)
            print("✅ Ejecutable copiado")
        else:
            print("❌ No se encontró el ejecutable")
            return False
        
        # Copiar archivos importantes
        archivos_incluir = [
            "README.md",
            "requirements.txt"
        ]
        
        for archivo in archivos_incluir:
            if os.path.exists(archivo):
                shutil.copy2(archivo, dist_folder)
                print(f"✅ {archivo} copiado")
        
        # Crear carpetas necesarias
        carpetas_crear = [
            "storage",
            "storage/logs", 
            "storage/backups",
            "storage/resumenes"
        ]
        
        for carpeta in carpetas_crear:
            carpeta_completa = os.path.join(dist_folder, carpeta)
            os.makedirs(carpeta_completa, exist_ok=True)
            
            # Crear archivo .gitkeep para mantener las carpetas
            gitkeep_path = os.path.join(carpeta_completa, ".gitkeep")
            with open(gitkeep_path, 'w') as f:
                f.write("# Carpeta necesaria para el funcionamiento del sistema\n")
        
        # Crear archivo de instrucciones
        instrucciones = f"""
🚀 SISTEMA DE PRODUCTIVIDAD PERSONAL
====================================

📋 INSTRUCCIONES DE USO:

1. PRIMERA EJECUCIÓN:
   • Ejecuta ProductividadPersonal.exe
   • Completa la configuración inicial
   • Define tu nombre y preferencias

2. USO DIARIO:
   • El sistema se ejecuta en segundo plano
   • Aparecerá un icono en la bandeja del sistema (esquina inferior derecha)
   • Haz clic derecho en el icono para ver las opciones

3. FUNCIONES PRINCIPALES:
   • 📊 Monitoreo automático de actividad
   • 🍅 Temporizador Pomodoro integrado
   • 🎯 Gestión de objetivos diarios
   • 📈 Reportes de productividad

4. ARCHIVOS DEL SISTEMA:
   • Los datos se guardan en la carpeta 'storage'
   • Tus datos son completamente privados y locales
   • No se envía información a internet

5. INICIO AUTOMÁTICO:
   • En la configuración inicial puedes activar el inicio con Windows
   • También puedes crear un acceso directo en la carpeta de inicio

📞 SOPORTE:
   Para más información, consulta el archivo README.md

🔒 PRIVACIDAD:
   Todos los datos se almacenan ÚNICAMENTE en tu computadora.
   El sistema respeta completamente tu privacidad.

¡Que tengas días productivos! 🌟
        """.strip()
        
        with open(os.path.join(dist_folder, "INSTRUCCIONES.txt"), 'w', encoding='utf-8') as f:
            f.write(instrucciones)
        
        print(f"✅ Paquete de distribución creado en: {dist_folder}")
        print(f"📂 Tamaño del ejecutable: {os.path.getsize(exe_path) // (1024*1024)} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear distribución: {e}")
        return False

def main():
    """Función principal para generar el ejecutable"""
    print("🔧 GENERADOR DE EJECUTABLE")
    print("=" * 40)
    
    # Verificaciones previas
    if not verificar_pyinstaller():
        print("\n💡 Para instalar PyInstaller:")
        print("   pip install pyinstaller")
        return False
    
    # Limpiar archivos anteriores
    print("\n🧹 Limpiando archivos anteriores...")
    limpiar_build_anterior()
    
    # Crear icono
    print("\n🎨 Creando icono...")
    crear_icono()
    
    # Compilar
    print("\n⚙️ Compilando aplicación...")
    if not compilar_ejecutable():
        print("❌ La compilación falló")
        return False
    
    # Crear distribución
    print("\n📦 Creando paquete final...")
    if not crear_carpeta_distribucion():
        print("❌ No se pudo crear el paquete de distribución")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ¡EJECUTABLE GENERADO EXITOSAMENTE!")
    print("=" * 60)
    print("\n📂 Archivos generados:")
    print("   • ProductividadPersonal_Distribucion/ (carpeta completa)")
    print("   • ProductividadPersonal_Distribucion/ProductividadPersonal.exe")
    print("   • ProductividadPersonal_Distribucion/INSTRUCCIONES.txt")
    print("\n💡 Instrucciones:")
    print("   1. Comparte la carpeta 'ProductividadPersonal_Distribucion'")
    print("   2. El usuario solo necesita ejecutar ProductividadPersonal.exe")
    print("   3. No requiere instalación de Python ni dependencias")
    print("\n✅ El ejecutable es completamente independiente")
    print("🔒 Funciona sin conexión a internet")
    print("💾 Todos los datos se guardan localmente")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Generación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        
    input("\nPresiona Enter para salir...")

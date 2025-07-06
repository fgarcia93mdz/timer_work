@echo off
title Sistema de Productividad Personal
echo.
echo ========================================
echo  SISTEMA DE PRODUCTIVIDAD PERSONAL
echo ========================================
echo.
echo 🚀 Iniciando tu compañero de productividad...
echo.

cd /d "%~dp0"

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\python.exe" (
    echo ❌ Entorno virtual no encontrado.
    echo.
    echo 💡 Ejecuta primero: python setup.py
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual y ejecutar
echo ✅ Activando entorno virtual...
call venv\Scripts\activate.bat

echo ✅ Iniciando sistema...
echo.
echo 💡 TIP: Busca el icono en la bandeja del sistema
echo    (esquina inferior derecha de la pantalla)
echo.

python main.py

echo.
echo 👋 ¡Hasta luego! Sistema detenido.
pause

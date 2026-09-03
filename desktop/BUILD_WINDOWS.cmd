@echo off
setlocal
cd /d "%~dp0"
title Construir Fiscalizacion L26 para Windows

echo ============================================================
echo   FISCALIZACION L26 - CONSTRUCCION WINDOWS
echo ============================================================
echo.

where node >nul 2>nul
if errorlevel 1 (
  echo ERROR: Node.js no esta instalado en este equipo.
  echo Instale Node.js LTS y vuelva a ejecutar este archivo.
  pause
  exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
  echo ERROR: npm no esta disponible.
  pause
  exit /b 1
)

echo [1/3] Instalando dependencias de construccion...
call npm config set fetch-retries 5
call npm config set fetch-retry-mintimeout 10000
call npm config set fetch-retry-maxtimeout 60000
call npm install --no-audit --no-fund --prefer-offline
if errorlevel 1 goto :error

echo.
echo [2/3] Ejecutando pruebas del wrapper...
call npm test
if errorlevel 1 goto :error

echo.
echo [3/3] Generando instalador y portable de Windows...
call npm run dist:win
if errorlevel 1 goto :error

echo.
echo ============================================================
echo CONSTRUCCION COMPLETA
echo Instaladores generados:
dir /b dist\Fiscalizacion-L26-Setup-*.exe 2^>nul
dir /b dist\Fiscalizacion-L26-Portable-*.exe 2^>nul
echo ============================================================
start "" "%~dp0dist"
pause
exit /b 0

:error
echo.
echo ERROR: La construccion no termino correctamente.
echo Revise el mensaje anterior. El codigo original de L26 no se modifica.
pause
exit /b 1

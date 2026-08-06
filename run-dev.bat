@echo off
setlocal
set "ROOT=%~dp0"
set "PY=python"
if exist "%ROOT%.venv\Scripts\python.exe" set "PY=%ROOT%.venv\Scripts\python.exe"

if /i "%~1"=="backend" goto backend
if /i "%~1"=="frontend" goto frontend

echo EnergySpirit dev runner
echo.
echo [1] Monitor backend
echo [2] Monitor frontend
echo [3] Monitor backend + frontend
echo.
choice /c 123 /n /m "Pilih opsi [1-3]: "

if errorlevel 3 goto both
if errorlevel 2 goto frontend
goto backend

:backend
cd /d "%ROOT%"
"%PY%" main.py
goto end

:frontend
cd /d "%ROOT%Interfaces\frontend"
call npm run dev
goto end

:both
start "EnergySpirit Backend" "%ComSpec%" /k call "%~f0" backend
start "EnergySpirit Frontend" "%ComSpec%" /k call "%~f0" frontend
echo Backend dan frontend sudah dibuka di window terpisah.

:end
endlocal

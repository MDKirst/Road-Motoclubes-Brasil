@echo off
rem Couro ^& Asfalto - BR-277: abre o jogo no navegador (servidor local, nada para instalar)
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0servidor.ps1"

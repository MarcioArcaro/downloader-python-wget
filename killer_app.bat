@echo off
taskkill /F /IM wget.exe >nul 2>&1
taskkill /F /IM downloader.exe >nul 2>&1
exit
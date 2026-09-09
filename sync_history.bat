@echo off
chcp 65001 > nul
echo ==============================================
echo  Synchronizing Antigravity History & Transcripts
echo ==============================================
python "%~dp0sync_history.py"
echo.
pause

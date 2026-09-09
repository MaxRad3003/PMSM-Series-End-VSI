# Synchronize Antigravity History & Transcripts
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptDir\sync_history.py"

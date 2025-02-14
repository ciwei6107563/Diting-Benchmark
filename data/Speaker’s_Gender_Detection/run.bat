@echo off
start "MyExperimentWindow" cmd /c "experiment.cmd & exit"
timeout /t 40
taskkill /fi "WINDOWTITLE eq MyExperimentWindow" /f
start "MyExperimentWindow1" cmd /c "run.bat & exit"

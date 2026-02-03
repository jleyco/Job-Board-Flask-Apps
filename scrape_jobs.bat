@echo off
echo ====================================
echo Running Job Scrapers
echo ====================================
echo.
cd /d "%~dp0"
python run_scrapers.py
echo.
echo Jobs saved to scraped_jobs.json
echo Refresh your browser to see the new jobs!
echo.
pause

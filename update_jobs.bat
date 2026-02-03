@echo off
echo ====================================
echo Updating Jobs Data
echo ====================================
echo.
echo Copying scraped_jobs.json from parent directory...
copy /Y "..\scraped_jobs.json" "scraped_jobs.json"
echo.
echo Done! Jobs data updated.
echo You can now refresh your browser to see the latest jobs.
echo.
pause

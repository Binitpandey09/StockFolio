@echo off
echo Pushing changes to GitHub...
echo.

REM Remove git lock file if exists
if exist .git\index.lock (
    echo Removing git lock file...
    del /F .git\index.lock
)

REM Add all changes
echo Adding all changes...
git add -A

REM Show status
echo.
echo Current status:
git status

REM Commit changes
echo.
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Major improvements: Enhanced UI and performance optimization

git commit -m "%commit_msg%"

REM Push to GitHub
echo.
echo Pushing to GitHub...
git push origin main

echo.
echo Done!
pause

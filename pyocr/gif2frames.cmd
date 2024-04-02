@echo off
setlocal

set "SRC_DIR=%~dp0srcimg"
set "DEST_DIR=%~dp0ocrimg"
set "GIF_FILE=%SRC_DIR%\example.gif"

if not exist "%GIF_FILE%" (
    echo file not found: %GIF_FILE%
    exit /b 1
)

if not exist "%DEST_DIR%" (
    mkdir "%DEST_DIR%"
)

echo Converting GIF to JPEG frames...
magick convert -coalesce "%GIF_FILE%" "%DEST_DIR%/frame%%03d.jpg"

echo process complete...
endlocal
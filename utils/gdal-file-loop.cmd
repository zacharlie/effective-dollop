@echo off
@rem can't seem to find a way to merge gpkg rasters after the fact. Leaving the logic for now
@setlocal enableextensions
@cd /d "%~dp0"

set PATH=%PATH%;%~dp0;
set PATH=%PATH%%~dp0bin;
call C:\OSGeo4W\bin\o4w_env.bat;

set INDIR=%~dp0input_data
set TMPPATH=%~dp0tmp
rem set OUTFILE=%~dp0output.gpkg
REM Specify the file extension for input files
set EXT=tif

if not exist "%TMPPATH%" (mkdir %TMPPATH%)

if exist "%OUTFILE%" (
    if exist "%OUTFILE%.old" (
        del /q "%OUTFILE%.old"
        echo "Previous database backup removed..."
    )
    rename "%OUTFILE%" "%OUTFILE%.old"
    echo "renamed previous database to $OUTFILE.old..."
)

cd "%INDIR%"

for %%f in (*.%EXT%) do (
    rem gdal_translate -of gpkg "%%f" "%OUTFILE%" -co "RASTER_TABLE=%%~nf"
    gdal_translate -of gpkg "%%f" "%TMPPATH%\%%~nf.gpkg" -co TILE_FORMAT=AUTO
    rem gdalmanage copy -f gpkg "%OUTFILE%"  "%TMPPATH%\%%~nf.gpkg" -co "RASTER_TABLE=%%~nf"
    rem del /f "%TMPPATH%\%%~nf.gpkg"
    echo "Processed %%~nf..."
)

echo "Processing complete. Press a key continue..."

pause

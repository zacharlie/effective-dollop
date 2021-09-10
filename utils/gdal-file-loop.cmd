@echo off
@setlocal enableextensions
@cd /d "%~dp0"

set PATH=%PATH%;%~dp0;
set PATH=%PATH%%~dp0bin;
call C:\OSGeo4W\bin\o4w_env.bat;

set INDIR=%~dp0input_data
set OUTFILE=%~dp0output.gpkg
REM Specify the file extension for input files
set EXT=shp

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
    ogr2ogr -f gpkg -append -update -skipfailures "%OUTFILE%" "%%f"
    echo "Appended %%~nf..."
)

echo "Processing complete. Press a key continue..."

pause

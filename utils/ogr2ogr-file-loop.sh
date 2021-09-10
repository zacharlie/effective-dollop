#!/usr/bin/bash

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

INDIR="$THISDIR/input_dir"
OUTFILE="$THISDIR/output.gpkg"
# Specify the file extension for input files
EXT="shp"

cd "$INDIR"

# Make backup of previous data before overwriting
if test -f "$OUTFILE"; then
    cp $OUTFILE $OUTFILE.old
    echo "Copied previous database to $OUTFILE.old..."
    rm $OUTFILE
    echo "Previous database removed..."
fi

for filename in *.${EXT}; do
    ogr2ogr -f gpkg -append -update -skipfailures "$OUTFILE" "$filename"
    echo "Appended $filename..."

done

read -p "Processing complete. Press a key continue..."

#!/bin/bash
# Script to wrap mathematical expressions in double backticks

for file in 01_vector_problems_id.txt 02_matrix_problems_id.txt 03_linear_transformation_problems_id.txt 04_linear_systems_problems_id.txt 05_gauss_jordan_problems_id.txt; do
    echo "Processing $file..."

    # Create backup
    cp "$file" "$file.bak"

    # Apply transformations using sed
    sed -i.tmp \
        -e 's/\bRR\^\([0-9n]\)/``RR^\1``/g' \
        -e 's/\[\[\([^]]*\)\]\]/``[[\1]]``/g' \
        -e 's/\[\([0-9, -]*\)\]/``[\1]``/g' \
        -e 's/(\([xyz]\),\([xyz]\))/``(\1,\2)``/g' \
        -e 's/(\([xyz]\),\([xyz]\),\([xyz]\))/``(\1,\2,\3)``/g' \
        -e 's/\b\([a-z]\) = \([0-9-]*\)/``\1 = \2``/g' \
        -e 's/\bR_\([0-9]\)/``R_\1``/g' \
        -e 's/\b\([0-9]\+\)\/\([0-9]\+\)/``\1\/\2``/g' \
        -e 's/ cdot / ``cdot`` /g' \
        -e 's/ xx / ``xx`` /g' \
        -e 's/\bsqrt(/``sqrt(/g' \
        -e 's/)``/``)``/g' \
        "$file"

    # Remove temporary file
    rm -f "$file.tmp"

    echo "Completed $file"
done

echo "All files updated!"

#!/usr/bin/bash

#Create ugly images for all PDFs with bibtex superimposed to do dirty checks for correctness

for file in outbox/*.pdf; do
    echo making check image for $file
    basename="${file%.*}"

    #Save first page
    pdftoppm -png -f 1 -l 1 $file > ${basename}.png

    text=$(cat $basename.bib)
    #convert -pointsize 60 -gravity center -draw "text 0,300 Hello" ${basename}.png ${basename}.png

    # Throw bibtex on first page of image
    convert -font FreeSans -undercolor White ${basename}.png -gravity South -pointsize 24 -annotate +0+100 "$text" ${basename}.png

done

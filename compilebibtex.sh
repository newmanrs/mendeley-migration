#!/usr/bin/env bash

set -e

echo "Create single bib file from the .bib after resolving key collisions"

outputfile="library.bib"
truncate -s 0 $outputfile  # create or clear file

#Look for the cite key collisions
collist=$(head -n 1 -q outbox/*.bib | uniq -d | cut -d'{' -f 2  | sed 's/,//g')
nocollist=$(head -n 1 -q outbox/*.bib | uniq -u | cut -d'{' -f 2 | sed 's/,//g')

echo "bibtek citekey collisions list:" $collist

# Edit collisions out by adding md5sum of the bib file to the key.
# This prevents papers getting added in the future from colliding
# with the old ones
for col in $collist; do
    echo working on collision $col
    files=$(ls outbox/${col}*.bib | grep $col )
    for file in $files; do
        echo appending bibtex file: $file
        checksum=$(md5sum $file | cut -d ' ' -f 1)
        echo resolving collision with checksum: $checksum
        sedstring="s/${col}/${col}_${checksum}/g"
        cat $file | sed $sedstring >> $outputfile
    done
done

# Append the rest
for col in $nocollist; do
    echo working on file $col
    file=$(ls outbox/${col}*.bib | grep $col )   # unique match
    echo appending bibtex file: $file
    cat $file >> $outputfile
    #done
done

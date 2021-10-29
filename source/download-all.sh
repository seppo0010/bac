#!/bin/bash

for url in $(xsv select 'tender/documents/0/url' releases_documents_items.csv |sort |uniq|grep -v 'tender/documents/0/url'); do
    path="${url//\//_}"
    if [ ! -f "data/$path" ]; then
        wget "$url" -O "data/$path"
    else
        echo "$url already downloaded" >&2
    fi
done

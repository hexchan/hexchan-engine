#!/usr/bin/env bash

set -e

echo Build started at: $(date)

echo "Prepare output folder"
rm -rf dev/fronted
mkdir -p dev/frontend

echo "Build scripts"
npx rollup -cm

echo "Build styles"
npx lessc --source-map src/frontend/style.less dev/frontend/style.css

echo "Copy assets"
cp src/frontend/favicon.png dev/frontend/favicon.png
cp -r src/frontend/fonts dev/frontend/
cp -r src/frontend/images dev/frontend/

echo "Copy libraries"
mkdir -p dev/frontend/libs
cp -r node_modules/lightbox2/dist dev/frontend/libs/lightbox
cp node_modules/jquery/dist/jquery.min.js dev/frontend/libs/jquery.min.js

echo "Done"

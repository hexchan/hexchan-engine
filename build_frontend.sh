#!/usr/bin/env bash

set -e

STORAGE_PATH=${1:-storage}

echo Build started at: $(date)

echo "Prepare output folder"
rm -rf $STORAGE_PATH/fronted
mkdir -p $STORAGE_PATH/frontend

echo "Build scripts"
npx rollup -cm

echo "Build styles"
npx lessc --source-map src/frontend/style.less $STORAGE_PATH/frontend/style.css

echo "Copy assets"
cp src/frontend/favicon.png $STORAGE_PATH/frontend/favicon.png
cp -r src/frontend/fonts $STORAGE_PATH/frontend/
cp -r src/frontend/images $STORAGE_PATH/frontend/

echo "Copy libraries"
mkdir -p $STORAGE_PATH/frontend/libs
cp -r node_modules/lightbox2/dist $STORAGE_PATH/frontend/libs/lightbox
cp node_modules/jquery/dist/jquery.min.js $STORAGE_PATH/frontend/libs/jquery.min.js

echo "Done"

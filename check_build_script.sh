#!/bin/bash

echo "Checking for build.sh..."

if [ -f build.sh ]; then
    echo "build.sh exists:"
    ls -l build.sh
else
    echo "build.sh does not exist"
fi

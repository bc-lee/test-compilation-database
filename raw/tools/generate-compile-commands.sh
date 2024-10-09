#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$ROOT_DIR"

CXX=${CXX:-g++}

rm -f out/compile_commands.json
mkdir -p out
cat <<EOF > out/compile_commands.json
[
  {
     "directory": "$ROOT_DIR/out",
     "file": "../api/main.cc",
     "command": "$CXX -std=c++17 -c ../api/main.cc -o main.o"
   }
]
EOF

#!/bin/bash

build_kwcount=false
build_tar=false

while [ -n "$1" ]; do
  case "$1" in
  --build-kwcount)
    build_kwcount=true
    shift 1
    ;;
  --tar)
    build_tar=true
    shift 1
    ;;
  *)
    echo "Unknown option: $1"
    exit 1
    ;;
  esac
done

if ${build_kwcount}; then
  cd btor2kwcount/
  ./configure.sh --static
  cd build
  make
  cd ../..
fi

mkdir lib
pip3.10 install joblib==1.4.2 --target=./lib
pip3.10 install numpy==1.26.4 --target=./lib
pip3.10 install xgboost==2.0.3 --target=./lib

if ${build_tar}; then
  tar -czvf ../btor2select_pw.tar.gz .
fi

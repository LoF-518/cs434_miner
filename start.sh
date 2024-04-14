#!/bin/bash

echo "Analyzing Drivers for Java..."
./main.sh java_mongodb_drivers.csv $1
./main.sh java_cass_drivers.csv $1

echo "Analyzing Drivers for Python..."
./main.sh py_mongodb_drivers.csv $1
./main.sh py_cass_drivers.csv $1

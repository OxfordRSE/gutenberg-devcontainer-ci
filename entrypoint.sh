#!/bin/sh -l

echo "Hello $1"
time=$(date)
echo "time=$time" >> "$GITHUB_OUTPUT"

python -e "print('Hello from Python, too!')"
pwd

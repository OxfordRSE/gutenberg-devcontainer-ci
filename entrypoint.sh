#!/bin/sh -l

echo "Hello $1"
time=$(date)
echo "time=$time" >> "$GITHUB_OUTPUT"

python -c "print('Hello from Python, too!')"
pwd
ls -l
ls -l ..

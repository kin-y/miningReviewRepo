#!/bin/bash
until python index.py;
do
    echo "'index.py' crashed with exit code $?. Restarting..." >&2
    sleep 10
done

#!/bin/bash
echo >> cola.txt
cat "$@" >> cola.txt
cat cola.txt
refresh

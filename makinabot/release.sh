#!/bin/bash
rm -rf .git
rm -rf node_modules
rm -rf .cache 
git prune
git gc

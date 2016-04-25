#!/bin/bash

forever start -c "npm start" ./
cd Website
forever start -c python Twitter_Utils/main.py

#Line counter
cd ../Twitter_Utils/data/tweets/
find . -name '*.txt' | xargs wc -l
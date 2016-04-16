#!/bin/bash

forever start -c "npm start" ./
cd Website
forever start -c python Twitter_Utils/main.py
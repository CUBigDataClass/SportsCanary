[![Build Status](https://travis-ci.org/CUBigDataClass/SportsCanary.svg?branch=master)](https://travis-ci.org/CUBigDataClass/SportsCanary)  [![Coverage Status](https://coveralls.io/repos/github/CUBigDataClass/SportsCanary/badge.svg?branch=master)](https://coveralls.io/github/CUBigDataClass/SportsCanary?branch=master)

Uses data from Twitter to generate "crowd-sourced" gambling odds for major sporting events.

Website: [Sports Canary](www.sportscanary.com)

##Getting Started
There are two parts to this repo.  In **Website** you can find our MEN stack (Mongo, Express, Node) website.  In **Eternal_Utils**, **Gambling_Utils** and **Twitter_Utils** you can find our python backend for our data gathering, processing and result creation.


###Code Instrumentation
```
Make sure the relevant function/method is decorated with:
@profile

Then run:
$ kernprof -v FILE_LOCATION.py > OutputFile.txt

Results are also saved to a binary file with .lprof ending.
To view this file:
$ python -m line_profiler FILE_LOCATION.lprof
```

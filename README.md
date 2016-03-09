[![Build Status](https://travis-ci.org/CUBigDataClass/SportsCanary.svg?branch=master)](https://travis-ci.org/CUBigDataClass/SportsCanary)  [![Coverage Status](https://coveralls.io/repos/github/CUBigDataClass/SportsCanary/badge.svg?branch=master)](https://coveralls.io/github/CUBigDataClass/SportsCanary?branch=master)

Uses data from Twitter to generate "crowd-sourced" gambling odds for major sporting events.


##Getting Started
There are two parts to this repo.  In **Website** you can find our MEN stack (Mongo, Express, Node) website.  In **Eternal_Utils**, **Gambling_Utils** and **Twitter_Utils** you can find our python backend for our data gathering, processing and result creation.

####To test Map and Reduce
```
$ cat AllStarsGameData.txt| python Twitter_Utils/Mapper.py | sort | python Twitter_Utils/Reducer.py | sort -n
```

####To generate test coverage for python

```
py.test --cov=Twitter_Utils --cov=Gambling_Utils --cov=Eternal_Utils --cov-report=term-missing --cov-report=html
```

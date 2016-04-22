<p align="center">
  <img height="300" width="300" src="sports-canary.png" />
</p>

# [Sports Canary](http://sportscanary.com/)

[![Build Status](https://travis-ci.org/CUBigDataClass/SportsCanary.svg?branch=master)](https://travis-ci.org/CUBigDataClass/SportsCanary)  [![Coverage Status](https://coveralls.io/repos/github/CUBigDataClass/SportsCanary/badge.svg?branch=master)](https://coveralls.io/github/CUBigDataClass/SportsCanary?branch=master)


###SportsCanary uses data from Twitter to generate "crowd-sourced" predictions for major sporting events.  Currently supports MLB, NHL and NBA.
#####As of 04/22 we have correctly predicted 64.865% of NBA games, 46.73% of MLB games and 55% of NHL games.

##Getting Started
There are four parts to this repo: 

* **Website** contains our MEN stack (Mongo, Express, Node) website.    
* **Twitter_Utils** contains our python backend responsible for gathering data for the days games and predicting who will win.
* **Gnip_Client** contains scripts for interacting with the GNIP search API as well as interfacing with the IBM Watson Tone Analyzer.
* **Gambling_Utils** contains our proxy as well as code for interfacing with the BetfairAPI (which expects a non US connection due to US gambling laws.)
* **Eternal_Utils** mostly contains scripts for retroactivley updating our database, instrumenting our code, and sending encrypted data.

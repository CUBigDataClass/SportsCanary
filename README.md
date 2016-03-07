[![Coverage Status](https://coveralls.io/repos/github/CUBigDataClass/SportsCanary/badge.svg?branch=master)](https://coveralls.io/github/CUBigDataClass/SportsCanary?branch=master)

#Sports Canary

###To test Map and Reduce
```
$ cat AllStarsGameData.txt| python Twitter_Utils/Mapper.py | sort | python Twitter_Utils/Reducer.py | sort -n
```

###To generate test coverage

```
py.test --cov=Twitter_Utils --cov=Gambling_Utils --cov=Eternal_Utils --cov-report=term-missing --cov-report=html
```

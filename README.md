[![Build Status](https://travis-ci.org/CUBigDataClass/BigDataMonsters.svg?branch=master)](https://travis-ci.org/CUBigDataClass/BigDataMonsters)  [![Coverage Status](https://coveralls.io/repos/github/CUBigDataClass/BigDataMonsters/badge.svg?branch=master)](https://coveralls.io/github/CUBigDataClass/BigDataMonsters?branch=master)

#Sports Canary

###To test Map and Reduce
```
$ cat AllStarsGameData.txt| python Twitter_Utils/Mapper.py | sort | python Twitter_Utils/Reducer.py | sort -n
```

###To generate test coverage

```
py.test --cov=Twitter_Utils --cov=Gambling_Utils --cov-report=term-missing --cov-report=html
```
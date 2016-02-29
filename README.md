[![Build Status](https://travis-ci.org/CUBigDataClass/BigDataMonsters.svg?branch=master)](https://travis-ci.org/CUBigDataClass/BigDataMonsters)  [![Coverage Status](https://coveralls.io/repos/github/CUBigDataClass/BigDataMonsters/badge.svg?branch=master)](https://coveralls.io/github/CUBigDataClass/BigDataMonsters?branch=master)

#Team BIG Data Monsters

###To test Map and Reduce
```
$ cat AllStarsGameData.txt| python Twitter_Utils/Mapper.py | sort | python Twitter_Utils/Reducer.py | sort -n
```
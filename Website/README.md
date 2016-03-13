###Setup

Website: [Sports Canary](www.sportscanary.com)

Install **node** and **npm**
```
OSX:
$ brew install node

Ubuntu:
$ sudo apt-get install nodejs
$ sudo apt-get install npm
```

Install **MongoDB**
```
OSX:
$ brew install mongodb
```


Install dependencies
```
$ npm install
```

Dependencies can be found in package.json


###Run
```
$ npm start

Suggested
$ nodemon npm start
```
Go to localhost


###Elastic Search Installation
```
Download Elastic Search from https://www.elastic.co/downloads/elasticsearch
Unzip
cd into directory
$ bin/elasticsearch
$ curl -X GET http://localhost:9200/
$ pip install -r requirements.txt
$ mongod --replSet "rs0"
$ mongo
$ rs.initiate()
In: elastic2-doc-manager
$ mongo-connector -m localhost:27017 -t localhost:9200 -d elastic2_doc_manager
To Test:
$ curl -XPOST http://localhost:9200/sportscanary/_search -d '{"query": {"match": {"_all": "vs"}}}'
```

###Sports Canary - Twitter Utilities


###Setup

```
sudo pip install -r requirements.txt
```

Before running this script, you will have to establish environment variables for Twitter API keys.
```
export NUMBER_OF_TWITTER_KEYS_AVAILABLE='#'
export TWITTER_APP_KEY_0='your key'
export TWITTER_APP_SECRET_0='your key'
export TWITTER_OAUTH_TOKEN_0='your key'
export TWITTER_OAUTH_TOKEN_SECRET_0='your key'
```
Then, either load a new bash prompt or run
```
source ~/.bashrc
```

If that does not work, copy the all the auth variables to the utils.env file

###NLTK Setup
Make sure you've installed the requirements prior to this step.
```
$ python -m nltk.downloader stopwords
$ python -m nltk.downloader punkt
$ python -m nltk.downloader wordnet
```
Select the 'Corpora' tab and then download 'twitter_samples'

###Testing
```
Within Outer Directory
$ py.test
```
**With Coverage**
```
Within Outer Directory
$ py.test --cov=Twitter_Utils --cov=Gambling_Utils --cov=Eternal_Utils --cov=Gnip_Client --cov-report=term-missing --cov-report=html
```


####To test Map and Reduce
```
Within the Twitter_Utils directory
$ cat DATA | python Mapper.py | sort | python Reducer.py | sort -n
```



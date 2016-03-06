###Sports Canary - Twitter Utilities


###Setup

```
pip install -r requirements.txt
```

Before running this script, you will have to establish environment variables for Twitter API keys.
```
export TWITTER_APP_KEY='your key'
export TWITTER_APP_SECRET='your key'
export TWITTER_OAUTH_TOKEN='your key'
export TWITTER_OAUTH_TOKEN_SECRET='your key'
```
Then, either load a new bash prompt or run
```
source ~/.bashrc
```

If that does not work, copy the all the auth variables to the utils.env file

###NLTK Setup
Make sure you've installed the requirements prior to this step.
```
$ python
$ import nltk
$ nltk.download()
```
Select the 'Corpora' tab and then download 'twitter_samples'

###Testing
```
$ py.test
```


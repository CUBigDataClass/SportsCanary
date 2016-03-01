###Sports Canary - Gambling Utilities 


###Setup

```
pip install -r requirements.txt
```

Before running this script, you will have to establish environment variables for Twitter API keys.
```
export BET_FAIR_APP_KEY_DELAYED='yourkey'
export BET_FAIR_APP_KEY_NONDELAYED='yourkey'
export BET_FAIR_SESSION_TOKEN='yourkey'
export BET_FAIR_USERNAME='yourkey'
export BET_FAIR_PASSWORD='yourkey'
```
Then, either load a new bash prompt or run
```
source ~/.bashrc
```

###Testing
```
$ py.test
```


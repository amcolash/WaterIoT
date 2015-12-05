# WaterPi
A simple python-based program for a raspberry pi to check water level of a plant, which triggers a notification.

# Setting Things Up
In addition to cloning this repository, there are a few extra steps if you want to have a similar setup.

## Install Python and Dev Requirements
`sudo apt get install pthon-dev python-pip libffi-dev libssl-dev`

## Install python-twitter (Twitter API for Python)
Note: If you want to keep things clean it is recommended to use a virtual environment, otherwise you can just globally install python-twitter

For me, I did: `sudo pip install python-twitter`

## Set up credentials
You will need to make a new Twitter Application and add your own twitter credentails to a file. More on getting credentials [here](https://dev.twitter.com/oauth/overview/application-owner-access-tokens)

After you have your credentials, add them to a file named `auth.py` in the root directory of the project.
Inside of `auth.py`, fill in the following lines as such:

```
consumer_key='key_here'
consumer_secret='key_here'
access_token_key='key_here'
access_token_scret='key_here'
```

## Set pins used
Make sure to set the pins you are using with your setup, or use the ones I did:
GPIO23 = Input (from digital output)
GPIO24 = Output (vcc for hygrometer)

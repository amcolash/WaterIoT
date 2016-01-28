# WaterIoT
A simple python-based program for a IoT device to check water level of a plant, graph on website and can trigger a notification if dry.

This branch (master) contains code for an Intel Galileo/Edison/etc. If you have a raspberry pi or similar, check the (raspberry_pi) branch - which covers extra steps for analog input readings.

# Setting Things Up
In addition to cloning this repository, there are a few extra steps if you want to have a similar setup.

## Install Requirements
By default, the standard linux distro for the Galileo has python and node (I think for Edison too!). There should be very little required to get things set up.

## NodeJS installation
I used bower for this project and set up a custom npm install location to avoid using root access to install node packages.
```
mkdir ~/.npm-packages
npm config set prefix '~/.npm-packages'
npm install -g bower
```

Additionally, add the following to your `~/.bashrc` file: `export PATH="$PATH:$HOME/.npm-packages/bin"`

## Install python-twitter (Twitter API for Python)
Note: If you want to keep things clean it is recommended to use a virtual environment, otherwise you can just globally install python-twitter

For me, I did: `pip install python-twitter`

Pip packages for security: `pip install 'requests[security]'`

## Clone the repository
To clone this project, simply do `git clone git@github.com:amcolash/WaterIoT.git`

## Set up credentials
You will need to make a new Twitter Application and add your own twitter credentails to a file. More on getting credentials [here](https://dev.twitter.com/oauth/overview/application-owner-access-tokens)

After you have your credentials, add them to a file named `auth.py` in the root directory of the project. Inside of `auth.py`, fill in the following lines as such:

```
consumer_key='key_here'
consumer_secret='key_here'
access_token_key='key_here'
access_token_secret='key_here'
```

## Set pins used
Make sure to set the pins you are using with your setup, or use the ones I did:

A0 = Input (attached to digital output of hygrometer)

D13 = Output (vcc for hygrometer)

## Setting up the web server and startup
Since all I am using my Galileo for is this water sensor, I chose to put the server and script into an [upstart](http://upstart.ubuntu.com/) script. To keep things easier, I have included my own script in this repository - it is named `wateriot`. Simple copy into `/etc/init.d/` and then run `update-rc.d wateriot defaults`

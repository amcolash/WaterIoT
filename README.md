# WaterPi
A simple python-based program for a raspberry pi to check water level of a plant, which triggers a notification.

# Setting Things Up
In addition to cloning this repository, there are a few extra steps if you want to have a similar setup.

## Install Python and Dev Requirements
`sudo apt get install python-dev python-pip libffi-dev libssl-dev git`

## NodeJS installation
I used bower for this project, so you will need nodejs as well. I installed this via adafruit's repository and set up a custom npm install location to avoid using root access to install node packages.
```
curl -sLS https://apt.adafruit.com/add | sudo bash
sudo apt-get install node
mkdir ~/.npm-packages
`npm config set prefix '~/.npm-packages'
```

Additionally, add the following to your `~/.bashrc` file: `export PATH="$PATH:$HOME/.npm-packages/bin"`

## Install python-twitter (Twitter API for Python)
Note: If you want to keep things clean it is recommended to use a virtual environment, otherwise you can just globally install python-twitter

For me, I did: `sudo pip install python-twitter`

Pip packages for security: `pip install 'requests[security]'`

## Clone the repository
To clone this project, simply do `git clone git@github.com:amcolash/WaterPi.git`

## Set up credentials
You will need to make a new Twitter Application and add your own twitter credentails to a file. More on getting credentials [here](https://dev.twitter.com/oauth/overview/application-owner-access-tokens)

After you have your credentials, add them to a file named `auth.py` in the root directory of the project. Inside of `auth.py`, fill in the following lines as such:

```
consumer_key='key_here'
consumer_secret='key_here'
access_token_key='key_here'
access_token_scret='key_here'
```

## Set pins used
Make sure to set the pins you are using with your setup, or use the ones I did:

GPIO23 = Input (attached to digital output of hygrometer)

GPIO24 = Output (vcc for hygrometer)

## Having things run on startup
Since all I am using my pi for is this water sensor, I chose to put the script and server in `/etc/rc.local`.
In this file, I added the following line (for my setup): `python /home/pi/WaterPi/water.py`

If you want to keep things more organized, I would suggest using [upstart](http://upstart.ubuntu.com/getting-started.html).

## Configuring the web server
In this project I have included some code that allows for a web server to be run. You will need to have some way to start this server. In my case, I just symlinked `/var/www` to `/home/pi/WaterPi/public`. There are better ways of doing this if you want more control however, like setting up a python or node static http file server.

# WaterPi
A simple python-based program for a raspberry pi to check water level of a plant, which triggers a notification.

# Setting Things Up
In addition to cloning this repository, there are a few extra steps if you want to have a similar setup.

This project supports both digital and analog outputs. An analog output will give better readings, but requires you to have an ADC for conversion to digital output. I used an MPC3002. The analog branch will be recieving updates, but the digital branch does have a working server and copy of the python code.

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
access_token_secret='key_here'
```

## Set pins used
Make sure to set the pins you are using with your setup, or use the ones I did:

GPIO23 = Input (attached to digital output of hygrometer)

GPIO24 = Output (vcc for hygrometer)

## Setting up the web server and startup
I set up a simple node server for monitoring my plant: `npm install http-server -g`.

Since all I am using my pi for is this water sensor, I chose to put the script and server in `/etc/rc.local`.

```
nohup python /home/pi/WaterPi/water.py &
nohup /home/pi/.npm-packages/bin/http-server /home/pi/WaterPi/public -p 80 &
```

If you want to keep things more organized, I would suggest using [upstart](http://upstart.ubuntu.com/getting-started.html).

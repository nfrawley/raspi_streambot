#!/bin/bash

# Setup wayland so that VNC over rpi-connect is available.
raspi-config nonint do_wayland W2

# Make sure python3/pip installed... in case of dummies. + chromium-webdriver for the magic
apt-get install python3 python3-pip chromium-chromedriver

# Check if venv exists, create if no (It shouldn't on first start)
if [ ! -d "/venv_streambot"]; then
    echo "Creating virtual env.."
    python -m venv /venv_streambot
else
    echo "Already there, champ"
fi

# Activate the venv
source /venv_streambot/bin/activate

# Install py library dependencies
pip install selenium python-dotenv webdriver-manager
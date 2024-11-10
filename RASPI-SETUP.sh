# Setup wayland so that VNC over rpi-connect is available.
raspi-config nonint do_wayland W2

# Create Python VENV to isolate
apt-get install python3 python3-pip
python -m venv streambot
source streambot/bin/activate

# Install dependencies
apt-get install chromium-chromedriver
pip install selenium python-dotenv webdriver-manager

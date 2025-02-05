#!/usr/bin/env bash
# Bash script that sets up web servers for the deployment of web_static

# Install nginx
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

# Create directories to use
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Fake html file to test config
sudo touch /data/web_static/releases/test/index.html
sudo echo "<html><head></head><body>Hello there!</body></html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link everytime script is run
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Change ownership of the /data folder
sudo chown -R ubuntu:ubuntu /data

# Update the Nginx config to serve the content of /hbnb_static from .../current
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart nginx
sudo service nginx restart

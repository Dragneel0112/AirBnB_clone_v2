#!/usr/bin/env bash
# Set a web server for deployment

# Update ubuntu and install nginx
sudo apt-get update -y
sudo apt-get install nginx -y

# Create directories, simple html and link
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "<html>
  <head>
  </head>
  <body>
    ALX School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change Ownership of data folder 
sudo chown -R ubuntu:ubuntu /data/

# Adds alias to nginx configuration
sudo sed -i '47i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# restart web server
sudo service nginx restart

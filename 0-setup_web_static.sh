#!/usr/bin/env bash
# Write a Bash script that sets up your web servers for the deploy of web_static

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y nginx
sudo service nginx start

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu /data/
sudo chgrp -R ubuntu /data/

printf %s "server {
     listen      80 default_server;
     listen      [::]:80 default_server;
     add_header X-Served-By $HOSTNAME;
     root        /var/www/html;
     index       index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
     location /redirect_me {
           return 301 http://www.staggeringbeauty.com/;
      }
     error_page 404 /404.html;
     location /404 {
       root /var/www/html;
       internal;
    }
}
" | sudo tee /etc/nginx/sites-available/default
sudo service nginx restart

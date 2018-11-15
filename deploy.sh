#!/bin/bash

eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 700 tvp2017-dumas.pem # Allow read access to the private key
ssh-add tvp2017-dumas.pem # Add the private key to SSH

git config --global push.default matching
git remote add deploy ssh://ubuntu@193.40.33.98:22/var/www/chatbot2/chatbot
git push deploy

ssh apps@193.40.33.98 -p 22 <<EOF
  cd /var/www/chatbot2/chatbot
  #git push deploy master
  #systemctl start apache2
  #python manager.py runserver
EOF
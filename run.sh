#!/bin/bash

function setup_config() {
    cp ./config-sample.env ./config.env

    if grep --quiet '{KEY_HERE}' ./config.env; then
      random_str=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
      sed -i "s/{KEY_HERE}/${random_str}/g" ./config.env
    fi

    if grep --quiet '{LOGIN_HERE}' ./config.env; then
      read -p "Enter your login [admin]: " uname
      uname=${uname:-admin}
      sed -i "s/{LOGIN_HERE}/${uname}/g" ./config.env
    fi

    if grep --quiet '{HASH_HERE}' ./config.env; then
      read -s -p "Enter your password: " password && echo
      passwd_hash=$(echo -n $password | md5sum | awk '{print $1}')
      sed -i "s/{HASH_HERE}/${passwd_hash}/g" ./config.env
    fi
}

# Setup config if not exist
[ -f ./config.env ] || setup_config
[ -d "src/static/upload" ] || mkdir src/static/upload

if [[ $1 == '--no-docker' ]]; then
  eval $(egrep -v '^#' config.env | xargs) ./gunicorn.sh
else
  docker-compose up -d
fi
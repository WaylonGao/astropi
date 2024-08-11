#!/usr/bin/env bash

sudo systemctl stop flaskapp


sleep 1
git pull

sudo systemctl start flaskapp
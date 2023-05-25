#!/bin/bash

export DJANGO_SETTINGS_MODULE=trout.settings
export DJANGO_SECRET_KEY="testkey"

ls
pwd
ls -R

pytest

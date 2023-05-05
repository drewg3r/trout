#!/bin/bash

export DJANGO_SETTINGS_MODULE=trout.settings
export DJANGO_SECRET_KEY="testkey"
export RUN_TASKS_SYNCHRONOUSLY="True"

ls
pwd
ls -R

pytest

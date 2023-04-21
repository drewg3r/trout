#!/bin/bash

export DJANGO_SECRET_KEY="testkey"
export RUN_TASKS_SYNCHRONOUSLY="True"

pytest

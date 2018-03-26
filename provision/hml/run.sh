#!/bin/bash

sleep 20
gunicorn voxpopapi.wsgi -b 0.0.0.0:8000

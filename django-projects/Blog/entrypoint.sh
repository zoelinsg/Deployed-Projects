#!/bin/bash
# 運行 Django 伺服器
gunicorn core.wsgi:application --bind 0.0.0.0:8000
#!/bin/bash

# Очистка предыдущей сборки
rm -rf build dist

# Установка зависимостей для сборки
pip install py2app

# Сборка приложения
python setup.py py2app

# Создание DMG
create-dmg \
  --volname "Activity Tracker" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "ActivityTracker.app" 175 120 \
  --hide-extension "ActivityTracker.app" \
  --app-drop-link 425 120 \
  "ActivityTracker.dmg" \
  "dist/" 
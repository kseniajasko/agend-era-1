@echo off

echo Sorting imports...
python -m isort app

echo Running black...
python -m black app

echo Code formatted

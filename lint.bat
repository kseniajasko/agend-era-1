@echo off
setlocal

echo Running flake8...
python -m flake8 app || goto :error

echo Running mypy...
python -m mypy app || goto :error

echo Checking isort...
python -m isort -c --diff app || goto :error

echo Checking black...
python -m black --check --diff app || goto :error

echo All lint checks passed.
endlocal
exit /b 0

:error
echo Lint failed.
endlocal
exit /b 1

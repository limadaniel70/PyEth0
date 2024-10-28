#!/usr/bin/env bash

poetry run black pyeth0
poetry run isort pyeth0
poetry run pylint pyeth0 >> pylint.log
echo "##########################################" >> mypy.log
poetry run mypy pyeth0 >> mypy.log
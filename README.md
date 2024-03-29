<p align="center"></p>
<h2 align="center">Check Bump</h2>
<p align="center">
<a href="https://github.com/rgryta/Check-Bump/actions/workflows/main.yml"><img alt="Build" src="https://github.com/rgryta/Check-Bump/actions/workflows/main.yml/badge.svg?branch=main"></a>
<a href="https://pypi.org/project/check-bump/"><img alt="PyPI" src="https://img.shields.io/pypi/v/check-bump"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/PyCQA/pylint"><img alt="pylint" src="https://img.shields.io/badge/linting-pylint-yellowgreen"></a>
<a href="https://github.com/rgryta/NoPrint"><img alt="NoPrint" src="https://img.shields.io/badge/NoPrint-enabled-blueviolet"></a>
</p>

## About

Want to add version bump checks to your CI/CD pipeline? This packages makes it easy.
Simply execute `check-vbump` within a directory where your `pyproject.toml` is located.

If there was a version bump, process will finish with exit code 0 - read stdout for the new version.
Otherwise, process will finish with exit code 1.

## Requirements

This package requires `tomlkit` package.

## Usage

Simply execute `check-bump` within a directory where your `pyproject.toml` is located. Or provide a path using `--path` argument.

```bash
user$ check-bump --help
usage: check-bump [-h] [-p PATH]

Detect and retrieve version bump

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path to pyproject.toml file
```

## Development

### Installation

Install virtual environment and check_bump package in editable mode with dev dependencies.

```bash
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
```


### Formatting

Use black and isort (with black profile) to format the code.

```bash
isort .
black .
```

### Syntax checks

Use pylint to check the code for errors and potential problems.
Also use noprint to detect print statements in the code (use logging instead!).

```bash
isort -c .
black --check .
pylint check_bump tests
noprint -ve check_bump tests
```

### Testing

For testing use coverage with pytest workers - this is due to errors that pytest-cov sometimes has with Python 3.9 and above.

```bash
coverage run -m pytest -xv tests
coverage report -m --fail-under=30
coverage erase
```

### Clean up

Clean up the project directory from temporary files and directories. Purge virual environment.

```bash
coverage erase
rm -rf check_bump.egg-info/ dist/ build/
rm -rf venv/
```

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

### Command

Simply execute `check-bump` within a directory where your `pyproject.toml` is located. Or provide a path using `--path` argument.

```bash
user$ check-bump --help
usage: check-bump [-h] [-p PATH]

Detect and retrieve version bump

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path to pyproject.toml file
```

### Github Actions

#### Inputs

##### `path`

**Optional** Relative path of pyproject.toml file. Example: `'python_src/pyproject.toml'`

##### `prefix`

**Optional** Prefix to provide for version output. Example: `'v'`

#### Outputs

##### `bump`

**always** Whether there was a bump or not. Values: `'true'`|`'false'`

##### `version`

**optional** Current (if bumped) version with prefix. If there was no version bump - no output is provided.

## Example usage

```yml
- name: Check bump
  id: vbump
  uses: rgryta/Check-Bump@main
  with:
    prefix: 'v'
```

And then you can later reference like:
```yml
- name: Tag repository
  if: steps.vbump.outputs.bump == 'true'
  run: |
    echo "I was bumped to version: ${{ steps.vbump.outputs.version }}"
```

## Development

### Installation

Install virtual environment and check_bump package in editable mode with dev dependencies.

```bash
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
```


### How to?

Automate as much as we can, see configuration in `pyproject.toml` file to see what are the flags used.

```bash
staging format  # Reformat the code
staging lint    # Check for linting issues
staging test    # Run unit tests and coverage report
```